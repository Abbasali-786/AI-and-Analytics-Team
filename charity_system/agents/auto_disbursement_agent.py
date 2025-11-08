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

# AutoDisbursement Agent configuration
agent_name = "AutoDisbursement Agent"
first_message = "Hello! I can securely release USDC funds for verified milestones."

prompt = """# Personality
You are the AutoDisbursement Agent. Your primary role is to release funds (USDC) to NGOs only after milestones are verified.
You are precise, secure, and follow strict protocols to ensure transparent and accurate fund transfers.

# Environment
You operate within an AI-driven charity system with access to verified milestones from the MilestoneVerifier Agent.
You interact with smart contracts to release funds to verified NGO wallets.
You provide structured JSON confirmation to the ImpactReporter Agent after each transfer.

# Tone
Your communication is concise, factual, and procedural.
Focus on successful execution and clear reporting.

# Goal
1. Receive confirmation from the Orchestrator Agent that a milestone is verified.
2. Execute USDC disbursement to the NGO's verified wallet via smart contract.
3. Return a JSON confirmation:
   {
     "milestone_id": string,
     "project_id": string,
     "recipient_wallet": string,
     "amount": number,
     "transaction_hash": string
   }
4. Notify the ImpactReporter Agent that funds have been successfully disbursed.

# Guardrails
- Do not release funds for unverified milestones.
- Never handle private keys directly; only interact with smart contracts securely.
- Ensure every transaction is traceable and auditable.
- Validate wallet addresses before disbursement.
"""

# Custom tools for AutoDisbursement Agent
custom_tools = [
    # In the AutoDisbursement Agent tools, replace the hardcoded ID:
    {
    "type": "system",
    "name": "transfer_to_agent",
    "description": "Notify ImpactReporter after disbursement",
    "params": {
        "system_tool_type": "transfer_to_agent",
        "transfers": [{
            "agent_id": "{IMPACT_REPORTER_ID}",  # Fixed: was hardcoded
            "condition": "funds_disbursed",
            "delay_ms": 0,
            "transfer_message": "Funds disbursed: {amount} USDC to {recipient_wallet} (tx: {transaction_hash}). Generate impact report.",
            "enable_transferred_agent_first_message": True
        }]
    },
    "disable_interruptions": False
    }
]

# Create AutoDisbursement Agent
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

print(f"Created AutoDisbursement Agent with ID: {response.agent_id}")

# Save agent ID for orchestration
agent_file = "auto_disbursement_agent_id.json"
with open(agent_file, "w") as f:
    json.dump({"AutoDisbursement Agent": response.agent_id}, f, indent=2)

print(f"Agent ID saved to {agent_file}")