import json
import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=api_key)

# Load agent directory
with open('agent_directory.json', 'r') as f:
    agent_directory = json.load(f)

def check_agent_health(agent_name, agent_id):
    """Check if an agent is accessible and functioning"""
    try:
        agent_info = client.conversational_ai.agents.get(agent_id)
        status = "✅ ACTIVE"
        details = f"Name: {agent_info.name}, Status: Ready"
        return status, details
    except Exception as e:
        return "❌ INACCESSIBLE", f"Error: {str(e)}"

print("🔍 AI CHARITY PAYMENT OPTIMIZER - SYSTEM HEALTH CHECK")
print("=" * 60)

all_healthy = True
for agent_name, agent_id in agent_directory.items():
    status, details = check_agent_health(agent_name, agent_id)
    print(f"{agent_name:<25} {status}")
    print(f"   ID: {agent_id}")
    if "ACTIVE" in status:
        print(f"   {details}")
    else:
        all_healthy = False
    print()

if all_healthy:
    print("🎯 SYSTEM STATUS: ✅ ALL SYSTEMS GO!")
    print("💫 All 9 agents are active and ready for integration!")
else:
    print("🚨 SYSTEM STATUS: ❌ Some agents need attention")