import hashlib
import json
from time import time
from uuid import uuid4 

from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
  
        block = {
            # TODO
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof, #proof used to mine this block - so we pass the proof in
            'previous_hash': previous_hash #passed in - or we could get the hash of the last block (self.hash(self.chain[-1]))
        }

        self.current_transactions = []
        self.chain.append(block)
        return block
        

    def hash(self,block):
   
        string_object = json.dumps(block, sort_keys=True).encode() #sort_keys is only needed for older versions of python
        raw_hash = hashlib.sha256(string_object)
        hex_hash = raw_hash.hexdigest() 
        return hex_hash
        

    @property
    def last_block(self):
        return self.chain[-1]

    # def proof_of_work(self, block):

    #     block_string = json.dumps(block)
    #     proof = 0
    #     while self.valid_proof(block_string, proof) is False:
    #         proof += 1
    #     return proof
        
       

    @staticmethod
    def valid_proof(block_string, proof):

        guess = f"{block_string}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:3] == "000"
        
        # return True or False

    def new_transaction(self, sender, recipient, amount):
        """
        creates a new transaction to go into the next mined block

        :param sender: <str> Address of the sender
        :param recipient: <str> Name of the recipient
        :param amount: <float> Amount of transaction
        :return: <index> The block that will hold the transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        # return len(self.chain)
        return self.last_block['index'] + 1


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


# @app.route('/mine', methods=['GET'])
# def mine():
#     # Run the proof of work algorithm to get the next proof
#     proof = blockchain.proof_of_work(blockchain.last_block)
#     # Forge the new Block by adding it to the chain with the proof
#     previous_hash = blockchain.hash(blockchain.last_block)
#     block = blockchain.new_block(proof, previous_hash)

#     response = {
#         # TODO: Send a JSON response with the new block
#         'new_block': block
#     }

#     return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    data = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in data for k in required):
        response = {'message: "Missing values'}
        return jsonify(response), 400

    # create new transaction

    index = blockchain.new_transaction(data['sender'], 
                                       data['recipient'], 
                                       data['amount'])

    response = {
        'message': f'Transaction will post to block {index}.',

    }
    return jsonify(response), 201

@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
    required = ['proof', 'id']
    if not all (k in data for k in required):
        response = {'message: "Missing values'}
        return jsonify(response), 400
    
    last_block = blockchain.last_block
    last_block_string = json.dumps(last_block, sort_keys=True)
    check = blockchain.valid_proof(last_block_string, data['proof'])
    # print(blockchain.valid_proof(last_block_string, data['proof'])
    # breakpoint()
    if blockchain.valid_proof(last_block_string, data['proof']):
       # Forge the new Block by adding it to the chain with the proof
        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(data['proof'], previous_hash) 

        blockchain.new_transaction(
            sender="0",
            recipient=data['id'],
            amount=100
        )
        response = {
            'message': 'New Block Forged',
            'new_block': block
        }

        return jsonify(response), 200
    else: 
        response = {
            'message': 'Proof is invalid or already submitted'
        }
        return jsonify(response), 200


    


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'length': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200 

@app.route('/last_block', methods=['GET'])
def last_block():
    response = {
        'last_block': blockchain.last_block
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #to auto update set debug=True
    #, else you have to manually restart server each time



# import hashlib
# import json
# from time import time
# from uuid import uuid4 

# from flask import Flask, jsonify, request
# from miner import proof_of_work
# from werkzeug.exceptions import BadRequest


# class Blockchain(object):
#     def __init__(self):
#         self.chain = []
#         self.current_transactions = []

#         self.new_block(previous_hash=1, proof=100)

#     def new_block(self, proof, previous_hash=None):
  
#         block = {
#             # TODO
#             'index': len(self.chain) + 1,
#             'timestamp': time(),
#             'transactions': self.current_transactions,
#             'proof': proof, #proof used to mine this block - so we pass the proof in
#             'previous_hash': previous_hash #passed in - or we could get the hash of the last block (self.hash(self.chain[-1]))
#         }

#         self.current_transactions = []
#         self.chain.append(block)
#         return block
        

#     def hash(self,block):
   
#         string_object = json.dumps(block, sort_keys=True).encode() #sort_keys is only needed for older versions of python
#         raw_hash = hashlib.sha256(string_object)
#         hex_hash = raw_hash.hexdigest() 
#         return hex_hash
        

#     @property
#     def last_block(self):
#         return self.chain[-1]

#     # def proof_of_work(self, block):

#     #     block_string = json.dumps(block)
#     #     proof = 0
#     #     while self.valid_proof(block_string, proof) is False:
#     #         proof += 1
#     #     return proof
        
       

#     @staticmethod
#     def valid_proof(block_string, proof):

#         guess = f"{block_string}{proof}".encode()
#         guess_hash = hashlib.sha256(guess).hexdigest()

#         return guess_hash[:3] == "000"
        
#         return True or False

#     def new_transaction(self, sender, recipient, amount):
#         """
#         creates a new transaction to go into the next mined block

