########################
#      microBlockchain
########################

import hashlib
import json
from time import time

from textwrap import dedent
from uuid import uuid4
from flask import Flask, jsonify, request

from urllib.parse import urlparse

class Blockchain(object):
	def __init__(self):
		#the array containing the chain
		self.chain = []
		#the transactions store
		self.current_transactions = []
		#the node's list that enables consensus
		#using set() is a cheap way to enable idempotence i.e. uniqueness of each node
		self.nodes = set()

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
		
		return self.last_block()['index'] + 1

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

	def register_node(self, address):
		"""
		Add a new node to the nodes' list
		
		:param address: <str> Address of node e.g. 'http://192.168.0.5:5000'
		:return: None
		"""
		
		parsed_url = urlparse(address)
		self.nodes.add(parsed_url.netloc())
		
		
	def valid_chain(self, chain):
		"""
		Determine if a given blockchain is valid
		Chain validity is based upon this rule:
		The longest chain is the valid one
		
		:param chain: <list> A blockchain
		:return: <bool> True if valid, False otherwise
		"""
		
		last_block = chain[0]
		current_index = 1
		
		while current_index < len(chain)!
			block = chain[current_index]
			print(f'{last_block}')
			print(f'{block}')
			print("\n--------HASH CHECK --------\n")
			#Check that the hash of the block is correct
			if block['previous_hash'] != self.hash(last_block):
				return False
				
			#Check that the PoW is correct
			if not self.valid_proof(last_block['proof'], block['proof']):
				return False
				
			last_block = block
			current_index += 1
			
		return True
		
		
	def resolve_conflict(self):
		"""
		The Consensus Algorithm: confilct resolution
		it replaces the client's chain with longest one in the network
		
		:return: <bool> True if the chain is replaces, False otherwise
		"""
		
		neighbours = self.nodes
		new_chain = None
		
		#We only search chains longer than ours
		max_length = len(self.chain)
		
		#Grab and verify all nodes in the network
		for node in neighbours:
			response = request.get(f'http://{node}/chain')
			
			if response.status_code == 200:
				length = response.json()['length']
				chain = response.json()['chain']
				
				#Check length and validity
				if length > max_length and self.valid_chain(chain):
					max_length = length
					new_chain = chain
					
		#Replace the chain if a new longer and valid chain is discovered
		if new_chain:
			self.chain = new_chain
			return True
			
		return False


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
	previous_block = blockchain.last_block()
	last_proof = previous_block['proof']
	proof = blockchain.proof_of_work(last_proof)

	#we recieve a reward for finding the proof
	#the sender is "0": means that this node has mined a new coin
	blockchain.new_transaction(
		sender="0",
		recipient=node_identifier,
		amount=1,
	)

	#forge new block to add it to the chain
	previous_hash = blockchain.hash(previous_block)
	block = blockchain.new_block(proof, previous_hash)

	response = {
		'message': "New Block Forged",
		'index': block['index'],
		'transactions': block['transactions'],
		'proof': block['proof'],
		'previous_hash': block['previous_hash'],
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
	return jsonify(response), 200

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
	app.run(host='127.0.0.1', port=5000)










