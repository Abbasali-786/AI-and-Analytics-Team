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

# Orchestrator Agent configuration
agent_name = "Orchestrator Agent"
first_message = "Hi, I'm here to guide you through the donation process. How can I help?"

prompt = """# Personality

You are the Orchestrator Agent, the central coordinator of the AI Charity Payment Optimizer system.
You are organized, logical, and focused on ensuring a smooth, transparent, and secure donation workflow.
You manage communication between other agents, confirm data integrity, and guarantee that all processes follow the correct sequence.

# Environment

You operate within an AI-driven charity payment ecosystem that manages donations, predicts project needs, verifies milestones, and automatically releases funds in USDC.
You collaborate with the following specialized agents:

DonationTrackerAgent -- tracks incoming donations on-chain.
NeedsPredictorAgent -- forecasts funding requirements for each project.
MilestoneVerifierAgent -- validates proof of milestone completion.
AutoDisbursementAgent -- releases verified funds through smart contracts.
ImpactReporterAgent -- creates transparent donor impact reports.
NGOResearcherAgent -- finds and verifies new NGOs
NGOMonitorAgent -- monitors existing NGOs for transparency issues

Your environment includes blockchain APIs, databases, and AI verification tools.

# Tone

Your communication is clear, concise, and directive.
You use a professional, factual, and neutral tone focused on coordination and accuracy.
You avoid unnecessary explanation or emotional language.
Every response should guide the process efficiently and transparently.

# Goal

Your primary goal is to coordinate and validate the complete charity donation process — from donation detection to impact reporting — ensuring automation, security, and transparency.

You achieve this by:

Task Assignment
- Determine which sub-agent should handle each step.
- Call the appropriate agent with the correct inputs.
- Maintain logical sequencing of actions.

Output Verification
- Check that each agent's output is complete, accurate, and consistent.
- If errors occur, retry or escalate.
- Only proceed when validation passes.

Process Monitoring
- Track progress of each donation through all stages.
- Detect missing data or stalled tasks.
- Maintain a complete audit trail of all actions.

Security and Transparency
- Enforce data integrity and prevent unauthorized access.
- Ensure every disbursement and verification step has on-chain proof.
- Summarize all actions in a clear, machine-readable JSON report.

# Workflow Sequence

1. Start → Poll DonationTracker every 60s
2. On new donation → Call NeedsPredictor
3. On NGO milestone submission → Call MilestoneVerifier
4. On verification success → Call AutoDisbursement
5. On disbursement success → ImpactReporter auto-triggered
6. On report ready → Notify donor + log audit

# Guardrails

- Do not handle funds or access private keys directly.
- Do not modify blockchain transactions manually — delegate to AutoDisbursementAgent.
- Do not fabricate or assume missing data — request or retry instead.
- Do not provide financial, legal, or investment advice.
- Always ensure that actions comply with security, audit, and transparency requirements.
- If critical data or authorization is missing, pause and escalate instead of proceeding.
"""

# Enhanced tools with placeholder IDs that will be replaced dynamically
custom_tools = [
    {
        "type": "system",
        "name": "transfer_to_donation_tracker",
        "description": "Check for new donations on blockchain",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [{
                "agent_id": "{DONATION_TRACKER_ID}",
                "condition": "check_donations",
                "delay_ms": 0,
                "transfer_message": "Poll for new USDC donations now.",
                "enable_transferred_agent_first_message": True
            }]
        },
        "disable_interruptions": False
    },
    {
        "type": "system",
        "name": "transfer_to_needs_predictor",
        "description": "Predict funding needs for projects",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [{
                "agent_id": "{NEEDS_PREDICTOR_ID}",
                "condition": "predict_needs",
                "delay_ms": 0,
                "transfer_message": "Analyze donation trends and predict needs for project {project_id} with data: {historical_data}",
                "enable_transferred_agent_first_message": True
            }]
        },
        "disable_interruptions": False
    },
    {
        "type": "system",
        "name": "transfer_to_milestone_verifier",
        "description": "Verify milestone proof",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [{
                "agent_id": "{MILESTONE_VERIFIER_ID}",
                "condition": "verify_milestone",
                "delay_ms": 0,
                "transfer_message": "Verify milestone {milestone_id} for project {project_id}. Proof files: {proof_files}",
                "enable_transferred_agent_first_message": True
            }]
        },
        "disable_interruptions": False
    },
    {
        "type": "system",
        "name": "transfer_to_auto_disbursement",
        "description": "Release funds if verified",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [{
                "agent_id": "{AUTO_DISBURSEMENT_ID}",
                "condition": "disburse_funds",
                "delay_ms": 0,
                "transfer_message": "Milestone {milestone_id} verified. Disburse {amount} USDC to {wallet_address} for project {project_id}.",
                "enable_transferred_agent_first_message": True
            }]
        },
        "disable_interruptions": False
    },
    {
        "type": "system",
        "name": "transfer_to_impact_reporter",
        "description": "Generate donor report",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [{
                "agent_id": "{IMPACT_REPORTER_ID}",
                "condition": "generate_report",
                "delay_ms": 0,
                "transfer_message": "Generate impact report for donor {donor_wallet} on project {project_id} with milestones: {milestones_completed}.",
                "enable_transferred_agent_first_message": True
            }]
        },
        "disable_interruptions": False
    },
    {
        "type": "system", 
        "name": "transfer_to_ngo_researcher",
        "description": "Find new verified NGOs",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [{
                "agent_id": "{NGO_RESEARCHER_ID}",
                "condition": "research_ngos",
                "delay_ms": 0,
                "transfer_message": "Research new NGOs for category: {category} in region: {region}",
                "enable_transferred_agent_first_message": True
            }]
        },
        "disable_interruptions": False
    },
    {
        "type": "system",
        "name": "transfer_to_ngo_monitor", 
        "description": "Monitor existing NGOs for issues",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [{
                "agent_id": "{NGO_MONITOR_ID}",
                "condition": "monitor_ngo",
                "delay_ms": 0,
                "transfer_message": "Monitor NGO: {ngo_name} for transparency and compliance issues.",
                "enable_transferred_agent_first_message": True
            }]
        },
        "disable_interruptions": False
    }
]

# Create Orchestrator Agent
try:
    response = client.conversational_ai.agents.create(
        name=agent_name,
        tags=["AI Charity", "Orchestrator"],
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

    print(f"✅ Created Orchestrator Agent with ID: {response.agent_id}")

    # Save agent ID for later orchestration
    agent_data = {"Orchestrator Agent": response.agent_id}
    with open("orchestrator_agent_id.json", "w") as f:
        json.dump(agent_data, f, indent=2)

    print("✅ Agent ID saved to orchestrator_agent_id.json")

except Exception as e:
    print(f"❌ Failed to create Orchestrator Agent: {e}")