#         :param sender: <str> Address of the sender
#         :param recipient: <str> Name of the recipient
#         :param amount: <float> Amount of transaction
#         :return: <index> The block that will hold the transaction
#         """
#         self.current_transactions.append({
#             'sender': sender,
#             'recipient': recipient,
#             'amount': amount
#         })

#         # return len(self.chain)
#         return self.last_block['index'] + 1


# # Instantiate our Node
# app = Flask(__name__)

# # Generate a globally unique address for this node
# node_identifier = str(uuid4()).replace('-', '')

# # Instantiate the Blockchain
# blockchain = Blockchain()


# # @app.route('/mine', methods=['GET'])
# # def mine():
# #     # Run the proof of work algorithm to get the next proof
# #     proof = blockchain.proof_of_work(blockchain.last_block)
# #     # Forge the new Block by adding it to the chain with the proof
# #     previous_hash = blockchain.hash(blockchain.last_block)
# #     block = blockchain.new_block(proof, previous_hash)

# #     response = {
# #         # TODO: Send a JSON response with the new block
# #         'new_block': block
# #     }

# #     return jsonify(response), 200
# @app.route('/transactions/new', methods=['POST'])
# def new_transaction():
#     data = request.get_json()

#     required = ['sender', 'recipient', 'amount']
#     if not all(k in data for k in required):
#         response = {'message: "Missing values'}
#         return jsonify(response), 400

#     # create new transaction

#     index = blockchain.new_transaction(data['sender'], 
#                                        data['recipient'], 
#                                        data['amount'])

#     response = {
#         'message': f'Transaction will post to block {index}.',

#     }
#     return jsonify(response), 201


# @app.route('/mine', methods=['POST'])
# def mine():
#     data = request.get_json()
#     required = ['proof', 'id']
#     if not all (k in data for k in required):
#         response = {'message: "Missing values'}
#         return jsonify(response), 400
    
#     last_block = blockchain.last_block
#     last_block_string = json.dumps(last_block, sort_keys=True)

#     if blockchain.valid_proof(last_block_string, data['proof']):
#        # Forge the new Block by adding it to the chain with the proof
#         previous_hash = blockchain.hash(blockchain.last_block)
#         block = blockchain.new_block(data['proof'], previous_hash) 

  
#         response = {
#             'message': 'New Block Forged',
#             'new_block': block
#         }

#         return jsonify(response), 200
#     else: 
#         response = {
#             'message': 'Proof is invalid or already submitted'
#         }
#         return jsonify(response), 200


    


# @app.route('/chain', methods=['GET'])
# def full_chain():
#     response = {
#         'length': len(blockchain.chain),
#         'chain': blockchain.chain
#     }
#     return jsonify(response), 200 

# @app.route('/last_block', methods=['GET'])
# def last_block():
#     response = {
#         'last_block': blockchain.last_block
#     }
#     return jsonify(response), 200


# # Run the program on port 5000
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True) #to auto update set debug=True
#     #, else you have to manually restart server each time

