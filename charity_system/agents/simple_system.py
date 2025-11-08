import os
import inspect
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
import json

load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=api_key)

print("🔍 CHECKING simulate_conversation PARAMETERS")
print("=" * 50)

try:
    # Get the method signature
    method = client.conversational_ai.agents.simulate_conversation
    sig = inspect.signature(method)
    print(f"📋 Method signature: {sig}")
    
    # Check what parameters are required
    print("\n📝 Parameters:")
    for param_name, param in sig.parameters.items():
        print(f"  - {param_name}: {param.annotation} (default: {param.default})")
        
except Exception as e:
    print(f"❌ Could not inspect method: {e}")

# Try to find examples or documentation
print("\n🧪 Testing different parameter combinations...")

# Load agent directory
try:
    with open('agent_directory.json', 'r') as f:
        agent_directory = json.load(f)
    
    orchestrator_id = agent_directory["Orchestrator Agent"]
    print(f"\nTesting with Orchestrator Agent: {orchestrator_id}")
    
    # Test different parameter combinations
    test_cases = [
        {"agent_id": orchestrator_id, "text": "Hello, how are you?"},
        {"agent_id": orchestrator_id, "message": "Hello, how are you?"},
        {"agent_id": orchestrator_id, "input": "Hello, how are you?"},
        {"agent_id": orchestrator_id, "prompt": "Hello, how are you?"},
        {"agent_id": orchestrator_id, "query": "Hello, how are you?"},
    ]
    
    for i, params in enumerate(test_cases, 1):
        print(f"\n{i}. Testing parameters: {list(params.keys())}")
        try:
            result = client.conversational_ai.agents.simulate_conversation(**params)
            print(f"   ✅ SUCCESS! Response type: {type(result)}")
            if hasattr(result, 'response'):
                print(f"   💬 Response: {result.response}")
            break
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            
except Exception as e:
    print(f"Error: {e}")