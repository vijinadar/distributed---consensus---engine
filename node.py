import asyncio
from crypto_utils import *

from platform import node
from platform import node
import time
import random

FOLLOWER = "follower"
CANDIDATE = "candidate"
LEADER = "leader"
class Node:
   
    def __init__(self, node_id):

        self.private_key, self.public_key = generate_keys()

        self.node_id = node_id

        # Leader Election
        self.state = FOLLOWER
        self.current_term = 0
        self.voted_for = None
        self.last_heartbeat = time.time()

        # Paxos State
        self.promised_id = 0
        self.accepted_id = 0
        self.accepted_value = None
        self.proposal_id = 0

        # PBFT State
        self.pbft_log = {}

        # Ledger
        self.ledger = []

        # Cluster Peers
        self.peers = []

    # Leader Election

    async def send_heartbeats(self):

        while self.state == LEADER:

            print(f"[{self.node_id}] HEARTBEAT")

            self.last_heartbeat = time.time()

            await asyncio.sleep(2)

    async def handle_heartbeat(self, msg):

        self.last_heartbeat = time.time()

        if msg["term"] >= self.current_term:

            self.current_term = msg["term"]

            self.state = FOLLOWER

    async def monitor_leader(self):

        while True:

            timeout = random.randint(5, 10)

            if time.time() - self.last_heartbeat > timeout:

                print(f"[{self.node_id}] Leader timeout")

                await self.start_election()

                await asyncio.sleep(2)

                await self.run_paxos_demo()

            await asyncio.sleep(1)

    async def start_election(self):

        self.state = CANDIDATE

        self.current_term += 1

        self.voted_for = self.node_id

        votes = 3

        print(f"[{self.node_id}] Election started")

        if votes >= 3:

            self.state = LEADER

            print(f"[{self.node_id}] Became Leader")

            asyncio.create_task(self.send_heartbeats())

       # Paxos

    async def send_prepare(self, transaction):

        self.proposal_id += 1

        msg = {
            "type": "PREPARE",
            "proposal_id": self.proposal_id
        }

        print("Sending PREPARE:", msg)

    async def handle_prepare(self, msg):

        if msg["proposal_id"] > self.promised_id:

            self.promised_id = msg["proposal_id"]

            return {
                "type": "PROMISE",
                "proposal_id": msg["proposal_id"]
            }

    async def handle_accept(self, msg):

        if msg["proposal_id"] >= self.promised_id:

            self.accepted_id = msg["proposal_id"]

            self.accepted_value = msg["value"]

            return {
                "type": "ACCEPTED"
            }

    async def commit_transaction(self, transaction):

        self.ledger.append(transaction)

        with open("ledger.log", "a") as f:
            f.write(transaction + "\n")

        print("Committed:", transaction)

    async def paxos_consensus(self, transaction):

        self.proposal_id += 1

        proposal_id = self.proposal_id

        promises = 1

        print(f"\n[{self.node_id}] Starting Paxos")

        prepare_msg = {
            "proposal_id": proposal_id
        }

        for peer in self.peers:

            reply = await peer.handle_prepare(prepare_msg)

            if reply and reply["type"] == "PROMISE":
                promises += 1

        print("Promises:", promises)

        if promises < 3:
            print("Consensus Failed")
            return

        accepted_count = 1

        accept_msg = {
            "proposal_id": proposal_id,
            "value": transaction
        }

        for peer in self.peers:

            reply = await peer.handle_accept(accept_msg)

            if reply and reply["type"] == "ACCEPTED":
                accepted_count += 1

            print("Accepted:", accepted_count)

            if accepted_count >= 3:

                await self.commit_transaction(transaction)

            print("Consensus Reached")

    async def run_paxos_demo(self):

        transaction = "TXN001"

        print("\n--- PAXOS START ---")

        await self.send_prepare(transaction)

        prepare_msg = {
            "proposal_id": self.proposal_id
        }

        promise = await self.handle_prepare(prepare_msg)

        print("Promise received:", promise)

        accept_msg = {
            "proposal_id": self.proposal_id,
            "value": transaction
        }

        accepted = await self.handle_accept(accept_msg)

        print("Accepted:", accepted)

        await self.commit_transaction(transaction)

        print("--- PAXOS COMPLETE ---\n")

        transaction = "TXN001"

        print("\n--- PAXOS START ---")

        await self.send_prepare(transaction)

        prepare_msg = {
            "proposal_id": self.proposal_id
        }

        promise = await self.handle_prepare(prepare_msg)

        print("Promise received:", promise)

        accept_msg = {
            "proposal_id": self.proposal_id,
            "value": transaction
        }

        accepted = await self.handle_accept(accept_msg)

        print("Accepted:", accepted)

        await self.commit_transaction(transaction)

        print("--- PAXOS COMPLETE ---\n")

      # PBFT
    async def pbft_demo(self, transaction):

        print("\n--- PBFT START ---")

        message = transaction

        signature = sign_message(
            self.private_key,
            message
        )

        print("PRE-PREPARE")

        valid = verify_signature(
            self.public_key,
            message,
            signature
        )

        if valid:

            print("PREPARE")

            print("COMMIT")

            await self.commit_transaction(transaction)

            print("PBFT Consensus Reached")

            print("\n--- PBFT START ---")

            message = transaction

            signature = sign_message(
            self.private_key,
            message
            )

            print("PRE-PREPARE")

            valid = verify_signature(
                self.public_key,
                message,
                signature
            )

            if valid:

                print("PREPARE")

                print("COMMIT")

                await self.commit_transaction(transaction)

                print("PBFT Consensus Reached")

    async def handle_preprepare(self, msg):

        print("PBFT PRE-PREPARE")

    async def handle_prepare_pbft(self, msg):

        print("PBFT PREPARE")

    async def handle_commit_pbft(self, msg):

        print("PBFT COMMIT")

    # Message Router
  
    async def process_message(self, msg):

        msg_type = msg["type"]

        if msg_type == "PREPARE":

            await self.handle_prepare(msg)

        elif msg_type == "ACCEPT":

            await self.handle_accept(msg)

        elif msg_type == "HEARTBEAT":

            await self.handle_heartbeat(msg)
    

