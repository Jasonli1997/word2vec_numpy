"""
This is a implementation of Word2Vec using numpy. Uncomment the print functions to see Word2Vec in action! Also remember to change the number of epochs and set training_data to training_data[0] to avoid flooding your terminal. A Google Sheet implementation of Word2Vec is also available here - https://docs.google.com/spreadsheets/d/1mgf82Ue7MmQixMm2ZqnT1oWUucj6pEcd2wDs_JgHmco/edit?usp=sharing

Have fun learning!

Author: Derek Chia
Email: derek@derekchia.com
"""

import numpy as np
from collections import defaultdict

## Randomly initialise
getW1 = [[0.236, -0.962, 0.686, 0.785, -0.454, -0.833, -0.744, 0.677, -0.427, -0.066],
		[-0.907, 0.894, 0.225, 0.673, -0.579, -0.428, 0.685, 0.973, -0.070, -0.811],
		[-0.576, 0.658, -0.582, -0.112, 0.662, 0.051, -0.401, -0.921, -0.158, 0.529],
		[0.517, 0.436, 0.092, -0.835, -0.444, -0.905, 0.879, 0.303, 0.332, -0.275],
		[0.859, -0.890, 0.651, 0.185, -0.511, -0.456, 0.377, -0.274, 0.182, -0.237],
		[0.368, -0.867, -0.301, -0.222, 0.630, 0.808, 0.088, -0.902, -0.450, -0.408],
		[0.728, 0.277, 0.439, 0.138, -0.943, -0.409, 0.687, -0.215, -0.807, 0.612],
		[0.593, -0.699, 0.020, 0.142, -0.638, -0.633, 0.344, 0.868, 0.913, 0.429],
		[0.447, -0.810, -0.061, -0.495, 0.794, -0.064, -0.817, -0.408, -0.286, 0.149]]

getW2 = [[-0.868, -0.406, -0.288, -0.016, -0.560, 0.179, 0.099, 0.438, -0.551],
		[-0.395, 0.890, 0.685, -0.329, 0.218, -0.852, -0.919, 0.665, 0.968],
		[-0.128, 0.685, -0.828, 0.709, -0.420, 0.057, -0.212, 0.728, -0.690],
		[0.881, 0.238, 0.018, 0.622, 0.936, -0.442, 0.936, 0.586, -0.020],
		[-0.478, 0.240, 0.820, -0.731, 0.260, -0.989, -0.626, 0.796, -0.599],
		[0.679, 0.721, -0.111, 0.083, -0.738, 0.227, 0.560, 0.929, 0.017],
		[-0.690, 0.907, 0.464, -0.022, -0.005, -0.004, -0.425, 0.299, 0.757],
		[-0.054, 0.397, -0.017, -0.563, -0.551, 0.465, -0.596, -0.413, -0.395],
		[-0.838, 0.053, -0.160, -0.164, -0.671, 0.140, -0.149, 0.708, 0.425],
		[0.096, -0.995, -0.313, 0.881, -0.402, -0.631, -0.660, 0.184, 0.487]]

