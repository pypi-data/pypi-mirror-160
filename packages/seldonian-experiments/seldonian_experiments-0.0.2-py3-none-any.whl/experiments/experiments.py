""" Module for running Seldonian Experiments """

import os
import pickle
import autograd.numpy as np   # Thinly-wrapped version of Numpy
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
from functools import partial
from tqdm import tqdm
import copy

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.model_selection import train_test_split

from seldonian.utils.io_utils import load_pickle
from seldonian.dataset import (SupervisedDataSet,RLDataSet)
from seldonian.seldonian_algorithm import SeldonianAlgorithm

from fairlearn.reductions import ExponentiatedGradient
from fairlearn.metrics import (MetricFrame,selection_rate,
	false_positive_rate,true_positive_rate)
from fairlearn.reductions import (
	DemographicParity,FalsePositiveRateParity)

import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

class Experiment():
	def __init__(self,model_name,results_dir):
		""" Base class for running experiments

		:param model_name: The string name of the baseline model, 
			e.g 'logistic_regression'
		:type model_name: str

		:param results_dir: Parent directory for saving any
			experimental results
		:type results_dir: str

		"""
		self.model_name = model_name
		self.results_dir = results_dir

	def aggregate_results(self,**kwargs):
		""" Group together the data in each 
		trial file into a single CSV file.

		"""

		savedir_results = os.path.join(
			self.results_dir,
			f'{self.model_name}_results')
		os.makedirs(savedir_results,exist_ok=True)
		savename_results = os.path.join(savedir_results,
			f'{self.model_name}_results.csv')
		
		trial_dir = os.path.join(
			self.results_dir,
			f'{self.model_name}_results',
			'trial_data')
		df_list = []
		for data_pct in kwargs['data_pcts']:
			for trial_i in range(kwargs['n_trials']):
				filename = os.path.join(trial_dir,
					f'data_pct_{data_pct:.4f}_trial_{trial_i}.csv')
				df = pd.read_csv(filename)
				df_list.append(df)

		result_df = pd.concat(df_list)
		result_df.to_csv(savename_results,index=False)
		print(f"Saved {savename_results}")
		return

	def write_trial_result(self,data,
		colnames,trial_dir, 
		verbose=False):
		""" Write out the results from a single trial
		to a file.

		:param data: The information to save
		:type data: List

		:param colnames: Names of the items in the list. 
			These will comprise the header of the saved file
		:type colnames: List(str)

		:param trial_dir: The directory in which to save the file
		:type trial_dir: str

		:param verbose: if True, prints out saved filename
		:type verbose: bool
		"""
		result_df = pd.DataFrame([data])
		result_df.columns = colnames
		data_pct,trial_i = data[0:2]

		savename = os.path.join(trial_dir,
			f'data_pct_{data_pct:.4f}_trial_{trial_i}.csv')

		result_df.to_csv(savename,index=False)
		if verbose:
			print(f"Saved {savename}")
		return

