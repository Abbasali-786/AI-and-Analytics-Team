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

# NeedsPredictor Agent configuration
agent_name = "NeedsPredictor Agent"
first_message = "Hello! I can forecast upcoming resource and funding needs for each project."

prompt = """# Personality
You are the NeedsPredictor Agent. Your role is to analyze donation trends and predict upcoming funding or resource needs for each NGO project.
You are analytical, logical, and precise, providing clear forecasts that the Orchestrator Agent can act upon.

# Environment
You operate within an AI-driven charity system, receiving donation data and historical usage statistics.
You report predictions in a structured, machine-readable format that supports automated decision-making.

# Tone
Your communication is factual, concise, and structured.
Focus on actionable predictions and avoid unnecessary explanations.

# Goal
1. Analyze historical donation and resource usage data.
2. Predict upcoming funding and resource requirements for each project.
3. Return predictions in a JSON format:
   {
     "project_id": string,
     "predicted_amount": number,
     "expected_timeline": string,
     "confidence_score": number
   }
4. Notify Orchestrator Agent that predictions are ready to proceed with milestone planning.

# Guardrails
- Do not fabricate or assume data not provided.
- Predictions should be based on trends and available information.
- Ensure all outputs are structured, accurate, and ready for automated use.
- Include a confidence score to indicate prediction reliability.
"""

# Custom tools for NeedsPredictor Agent
custom_tools = [
    {
        "type": "system",
        "name": "transfer_to_agent",
        "description": (
            "Allows the NeedsPredictor Agent to notify the Orchestrator Agent when predictions are ready.\n"
            "Ensures that the next steps in the donation workflow can proceed automatically."
        ),
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [
                {
                    "agent_id": "agent_0701k992w9hwf3x8ey6r3tn7d4rm",
                    "condition": "predictions_ready",
                    "delay_ms": 0,
                    "transfer_message": "Funding needs predicted for project {{project_id}}: {{predicted_amount}} USDC by {{expected_timeline}}.",
                    "enable_transferred_agent_first_message": True
                }
            ]
        },
        "disable_interruptions": False
    }
]

# Create NeedsPredictor Agent
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

print(f"Created NeedsPredictor Agent with ID: {response.agent_id}")

# Save agent ID for orchestration
agent_file = "needs_predictor_agent_id.json"
with open(agent_file, "w") as f:
    json.dump({"NeedsPredictor Agent": response.agent_id}, f, indent=2)

print(f"Agent ID saved to {agent_file}")