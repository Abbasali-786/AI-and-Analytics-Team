# agents/ngo_researcher_agent.py
import os
import json
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

agent_name = "NGO Researcher Agent"
first_message = "Searching for verified NGOs..."

prompt = """You find real NGOs using web search.
Query: "climate Europe"
1. Search web
2. Extract name, country, website, EIN
3. Verify rating >80
4. Output JSON
5. Transfer to Orchestrator
"""

custom_tools = [
    {
        "type": "system",
        "name": "transfer_to_orchestrator",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [{
                "agent_id": "agent_0701k992w9hwf3x8ey6r3tn7d4rm",
                "condition": "found",
                "transfer_message": "Found {{count}} verified NGOs.",
                "enable_transferred_agent_first_message": True
            }]
        }
    }
]

try:
    response = client.conversational_ai.agents.create(
        name=agent_name, tags=["AI Charity"],
        conversation_config={
            "tts": {"voice_id": "21m00Tcm4TlvDq8ikWAM", "model_id": "eleven_flash_v2"},
            "agent": {"first_message": first_message, "prompt": {"prompt": prompt}},
            "tools": custom_tools
        }
    )
    print(f"Created {agent_name}: {response.agent_id}")
    with open("ngo_researcher_agent_id.json", "w") as f:
        json.dump({agent_name: response.agent_id}, f, indent=2)
except Exception as e:
    print("Error:", e)