class BaselineExperiment(Experiment):
	def __init__(self,model_name,results_dir):
		""" Class for running baseline experiments
		against which to compare Seldonian Experiments 

		:param model_name: The string name of the baseline model, 
			e.g 'logistic_regression'
		:type model_name: str

		:param results_dir: Parent directory for saving any
			experimental results
		:type results_dir: str

		:ivar model_class_dict: Dictionary mapping model_name 
			to a method of this class that runs the baseline model
		:vartype model_class_dict: dict
		"""
		super().__init__(model_name,results_dir)
		self.model_class_dict = {
			'logistic_regression':self.logistic_regression,
			'linear_svm':self.linear_svm}

	def run_experiment(self,**kwargs):
		""" Run the baseline experiment """

		test_features = kwargs['test_features']
		test_labels = kwargs['test_labels']

		helper = partial(
			self.model_class_dict[self.model_name],
			test_features=test_features,
			test_labels=test_labels,
			dataset=kwargs['dataset'],
			constraint_funcs=kwargs['constraint_funcs'],
			datagen_method=kwargs['datagen_method'],
			results_dir=kwargs['results_dir'],
			max_iter=kwargs['max_iter'],
			verbose=kwargs['verbose'],
			n_workers=kwargs['n_workers'],
		)
		data_pcts = kwargs['data_pcts']
		n_trials = kwargs['n_trials']

		data_pcts_vector = np.array([x for x in data_pcts for y in range(n_trials)])
		trials_vector = np.array([x for y in range(len(data_pcts)) for x in range(n_trials)])
		
		if n_workers == 1:
			for ii in range(len(data_pcts_vector)):
				data_pct = data_pcts_vector[ii]
				trial_i = trials_vector[ii]
				print(data_pct,trial_i)
				helper(data_pct,trial_i)
		elif n_workers > 1:
			with ProcessPoolExecutor(max_workers=n_workers,
				mp_context=mp.get_context('fork')) as ex:
				results = tqdm(ex.map(helper,data_pcts_vector,trials_vector),
					total=len(data_pcts_vector))
				for exc in results:
					if exc:
						print(exc)
		else:
			raise ValueError(f"n_workers value of {n_workers} must be >=1 ")

		self.aggregate_results(**kwargs)
	
	def logistic_regression(self,data_pct,trial_i,**kwargs):
		""" Run a trial of logistic regression 
		
		:param data_pct: Fraction of overall dataset size to use
		:type data_pct: float

		:param trial_i: The index of the trial 
		:type trial_i: int
		"""
		trial_dir = os.path.join(
				kwargs['results_dir'],
				'logistic_regression_results',
				'trial_data')

		os.makedirs(trial_dir,exist_ok=True)
		dataset = kwargs['dataset']
		label_column = dataset.label_column
		orig_df = dataset.df
		# number of points in this partition of the data
		n_points = int(round(data_pct*len(orig_df))) 

		test_features = kwargs['test_features']
		test_labels = kwargs['test_labels']
		
		if kwargs['datagen_method'] == 'resample':
			resampled_filename = os.path.join(kwargs['results_dir'],
			'resampled_dataframes',f'trial_{trial_i}.pkl')
			with open(resampled_filename,'rb') as infile:
				df = pickle.load(infile).iloc[:n_points]
			# df = pd.read_csv(resampled_filename).iloc[:n_points]

		else:
			raise NotImplementedError(f"datagen_method: {datagen_method} not implemented")

		# Set up for initial solution
		labels = df[label_column]
		features = df.loc[:,
			df.columns != label_column]
		
		if not dataset.include_sensitive_columns:
			features = features.drop(
				columns=dataset.sensitive_column_names)

		if dataset.include_intercept_term:
			features.insert(0,'offset',1.0) # inserts a column of 1's
		
		lr_model = LogisticRegression(max_iter=kwargs['max_iter'])
		lr_model.fit(features, labels)
		theta_solution = np.hstack([lr_model.intercept_,lr_model.coef_[0]])
		# predict the class label, not the probability
		prediction_test = lr_model.predict(test_features) 
		
		# Calculate accuracy 
		acc = np.mean(1.0*prediction_test==test_labels)
		performance = acc
		print(f"Accuracy = {performance}")
		# Determine whether this solution
		# violates any of the constraints 
		# on the test dataset
		failed = False
		for parse_tree in parse_trees:
			parse_tree.evaluate_constraint(theta=theta_solution,
				dataset=dataset,
				model=lr_model,regime='supervised',
				branch='safety_test')

			g = parse_tree.root.value
			if g > 0:
				failed = True

		# Write out file for this data_pct,trial_i combo
		data = [data_pct,
			trial_i,
			performance,
			failed]
		colnames = ['data_pct','trial_i','performance','failed']
		self.write_trial_result(
			data,
			colnames,
			trial_dir,
			verbose=kwargs['verbose'])
		return 

	def linear_svm(self,data_pct,trial_i,**kwargs):
		""" Run a trial of logistic regression 
		
		:param data_pct: Fraction of overall dataset size to use
		:type data_pct: float

		:param trial_i: The index of the trial 
		:type trial_i: int
		"""
		trial_dir = os.path.join(
				kwargs['results_dir'],
				'linear_svm_results',
				'trial_data')

		os.makedirs(trial_dir,exist_ok=True)
		dataset = kwargs['dataset']
		orig_df = dataset.df
		# number of points in this partition of the data
		n_points = int(round(data_pct*len(orig_df))) 

		test_features = kwargs['test_features']
		test_labels = kwargs['test_labels']
		
		if kwargs['datagen_method'] == 'resample':
			resampled_filename = os.path.join(kwargs['results_dir'],
			'resampled_dataframes',f'trial_{trial_i}.csv')
			n_points = int(round(data_pct*len(test_features))) 
			with open(resampled_filename,'rb') as infile:
				df = pickle.load(infile).iloc[:n_points]
			# df = pd.read_csv(resampled_filename).iloc[:n_points]
		else:
			raise NotImplementedError(f"datagen_method: {datagen_method} not implemented")
		# set labels to 0 and 1, not -1 and 1, like some classification datasets will have
		df.loc[df[dataset.label_column]==-1.0,dataset.label_column]=0.0

		features = df.loc[:,
			df.columns != dataset.label_column]

		features = features.drop(
			columns=dataset.sensitive_column_names)

		labels = df[dataset.label_column]
		
		clf = make_pipeline(StandardScaler(),
		  SGDClassifier(loss='hinge',max_iter=kwargs['max_iter']))
		
		clf.fit(features, labels)

		prediction = clf.predict(test_features)
		
		# Calculate accuracy 
		acc = np.mean(1.0*prediction==test_labels)
		performance = acc
		# Determine whether this solution
		# violates any of the constraints 
		# on the test dataset
		failed = False
		for gfunc in kwargs['constraint_funcs']:
			for parse_tree in parse_trees:
				parse_tree.evaluate_constraint(theta=candidate_solution,
					dataset=dataset,
					model=model,regime='supervised',
					branch='safety_test')
				g = parse_tree.root.value
				if g > 0:
					failed = True

		# Write out file for this data_pct,trial_i combo
		data = [data_pct,
			trial_i,
			performance,
			failed]
		colnames = ['data_pct','trial_i','performance','failed']
		self.write_trial_result(
			data,
			colnames,
			trial_dir,
			verbose=kwargs['verbose'])
		return 