class skipgram():

	def __init__(self, settings):
		self.n = settings['n']
		self.lr = settings['learning_rate']
		self.epochs = settings['epochs']
		self.window = settings['window_size']
		self.negative_samples = settings['negative_samples']

	def generate_training_data(self, corpus):
		# Find unique word counts using dictonary
		word_counts = defaultdict(int)
		for row in corpus:
			for word in row:
				word_counts[word] += 1
		#########################################################################################################################################################
		# print(word_counts)																																	#
		# # defaultdict(<class 'int'>, {'natural': 1, 'language': 1, 'processing': 1, 'and': 2, 'machine': 1, 'learning': 1, 'is': 1, 'fun': 1, 'exciting': 1})	#
		#########################################################################################################################################################

		## How many unique words in vocab? 9
		self.v_count = len(word_counts.keys())
		#########################
		# print(self.v_count)	#
		# 9						#
		#########################

		# Generate Lookup Dictionaries (vocab)
		self.words_list = list(word_counts.keys())
		#################################################################################################
		# print(self.words_list)																		#
		# ['natural', 'language', 'processing', 'and', 'machine', 'learning', 'is', 'fun', 'exciting']	#
		#################################################################################################
		
		# Generate word:index
		self.word_index = dict((word, i) for i, word in enumerate(self.words_list))
		#############################################################################################################################
		# print(self.word_index)																									#
		# # {'natural': 0, 'language': 1, 'processing': 2, 'and': 3, 'machine': 4, 'learning': 5, 'is': 6, 'fun': 7, 'exciting': 8}	#
		#############################################################################################################################

		# Generate index:word
		self.index_word = dict((i, word) for i, word in enumerate(self.words_list))
		#############################################################################################################################
		# print(self.index_word)																									#
		# {0: 'natural', 1: 'language', 2: 'processing', 3: 'and', 4: 'machine', 5: 'learning', 6: 'is', 7: 'fun', 8: 'exciting'}	#
		#############################################################################################################################

		training_data = []

		# Cycle through each sentence in corpus
		for sentence in corpus:
			sent_len = len(sentence)

			if sent_len == 1:
				continue 

			# Cycle through each word in sentence
			for i, word in enumerate(sentence):
				# Save target word 
				w_target = word

				# Cycle through context window
				w_context = []

				# Note: window_size 2 will have range of 5 values
				for j in range(i - self.window, i + self.window+1):
					# Criteria for context word 
					# 1. Target word cannot be context word (j != i)
					# 2. Index must be greater or equal than 0 (j >= 0) - if not list index out of range
					# 3. Index must be less or equal than length of sentence (j <= sent_len-1) - if not list index out of range 
					if j != i and j <= sent_len-1 and j >= 0:
						# Append context word to w_context
						w_context.append(sentence[j])
						# print(sentence[i], sentence[j]) 
						#########################
						# Example:				#
						# natural language		#
						# natural processing	#
						# language natural		#
						# language processing	#
						# language append 		#
						#########################
						
				# training_data contains a one-hot representation of the target word and context words
                # only the word is store instead of its one-hot encoding due to storage limit and it crashes kernel
				#################################################################################################
				# Example:																						#
				# [Target] natural, [Context] language, [Context] processing									#
				# print(training_data)																			#
				# [[[1, 0, 0, 0, 0, 0, 0, 0, 0], [[0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0]]]]	#
				#################################################################################################
				training_data.append([w_target, w_context])

		return training_data

	def word2onehot(self, word):
		# word_vec - initialise a blank vector
		word_vec = np.zeros(self.v_count)
		#############################
		# print(word_vec)			#
		# [0, 0, 0, 0, 0, 0, 0, 0]	#
		#############################

		# Get ID of word from word_index
		word_index = self.word_index[word]

		# Change value from 0 to 1 according to ID of the word
		word_vec[word_index] = 1

		return word_vec

	def train(self, training_data):
		# Initialising weight matrices
		# np.random.uniform(HIGH, LOW, OUTPUT_SHAPE)
		# https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.random.uniform.html
		self.w1 = np.array(getW1)
		self.w2 = np.array(getW2)
		# self.w1 = np.random.uniform(-1, 1, (self.v_count, self.n))
		# self.w2 = np.random.uniform(-1, 1, (self.n, self.v_count))
		
		if self.negative_samples == 0:
			# Cycle through each epoch
			for i in range(self.epochs):
				print(f'Start Epoch {i}...')

				# Intialise loss to 0
				self.loss = 0

				# Cycle through each training sample
				# w_t = vector for target word, w_c = vectors for context words
				for w_t, w_c in training_data:
					w_t = self.word2onehot(w_t).reshape((-1, 1))
					w_c = [self.word2onehot(context) for context in w_c]
					# Forward pass
					# 1. predicted y using softmax (y_pred) 2. matrix of hidden layer (h) 3. output layer before softmax (u)
					y_pred, h, u = self.forward_pass(w_t)
					#########################################
					# print("Vector for target word:", w_t)	#
					# print("W1-before backprop", self.w1)	#
					# print("W2-before backprop", self.w2)	#
					#########################################

					# Calculate error
					# 1. For a target word, calculate difference between y_pred and each of the context words
					# 2. Sum up the differences using np.sum to give us the error for this particular target word
					EI = np.sum([np.subtract(y_pred, word.reshape((-1, 1))) for word in w_c], axis=0)
					#########################
					# print("Error", EI)	#
					#########################

					# Backpropagation
					# We use SGD to backpropagate errors - calculate loss on the output layer 
					self.backprop(EI, h, w_t)
					#########################################
					#print("W1-after backprop", self.w1)	#
					#print("W2-after backprop", self.w2)	#
					#########################################

					# Calculate loss
					# There are 2 parts to the loss function
					# Part 1: -ve sum of all the output +
					# Part 2: length of context words * log of sum for all elements (exponential-ed) in the output layer before softmax (u)
					# Note: word.index(1) returns the index in the context word vector with value 1
					# Note: u[word.index(1)] returns the value of the output layer before softmax
					self.loss += -np.sum([u[np.where(word == 1)[0][0]] for word in w_c]) + len(w_c) * np.log(np.sum(np.exp(u)))
					
					#############################################################
					# Break if you want to see weights after first target word 	#
					# break 													#
					#############################################################
				print('Epoch:', i, "Loss:", self.loss)
		
		else:
			# Cycle through each epoch
			for i in range(self.epochs):
				print(f'Start Epoch {i}...')

				# Intialise loss to 0
				self.loss = 0

				# Cycle through each training sample
				# w_t = vector for target word, w_c = vectors for context words
				for w_t, w_c in training_data:
					w_t = self.word2onehot(w_t).reshape((-1, 1))
					w_c = [self.word2onehot(context) for context in w_c]
					# Forward pass
					# 1. matrix of hidden layer (h) 2. output layer before softmax (u)
					# Run through first matrix (w1) to get hidden layer - NxV @ Vx1
					h = np.matmul(self.w1.T, w_t)
					# Dot product hidden layer with second matrix (w2) - VxN @ Nx1
					# Note: outputs before softmax are important since they stay the same 
					# and allow us to alter w2 without worrying about the loss function
					u = np.matmul(self.w2.T, h)

					#########################################
					# print("Vector for target word:", w_t)	#
					# print("W1-before backprop", self.w1)	#
					# print("W2-before backprop", self.w2)	#
					#########################################

					# Initialize EH for backpropagating to w1
					EH = np.zeros((self.n, 1))

					# Iterate through every context word as postive sample
					# and use uniform distribution to draw negative samples
					# TODO: uniform distribution for now but will do more research on unigram
					for j in range(len(w_c)):
						# Get postive and negative samples
						pos_sample = w_c[j]
						neg_samples = np.random.randint(low=0, high=self.v_count, size=self.negative_samples)

						# Get the intermediate steps and store the tuples (idx, u[idx]) in updates to avoid redundant computation
						# First element in updates is always the positive sample
						updates = []
						updates.append((np.where(pos_sample == 1)[0][0], self.sigmoid(u[np.where(pos_sample == 1)[0][0]])))
						for idx in neg_samples:
							updates.append((idx, self.sigmoid(-u[idx])))
						
						# Calculate loss
						# There are 2 parts to the loss function (postive sample and negative samples)
						self.loss += -np.log(updates[0][1]) - sum([np.log(neg) for _, neg in updates[1:]])

						# Backpropagation
						# We use SGD to backpropagate errors - calculate loss on the output layer
						# Update vector in w2 (NxV) corresponding to the positive sample
						self.w2[:, [updates[0][0]]] = self.w2[:, [updates[0][0]]] - (self.lr * (updates[0][1] - 1) * h)
						EH += (updates[0][1] - 1) * self.w2[:, [updates[0][0]]]
						
						# Update vector in w2 corresponding to the negative sample
						for (idx, neg) in updates[1:]:
							self.w2[:, [idx]] = self.w2[:, [idx]] - (self.lr * (1 - neg) * h)
							EH += (1 - neg) * self.w2[:, [idx]]
					
					# After calculating EH for each context word, we can now update w1 as normal skipgram
					dl_dw1 = np.outer(w_t, EH)
					self.w1 = self.w1 - (self.lr * dl_dw1)

					#########################################
					#print("W1-after backprop", self.w1)	#
					#print("W2-after backprop", self.w2)	#
					#########################################
				
					#############################################################
					# Break if you want to see weights after first target word 	#
					# break 													#
					#############################################################
				print('Epoch:', i, "Loss:", self.loss)

	def forward_pass(self, x):
		# x is one-hot vector for target word, shape - Vx1
		# Run through first matrix (w1) to get hidden layer - NxV @ Vx1
		h = np.matmul(self.w1.T, x)
		# Dot product hidden layer with second matrix (w2) - VxN @ Nx1 
		u = np.matmul(self.w2.T, h)
		# Run 1x9 through softmax to force each element to range of [0, 1] - 1x8
		y_c = self.softmax(u)
		return y_c, h, u

	def softmax(self, x):
		e_x = np.exp(x - np.max(x))
		return e_x / e_x.sum(axis=0)
	
	def sigmoid(self, x):
		return 1/(1+np.exp(-x))

	def backprop(self, e, h, x):
		# https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.outer.html
		# Column vector EI represents row-wise sum of prediction errors across each context word for the current center word
		# Going backwards, we need to take derivative of E with respect of w2
		# h - shape 10x1, e - shape 9x1, dl_dw2 - shape 10x9
		# x - shape 9x1, w2 - 10x9, e.T - 9x1
		dl_dw2 = np.outer(h, e)
		dl_dw1 = np.outer(x, np.dot(self.w2, e))
		########################################
		# print('Delta for w2', dl_dw2)			#
		# print('Hidden layer', h)				#
		# print('np.dot', np.dot(self.w2, e.T))	#
		# print('Delta for w1', dl_dw1)			#
		#########################################

		# Update weights
		self.w1 = self.w1 - (self.lr * dl_dw1)
		self.w2 = self.w2 - (self.lr * dl_dw2)

	# Get vector from word
	def word_vec(self, word):
		w_index = self.word_index[word]
		v_w = self.w1[w_index]
		return v_w

	# Input vector, returns nearest word(s)
	def vec_sim(self, word, top_n):
		v_w1 = self.word_vec(word)
		word_sim = {}

		for i in range(self.v_count):
			if self.index_word[i] != word:
				# Find the cosine similary score for each word in vocab except for the current word
				v_w2 = self.w1[i]
				theta_sum = np.dot(v_w1, v_w2)
				theta_den = np.linalg.norm(v_w1) * np.linalg.norm(v_w2)
				theta = theta_sum / theta_den

				w2 = self.index_word[i]
				word_sim[w2] = theta

		words_sorted = sorted(word_sim.items(), key=lambda kv: kv[1], reverse=True)

		for word, sim in words_sorted[:top_n]:
			print(word, sim)

#####################################################################
settings = {
	'window_size': 2,			# context window +- center word
	'n': 10,					# dimensions of word embeddings, also refer to size of hidden layer
	'epochs': 50,				# number of training epochs
	'learning_rate': 0.01,		# learning rate
	'negative_samples': 3   	# number of negative samples
								# 0 -> normal skipgram
}

text = "natural language processing and machine learning is fun and exciting"

# Note the .lower() as upper and lowercase does not matter in our implementation
# [['natural', 'language', 'processing', 'and', 'machine', 'learning', 'is', 'fun', 'and', 'exciting']]
corpus = [[word.lower() for word in text.split()]]

# Initialise object
w2v = skipgram(settings)

# Numpy ndarray with one-hot representation for [target_word, context_words]
training_data = w2v.generate_training_data(corpus)

# Training
w2v.train(training_data)

# Get vector for word
word = "machine"
vec = w2v.word_vec(word)
print(word, vec)

# Find similar words
w2v.vec_sim("machine", 3)
