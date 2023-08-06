from operator import itemgetter
from functools import reduce,partial
import pandas as pd
import autograd.numpy as np

from seldonian.utils.stats_utils import *


class Node(object):
	def __init__(self,name,lower,upper):
		"""The base class for all parse tree nodes
		
		:param name: 
			The name of the node
		:type name: str

		:param lower: 
			Lower confidence bound
		:type lower: float

		:param upper: 
			Upper confidence bound
		:type upper: float
		
		:ivar index: 
			The index of the node in the tree
		:vartype index: int

		:ivar left: 
			Left child node
		:vartype left: Node object, defaults to None

		:ivar right: 
			Right child node
		:vartype right: Node object, defaults to None
		
		:ivar will_lower_bound: 
			Whether this node needs a lower bound
		:vartype will_lower_bound: bool
		
		:ivar will_upper_bound: 
			Whether this node needs an upper bound
		:vartype will_upper_bound: bool

		"""
		self.name = name
		self.index = None 
		self.left  = None 
		self.right = None 
		self.lower = lower 
		self.upper = upper 
		self.will_lower_bound = True
		self.will_upper_bound = True

	def __repr__(self):
		""" The string representation of the node. 
		Also, what is displayed inside the node box 
		in the visual graph 
		"""
		lower_bracket = '(' if np.isinf(self.lower) else '[' 
		upper_bracket = ')' if np.isinf(self.upper) else ']'

		lower_str = f'{self.lower:g}' if self.will_lower_bound else '_'
		upper_str = f'{self.upper:g}' if self.will_upper_bound else '_'


		bounds_str = \
			f'{lower_bracket}{lower_str}, {upper_str}{upper_bracket}' \
			if (self.lower!= None or self.upper!=None) else '()'

		return '\n'.join(
			[
				'['+str(self.index)+']',
				str(self.name),
				u'\u03B5' + ' ' + bounds_str
			]
		) 
  