class FairlearnExperiment(Experiment):

	def __init__(self,results_dir):
		""" Class for running Seldonian experiments

		:param model_name: The string name of the Seldonian model, 
			only option is currently: 'qsa' (quasi-Seldonian algorithm) 
		:type model_name: str

		:param results_dir: Parent directory for saving any
			experimental results
		:type results_dir: str

		:param fairlearn_sensitive_feature_names: List of column names
			that Fairlearn will use as sensitive features
		:type fairlearn_sensitive_feature_names: List(str) 
		"""
		super().__init__(results_dir=results_dir,model_name='Fairlearn')

	def run_experiment(self,**kwargs):
		""" Run the Fairlearn experiment """
		n_workers = kwargs['n_workers']
		partial_kwargs = {key:kwargs[key] for key in kwargs \
			if key not in ['data_pcts','n_trials']}

		helper = partial(
			self.run_fairlearn_trial,
			**partial_kwargs
		)

		data_pcts = kwargs['data_pcts']
		n_trials = kwargs['n_trials']
		data_pcts_vector = np.array([x for x in data_pcts for y in range(n_trials)])
		trials_vector = np.array([x for y in range(len(data_pcts)) for x in range(n_trials)])

		if n_workers == 1:
			for ii in range(len(data_pcts_vector)):
				data_pct = data_pcts_vector[ii]
				trial_i = trials_vector[ii]
				print(data_pct,trial_i)
				helper(data_pct,trial_i)
		elif n_workers > 1:
			with ProcessPoolExecutor(max_workers=n_workers,
				mp_context=mp.get_context('fork')) as ex:
				results = tqdm(ex.map(helper,data_pcts_vector,trials_vector),
					total=len(data_pcts_vector))
				for exc in results:
					if exc:
						print(exc)
		else:
			raise ValueError(f"n_workers value of {n_workers} must be >=1 ")

		self.aggregate_results(**kwargs)
	
	def run_fairlearn_trial(self,data_pct,trial_i,**kwargs):
		""" Run a trial of the quasi-Seldonian algorithm  
		
		:param data_pct: Fraction of overall dataset size to use
		:type data_pct: float

		:param trial_i: The index of the trial 
		:type trial_i: int
		"""
		spec = kwargs['spec']
		verbose=kwargs['verbose']
		datagen_method = kwargs['datagen_method']
		fairlearn_sensitive_feature_names = kwargs['fairlearn_sensitive_feature_names']
		fairlearn_constraint_name = kwargs['fairlearn_constraint_name']
		fairlearn_epsilon_constraint = kwargs['fairlearn_epsilon_constraint']
		fairlearn_epsilon_eval = kwargs['fairlearn_epsilon_eval']
		fairlearn_eval_kwargs = kwargs['fairlearn_eval_kwargs']
		perf_eval_fn = kwargs['perf_eval_fn']
		perf_eval_kwargs = kwargs['perf_eval_kwargs']
		constraint_eval_fns = kwargs['constraint_eval_fns']
		constraint_eval_kwargs = kwargs['constraint_eval_kwargs']

		regime=spec.dataset.regime
		assert regime == 'supervised'

		trial_dir = os.path.join(
				self.results_dir,
				'fairlearn_results',
				'trial_data')

		savename = os.path.join(trial_dir,
			f'data_pct_{data_pct:.4f}_trial_{trial_i}.csv')

		if os.path.exists(savename):
			if verbose:
				print(f"Trial {trial_i} already run for"
					  f"this data_pct: {data_pct}. Skipping this trial. ")
			return

		os.makedirs(trial_dir,exist_ok=True)
		
		parse_trees = spec.parse_trees
		dataset = spec.dataset

		##############################################
		""" Setup for running Fairlearn algorithm """
		##############################################

		sensitive_column_names = dataset.sensitive_column_names
		include_sensitive_columns = dataset.include_sensitive_columns
		include_intercept_term = False 
		label_column = dataset.label_column

		if datagen_method == 'resample':
			resampled_filename = os.path.join(self.results_dir,
				'resampled_dataframes',f'trial_{trial_i}.pkl')
			n_points = int(round(data_pct*len(dataset.df))) 

			with open(resampled_filename,'rb') as infile:
				resampled_df = pickle.load(infile).iloc[:n_points]

			if verbose:
				print(f"Using resampled dataset {resampled_filename} "
					  f"with {len(resampled_df)} datapoints")
		else:
			raise NotImplementedError(
				f"datagen_method: {datagen_method} "
				f"not supported for regime: {regime}")
		

		# Prepare features and labels

		features = resampled_df.loc[:,
		    resampled_df.columns != label_column]
		labels = resampled_df[label_column].astype('int')

		# Drop sensitive features from training set
		if not include_sensitive_columns:
		    features = features.drop(
		        columns=dataset.sensitive_column_names)	

		# Get fairlearn sensitive features
		fairlearn_sensitive_features = resampled_df.loc[:,
			fairlearn_sensitive_feature_names]

		

		##############################################
		"""" Run Fairlearn algorithm on trial data """
		##############################################

		if fairlearn_constraint_name == "disparate_impact":
			print("Enforcing demographic parity with epsilon: "
				  f"{fairlearn_epsilon_constraint}")
			fairlearn_constraint = DemographicParity(
				difference_bound=fairlearn_epsilon_constraint)
		elif fairlearn_constraint_name == "demographic_parity":
			fairlearn_constraint = DemographicParity(
				difference_bound=fairlearn_epsilon_constraint)
		elif fairlearn_constraint_name == "predictive_equality":
			fairlearn_constraint = FalsePositiveRateParity(
				difference_bound=fairlearn_epsilon_constraint)
		else:
			raise NotImplementedError(
				"Fairlearn constraints of type: "
			   f"{fairlearn_constraint_name} "
			    "is not supported.")

		classifier = LogisticRegression()
		
		mitigator = ExponentiatedGradient(classifier, 
			fairlearn_constraint)
		
		mitigator.fit(features, labels, 
			sensitive_features=fairlearn_sensitive_features)

		#########################################################
		"""" Calculate performance and safety on ground truth """
		#########################################################
		
		fairlearn_eval_kwargs['model'] = mitigator

		performance = perf_eval_fn(
			solution=None,
			**fairlearn_eval_kwargs)
			
		if verbose:
			print(f"Performance = {performance}")
			
		########################################
		""" Calculate safety on ground truth """
		########################################
		if verbose:
			print("Determining whether solution "
				  "is actually safe on ground truth")
		
		# predict the class label, not the probability
		# Determine whether this solution
		# violates any of the constraints 
		# on the test dataset
		
		failed = self.evaluate_constraint_functions(
			mitigator=mitigator,
			test_features=fairlearn_eval_kwargs['X'],
			test_labels=fairlearn_eval_kwargs['y'],
			fairlearn_constraint_name=fairlearn_constraint_name,
			epsilon_eval=fairlearn_epsilon_eval,
			sensitive_features=fairlearn_eval_kwargs['sensitive_features'])
		
		# Write out file for this data_pct,trial_i combo
		data = [data_pct,
			trial_i,
			performance,
			failed]

		colnames = ['data_pct','trial_i','performance','failed']
		self.write_trial_result(
			data,
			colnames,
			trial_dir,
			verbose=kwargs['verbose'])
		return
	
	def evaluate_constraint_functions(self,
		mitigator,
		test_features,
		test_labels,
		fairlearn_constraint_name,
		epsilon_eval,
		sensitive_features):
		""" Helper function 
		
		"""
		print(f"Evaluating constraint for: {fairlearn_constraint_name}")
		failed = False

		# print(f"Epsilon = {epsilon}")
		y_pred = mitigator.predict(test_features)

		if fairlearn_constraint_name == "demographic_parity":
			# g = abs((PR | ATR1) - (PR | ATR2)) - eps
			PR_frame = MetricFrame(
				metrics=selection_rate,
				y_true=test_labels, y_pred=y_pred,
				sensitive_features=sensitive_features)
			PR_grouped = PR_frame.by_group
			PR_group1 = PR_grouped.iloc[0]
			PR_group2 = PR_grouped.iloc[1]
			g = abs(PR_group1 - PR_group2) - epsilon_eval

		elif fairlearn_constraint_name == "predictive_equality":
			# g = abs((FPR | ATR1) - (FPR | ATR2)) - eps
			FPR_frame = MetricFrame(
				metrics=false_positive_rate,
				y_true=test_labels, y_pred=y_pred,
				sensitive_features=sensitive_features)
			FPR_grouped = FPR_frame.by_group
			FPR_group1 = FPR_grouped.iloc[0]
			FPR_group2 = FPR_grouped.iloc[1]
			g = abs(FPR_group1 - FPR_group2) - epsilon_eval

		elif fairlearn_constraint_name == "disparate_impact":
			# g = epsilon - min((PR | ATR1)/(PR | ATR2),(PR | ATR2)/(PR | ATR1))
			PR_frame = MetricFrame(
				metrics=selection_rate,
				y_true=test_labels, y_pred=y_pred,
				sensitive_features=sensitive_features)
			PR_grouped = PR_frame.by_group
			PR_group1 = PR_grouped.iloc[0]
			PR_group2 = PR_grouped.iloc[1]
			print(PR_group1,PR_group2,PR_group1/PR_group2,PR_group2,PR_group1)
			g = epsilon_eval - min(PR_group1/PR_group2,PR_group2/PR_group1) 
		else:
			raise NotImplementedError(
				"Evaluation for Fairlearn constraints of type: "
			   f"{fairlearn_constraint.short_name} "
			    "is not supported.")
		
		print(f"g = {g}")
		if g > 0:
			failed = True

		return failed

