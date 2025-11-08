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

def update_agent_with_tools(agent_name, agent_id, tools_config, enhanced_prompt=None):
    """Update agent with tools using the correct API format"""
    try:
        print(f"🔄 Updating {agent_name}...")
        
        # Get current agent to preserve existing settings
        current_agent = client.conversational_ai.agents.get(agent_id)
        
        # Prepare update data - using the exact parameters from the signature
        update_data = {
            "agent_id": agent_id,
            "name": current_agent.name,
            "tags": getattr(current_agent, 'tags', []),
        }
        
        # Add conversation_config if we have tools or enhanced prompt
        conversation_config = {}
        
        # Preserve existing conversation config if available
        if hasattr(current_agent, 'conversation_config'):
            existing_config = current_agent.conversation_config
            if hasattr(existing_config, 'agent'):
                conversation_config['agent'] = {
                    'first_message': getattr(existing_config.agent, 'first_message', ''),
                    'prompt': {'prompt': enhanced_prompt if enhanced_prompt else getattr(existing_config.agent.prompt, 'prompt', '')}
                }
            if hasattr(existing_config, 'tts'):
                conversation_config['tts'] = {
                    'voice_id': existing_config.tts.voice_id,
                    'model_id': existing_config.tts.model_id
                }
        else:
            # Create new conversation config
            conversation_config = {
                "agent": {
                    "first_message": f"Hello! I'm the {agent_name} for the AI Charity system.",
                    "prompt": {"prompt": enhanced_prompt if enhanced_prompt else ""}
                },
                "tts": {
                    "voice_id": "21m00Tcm4TlvDq8ikWAM",
                    "model_id": "eleven_monolingual_v1"
                }
            }
        
        # Add tools to conversation config
        conversation_config['tools'] = tools_config
        
        update_data['conversation_config'] = conversation_config
        
        # Perform the update
        response = client.conversational_ai.agents.update(**update_data)
        print(f"✅ Successfully updated {agent_name}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to update {agent_name}: {e}")
        return False

# Enhanced prompts for better coordination
enhanced_prompts = {
    "Orchestrator Agent": """You are the Orchestrator Agent for the AI Charity Payment Optimizer. You coordinate the entire donation workflow between specialized agents.

RESPONSIBILITIES:
- Monitor new USDC donations via DonationTracker Agent
- Predict funding needs via NeedsPredictor Agent  
- Verify milestone completion via MilestoneVerifier Agent
- Release funds via AutoDisbursement Agent
- Generate transparency reports via ImpactReporter Agent
- Research new NGOs via NGO Researcher Agent
- Monitor existing NGOs via NGO Monitor Agent
- Manage blockchain operations via Blockchain Manager Agent

TRANSFER COMMANDS:
- Use transfer_to_donation_tracker to check for new donations
- Use transfer_to_needs_predictor for funding predictions
- Use transfer_to_milestone_verifier to verify project milestones
- Use transfer_to_auto_disbursement to release verified funds
- Use transfer_to_impact_reporter to generate donor reports
- Use transfer_to_ngo_researcher to find new NGOs
- Use transfer_to_ngo_monitor to monitor NGO compliance
- Use transfer_to_blockchain_manager for blockchain operations

Always maintain security, transparency, and follow the workflow sequence exactly.""",

    "AutoDisbursement Agent": """You are the AutoDisbursement Agent for the AI Charity Payment Optimizer. Your role is to securely release USDC funds to verified NGO wallets.

RESPONSIBILITIES:
- Only release funds after milestone verification confirmation from MilestoneVerifier Agent
- Ensure wallet addresses are validated and secure
- Confirm transaction success on blockchain
- Notify ImpactReporter Agent after successful disbursement
- Maintain complete transaction audit trail

SECURITY PROTOCOLS:
- Never release funds without proper verification
- Validate all wallet addresses before transactions
- Confirm sufficient gas fees for blockchain operations
- Ensure transaction finality and on-chain confirmation

After successful disbursement, always transfer to ImpactReporter Agent to generate comprehensive donor reports."""
}