class BaseNode(Node):
	def __init__(self,
		name,
		lower=float('-inf'),
		upper=float('inf'),
		conditional_columns=[],
		**kwargs):
		""" Class for base variable leaf nodes
		in the parse tree.

		:param name: 
			The name of the node
		:type name: str
		
		:param lower: 
			Lower confidence bound
		:type lower: float

		:param upper: 
			Upper confidence bound
		:type upper: float

		:param conditional_columns: 
			When calculating confidence bounds on a measure 
			function, condition on these columns being == 1
		:type conditional_columns: List(str)

		:ivar node_type: 
			equal to 'base_node'
		:vartype node_type: str

		:ivar delta: 
			The share of the confidence put into this node
		:vartype delta: float

		:ivar measure_function_name: str
			The name of the statistical measurement
			function that this node represents, e.g. "FPR". 
			Must be contained in measure_functions
			list in :py:mod:`.operators`
		:vartype measure_function_name: str
		"""
		super().__init__(name,lower,upper,**kwargs)
		self.conditional_columns = conditional_columns
		
		self.node_type = 'base_node'
		self.delta = 0  
		self.measure_function_name = '' 

	def __repr__(self):
		""" Overrides Node.__repr__()
		"""
		return super().__repr__() + ', ' + u'\u03B4' + f'={self.delta:g}'
	
	def calculate_value(self,
		**kwargs):
		"""
		Calculate the value of the node 
		given model weights, etc. This is
		the expected value of the base variable,
		not the bound.
		""" 
	
		model = kwargs['model']
		theta = kwargs['theta']
		data_dict = kwargs['data_dict']
		value = model.evaluate_statistic(
			statistic_name=self.measure_function_name,
			theta=theta,
			data_dict=data_dict)
		return value

	def mask_dataframe(self,
		dataset,
		conditional_columns):
		"""Mask dataset's dataframe using 
		a joint AND mask where each of the
		conditional columns is True.

		:param dataset: 
			The candidate or safety dataset
		:type dataset: dataset.Dataset object
		
		:param conditional_columns: 
			List of columns for which to create
			the joint AND mask on the dataset
		:type conditional_columns: List(str)

		:return: The masked dataframe 
		:rtype: numpy ndarray
		"""
		col_indices=[0 if conditional_columns[0]=='M' else 1]
		masks = reduce(np.logical_and,(dataset.df.values[:,col_index]==1 for col_index in col_indices))
		masked_df = dataset.df.values[masks] 
		return masked_df

	def calculate_data_forbound(self,**kwargs):
		"""
		Prepare data inputs
		for confidence bound calculation.
		"""
		theta,dataset,model,regime,branch = itemgetter(
					'theta','dataset','model',
					'regime','branch')(kwargs)

		if branch == 'candidate_selection':
			# Then we're in candidate selection
			n_safety = kwargs['n_safety']

		# If in candidate selection want to use safety data size
		# in bound calculation
		
		if regime == 'supervised':
			# mask the data using the conditional columns, if present
			if self.conditional_columns:
				dataframe = self.mask_dataframe(
					dataset,self.conditional_columns)
			else:
				dataframe = dataset.df.values

			if branch == 'candidate_selection':
				frac_masked = len(dataframe)/len(dataset.df)
				datasize = int(round(frac_masked*n_safety))
			else:
				datasize = len(dataframe)
			
			# Separate features from label
			label_column = dataset.label_column
			# label_column_index = dataset.df.columns.get_loc(label_column)
			label_column_index = -1
			labels = dataframe[:,label_column_index]
			# features = dataframe.loc[:, dataframe.columns != label_column]
			features = np.delete(dataframe,label_column_index,axis=1)

			# drop sensitive column names, unless instructed to keep them
			if not dataset.include_sensitive_columns:
				if dataset.sensitive_column_names:
					# sensitive_col_indices = [dataset.df.columns.get_loc(col) for col in dataset.sensitive_column_names]
					sensitive_col_indices = [0,1]
					# features = features.drop(columns=dataset.sensitive_column_names)
					features = np.delete(features,sensitive_col_indices,axis=1)

			# Intercept term
			if dataset.include_intercept_term:
				# features.insert(0,'offset',1.0) # inserts a column of 1's
				features = np.insert(features,0,np.ones(len(dataframe)),axis=1)

			data_dict = {'features':features,'labels':labels}  
			
		elif regime == 'RL':
			gamma = kwargs['gamma']
			episodes = dataset.episodes

			if branch == 'candidate_selection':
				datasize = n_safety
			else:
				datasize = len(episodes)
			
			# Precalculate expected return from behavioral policy
			returns = [weighted_sum_gamma(ep.rewards,gamma) for ep in episodes]
			if kwargs['normalize_returns']==True:
				# normalize returns 
				min_return = kwargs['min_return']
				max_return = kwargs['max_return']
				returns = (returns-min_return)/(max_return-min_return)

			data_dict = {
				'episodes':episodes,
				'reward_sums_by_episode':returns
			}

		return data_dict,datasize

	def zhat(self,model,theta,data_dict):
		"""
		Calculate an unbiased estimate of the 
		base variable node.
	
		:param model: The machine learning model
		:type model: models.SeldonianModel object
	
		:param theta: 
			model weights
		:type theta: numpy ndarray
		
		:param data_dict: 
			Contains inputs to model, 
			such as features and labels
		:type data_dict: dict
		"""

		return model.sample_from_statistic(
			statistic_name=self.measure_function_name,
			theta=theta,data_dict=data_dict)
					
	def calculate_bounds(self,
		**kwargs):
		"""Calculate confidence bounds given a bound_method, 
		such as t-test.
		""" 
		if 'bound_method' in kwargs:
			bound_method = kwargs['bound_method']
			if bound_method == 'manual':
				# Bounds set by user
				return {'lower':self.lower,
						'upper':self.upper}

			elif bound_method == 'random':
				# Randomly assign lower and upper bounds
				lower, upper = (
					np.random.randint(0,2),
					np.random.randint(2,4)
					)
				return {'lower':lower,'upper':upper}
		
			else:
				# Real confidence bound 

				# --TODO-- abstract away to support things like 
				# getting confidence intervals from bootstrap
				# and RL cases
				branch = kwargs['branch']
				model = kwargs['model']
				theta = kwargs['theta']
				data_dict = kwargs['data_dict']
				estimator_samples = self.zhat(
					model=model,
					theta=theta,
					data_dict=data_dict)
				if self.will_lower_bound and self.will_upper_bound:
					if branch == 'candidate_selection':
						lower,upper = self.predict_HC_upper_and_lowerbound(
							data=estimator_samples,
							delta=self.delta,
							**kwargs)  
					elif branch == 'safety_test':
						lower,upper = self.compute_HC_upper_and_lowerbound(
							data=estimator_samples,
							delta=self.delta,
							**kwargs)  
					return {'lower':lower,'upper':upper}
				
				elif self.will_lower_bound:
					if branch == 'candidate_selection':
						lower = self.predict_HC_lowerbound(
							data=estimator_samples,
							delta=self.delta,
							**kwargs)  
					elif branch == 'safety_test':
						lower = self.compute_HC_lowerbound(
							data=estimator_samples,
							delta=self.delta,
							**kwargs)  
					return {'lower':lower}

				elif self.will_upper_bound:
					if branch == 'candidate_selection':
						upper = self.predict_HC_upperbound(
							data=estimator_samples,
							delta=self.delta,
							**kwargs)  
					elif branch == 'safety_test':
						upper = self.compute_HC_upperbound(
							data=estimator_samples,
							delta=self.delta,
							**kwargs)  
					return {'upper':upper}

				raise AssertionError("will_lower_bound and will_upper_bound cannot both be False")

	def predict_HC_lowerbound(self,
		data,
		datasize,
		delta,
		**kwargs):
		"""
		Calculate high confidence lower bound
		that we expect to pass the safety test.
		Used in candidate selection

		:param data: 
			Vector containing base variable  
			evaluated at each observation in dataset
		:type data: numpy ndarray 

		:param datasize: 
			The number of observations in the safety dataset
		:type datasize: int
		
		:param delta: 
			Confidence level, e.g. 0.05
		:type delta: float
		""" 
		if 'bound_method' in kwargs:
			bound_method = kwargs['bound_method']

			if bound_method == 'ttest':
				lower = data.mean() - 2*stddev(data) / np.sqrt(datasize) * tinv(1.0 - delta, datasize - 1)
			else:
				raise NotImplementedError(f"Bounding method {bound_method} is not supported")
		
		return lower

	def predict_HC_upperbound(self,
		data,
		datasize,
		delta,
		**kwargs):
		"""
		Calculate high confidence upper bound
		that we expect to pass the safety test.
		Used in candidate selection

		:param data: 
			Vector containing base variable  
			evaluated at each observation in dataset
		:type data: numpy ndarray 

		:param datasize: 
			The number of observations in the safety dataset
		:type datasize: int
		
		:param delta: 
			Confidence level, e.g. 0.05
		:type delta: float
		"""  
		if 'bound_method' in kwargs:
			bound_method = kwargs['bound_method']
			if bound_method == 'ttest':
				lower = data.mean() + 2*stddev(data) / np.sqrt(datasize) * tinv(1.0 - delta, datasize - 1)
			else:
				raise NotImplementedError(f"Bounding method {bound_method} is not supported")
			
		return lower

	def predict_HC_upper_and_lowerbound(self,
		data,
		datasize,
		delta,
		**kwargs):
		"""
		Calculate high confidence lower and upper bounds
		that we expect to pass the safety test.
		Used in candidate selection.
	
		Depending on the bound_method,
		this is not always equivalent
		to calling predict_HC_lowerbound() and 
		predict_HC_upperbound() independently.

		:param data: 
			Vector containing base variable  
			evaluated at each observation in dataset
		:type data: numpy ndarray 

		:param datasize: 
			The number of observations in the safety dataset
		:type datasize: int
		
		:param delta: 
			Confidence level, e.g. 0.05
		:type delta: float
		""" 
		if 'bound_method' in kwargs:
			bound_method = kwargs['bound_method']
			if bound_method == 'ttest':
				lower = self.predict_HC_lowerbound(data=data,
					datasize=datasize,delta=delta/2,
					**kwargs)
				upper = self.predict_HC_upperbound(data=data,
					datasize=datasize,delta=delta/2,
					**kwargs)

			elif bound_method == 'manual':
				pass
			else:
				raise NotImplementedError(
					f"Bounding method {bound_method}"
					" is not supported")

			
		return lower,upper

	def compute_HC_lowerbound(self,
		data,
		datasize,
		delta,
		**kwargs):
		"""
		Calculate high confidence lower bound
		Used in safety test

		:param data: 
			Vector containing base variable  
			evaluated at each observation in dataset
		:type data: numpy ndarray 

		:param datasize: 
			The number of observations in the safety dataset
		:type datasize: int
		
		:param delta: 
			Confidence level, e.g. 0.05
		:type delta: float
		"""  
		if 'bound_method' in kwargs:
			bound_method = kwargs['bound_method']
			if bound_method == 'ttest':	
				lower = data.mean() - stddev(data) / np.sqrt(datasize) * tinv(1.0 - delta, datasize - 1)
			else:
				raise NotImplementedError(
					f"Bounding method {bound_method}"
					" is not supported")
		return lower

	def compute_HC_upperbound(self,
		data,
		datasize,
		delta,
		**kwargs):
		"""
		Calculate high confidence upper bound
		Used in safety test

		:param data: 
			Vector containing base variable  
			evaluated at each observation in dataset
		:type data: numpy ndarray 

		:param datasize: 
			The number of observations in the safety dataset
		:type datasize: int
		
		:param delta: 
			Confidence level, e.g. 0.05
		:type delta: float
		"""
		if 'bound_method' in kwargs:
			bound_method = kwargs['bound_method']
			if bound_method == 'ttest':
				upper = data.mean() + stddev(data) / np.sqrt(datasize) \
					* tinv(1.0 - delta, datasize - 1)
			else:
				raise NotImplementedError(
					f"Bounding method {bound_method}"
					" is not supported")
			
		return upper
	
	def compute_HC_upper_and_lowerbound(self,
		data,
		datasize,
		delta,
		**kwargs):
		"""
		Calculate high confidence lower and upper bounds
		Used in safety test.
	
		Depending on the bound_method,
		this is not always equivalent
		to calling compute_HC_lowerbound() and 
		compute_HC_upperbound() independently.

		:param data: 
			Vector containing base variable  
			evaluated at each observation in dataset
		:type data: numpy ndarray 

		:param datasize: 
			The number of observations in the safety dataset
		:type datasize: int
		
		:param delta: 
			Confidence level, e.g. 0.05
		:type delta: float
		"""
		if 'bound_method' in kwargs:
			bound_method = kwargs['bound_method']
			if bound_method == 'ttest':
				lower = self.compute_HC_lowerbound(data=data,
					datasize=datasize,delta=delta/2,
					**kwargs)
				upper = self.compute_HC_upperbound(data=data,
					datasize=datasize,delta=delta/2,
					**kwargs)

			elif bound_method == 'manual':
				pass
			else:
				raise NotImplementedError(
					f"Bounding method {bound_method}"
					" is not supported")
		else:
			raise NotImplementedError("Have not implemented" 
					"confidence bounds without the keyword bound_method")

		return lower,upper
  
