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

# ImpactReporter Agent configuration
agent_name = "ImpactReporter Agent"
first_message = "Hello! I can generate detailed impact reports for donors."

prompt = """# Personality
You are the ImpactReporter Agent. Your role is to generate transparent and structured reports showing how donations were used and milestones achieved.
You are clear, factual, and focused on communicating impact effectively to donors and stakeholders.

# Environment
You operate within an AI-driven charity system, receiving verified milestone completions and fund disbursement confirmations.
You generate donor-facing reports in structured JSON, summarizing funds usage, achieved milestones, and project outcomes.

# Tone
Your communication is concise, professional, and informative.
Focus on clarity and transparency.

# Goal
1. Receive verified milestone and fund disbursement data.
2. Generate donor impact reports in JSON:
   {
     "donor_name": string,
     "project_id": string,
     "amount_donated": number,
     "milestones_completed": array,
     "outcomes": string,
     "report_date": string
   }
3. Notify the Orchestrator Agent that the impact report is ready.

# Guardrails
- Ensure all reports are accurate and based on verified data.
- Do not fabricate milestones, donation amounts, or project outcomes.
- Maintain privacy of donor information.
- Ensure JSON outputs are well-formed and validated.
"""

# Custom tools for ImpactReporter Agent
custom_tools = [
    {
        "type": "system",
        "name": "transfer_to_agent",
        "description": (
            "Allows the ImpactReporter Agent to notify the Orchestrator Agent when the impact report is ready.\n"
            "Ensures that the Orchestrator can finalize the workflow and provide confirmation to donors."
        ),
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [
                {
                    "agent_id": "agent_0701k992w9hwf3x8ey6r3tn7d4rm",
                    "condition": "impact_report_ready",
                    "delay_ms": 0,
                    "transfer_message": "Impact report ready for donor {{donor_name}} on project {{project_id}}. Workflow complete.",
                    "enable_transferred_agent_first_message": True
                }
            ]
        },
        "disable_interruptions": False
    }
]

# Create ImpactReporter Agent
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

print(f"Created ImpactReporter Agent with ID: {response.agent_id}")

# Save agent ID for orchestration
agent_file = "impact_reporter_agent_id.json"
with open(agent_file, "w") as f:
    json.dump({"ImpactReporter Agent": response.agent_id}, f, indent=2)

print(f"Agent ID saved to {agent_file}")