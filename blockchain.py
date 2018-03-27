########################
#      microBlockchain
########################

import hashlib
import json
from time import time

from textwrap import dedent
from uuid import uuid4
from flask import Flask, jsonify, request

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
			'previous_hash': previous_hash or self.hash(self.chain[-1]),		
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

		self.current_transactions.append({
			'sender': sender,
			'recipient': recipient,
			'amount': amount,		
		})
		
<<<<<<< HEAD
		return self.last_block()['index'] + 1
=======
		lst_block = self.last_block()
		return lst_block['index'] + 1
>>>>>>> 33fbf58a74cb78809378c72c85320384b546ecb6

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

	#@property
	def last_block(self):
		#Returns the last Block in the chain
		return self.chain[-1]


	def proof_of_work(self, last_proof):
		"""
		Simple PoW algo:
		-find a number p' s.t. hash(pp') contains leading 4 zeros, where p is the previous p'
		-p is the previous proof, and p' the new one

		:param last_proof: <int>
		:return: <int>
		"""

		proof = 0
		while self.valid_proof(last_proof, proof) is False:
			proof += 1
		
		return proof

	@staticmethod
	def valid_proof(last_proof, proof):
		"""
		Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?

		:param last_proof: <int> Prev proof
		:param proof: <int> Current proof
		:return: <bool> True if verified False else.
		"""

		guess = f'{last_proof}{proof}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000" #the number of leading zeroes adjusts the difficulty of the algo




#Instantiate our Node
app = Flask(__name__)

#Generate globally unique adress for the node
node_identifier = str(uuid4()).replace('-','')

#Instantiate the Blockchain
blockchain = Blockchain()

#Mining endpoint
@app.route('/mine', methods=['GET'])
def mine():
	#run the PoW algo to get the next proof
<<<<<<< HEAD
	previous_block = blockchain.last_block()
	last_proof = previous_block['proof']
=======
	last_block = blockchain.last_block()
	last_proof = last_block['proof']
>>>>>>> 33fbf58a74cb78809378c72c85320384b546ecb6
	proof = blockchain.proof_of_work(last_proof)

	#we recieve a reward for finding the proof
	#the sender is "0": means that this node has mined a new coin
	blockchain.new_transaction(
		sender="0",
		recipient=node_identifier,
		amount=1,
	)

	#forge new block to add it to the chain
<<<<<<< HEAD
	previous_hash = blockchain.hash(previous_block)
=======
	previous_hash = blockchain.hash(last_block)
>>>>>>> 33fbf58a74cb78809378c72c85320384b546ecb6
	block = blockchain.new_block(proof, previous_hash)

	response = {
		'message': "New Block Forged",
		'index': block['index'],
		'transactions': block['transactions'],
		'proof': block['proof'],
<<<<<<< HEAD
		'previous_hash': block['previous_hash'],
=======
		'previous_hash': block['previous_hash']
>>>>>>> 33fbf58a74cb78809378c72c85320384b546ecb6
	}
	
	return jsonify(response), 200

#New transactions endpoint
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
	values = request.get_json()

	#check that required fields are in POST data
	required = ['sender', 'recipient', 'amount']
	if not all(k in values for k in required):
		return 'Missing values', 400

	#create a new transaction
	index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

	response = {'message': f'Transaction will be added to Block {index}'}
	return jsonify(response), 201

#Full chain endpoint
@app.route('/chain', methods=['GET'])
def full_chain():
	response = {
		'chain': blockchain.chain,
		'length': len(blockchain.chain),
	}
	return jsonify(response), 200

#Run the server on port 5000
if __name__ == '__main__':
<<<<<<< HEAD
	app.run(host='0.0.0.0', port=5000)
=======
	app.run(host='127.0.0.1', port=5000)
>>>>>>> 33fbf58a74cb78809378c72c85320384b546ecb6










