# agents/ngo_monitor_agent.py
import os
import json
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

# === LOAD ENV & INIT CLIENT ===
load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    raise ValueError("ELEVENLABS_API_KEY not found in .env")

client = ElevenLabs(api_key=api_key)

# === AGENT CONFIG ===
agent_name = "NGO Monitor Agent"
first_message = "Monitoring NGOs for transparency issues..."

prompt = """You are the NGO Monitor Agent.
Your job: Weekly scan for scandals.

For each NGO:
1. Search X and web: "{ngo_name} scandal" OR "fraud" OR "misuse"
2. If >2 credible sources → flag
3. Output: { "ngo": "...", "alert": true, "sources": [...] }
4. Transfer to Orchestrator with alert.

Never flag without evidence.
"""

custom_tools = [
    {
        "type": "system",
        "name": "transfer_to_orchestrator",
        "description": "Send alert to Orchestrator",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [
                {
                    "agent_id": "agent_0701k992w9hwf3x8ey6r3tn7d4rm",
                    "condition": "alert",
                    "delay_ms": 0,
                    "transfer_message": "ALERT: {{ngo}} has transparency issues. Sources: {{sources}}",
                    "enable_transferred_agent_first_message": True
                }
            ]
        },
        "disable_interruptions": False
    }
]

# === CREATE AGENT ===
try:
    response = client.conversational_ai.agents.create(
        name=agent_name,
        tags=["AI Charity", "Monitoring"],
        conversation_config={
            "tts": {
                "voice_id": "21m00Tcm4TlvDq8ikWAM",
                "model_id": "eleven_flash_v2"
            },
            "agent": {
                "first_message": first_message,
                "prompt": {"prompt": prompt}
            },
            "tools": custom_tools
        }
    )

    agent_id = response.agent_id
    print(f"SUCCESS! Created {agent_name}: {agent_id}")

    # Save ID
    with open("ngo_monitor_agent_id.json", "w") as f:
        json.dump({agent_name: agent_id}, f, indent=2)
    print("ID saved to ngo_monitor_agent_id.json")

except Exception as e:
    print(f"FAILED to create {agent_name}: {e}")