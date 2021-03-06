import numpy as np
import gc
import time

class database:
	def __init__(self, size, input_dims):
		self.size = size
		self.states = np.zeros([self.size, 84, 84], dtype='float') # image dimensions
		self.actions = np.zeros(self.size, dtype='float')
		self.terminals = np.zeros(self.size, dtype='float')
		self.rewards = np.zeros(self.size, dtype='float')
		
		self.counter = 0 # keep track of next empty state
		self.batch_counter = 0
		self.rand_idxs = np.arrange(3, 300)
		self.flag = False
		return
	
	def four_image(self, idx):
		four_s = np.zeros([84, 84, 4])
		four_n = np.zeros([84, 84, 4])
		for i in range(0, 4):
			four_s[:,:,i] = self.states[idx-3+i]
			four_n[:,:,i] = self.states[idx-2+i]
			
		return four_s,self.actions[idx],self.terminals[idx],four_n,self.rewards[idx]
	
	def batches(self, bat_size):
		bat_s = np.zeros([bat_size,84,84,4])
		bat_a = np.zeros([bat_size])
		bat_t = np.zeros([bat_size])
		bat_n = np.zeros([bat_size,84,84,4])
		bat_r = np.zeros([bat_size])
		ss = time.time()
		for i in range(bat_size):
			if self.batch_counter >= len(self.rand_idxs) - bat_size:
				self.rand_idxs = np.arange(3, self.get_size()-1)
				np.random.shuffle(self.rand_idxs)
				self.batch_counter = 0
			s,a,t,n,r = self.four_image(self.rand_idxs[self.batch_counter])
			bat_s[i] = s
			bat_a[i] = a
			bat_t[i] = t
			bat_n[i] = n
			bat_r[i] = r
			self.batch_counter += 1
		return bat_s, bat_a, bat_t, bat_n, bat_r
	
	def insert(self, prevstate_proc, reward, action, terminal):
		self.states[self.counter] = prevstate_proc
		self.rewards[self.counter] = reward
		self.actions[self.counter] = action
		self.terminals[self.counter] = terminal
		
		self.counter += 1
		if self.counter >= self.size:
			self.flag = True
			self.counter = 0
		return 

	def get_size(self):
		if self.flag == False:
			return self.counter
		else:
			return self.size 
