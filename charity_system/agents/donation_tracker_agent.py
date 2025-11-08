import os
import json
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

# Load API key from .env
load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    raise ValueError("API key not found in .env. Please add ELEVENLABS_API_KEY=YOUR_KEY")

# Initialize ElevenLabs client
client = ElevenLabs(api_key=api_key)

# DonationTracker Agent configuration
agent_name = "DonationTracker Agent"
first_message = "Hello! I can track all new donations and summarize them."

prompt = """# Personality
You are the DonationTracker Agent. Your primary role is to track all incoming donations to the AI Charity Payment Optimizer system.
You are accurate, timely, and structured. You ensure that every new donation is detected and recorded correctly.

# Environment
You operate within an AI-driven charity system connected to blockchain APIs and donation databases.
You have access to transaction data, donor identifiers, and timestamps.
You report results in a machine-readable format for the Orchestrator Agent.

# Tone
Your communication is concise, factual, and structured.
You avoid unnecessary language and focus on clarity and correctness.

# Goal
1. Detect new USDC donations on-chain as they arrive.
2. Provide donor name, amount, transaction hash, and timestamp.
3. Return all data in a structured JSON format:
   {
     "donor_name": string,
     "amount": number,
     "transaction_hash": string,
     "timestamp": string,
     "project_id": string
   }
4. Notify Orchestrator Agent immediately upon new donations.

# Guardrails
- Do not modify blockchain transactions.
- Do not assume or fabricate donation data.
- Always provide accurate and complete information.
- Ensure JSON outputs are well-formed and validated.
"""

# Custom tools for DonationTracker Agent
custom_tools = [
    {
        "type": "system",
        "name": "transfer_to_agent",
        "description": (
            "Allows the DonationTracker Agent to notify the Orchestrator Agent when new donations are detected.\n"
            "Ensures that each donation triggers the next step in the workflow automatically."
        ),
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [
                {
                    "agent_id": "agent_0701k992w9hwf3x8ey6r3tn7d4rm",
                    "condition": "new_donation_detected",
                    "delay_ms": 0,
                    "transfer_message": "New donation detected: {{amount}} USDC from {{donor_name}}. Trigger needs prediction.",
                    "enable_transferred_agent_first_message": True
                }
            ]
        },
        "disable_interruptions": False
    },
    {
        "type": "system",
        "name": "skip_turn",
        "description": "Allows DonationTracker to pause its turn if no new donations are available or system requests a wait.",
        "params": {
            "system_tool_type": "skip_turn",
            "transfers": [],
            "voicemail_message": ""
        },
        "disable_interruptions": False
    }
]

# Create DonationTracker Agent
response = client.conversational_ai.agents.create(
    name=agent_name,
    tags=["AI Charity"],
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

print(f"Created DonationTracker Agent with ID: {response.agent_id}")

# Save agent ID for orchestration
agent_file = "donation_tracker_agent_id.json"
with open(agent_file, "w") as f:
    json.dump({"DonationTracker Agent": response.agent_id}, f, indent=2)

print(f"Agent ID saved to {agent_file}")