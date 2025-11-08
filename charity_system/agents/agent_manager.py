import json
import os
from datetime import datetime

class AgentDirectoryManager:
    def __init__(self, directory_file='agent_directory.json'):
        self.directory_file = directory_file
        self.agents = self.load_directory()
    
    def load_directory(self):
        """Load the agent directory from JSON file"""
        if os.path.exists(self.directory_file):
            with open(self.directory_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_directory(self):
        """Save the agent directory to JSON file"""
        with open(self.directory_file, 'w') as f:
            json.dump(self.agents, f, indent=2)
    
    def add_agent(self, agent_name, agent_id):
        """Add or update an agent in the directory"""
        self.agents[agent_name] = agent_id
        self.save_directory()
        print(f"✅ Added {agent_name}: {agent_id}")
    
    def get_agent_id(self, agent_name):
        """Get agent ID by name"""
        return self.agents.get(agent_name)
    
    def list_agents(self):
        """List all agents in the directory"""
        print("\n🤖 AGENT DIRECTORY")
        print("=" * 40)
        for name, agent_id in self.agents.items():
            print(f"🔹 {name}: {agent_id}")
        print(f"Total agents: {len(self.agents)}")
    
    def export_config(self):
        """Export configuration for deployment"""
        config = {
            "export_date": datetime.now().isoformat(),
            "system_name": "AI Charity Payment Optimizer",
            "agent_count": len(self.agents),
            "agents": self.agents
        }
        
        with open('agent_system_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ System configuration exported to agent_system_config.json")

# Usage example
if __name__ == "__main__":
    manager = AgentDirectoryManager()
    manager.list_agents()
    
    # Example: Add a new agent
    # manager.add_agent("New Agent Name", "agent_123456789")