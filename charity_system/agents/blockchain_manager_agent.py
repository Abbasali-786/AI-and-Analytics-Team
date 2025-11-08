import os
import json
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=api_key)

agent_name = "Blockchain Manager Agent"
first_message = "Blockchain operations ready."

prompt = """# Personality
You are the Blockchain Manager Agent. You handle all blockchain interactions including smart contract deployments, wallet validations, and transaction monitoring.

# Responsibilities
- Deploy and manage smart contracts
- Validate wallet addresses and contract integrity
- Monitor gas fees and optimize transactions
- Ensure blockchain security best practices
- Interface with Polygon/Ethereum networks

# Output Format
Always return structured JSON with transaction status, gas used, and confirmation details.

# Security
- Never expose private keys
- Validate all addresses before transactions
- Implement fail-safes for high gas scenarios
"""

custom_tools = [
    {
        "type": "system",
        "name": "transfer_to_orchestrator",
        "description": "Report blockchain status to orchestrator",
        "params": {
            "system_tool_type": "transfer_to_agent", 
            "transfers": [{
                "agent_id": "{ORCHESTRATOR_ID}",
                "condition": "blockchain_update",
                "transfer_message": "Blockchain operation {operation_type} completed with status: {status}",
                "enable_transferred_agent_first_message": True
            }]
        }
    }
]

try:
    response = client.conversational_ai.agents.create(
        name=agent_name,
        tags=["AI Charity", "Blockchain"],
        conversation_config={
            "tts": {"voice_id": "21m00Tcm4TlvDq8ikWAM", "model_id": "eleven_flash_v2"},
            "agent": {"first_message": first_message, "prompt": {"prompt": prompt}},
            "tools": custom_tools
        }
    )
    
    print(f"✅ Created {agent_name}: {response.agent_id}")
    with open("blockchain_manager_agent_id.json", "w") as f:
        json.dump({agent_name: response.agent_id}, f, indent=2)
        
except Exception as e:
    print(f"❌ Error creating {agent_name}: {e}")