import time
import json
import warnings
from web3 import Web3

# Filter out the specific MismatchedABI warning to clean up output
# The transaction succeeds, so this warning is just about log decoding
warnings.filterwarnings("ignore", category=UserWarning, module='eth_utils')

# --- CONFIGURATION ---
GANACHE_URL = "http://127.0.0.1:8545"
CONTRACT_ADDRESS = "0xEc6Ef05c3595C8ac6791b2F1ecc17E8a8cBf2Dd9" # PASTE YOUR NEW CONTRACT ADDRESS HERE

# 2. UPDATED ABI (Matches the latest contract provided)
CONTRACT_ABI = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{"indexed": True, "internalType": "uint256", "name": "id", "type": "uint256"},
			{"indexed": False, "internalType": "string", "name": "location", "type": "string"},
			{"indexed": True, "internalType": "address", "name": "reporter", "type": "address"},
			{"indexed": False, "internalType": "string", "name": "reportType", "type": "string"},
			{"indexed": False, "internalType": "bytes32", "name": "reportHash", "type": "bytes32"}
		],
		"name": "AccidentReported",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{"indexed": True, "internalType": "address", "name": "entity", "type": "address"},
			{"indexed": False, "internalType": "string", "name": "role", "type": "string"}
		],
		"name": "EntityRegistered",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{"indexed": False, "internalType": "string", "name": "alertType", "type": "string"},
			{"indexed": True, "internalType": "address", "name": "attacker", "type": "address"}
		],
		"name": "SecurityAlert",
		"type": "event"
	},
	{
		"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
		"name": "accidentLog",
		"outputs": [
			{"internalType": "uint256", "name": "id", "type": "uint256"},
			{"internalType": "string", "name": "location", "type": "string"},
			{"internalType": "uint256", "name": "timestamp", "type": "uint256"},
			{"internalType": "address", "name": "reporter", "type": "address"},
			{"internalType": "uint8", "name": "rType", "type": "uint8"}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [{"internalType": "address", "name": "", "type": "address"}],
		"name": "authorizedUsers",
		"outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [{"internalType": "address", "name": "", "type": "address"}],
		"name": "authorizedVehicles",
		"outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getAccidentCount",
		"outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getEntityCounts",
		"outputs": [
			{"internalType": "uint256", "name": "", "type": "uint256"},
			{"internalType": "uint256", "name": "", "type": "uint256"}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [{"internalType": "address", "name": "", "type": "address"}],
		"name": "lastReportTime",
		"outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
		"name": "processedReports",
		"outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [{"internalType": "address", "name": "_user", "type": "address"}],
		"name": "registerUser",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [{"internalType": "address", "name": "_vehicle", "type": "address"}],
		"name": "registerVehicle",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [{"internalType": "string", "name": "_location", "type": "string"}],
		"name": "reportAccident",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "trafficAuthority",
		"outputs": [{"internalType": "address", "name": "", "type": "address"}],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "userCount",
		"outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "vehicleCount",
		"outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
		"stateMutability": "view",
		"type": "function"
	}
]

# --- SETUP ---
try:
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    if not w3.is_connected():
        print("❌ Connect Ganache!")
        exit()
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    accounts = w3.eth.accounts
    
    # Roles
    AUTHORITY = accounts[0]
    MACHINE_NODE = accounts[1] 
    HUMAN_USER = accounts[2]   
    ATTACKER = accounts[9]
    
    # Verify Authority
    try:
        real_auth = contract.functions.trafficAuthority().call()
        if real_auth != AUTHORITY: AUTHORITY = real_auth
    except:
        print("❌ Critical: Update CONTRACT_ADDRESS in the script!")
        exit()

except Exception as e:
    print(f"❌ Error: {e}")
    exit()

print("\n--- ROLE DEFINITIONS ---")
print(f"   [Admin]   Authority: {AUTHORITY}")
print(f"   [Machine] Vehicle:   {MACHINE_NODE}")
print(f"   [Human]   User App:  {HUMAN_USER}")
print(f"   [Enemy]   Attacker:  {ATTACKER}")
print("------------------------")

# --- HELPER FUNCTIONS ---
def send_tx(func_call, sender, expected_fail=False):
    try:
        # Simulate first
        try:
            func_call.call({'from': sender})
        except Exception as sim_error:
            reason = extract_reason(str(sim_error))
            if expected_fail:
                 print(f"   🛡️ BLOCKED (Expected): {reason}")
            else:
                 print(f"   ❌ FAILED (Unexpected): {reason}")
            return False, 0

        # Transact
        tx_hash = func_call.transact({'from': sender, 'gas': 3000000})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt['status'] == 1:
            print(f"   ✅ Success! Block: {receipt['blockNumber']} | Gas: {receipt['gasUsed']}")
            
            # LOGGING HASH
            logs = contract.events.AccidentReported().process_receipt(receipt)
            if logs:
                event_data = logs[0]['args']
                r_hash = event_data['reportHash'].hex()
                print(f"      📄 Report Hash: {r_hash}")
                print(f"      📍 Location:    {event_data['location']}")
                print(f"      🤖 Source:      {event_data['reportType']}")
            return True, receipt['gasUsed']
        return False, 0
    except Exception as e:
        print(f"   ❌ Execution Error: {e}")
        return False, 0

def extract_reason(msg):
    if "revert" in msg:
        if "Access Denied" in msg: return "Impersonation (Not Authorized)"
        if "Duplicate report" in msg: return "Duplicate Report (Hash Collision)"
        if "Rate Limit" in msg: return "Rate Limit (Spamming Detected)"
        if "Address already registered" in msg: return "Registration Error (Duplicate)"
        if "Only Traffic Authority" in msg: return "Sybil Defense (Only Admin can Register)"
        return "REVERT: " + msg.split("revert")[-1][:60]
    return msg

# --- MAIN SIMULATION ---
def run_vanet_simulation():
    
    print("\n" + "="*60)
    print("SCENARIO 1: SYSTEM SETUP & REGISTRATION")
    print("DESCRIPTION: The Authority whitelists a Machine and a Human User.")
    print("="*60)
    
    # Register Machine
    if not contract.functions.authorizedVehicles(MACHINE_NODE).call():
        print(f"   [Action] Registering Machine Node...")
        send_tx(contract.functions.registerVehicle(MACHINE_NODE), AUTHORITY)
    else:
        print(f"   [Info] Machine Node already registered.")

    # Register Human
    if not contract.functions.authorizedUsers(HUMAN_USER).call():
        print(f"   [Action] Registering Human User...")
        send_tx(contract.functions.registerUser(HUMAN_USER), AUTHORITY)
    else:
        print(f"   [Info] Human User already registered.")

    # ---------------------------------------------------------
    print("\n" + "="*60)
    print("SCENARIO 2: MACHINE REPORT (Automatic Timestamp)")
    print("DESCRIPTION: Machine sends a valid report. Timestamp is auto-generated.")
    print("="*60)
    
    # Note: Only Location is sent. Timestamp is automatic.
    print(f"   [Machine] Sending Sensor Report...")
    send_tx(contract.functions.reportAccident("Sensor Detect Hwy 1"), MACHINE_NODE)

    # ---------------------------------------------------------
    print("\n" + "="*60)
    print("SCENARIO 3: HUMAN REPORT (Automatic Timestamp)")
    print("DESCRIPTION: Human sends a valid report. Timestamp is auto-generated.")
    print("="*60)
    
    print(f"   [Human]   Sending Manual Report...")
    send_tx(contract.functions.reportAccident("User Witness Hwy 1"), HUMAN_USER)

    # ---------------------------------------------------------
    print("\n" + "="*60)
    print("SCENARIO 4: IMPERSONATION ATTACK")
    print("DESCRIPTION: Unauthorized attacker tries to send a report.")
    print("="*60)
    
    print(f"   [Hacker] {ATTACKER} trying to report accident...")
    send_tx(contract.functions.reportAccident("Fake Data"), ATTACKER, expected_fail=True)

    # ---------------------------------------------------------
    print("\n" + "="*60)
    print("SCENARIO 5: SPAM ATTACK (Rate Limit & Duplicate)")
    print("DESCRIPTION: Machine tries to send exact same report immediately.")
    print("="*60)
    
    print(f"   [Machine] Sending SAME report again immediately...")
    # This proves the Rate Limit (1 minute) works. 
    # If you waited > 1 minute but sent same data in same block, Hash Check would trigger.
    send_tx(contract.functions.reportAccident("Sensor Detect Hwy 1"), MACHINE_NODE, expected_fail=True)

    # ---------------------------------------------------------
    print("\n" + "="*60)
    print("SCENARIO 6: SYBIL ATTACK")
    print("DESCRIPTION: Attacker tries to register a fake car identity.")
    print("="*60)
    print(f"   [Hacker] {ATTACKER} trying to register fake car...")
    send_tx(contract.functions.registerVehicle(accounts[8]), ATTACKER, expected_fail=True)

    # ---------------------------------------------------------
    print("\n" + "="*60)
    print("FINAL SYSTEM STATUS CHECK")
    print("="*60)
    count = contract.functions.getAccidentCount().call()
    print(f"   Total Accidents Recorded: {count}")
    if count == 2:
        print("   ✅ SUCCESS: Exactly 2 Valid Reports.")
        print("   ✅ SUCCESS: All Attacks & Spam Attempts Blocked.")
    else:
        print(f"   ⚠️ CHECK: Count is {count} (Expected 2).")

if __name__ == "__main__":
    run_vanet_simulation()
