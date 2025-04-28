import streamlit as st
import hashlib
import time
import json
import os

DATA_FILE = "blockchain_data.json"

# Blockchain class with data persistence
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        if os.path.exists(DATA_FILE):
            self.load_data()
        else:
            self.new_block(previous_hash='1', proof=100)  # genesis block
            self.save_data()

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        self.save_data()
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        self.save_data()
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump({
                "chain": self.chain,
                "current_transactions": self.current_transactions
            }, f, indent=4)

    def load_data(self):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            self.chain = data["chain"]
            self.current_transactions = data["current_transactions"]

# Initialize blockchain
blockchain = Blockchain()

# Streamlit UI
st.title("BSC23DS06 Blockchain Ledger")

st.subheader("Blockchain Ledger")
for block in blockchain.chain:
    st.write(f"Block {block['index']}")
    st.write(f"  Timestamp: {block['timestamp']}")
    st.write(f"  Transactions: {block['transactions']}")
    st.write(f"  Proof: {block['proof']}")
    st.write(f"  Previous Hash: {block['previous_hash']}")
    st.write("---")

# Add Transaction
st.subheader("Create a New Transaction")
with st.form("transaction_form"):
    sender = st.text_input("Sender")
    recipient = st.text_input("Recipient")
    amount = st.number_input("Amount", min_value=1)
    submit = st.form_submit_button("Add Transaction")
    if submit:
        if sender and recipient:
            blockchain.new_transaction(sender, recipient, amount)
            st.success(f"Transaction added: {sender} -> {recipient} ({amount})")

# Mine Block
st.subheader("Mine a New Block")
with st.form("mine_form"):
    proof = st.number_input("Proof", min_value=0)
    mine_submit = st.form_submit_button("Mine Block")
    if mine_submit:
        blockchain.new_block(proof, blockchain.hash(blockchain.last_block))
        st.success("Block mined and added to the blockchain.")