class MEDCustomBaseNode(BaseNode):
	def __init__(self,
		name,
		lower=float('-inf'),
		upper=float('inf'),
		**kwargs):
		""" 
		Custom base node that calculates pair-wise
		mean error differences between male and female
		points. This was used in the Seldonian regression algorithm 
		in the Thomas et al. 2019 Science paper (see Figure 2).

		Overrides several parent class methods 
		
		
		:param name: 
			The name of the node
		:type name: str
		
		:param lower: 
			Lower confidence bound
		:type lower: float
		
		:param upper: 
			Upper confidence bound
		:type upper: float

		:ivar delta: 
			The share of the confidence put into this node
		:vartype delta: float
		"""
		super().__init__(name,lower,upper,**kwargs)
		self.delta = 0  
		
	def calculate_data_forbound(self,**kwargs):
		""" 
		Overrides same method from parent class, :py:class:`.BaseNode`
		"""
		dataset = kwargs['dataset']
		dataframe = dataset.df
		
		# set up features and labels 
		label_column = dataset.label_column
		labels = dataframe[label_column]
		features = dataframe.loc[:, dataframe.columns != label_column]
		features.insert(0,'offset',1.0) # inserts a column of 1's
		
		# Do not drop the sensitive columns yet. 
		# They might be needed in precalculate_data()
		data_dict,datasize = self.precalculate_data(
			features,labels,**kwargs)

		if kwargs['branch'] == 'candidate_selection':
			n_safety = kwargs['n_safety']
			# frac_masked = len(dataframe)/len(dataset.df)
			frac_masked = datasize/len(dataframe)
			datasize = int(round(frac_masked*n_safety))

		return data_dict,datasize

	def precalculate_data(self,X,Y,**kwargs):
		""" 
		Preconfigure dataset for candidate selection or 
		safety test so that it does not need to be 
		recalculated on each iteration through the parse tree

		:param X: features
		:type X: pandas dataframe

		:param Y: labels
		:type Y: pandas dataframe		
		"""
		dataset = kwargs['dataset']

		male_mask = X.M == 1
		# drop sensitive column names 
		if dataset.sensitive_column_names:
			X = X.drop(columns=dataset.sensitive_column_names)
		X_male = X[male_mask]
		Y_male = Y[male_mask]
		X_female = X[~male_mask]
		Y_female = Y[~male_mask]
		N_male = len(X_male)
		N_female = len(X_female)
		N_least = min(N_male,N_female)
		
		# sample N_least from both without repeats 
		XY_male = pd.concat([X_male,Y_male],axis=1)
		XY_male = XY_male.sample(N_least,replace=True)
		X_male = XY_male.loc[:,XY_male.columns!= dataset.label_column]
		Y_male = XY_male[dataset.label_column]
		
		XY_female = pd.concat([X_female,Y_female],axis=1)
		XY_female = XY_female.sample(N_least,replace=True)
		X_female = XY_female.loc[:,XY_female.columns!= dataset.label_column]
		Y_female = XY_female[dataset.label_column]
		
		data_dict = {
			'X_male':X_male,
			'Y_male':Y_male,
			'X_female':X_female,
			'Y_female':Y_female}
		datasize=N_least
		return data_dict,datasize

	def zhat(self,model,theta,data_dict):
		"""
		Pair up male and female columns and compute a vector of:
		(y_i - y_hat_i | M) - (y_j - y_hat_j | F) - epsilon.
		There may not be the same number of male and female rows
		so the number of pairs is min(N_male,N_female)

		:param model: machine learning model
		:type model: models.SeldonianModel object

		:param theta: 
			model weights
		:type theta: numpy ndarray
		
		:param data_dict: 
			contains inputs to model, 
			such as features and labels
		:type data_dict: dict
		"""
		X_male = data_dict['X_male'].values
		Y_male = data_dict['Y_male'].values
		X_female = data_dict['X_female'].values
		Y_female = data_dict['Y_female'].values

		prediction_male = model.predict(theta,X_male)
		mean_error_male = prediction_male-Y_male

		prediction_female = model.predict(theta,X_female)
		mean_error_female = prediction_female-Y_female

		return mean_error_male - mean_error_female

class ConstantNode(Node):
	def __init__(self,name,value,**kwargs):
		""" 
		Class for constant leaf nodes 
		in the parse tree. Sets lower and upper
		bound as the value of the constant.

		:param name: 
			The name of the node
		:type name: str

		:param value: 
			The value of the constant the node represents
		:type value: float

		:ivar node_type: 
			'constant_node'
		:vartype node_type: str
		"""
		super().__init__(name=name,
			lower=value,upper=value,**kwargs)
		self.value = value
		self.node_type = 'constant_node'
  
class InternalNode(Node):
	def __init__(self,name,
		lower=float('-inf'),upper=float('inf'),**kwargs):
		""" 
		Class for internal (non-leaf) nodes 
		in the parse tree.
		These represent operators, such as +,-,*,/ etc.

		:param name: 
			The name of the node, which is the 
			string representation of the operation 
			the node performs
		:type name: str
		"""
		super().__init__(name,lower,upper,**kwargs)
		self.node_type = 'internal_node'
