import argparse
from fastapi import FastAPI
from uuid import uuid4
from pydantic import BaseModel
import time
from typing import ClassVar
import uvicorn

from chain import (BlakeChain, SHAChain, MD5Chain, SHA1Chain, SHA3Chain, Blake3Chain,Blake2sChain, Blake2sChain, SHA512Chain)
from merkle_tree import MerkleTree
import config as cfg


if cfg.hash == "blake2b":
    blockchain = BlakeChain()
elif cfg.hash == "sha256":
    blockchain = SHAChain()
elif cfg.hash == "md5":
    blockchain = MD5Chain()
elif cfg.hash == "sha1":
    blockchain = SHA1Chain()
elif cfg.hash == "sha3":
    blockchain = SHA3Chain()
elif cfg.hash == "blake3":
    blockchain = Blake3Chain()
elif cfg.hash == "blake2s":
    blockchain = Blake2sChain()
elif cfg.hash == "sha512":
    blockchain = SHA512Chain()
else:
    raise ValueError("Unsupported hash function")

merkle_tree = MerkleTree(cfg.hash)

miner_id ="1"

class TX(BaseModel):
    sender: ClassVar[str] = cfg.sender_id  # Mark as ClassVar
    recipient: ClassVar[str] = cfg.recipient_id  # Mark as ClassVar
    amount: int  

app = FastAPI() 

@app.get('/mine')
def mine(): 
    try:
        mining_start = time.time_ns()
        last_block = blockchain.last_block
        last_nonce = last_block['nonce']
        nonce, guess_hash = blockchain.proof_of_work(last_nonce)

        # Reward the miner
        blockchain.new_transaction(
            sender="0",
            recipient=miner_id,
            amount=1,
        )

        previous_hash = last_block['hash']
        txs = [str(tx) for tx in blockchain.current_transactions]
        merkle_tree.add_leaf(txs, True)
        merkle_tree.make_tree()
        merkle_root = merkle_tree.get_merkle_root()
        block = blockchain.new_block(guess_hash, merkle_root, nonce, previous_hash)
        time_took = time.time_ns() - mining_start
        
        print(time_took)
        # Prepare response
        response = {
            'message': 'New block added',
            'time took(ns)': time_took,
            'nonce': block['nonce'],
            'index': block['index'],
            'hash': block['hash'],
            'merkle_root': block['merkle_root'],
            'previous_hash': block['previous_hash'],
        }
        
        print(response)

        # Reset the Merkle tree for the next block
        merkle_tree.reset_tree()
        return response

    except Exception as e:
        return {"error": "Mining operation failed"}


@app.post('/tx/new')
def new_transaction(tx: TX):
    index = blockchain.new_transaction(tx.sender, tx.recipient, tx.amount)
    response = {'message':f"Transaction will be added to block {index}",
            'tx': tx}
    return response

@app.get('/chain')
def get_chain():
    response = {
            'chain' : blockchain.chain,
            'length': len(blockchain.chain),
            }

    return response

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=cfg.port)