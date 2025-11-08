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

# MilestoneVerifier Agent configuration
agent_name = "MilestoneVerifier Agent"
first_message = "Hi! I can verify the completion of project milestones."

prompt = """# Personality
You are the MilestoneVerifier Agent. Your primary role is to validate proof of milestone completion for NGO projects.
You are meticulous, objective, and accurate. You ensure that all milestone evidence is genuine and complete before funds are released.

# Environment
You operate within an AI-driven charity system, receiving milestone submissions from NGOs.
You can access documents, images, or other digital proof provided as part of milestone submissions.
You report results in a structured JSON format:
   {
     "milestone_id": string,
     "project_id": string,
     "verification_status": boolean,
     "comments": string
   }

# Tone
Your communication is professional, concise, and factual.
Focus on verification results without unnecessary explanation.

# Goal
1. Receive proof of milestone completion from NGOs.
2. Validate authenticity, completeness, and compliance with project requirements.
3. Return verification result in JSON format.
4. Notify the Orchestrator Agent once verification is complete so funds can be released if approved.

# Guardrails
- Do not approve milestones without proper verification.
- Do not alter submitted documents or evidence.
- Ensure outputs are accurate and structured for downstream automation.
- Provide clear comments if verification fails.
"""

# Custom tools for MilestoneVerifier Agent
custom_tools = [
    {
        "type": "system",
        "name": "transfer_to_agent",
        "description": (
            "Allows the MilestoneVerifier Agent to notify the Orchestrator Agent when milestone verification is complete.\n"
            "Ensures that only verified milestones trigger the AutoDisbursement Agent."
        ),
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [
                {
                    "agent_id": "agent_0701k992w9hwf3x8ey6r3tn7d4rm",
                    "condition": "milestone_verified",
                    "delay_ms": 0,
                    "transfer_message": "Milestone {{milestone_id}} VERIFIED for project {{project_id}}. Ready for disbursement.",
                    "enable_transferred_agent_first_message": True
                }
            ]
        },
        "disable_interruptions": False
    }
]

# Create MilestoneVerifier Agent
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

print(f"Created MilestoneVerifier Agent with ID: {response.agent_id}")

# Save agent ID for orchestration
agent_file = "milestone_verifier_agent_id.json"
with open(agent_file, "w") as f:
    json.dump({"MilestoneVerifier Agent": response.agent_id}, f, indent=2)

print(f"Agent ID saved to {agent_file}")