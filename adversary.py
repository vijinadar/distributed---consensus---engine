from node import Node

class Adversary:

    def __init__(self, node_id):
        self.node_id = node_id

    async def send_fake_prepare(self):

        print(f"[{self.node_id}] Sending fake PREPARE")

    print("Invalid signature detected")

    print("Message ignored by replicas")

class Adversary(Node):

    async def handle_prepare_pbft(self, msg):

        print(
            f"[{self.node_id}] Sending fake prepare"
        )

        return {
            "type": "FAKE_PREPARE"
        }
