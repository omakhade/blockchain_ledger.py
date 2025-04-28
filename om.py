import streamlit as st
import hashlib
import time
import json

# Blockchain class to manage the ledger
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []  # Reset current transactions
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        # We must ensure the dictionary is ordered, or we'll get inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

# Initialize the blockchain
blockchain = Blockchain()

# Streamlit UI elements
st.title("BSC23DS06 Blockchain Ledger")

# Display the blockchain's current state
st.subheader("Blockchain Ledger")
for block in blockchain.chain:
    st.write(f"Block {block['index']}:")
    st.write(f"  Timestamp: {block['timestamp']}")
    st.write(f"  Proof: {block['proof']}")
    st.write(f"  Previous Hash: {block['previous_hash']}")
    st.write(f"  Transactions: {block['transactions']}")
    st.write("---")

# Transaction Form
st.subheader("Create a New Transaction")
with st.form(key='transaction_form'):
    sender = st.text_input("Sender", key="sender")
    recipient = st.text_input("Recipient", key="recipient")
    amount = st.number_input("Amount", min_value=1, step=1, key="amount")
    submit_button = st.form_submit_button("Add Transaction")

    if submit_button:
        if sender and recipient and amount:
            # Add transaction to the current block
            blockchain.new_transaction(sender, recipient, amount)
            st.success(f"Transaction added: {sender} sent {amount} to {recipient}")

# Block Mining
st.subheader("Mine a New Block")
with st.form(key='mine_form'):
    proof = st.number_input("Proof (previous proof number)", min_value=0, key="proof", step=1)
    submit_mine_button = st.form_submit_button("Mine Block")

    if submit_mine_button:
        if proof >= 0:
            # Mine a new block
            blockchain.new_block(proof, blockchain.hash(blockchain.last_block))
            st.success("New Block Mined Successfully!")
            st.write(blockchain.last_block)
