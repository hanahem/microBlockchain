########################
#      µBlockchain
########################

import hashlib
import json
from time import time

class Blockchain(object):
	def __init__(self):
		#the array containing the chain
		self.chain = []
		#the transactions store
		self.current_transactions = []

		#Genesis block
		self.new_block(previous_hash=1, proof=100)

	def new_block(self, proof, previous_hash=None):
		"""
		Creates a new Block to the Blockchain

		:param proof: <int> PoW algorithm return
		:param previous_hash: <str> Hash of previous Block
		:return: <dict> New Block
		"""

		block = {
			'index': len(self.chain) + 1,
			'timestamp': time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1])		
		}

		#Reset current list of transactions
		self.current_transactions = []

		self.chain.append(block)
		return block

	def new_transaction(self, sender, recipient, amount):
		"""
		Creates a new transaction to be added to the next mined block

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
		"""
		Creates a SHA-256 hash of the Block
		
		:param block: <dict> Block
		:return: <str> Hash result
		"""
		#Make sure the Dictionnary is ordered to have consistent hashes
		block_string = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()

	@property
	def last_block(self):
		#Returns the last Block in the chain
		return self.chain[-1]
