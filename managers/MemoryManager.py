import unittest
import asyncio

class MemoryManager:
    def __init__(self) -> None:
        self.sessions = {}

    async def create_session(self, session_id: str):
        self.sessions[session_id] = []

    async def add_message_to_session(self, session_id: str, message: str ):
        if session_id not in self.sessions:
            await self.create_session(session_id)

        self.sessions[session_id].append(
            {
            "message": message
            }
            )
    
    async def get_session_history(self, session_id: str, field="message"):
        if session_id in self.sessions:
            return [entry[field] for entry in self.sessions[session_id]]
        else:
            return []
        
    # Get History
    # default last bot response
    async def get_latest_memory(self, session_id: str, read, travel=-1, layers=1):
        try:
            options = {
                "content": ("message", "content")
            }
            latest_memory_entry = self.sessions[session_id][travel]

            level_a, level_b = options[read]
            
            if (layers == 2):
                requested_data = latest_memory_entry[level_a][level_b]
            elif (layers == 1):
                requested_data = latest_memory_entry[level_a]
            elif (layers == 0):
                requested_data = latest_memory_entry

            return requested_data
        except:
            return ""
        
# Unit Tests
class TestMemoryManager(unittest.TestCase):

    def setUp(self):
        self.memory_manager = MemoryManager()

    def test_create_session(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.memory_manager.create_session("session1"))
        self.assertIn("session1", self.memory_manager.sessions)

    def test_add_message_to_session(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.memory_manager.add_message_to_session("session1", "Hello, world!"))
        self.assertIn("session1", self.memory_manager.sessions)
        self.assertEqual(len(self.memory_manager.sessions["session1"]), 1)
        self.assertEqual(self.memory_manager.sessions["session1"][0]["message"], "Hello, world!")

    def test_get_session_history(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.memory_manager.add_message_to_session("session1", "Hello, world!"))
        loop.run_until_complete(self.memory_manager.add_message_to_session("session1", "How are you?"))
        history = loop.run_until_complete(self.memory_manager.get_session_history("session1"))
        self.assertEqual(history, ["Hello, world!", "How are you?"])

    def test_get_latest_memory(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.memory_manager.add_message_to_session("session1", "Hello, world!"))
        loop.run_until_complete(self.memory_manager.add_message_to_session("session1", "How are you?"))
        
        latest_content = loop.run_until_complete(self.memory_manager.get_latest_memory("session1", "content"))
        self.assertEqual(latest_content, "How are you?")

if __name__ == "__main__":
    unittest.main()