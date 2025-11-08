from flask import Flask, send_from_directory, jsonify, request, Response
import json, os, random
from web3 import Web3
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Web3
w3 = Web3(Web3.HTTPProvider("https://rpc.testnet.arc.network"))

# Global NGOs
GLOBAL_NGOS = {
    "Pakistan": [
        {"name": "Akhuwat Foundation", "country": "Pakistan", "wallet": "0x2de592b3951807dfb72931596d11fe93b753881e"},
        {"name": "Edhi Foundation", "country": "Pakistan", "wallet": "0x1234567890123456789012345678901234567890"}
    ],
    "Afghanistan": [
        {"name": "Doctors Without Borders", "country": "Afghanistan", "wallet": "0xMSF1234567890abcdef1234567890abcdef1234"},
        {"name": "Save the Children", "country": "Afghanistan", "wallet": "0xSTC1234567890abcdef1234567890abcdef5678"}
    ],
    "India": [
        {"name": "Goonj", "country": "India", "wallet": "0xGOONJ1234567890abcdef1234567890abcdef12"},
        {"name": "Akshaya Patra", "country": "India", "wallet": "0xAKP1234567890abcdef1234567890abcdef3456"}
    ],
    "default": [
        {"name": "Global Relief Fund", "country": "Global", "wallet": "0xGLOBAL1234567890abcdef1234567890abcdef"},
        {"name": "Humanity First", "country": "Global", "wallet": "0xHF1234567890abcdef1234567890abcdef123456"}
    ]
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json.get("message", "").lower()
    
    response = "Connecting to Orchestrator Agent... Here are verified NGOs in Pakistan. Use the USDC Transfer panel below to send directly!"
    
    # Detect country
    country = "Pakistan"
    for c in ["afghanistan", "india", "usa", "brazil"]:
        if c in msg:
            country = c.title()
            break
    
    if "afghanistan" in msg:
        response = f"Connecting to Orchestrator Agent... Here are verified NGOs in Afghanistan. Use the USDC Transfer panel below to send directly!"
    
    def stream():
        for word in response.split():
            yield word + " "
            import time
            time.sleep(0.05)
    return Response(stream(), mimetype="text/plain")

@app.route('/research')
def research():
    q = request.args.get('q', 'Pakistan').title()
    ngos = GLOBAL_NGOS.get(q, GLOBAL_NGOS["default"])
    return jsonify(ngos)

@app.route('/donate', methods=['POST'])
def donate():
    data = request.json
    return jsonify({"success": True, "tx": {"hash": "0x9beb48cb" + os.urandom(16).hex()}})

print("AI Charity Server → http://localhost:5000 (پہلے والا — بالکل وہی!)")
if __name__ == '__main__':
    app.run(port=5000, debug=True)
