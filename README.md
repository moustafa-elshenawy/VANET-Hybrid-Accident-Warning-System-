# VANET-Hybrid-Accident-Warning-System-
A Blockchain-based solution for Vehicular Ad-hoc Networks (VANETs) implementing secure vehicle authentication, trusted accident data recording, and defenses against Impersonation, Replay, and Sybil attacks using Solidity and Python.
Secure VANET Accident Warning System 🚗🔗

A Blockchain-Based Approach for Secure Authentication and Trusted Data Recording in Vehicular Ad-Hoc Networks.

📖 Project Overview

Course: Blockchain Applications

Domain: Emerging Networks (VANET / IoT)

Status: Completed & Tested

This project addresses critical security challenges in Vehicular Ad-hoc Networks (VANETs), specifically the issues of trust and data integrity in accident reporting systems. In traditional vehicular networks, malicious actors can impersonate emergency vehicles, broadcast fake alerts to cause congestion, or replay old messages to disrupt operations.

To solve this, we designed and implemented a Hybrid Blockchain-Based Accident Warning System using Ethereum Smart Contracts. It enforces a decentralized "Root of Trust" that ensures only authorized vehicles can report accidents, preventing false alarms and traffic disruption.

🔑 Key Features & Security Logic

The system is designed to defend against three specific attack vectors outlined in the project requirements:

1. Secure Authentication (Access Control)

Mechanism: Strict Whitelisting. A central Traffic Authority must register vehicles (Machines) and users (Humans) before they can interact with the network.

Defense: Neutralizes Impersonation Attacks (unauthorized entities cannot write to the ledger) and Sybil Attacks (one entity cannot create multiple fake identities).

2. Trusted Data Recording

Mechanism: Immutable Logging. Accident reports are stored as tamper-proof blockchain Events containing location data, reporter identity, and timestamps.

Defense: Prevents Modification Attacks. Once a report is validated and mined, it cannot be altered or deleted.

3. Replay & Spam Prevention (Hybrid Logic)

Mechanism:

Automatic Timestamping: The contract uses block.timestamp to prevent users from injecting fake or old times.

Duplicate Hash Check: Prevents submitting the exact same report twice.

Rate Limiting: Enforces a cooldown period (1 minute for Machines, 3 minutes for Humans) to prevent spamming.

Defense: Mitigates Replay Attacks and DoS/Spam Attacks.

🛠️ Technology Stack

Smart Contract: Solidity (v0.8.0)

Blockchain Simulation: Ganache (Local Ethereum Blockchain)

Deployment: Remix IDE

Testing & Interaction: Python (Web3.py)

🚀 Installation & Usage

Follow these steps to run the simulation on your local machine.

Prerequisites

Node.js & Ganache:

npm install -g ganache


Python 3.x & Web3.py:

pip install web3


Step 1: Start the Blockchain

Open a terminal window and run a local Ganache instance:

ganache


Note the RPC Server URL (usually http://127.0.0.1:8545). Keep this terminal open.

Step 2: Deploy the Contract

Open Remix IDE.

Create a file named VANETSafety.sol and paste the contract code.

Go to the Deploy tab.

Set Environment to Dev - Ganache Provider (connect to https://www.google.com/search?q=http://127.0.0.1:8545).

Deploy the contract.

Step 3: Run the Simulation

Copy the Contract Address from Remix.

Open vanet_hybrid_demo.py.

Update the CONTRACT_ADDRESS variable on line 12.

Run the script:

python3 vanet_hybrid_demo.py


🛡️ Security Analysis (Simulation Results)

We validated the system using a custom Python script that acts as both a legitimate user and a malicious attacker.

Attack Vector

Defense Mechanism

Simulation Result

Impersonation

onlyAuthorized Modifier

🛡️ BLOCKED

Duplicate/Spam

Hash Check & Rate Limit

🛡️ BLOCKED

Sybil Attack

Centralized Registration

🛡️ BLOCKED

Modification

Blockchain Immutability

🛡️ BLOCKED

DoS Attack

Gas Fee Economic Barrier

Infeasible ($1.1M/hr cost)

Sample Output

4. IMPERSONATION ATTACK
   🛡️ BLOCKED (Expected): Access Denied: You are not authorized.

5. SPAM ATTACK (Rate Limit / Duplicate)
   [Machine] Sending SAME report again immediately...
   🛡️ BLOCKED (Expected): Error: Duplicate report detected.

6. SYBIL ATTACK
   🛡️ BLOCKED (Expected): Only Traffic Authority can perform this.


📊 Performance Evaluation

Gas Consumption Analysis:

Vehicle Registration: ~73,365 Gas (Low cost, one-time)

Accident Reporting: ~169,745 Gas (Medium cost, high security)

Latency:

Simulation: < 50ms (Instant)

Mainnet Projection: ~12 seconds (1 Block Confirmation)

Authors:
Moustafa Ahmed Elsayed
Hala Degol Abdelrahman
Hagar Mahmoud Fathy Soliman

📄 License

This project is open-source and available under the MIT License.
