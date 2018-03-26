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
		#Creates new block

	def new_transaction(self, sender, recipient, amount):
		"""
		Creates a new block and adds it to the chain

		:param sender: <str> Sender adress
		:param recipient: <str> Recipient adress
		:param amount: <int> Amount
		:return: <int> Index of the Block that will hold this transaction
		"""

		self.current_transactions.appen({
			'sender': sender,
			'recipient': recipient,
			'amount': amount,		
		})

		return self.last_block['index'] + 1

	@staticmethod
	def hash(block):
		#Returns a block's hash
		pass

	@property
	def last_block(self):
		#Returns the last Block in the chain