class Adversary(Node):

    async def send_fake_prepare(self):

        print(f"[{self.node_id}] Sending fake PREPARE")

        return {
            "type": "FAKE_PREPARE"
        }

    async def handle_prepare_pbft(self, msg):

        print(f"[{self.node_id}] Sending fake prepare")

        return {
            "type": "FAKE_PREPARE"
        }
    
# Test Driver

async def main():
    from adversary import Adversary
    evil = Adversary("evil_node")

    await evil.handle_prepare_pbft({})

    print("MAIN STARTED")
    node1 = Node("node1")
    node2 = Node("node2")
    node3 = Node("node3")
    node4 = Node("node4")
    node5 = Node("node5")

    print("\n--- CRYPTO DEMO ---")

    print("Node1 Public Key Generated")
    print("Node2 Public Key Generated")
    print("Node3 Public Key Generated")
    print("Node4 Public Key Generated")
    print("Node5 Public Key Generated")

    message = "TXN002"

    signature = sign_message(
        node1.private_key,
        message
    )

    valid = verify_signature(
        node1.public_key,
        message,
        signature
    )

    print("Message:", message)
    print("Signature Verified:", valid)
    
    evil = Adversary("evil_node")

    await evil.handle_prepare_pbft({})

     # Connect peers
    node1.peers = [node2, node3, node4, node5]
    node2.peers = [node1, node3, node4, node5]
    node3.peers = [node1, node2, node4, node5]
    node4.peers = [node1, node2, node3, node5]
    node5.peers = [node1, node2, node3, node4]
    
    # Elect leader
    await node1.start_election()

    await asyncio.sleep(2)

    # Run Paxos
    await node1.paxos_consensus("TXN001")

    await asyncio.sleep(5)

    print("\n--- PBFT DEMO START ---")

    await node1.pbft_demo("TXN002")

    print("--- PBFT DEMO END ---\n")

    await node1.start_election()

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())