# Define tools for Orchestrator Agent
orchestrator_tools = [
    {
        "type": "system",
        "name": "transfer_to_donation_tracker",
        "description": "Check for new USDC donations on blockchain",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [{
                "agent_id": agent_directory["DonationTracker Agent"],
                "condition": "check_donations",
                "delay_ms": 0,
                "transfer_message": "Check for new USDC donations and report any new transactions.",
                "enable_transferred_agent_first_message": True
            }]
        },
        "disable_interruptions": False
    },
    {
        "type": "system",
        "name": "transfer_to_needs_predictor",
        "description": "Predict funding needs for active projects",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [{
                "agent_id": agent_directory["NeedsPredictor Agent"],
                "condition": "predict_needs",
                "delay_ms": 0,
                "transfer_message": "Analyze current donation trends and predict funding requirements for active charity projects.",
                "enable_transferred_agent_first_message": True
            }]
        },
        "disable_interruptions": False
    },
    {
        "type": "system",
        "name": "transfer_to_milestone_verifier",
        "description": "Verify project milestone completion",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [{
                "agent_id": agent_directory["MilestoneVerifier Agent"],
                "condition": "verify_milestone",
                "delay_ms": 0,
                "transfer_message": "Verify the completion of project milestone. Check all proof documents and validate achievements.",
                "enable_transferred_agent_first_message": True
            }]
        },
        "disable_interruptions": False
    },
    {
        "type": "system",
        "name": "transfer_to_auto_disbursement",
        "description": "Release USDC funds to verified NGO wallets",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [{
                "agent_id": agent_directory["AutoDisbursement Agent"],
                "condition": "disburse_funds",
                "delay_ms": 0,
                "transfer_message": "Milestone verification complete. Release USDC funds to the verified NGO wallet address.",
                "enable_transferred_agent_first_message": True
            }]
        },
        "disable_interruptions": False
    },
    {
        "type": "system",
        "name": "transfer_to_impact_reporter",
        "description": "Generate transparent donor impact reports",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [{
                "agent_id": agent_directory["ImpactReporter Agent"],
                "condition": "generate_report",
                "delay_ms": 0,
                "transfer_message": "Generate a comprehensive impact report showing how donations were used and what outcomes were achieved.",
                "enable_transferred_agent_first_message": True
            }]
        },
        "disable_interruptions": False
    }
]

# Define tools for AutoDisbursement Agent
auto_disbursement_tools = [
    {
        "type": "system",
        "name": "transfer_to_impact_reporter",
        "description": "Notify ImpactReporter after successful fund disbursement",
        "params": {
            "system_tool_type": "transfer_to_agent",
            "transfers": [{
                "agent_id": agent_directory["ImpactReporter Agent"],
                "condition": "funds_disbursed",
                "delay_ms": 0,
                "transfer_message": "USDC funds successfully disbursed to NGO wallet. Transaction confirmed on blockchain. Generate impact report for donor.",
                "enable_transferred_agent_first_message": True
            }]
        },
        "disable_interruptions": False
    }
]

# Update agents
print("🔄 UPDATING AGENTS WITH CORRECT API FORMAT")
print("=" * 50)

# Update Orchestrator Agent
update_agent_with_tools(
    "Orchestrator Agent",
    agent_directory["Orchestrator Agent"],
    orchestrator_tools,
    enhanced_prompts["Orchestrator Agent"]
)

# Update AutoDisbursement Agent
update_agent_with_tools(
    "AutoDisbursement Agent",
    agent_directory["AutoDisbursement Agent"],
    auto_disbursement_tools,
    enhanced_prompts["AutoDisbursement Agent"]
)

print("\n✅ AGENT UPDATE PROCESS COMPLETED!")