class SeldonianExperiment(Experiment):
	def __init__(self,model_name,results_dir):
		""" Class for running Seldonian experiments

		:param model_name: The string name of the Seldonian model, 
			only option is currently: 'qsa' (quasi-Seldonian algorithm) 
		:type model_name: str

		:param results_dir: Parent directory for saving any
			experimental results
		:type results_dir: str

		"""
		super().__init__(model_name,results_dir)
		if self.model_name != 'QSA':
			raise NotImplementedError(
				"Seldonian experiments for model: "
				f"{self.model_name} are not supported.")

	def run_experiment(self,**kwargs):
		""" Run the Seldonian experiment """
		n_workers = kwargs['n_workers']
		partial_kwargs = {key:kwargs[key] for key in kwargs \
			if key not in ['data_pcts','n_trials']}

		helper = partial(
			self.QSA,
			**partial_kwargs
		)

		data_pcts = kwargs['data_pcts']
		n_trials = kwargs['n_trials']
		data_pcts_vector = np.array([x for x in data_pcts for y in range(n_trials)])
		trials_vector = np.array([x for y in range(len(data_pcts)) for x in range(n_trials)])

		if n_workers == 1:
			for ii in range(len(data_pcts_vector)):
				data_pct = data_pcts_vector[ii]
				trial_i = trials_vector[ii]
				print(data_pct,trial_i)
				helper(data_pct,trial_i)
		elif n_workers > 1:
			with ProcessPoolExecutor(max_workers=n_workers,
				mp_context=mp.get_context('fork')) as ex:
				results = tqdm(ex.map(helper,data_pcts_vector,trials_vector),
					total=len(data_pcts_vector))
				for exc in results:
					if exc:
						print(exc)
		else:
			raise ValueError(f"n_workers value of {n_workers} must be >=1 ")

		self.aggregate_results(**kwargs)
	
	def QSA(self,data_pct,trial_i,**kwargs):
		""" Run a trial of the quasi-Seldonian algorithm  
		
		:param data_pct: Fraction of overall dataset size to use
		:type data_pct: float

		:param trial_i: The index of the trial 
		:type trial_i: int
		"""
		spec = kwargs['spec']
		verbose=kwargs['verbose']
		datagen_method = kwargs['datagen_method']
		perf_eval_fn = kwargs['perf_eval_fn']
		perf_eval_kwargs = kwargs['perf_eval_kwargs']
		constraint_eval_fns = kwargs['constraint_eval_fns']
		constraint_eval_kwargs = kwargs['constraint_eval_kwargs']

		regime=spec.dataset.regime

		trial_dir = os.path.join(
				self.results_dir,
				'qsa_results',
				'trial_data')

		savename = os.path.join(trial_dir,
			f'data_pct_{data_pct:.4f}_trial_{trial_i}.csv')

		if os.path.exists(savename):
			if verbose:
				print(f"Trial {trial_i} already run for"
					  f"this data_pct: {data_pct}. Skipping this trial. ")
			return

		os.makedirs(trial_dir,exist_ok=True)
		
		parse_trees = spec.parse_trees
		dataset = spec.dataset

		##############################################
		""" Setup for running Seldonian algorithm """
		##############################################

		if regime == 'supervised':

			sensitive_column_names = dataset.sensitive_column_names
			include_sensitive_columns = dataset.include_sensitive_columns
			include_intercept_term = dataset.include_intercept_term
			label_column = dataset.label_column

			if datagen_method == 'resample':
				resampled_filename = os.path.join(self.results_dir,
					'resampled_dataframes',f'trial_{trial_i}.pkl')
				n_points = int(round(data_pct*len(dataset.df))) 

				with open(resampled_filename,'rb') as infile:
					resampled_df = pickle.load(infile).iloc[:n_points]

				if verbose:
					print(f"Using resampled dataset {resampled_filename} "
						  f"with {len(resampled_df)} datapoints")
			else:
				raise NotImplementedError(
					f"Eval method {datagen_method} "
					f"not supported for regime={regime}")
			dataset_for_experiment = SupervisedDataSet(
				df=resampled_df,
				meta_information=resampled_df.columns,
				label_column=label_column,
				sensitive_column_names=sensitive_column_names,
				include_sensitive_columns=include_sensitive_columns,
				include_intercept_term=include_intercept_term)

			# Make a new spec object where the 
			# only thing that is different is the dataset

			spec_for_experiment = copy.deepcopy(spec)
			spec_for_experiment.dataset = dataset_for_experiment
			model_instance = spec_for_experiment.model_class()

		elif regime == 'RL':
			RL_environment_obj = kwargs['RL_environment_obj']
			
			if datagen_method == 'generate_episodes':
				n_episodes_for_eval = perf_eval_kwargs['n_episodes']
				# Sample from resampled dataset on disk of n_episodes
				save_dir = os.path.join(self.results_dir,'resampled_datasets')
				# savename = os.path.join(save_dir,f'resampled_df_trial{trial_i}.csv')
				savename = os.path.join(save_dir,f'resampled_data_trial{trial_i}.pkl')
				
				episodes_all = load_pickle(savename)
				# Take data_pct episodes from this df
				n_episodes_all = len(episodes_all)

				n_episodes_for_exp = int(round(n_episodes_all*data_pct))
				print(f"Orig dataset should have {n_episodes_all} episodes")
				print(f"This dataset with data_pct={data_pct} should have"
					f" {n_episodes_for_exp} episodes")
				
				# Take first n_episodes episodes 
				episodes_for_exp = episodes_all[0:n_episodes_for_exp]
				assert len(episodes_for_exp) == n_episodes_for_exp

				dataset_for_experiment = RLDataSet(
					episodes=episodes_for_exp,
					meta_information=dataset.meta_information,
					regime=regime)

				# Make a new spec object from a copy of spec, where the 
				# only thing that is different is the dataset

				spec_for_experiment = copy.deepcopy(spec)
				spec_for_experiment.dataset = dataset_for_experiment
				model_instance = spec_for_experiment.model_class(RL_environment_obj)

			else:
				raise NotImplementedError(
					f"Eval method {datagen_method} "
					"not supported for regime={regime}")
		
		################################
		"""" Run Seldonian algorithm """
		################################

		SA = SeldonianAlgorithm(
			spec_for_experiment)
		passed_safety,candidate_solution = SA.run()

		print("Solution from running seldonian algorithm:")
		print(candidate_solution)
		print()
		
		# Handle whether solution was found 
		solution_found=True
		if type(candidate_solution) == str and candidate_solution == 'NSF':
			solution_found = False
		
		#########################################################
		"""" Calculate performance and safety on ground truth """
		#########################################################
		
		failed=False # flag for whether we were actually safe on test set

		if solution_found:
			solution = copy.deepcopy(candidate_solution)
			# If passed the safety test, calculate performance
			# using solution 
			if passed_safety:
				if verbose:
					print("Passed safety test. Calculating performance")

				#############################
				""" Calculate performance """
				#############################
			
				performance = perf_eval_fn(
					solution,
					**perf_eval_kwargs)
					
				if verbose:
					print(f"Performance = {performance}")
			
				########################################
				""" Calculate safety on ground truth """
				########################################
				if verbose:
					print("Determining whether solution "
						  "is actually safe on ground truth")
				
				if constraint_eval_fns == []:
					constraint_eval_kwargs['model']=model_instance
					constraint_eval_kwargs['spec_orig']=spec
					constraint_eval_kwargs['spec_for_experiment']=spec_for_experiment
					constraint_eval_kwargs['regime']=regime
					constraint_eval_kwargs['branch'] = 'safety_test'
					constraint_eval_kwargs['verbose']=verbose

				failed = self.evaluate_constraint_functions(
					solution=solution,
					constraint_eval_fns=constraint_eval_fns,
					constraint_eval_kwargs=constraint_eval_kwargs)
				
				if verbose:
					if failed:
						print("Solution was not actually safe on ground truth!")
					else:
						print("Solution was safe on ground truth")
					print()
			else:
				if verbose:
					print("Failed safety test ")
					performance = np.nan
		
		else:
			print("NSF")
			performance = np.nan
		# Write out file for this data_pct,trial_i combo
		data = [data_pct,
			trial_i,
			performance,
			passed_safety,
			failed]
		colnames = ['data_pct','trial_i','performance','passed_safety','failed']
		self.write_trial_result(
			data,
			colnames,
			trial_dir,
			verbose=kwargs['verbose'])
		return
		# except Exception as e:
		# 	return e
		# return None

	def evaluate_constraint_functions(self,
		solution,constraint_eval_fns,
		constraint_eval_kwargs):
		""" Helper function for QSA() to evaluate
		the constraint functions to determine
		whether solution was safe on ground truth

		:param solution: The weights of the model found
			during candidate selection in a given trial
		:type solution: numpy ndarray

		:param constraint_eval_fns: List of functions
			to use to evaluate each constraint. 
			An empty list results in using the parse
			tree to evaluate the constraints
		:type constraint_eval_fns: List(function)

		:param constraint_eval_kwargs: keyword arguments
			to pass to each constraint function 
			in constraint_eval_fns
		:type constraint_eval_kwargs: dict
		"""
		# Use safety test branch so the confidence bounds on
		# leaf nodes are not inflated
		failed = False
		if constraint_eval_fns == []:
			""" User did not provide their own functions
			to evaluate the constraints. Use the default: 
			the parse tree has a built-in way to evaluate constraints.
			"""
			constraint_eval_kwargs['theta'] = solution
			spec_orig = constraint_eval_kwargs['spec_orig']
			spec_for_experiment = constraint_eval_kwargs['spec_for_experiment']
			regime = constraint_eval_kwargs['regime']
			if regime == 'supervised':
				# Use the original dataset as ground truth
				constraint_eval_kwargs['dataset']=spec_orig.dataset 

			if regime == 'RL':
				# Generate episodes and create dataset object
				RL_environment_obj = constraint_eval_kwargs['RL_environment_obj']
				RL_environment_obj.param_weights = solution
				episodes_for_eval = RL_environment_obj.generate_data(
					n_episodes=constraint_eval_kwargs['n_episodes'],
					n_workers=1,
					parallel=False) 

				dataset_for_eval = RLDataSet(
					episodes=episodes_for_eval,
					meta_information=spec_for_experiment.dataset.meta_information,
					regime=regime)

				constraint_eval_kwargs['dataset'] = dataset_for_eval
				constraint_eval_kwargs['gamma'] = RL_environment_obj.gamma
				constraint_eval_kwargs['normalize_returns'] = spec_for_experiment.normalize_returns

				if spec_for_experiment.normalize_returns:
					constraint_eval_kwargs['min_return'] = RL_environment_obj.min_return
					constraint_eval_kwargs['max_return'] = RL_environment_obj.max_return

			for parse_tree in spec_for_experiment.parse_trees:
				parse_tree.evaluate_constraint(
					**constraint_eval_kwargs)
				
				g = parse_tree.root.value
				if g > 0:
					failed = True

		else:
			# User provided functions to evaluate constraints
			for eval_fn in constraint_eval_fns:
				g = eval_fn(solution)
				if g > 0:
					failed = True
		return failed