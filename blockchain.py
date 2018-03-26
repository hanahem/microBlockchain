########################
#      µBlockchain
########################

class Blockchain(object):
	def __init__(self):
		#the array containing the chain
		self.chain = []
		#the transactions store
		self.current_transactions = []

	def new_block(self):
		#Creates a new block and adds it to the chain
		pass

	def new_transaction(self):
		#Adds a transaction to the transactions' store
		pass

	@staticmethod
	def hash(block):
		#Returns a block's hash
		pass

	@property
	def last_block(self):
		#Returns the last Block in the chain
