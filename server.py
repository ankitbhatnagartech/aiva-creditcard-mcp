#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP
import pymongo

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME", "Veda_Rituals")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "wf-creditcards-ivr")

SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

if not MONGO_URI:
    print("ERROR: MONGO_URI environment variable not set in .env file.", file=sys.stderr)
    sys.exit(1)

# Initialize FastMCP Server
mcp = FastMCP("aiva-creditcard-mcp")

# Initialize FastAPI app
app = FastAPI(
    title="Wells Fargo Credit Card IVR REST Gateway",
    description="HTTP REST API proxy for the aiva-creditcard-mcp server to enable runtime testing via Postman.",
    version="1.0.0"
)

# Connect to MongoDB
def get_db_collection():
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        return db[COLLECTION_NAME]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}", file=sys.stderr)
        raise e

# Pydantic schema for FastAPI
class CreditCardRequest(BaseModel):
    account_number: str = Field(..., description="Wells Fargo Account Number (10 digits)", example="9876543210")
    card_number: str = Field(..., description="Last 4 digits of the card number", example="1111")
    query_or_action: str = Field(..., description="Action to perform: 'get_transactions', 'select_transaction', 'request_limit_increase', 'unblock_card', 'confirm_fraud', 'deny_fraud'", example="get_transactions")
    transaction_id: str = Field(None, description="Target transaction ID for disputes or limits", example="TXN_FAIL_001")
    security_answer: str = Field(None, description="Security answer to unblock card", example="Buddy")

# Core Banking Logic
def execute_banking_logic(
    account_number: str,
    card_number: str,
    query_or_action: str,
    transaction_id: str = None,
    security_answer: str = None
) -> str:
    collection = get_db_collection()
    
    # 1. Look up the customer account by account_number
    query = {
        "account_number": account_number,
        "$or": [
            {"card_details.card_number_masked": card_number},
            {"card_details.card_number_full": {"$regex": f"{card_number}$"}}
        ]
    }
    
    account = collection.find_one(query)
    if not account:
        return (
            f"Error: I couldn't find a credit card account matching that account number and card number. "
            f"Could you please check your details and try again?\n\n"
            f"[SYSTEM_LOG] Lookup Failed | Account: {account_number} | Card Ends: {card_number}"
        )
    
    customer_name = account.get("customer_name", "Valued Customer")
    card_details = account.get("card_details", {})
    card_masked = card_details.get("card_number_masked", "XXXX")
    card_status = card_details.get("status", "Active")
    credit_limit = card_details.get("credit_limit", 0.0)
    available_balance = card_details.get("available_balance", 0.0)
    action_logs = account.get("action_logs", [])
    
    # 2. Process based on query_or_action
    action_lower = query_or_action.strip().lower()
    
    # --- ACTION: get_transactions ---
    if action_lower == "get_transactions":
        txns = account.get("transactions", [])
        
        response_str = (
            f"==================================================\n"
            f"       WELLS FARGO CREDIT CARD SYSTEM (AIVA)      \n"
            f"==================================================\n"
            f"Customer Name     : {customer_name}\n"
            f"Account Number    : {account_number}\n"
            f"Card Number       : XXXX-XXXX-XXXX-{card_masked}\n"
            f"Card Status       : {card_status}\n"
            f"Available Credit  : ${available_balance:,.2f}\n"
            f"Daily Limit       : ${credit_limit:,.2f}\n"
            f"--------------------------------------------------\n"
            f"Recent Transaction History (Last 5-10):\n"
        )
        
        if not txns:
            response_str += "  No transactions found for this card.\n"
        else:
            for idx, t in enumerate(txns, 1):
                t_id = t.get("transaction_id", "N/A")
                merchant = t.get("merchant", "Merchant")
                amt = t.get("amount", 0.0)
                status = t.get("status", "Success")
                reason = t.get("failure_reason")
                flagged = t.get("flagged_suspicious", False)
                disputed = t.get("is_disputed", False)
                
                status_desc = status
                if status == "Failed" and reason:
                    status_desc = f"Failed ({reason})"
                elif flagged:
                    status_desc = "Success (FLAGGED SUSPICIOUS)"
                elif disputed:
                    status_desc = "Success (DISPUTED)"
                    
                response_str += f"  {idx}. ID: {t_id} | {merchant:<20} | ${amt:<8,.2f} | {status_desc}\n"
                
        response_str += (
            f"--------------------------------------------------\n"
            f"[AIVA IVR Dialogue]\n"
            f"\"Here is your recent statement. Which transaction do you have a question about?\""
        )
        return response_str

    # --- ACTION: select_transaction ---
    elif action_lower == "select_transaction":
        # Blocked Card exception logic (if card is blocked and transaction_id is omitted)
        if card_status == "Blocked" and not transaction_id:
            security_question = card_details.get("security_question", "your security question")
            
            # Check for permanent fraud compromise first
            has_fraud_compromise = any(log.get("action_type") == "FRAUD_CONFIRMED_CARD_BLOCKED" for log in action_logs)
            if has_fraud_compromise:
                return (
                    f"[AIVA IVR Dialogue]\n"
                    f"\"For your safety, the card ending in {card_masked} has been permanently deactivated due to a confirmed fraud dispute. A replacement card is on its way. Let me connect you directly with a representative for further help.\"\n\n"
                    f"[SYSTEM_LOG] Account: {account_number} | Status: Hot-Carded / Deactivated (ISO 8583 Code: 43 - Stolen Card)"
                )
            
            # Retrieve failed unblock attempts to see if already locked out
            failed_attempts = sum(1 for log in action_logs if log.get("action_type") == "FAILED_UNBLOCK_ATTEMPT")
            if failed_attempts >= 3:
                return (
                    f"[AIVA IVR Dialogue]\n"
                    f"\"For your security, we've locked unblocking attempts on this card because the answer didn't match our records after multiple attempts. To help you get this resolved, let's get you connected to a customer service specialist right away. Please hold on.\"\n\n"
                    f"[SYSTEM_LOG] Account: {account_number} | Card ending in {card_masked} LOCKED OUT (ISO 8583 Code: 38 - PIN Try Limit Exceeded)"
                )
                
            return (
                f"[AIVA IVR Dialogue]\n"
                f"\"I see your card ending in {card_masked} is currently blocked for security. I can easily unblock this for you. First, let's verify your identity. Could you please tell me: {security_question}?\"\n\n"
                f"[SYSTEM_LOG] Account: {account_number} | Status: Blocked (ISO 8583 Code: 57 - Restricted Card) | Attempt: {failed_attempts}/3"
            )
            
        if not transaction_id:
            return (
                f"Error: Please specify a transaction ID to review.\n\n"
                f"[SYSTEM_LOG] Request Rejected | Transaction ID missing"
            )
            
        txns = account.get("transactions", [])
        target_txn = next((t for t in txns if t.get("transaction_id") == transaction_id), None)
        
        if not target_txn:
            return (
                f"Error: I couldn't find transaction ID '{transaction_id}' in your statement history.\n\n"
                f"[SYSTEM_LOG] Request Rejected | Transaction ID not found: {transaction_id}"
            )
            
        t_id = target_txn.get("transaction_id")
        merchant = target_txn.get("merchant")
        amt = target_txn.get("amount", 0.0)
        status = target_txn.get("status")
        reason = target_txn.get("failure_reason")
        flagged = target_txn.get("flagged_suspicious", False)
        
        response_str = (
            f"WELLS FARGO TRANSACTION INQUIRY REPORT\n"
            f"----------------------------------\n"
            f"Transaction ID : {t_id}\n"
            f"Merchant       : {merchant}\n"
            f"Amount         : ${amt:,.2f}\n"
            f"Status         : {status}\n"
        )
        
        if status == "Failed":
            response_str += (
                f"Failure Reason : {reason}\n\n"
                f"[AIVA IVR Dialogue]\n"
                f"\"I found a failed transaction of ${amt:,.2f} at {merchant} because it exceeded your daily credit limit. To help you with this, I can temporarily increase your credit limit so you can complete your purchase. Would you like me to do that?\"\n\n"
                f"[SYSTEM_LOG] Transaction ID: {t_id} | Decline Reason: {reason} (ISO 8583 Code: 51 - Insufficient Funds)"
            )
        elif flagged:
            response_str += (
                f"Flagged State  : FLAGGED SUSPICIOUS BY FRAUD DETECTION\n\n"
                f"[AIVA IVR Dialogue]\n"
                f"\"I see a charge of ${amt:,.2f} at {merchant} on your statement that has been flagged as suspicious. Did you authorize this purchase?\"\n\n"
                f"[SYSTEM_LOG] Transaction ID: {t_id} | Status: Flagged Suspicious (ISO 8583 Code: 34 - Suspected Fraud)"
            )
        else:
            response_str += (
                f"Flagged State  : Normal / Safe\n\n"
                f"[AIVA IVR Dialogue]\n"
                f"\"I see that your transaction of ${amt:,.2f} at {merchant} was processed successfully. Do you have a question about this transaction?\"\n\n"
                f"[SYSTEM_LOG] Transaction ID: {t_id} | Status: Approved (ISO 8583 Code: 00 - Approved)"
            )
        return response_str

    # --- ACTION: request_limit_increase (Failed Transaction flow) ---
    elif action_lower == "request_limit_increase":
        # Reject limit adjustments on Blocked, Locked Out, or Stolen accounts
        failed_attempts = sum(1 for log in action_logs if log.get("action_type") == "FAILED_UNBLOCK_ATTEMPT")
        has_fraud_compromise = any(log.get("action_type") == "FRAUD_CONFIRMED_CARD_BLOCKED" for log in action_logs)
        
        if card_status == "Blocked" or failed_attempts >= 3 or has_fraud_compromise:
            reason_str = "permanently deactivated" if has_fraud_compromise else "temporarily locked out" if failed_attempts >= 3 else "restricted"
            iso_code = "43" if has_fraud_compromise else "38" if failed_attempts >= 3 else "57"
            return (
                f"Error: I cannot process a credit limit increase because there is currently a security hold on this card. Let's get the security hold resolved first.\n\n"
                f"[SYSTEM_LOG] Request Denied | Card Status: {card_status} ({reason_str}) (ISO 8583 Code: {iso_code})"
            )

        if not transaction_id:
            return (
                f"Error: Transaction ID is required to request a limit increase.\n\n"
                f"[SYSTEM_LOG] Request Rejected | Transaction ID missing"
            )
            
        txns = account.get("transactions", [])
        target_txn = next((t for t in txns if t.get("transaction_id") == transaction_id), None)
        
        if not target_txn:
            return (
                f"Error: I couldn't find transaction ID '{transaction_id}' in your statement history.\n\n"
                f"[SYSTEM_LOG] Request Rejected | Transaction ID not found: {transaction_id}"
            )
            
        if target_txn.get("status") != "Failed":
            return (
                f"Error: That transaction was not a failed transaction. Your current daily limit is ${credit_limit:,.2f}.\n\n"
                f"[SYSTEM_LOG] Request Rejected | Target transaction '{transaction_id}' is not failed."
            )
            
        # Log limit increase in database
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        log_entry = {
            "timestamp": timestamp,
            "action_type": "TEMPORARY_LIMIT_INCREASE",
            "details": f"Approved temporary daily limit increase from ${credit_limit} to $2,000.00 for {transaction_id}."
        }
        
        collection.update_one(
            {"_id": account["_id"]},
            {
                "$set": {
                    "card_details.credit_limit": 2000.00,
                    "card_details.available_balance": available_balance + 1000.00
                },
                "$push": {"action_logs": log_entry}
            }
        )
        
        return (
            f"[AIVA IVR Dialogue]\n"
            f"\"Your limit increase has been approved! The daily limit for your card ending in {card_masked} has been temporarily increased to $2,000.00. You can now retry your purchase of ${target_txn.get('amount'):,.2f} at {target_txn.get('merchant')}. Is there anything else I can do for you today?\"\n\n"
            f"[SYSTEM_LOG] Daily credit limit increased to $2,000.00 | Account: {account_number} (ISO 8583 Code: 00 - Decline Code 51 Resolved)"
        )

    # --- ACTION: unblock_card (Blocked Card flow) ---
    elif action_lower == "unblock_card":
        if card_status != "Blocked":
            return (
                f"[AIVA IVR Dialogue]\n"
                f"\"Your credit card ending in {card_masked} is already active and ready for use.\"\n\n"
                f"[SYSTEM_LOG] Unblock Request Ignored | Card is already Active (ISO 8583 Code: 00)"
            )
            
        if not security_answer:
            return (
                f"Error: Security answer is required to unblock this card.\n\n"
                f"[SYSTEM_LOG] Request Rejected | Security answer missing"
            )
            
        # Reject unblocking on permanently deactivated cards
        has_fraud_compromise = any(log.get("action_type") == "FRAUD_CONFIRMED_CARD_BLOCKED" for log in action_logs)
        if has_fraud_compromise:
            return (
                f"Error: This card has been permanently deactivated due to a reported fraud dispute. We cannot unblock this card. A replacement card is already on its way. Let me connect you with a representative for further assistance.\n\n"
                f"[SYSTEM_LOG] Unblock Denied | Card is Hot-Carded/Compromised (ISO 8583 Code: 43 - Stolen Card)"
            )
            
        # Check for 3-strike lockout rule
        failed_attempts = sum(1 for log in action_logs if log.get("action_type") == "FAILED_UNBLOCK_ATTEMPT")
        if failed_attempts >= 3:
            return (
                f"Error: For your security, we've locked self-service unblocking on this card due to multiple failed verification attempts. Let me connect you directly to a representative to assist you.\n\n"
                f"[SYSTEM_LOG] Unblock Locked Out | Attempt Limit Exceeded (3/3) (ISO 8583 Code: 38 - PIN Try Limit Exceeded)"
            )
            
        expected_answer = card_details.get("security_answer", "").strip().lower()
        provided_answer = security_answer.strip().lower()
        
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        if provided_answer == expected_answer:
            # Unblock in database
            log_entry = {
                "timestamp": timestamp,
                "action_type": "CARD_UNBLOCKED",
                "details": "Card unblocked successfully via IVR security question verification."
            }
            collection.update_one(
                {"_id": account["_id"]},
                {
                    "$set": {"card_details.status": "Active"},
                    "$push": {"action_logs": log_entry}
                }
            )
            return (
                f"[AIVA IVR Dialogue]\n"
                f"\"Perfect! That matches our records. Your credit card ending in {card_masked} has been successfully unblocked and is active for immediate use. You are good to go!\"\n\n"
                f"[SYSTEM_LOG] Card ending in {card_masked} set to Active | Account: {account_number} (ISO 8583 Code: 00 - Approved)"
            )
        else:
            # Log failed attempt
            log_entry = {
                "timestamp": timestamp,
                "action_type": "FAILED_UNBLOCK_ATTEMPT",
                "details": f"Failed unblock attempt. Input answer: '{security_answer}' did not match expected answer."
            }
            collection.update_one(
                {"_id": account["_id"]},
                {"$push": {"action_logs": log_entry}}
            )
            
            new_failed_count = failed_attempts + 1
            if new_failed_count >= 3:
                return (
                    f"Error: I'm sorry, that answer doesn't match our records. For your security, unblocking has been locked due to too many failed attempts. Let's get you connected to a representative right away to verify your identity.\n\n"
                    f"[SYSTEM_LOG] Security verification failed. Attempts: {new_failed_count}/3. Lockout triggered (ISO 8583 Code: 38 - PIN Try Limit Exceeded)"
                )
                
            return (
                f"Error: I'm sorry, that answer doesn't match our records. For your security, the card remains blocked. Would you like to try another name?\n\n"
                f"[SYSTEM_LOG] Security verification failed. Attempt: {new_failed_count}/3 (ISO 8583 Code: 57 - Restricted Card)"
            )

    # --- ACTION: confirm_fraud (Fraud Suspicion flow) ---
    elif action_lower == "confirm_fraud":
        if not transaction_id:
            return (
                f"Error: Transaction ID is required to confirm fraud.\n\n"
                f"[SYSTEM_LOG] Request Rejected | Transaction ID missing"
            )
            
        txns = account.get("transactions", [])
        target_txn = next((t for t in txns if t.get("transaction_id") == transaction_id), None)
        
        if not target_txn:
            return (
                f"Error: I couldn't find transaction ID '{transaction_id}' in your statement history.\n\n"
                f"[SYSTEM_LOG] Request Rejected | Transaction ID not found: {transaction_id}"
            )
            
        # Prevent duplicate dispute filings
        if target_txn.get("is_disputed", False):
            return (
                f"[AIVA IVR Dialogue]\n"
                f"\"This transaction is already disputed, and your claim is currently under review. Your card remains deactivated for your safety.\"\n\n"
                f"[SYSTEM_LOG] Transaction already disputed | Card ending in {card_masked} Stolen/Blocked (ISO 8583 Code: 43 - Stolen Card)"
            )
            
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        log_entry = {
            "timestamp": timestamp,
            "action_type": "FRAUD_CONFIRMED_CARD_BLOCKED",
            "details": f"Customer confirmed fraud on transaction {transaction_id}. Card blocked. Dispute filed. Replacement ordered."
        }
        
        # Block the card, dispute the transaction
        collection.update_one(
            {"_id": account["_id"]},
            {
                "$set": {
                    "card_details.status": "Blocked",
                    "transactions.$[elem].is_disputed": True
                },
                "$push": {"action_logs": log_entry}
            },
            array_filters=[{"elem.transaction_id": transaction_id}]
        )
        
        return (
            f"[AIVA IVR Dialogue]\n"
            f"\"Thank you for confirming. I have immediately blocked your card ending in {card_masked} so no further charges can go through. I've also filed a dispute for that ${target_txn.get('amount'):,.2f} charge, so you won't be held responsible. A new replacement card is on its way and will arrive in 3 to 5 business days. In the meantime, I have set up an instant digital copy of your new card in your mobile app, ready for Apple Pay or Google Wallet, so you can continue shopping without interruption!\"\n\n"
            f"[SYSTEM_LOG] Fraud Confirmed | Card ending in {card_masked} blocked, dispute filed, replacement card ordered, digital wallet copy provisioned (ISO 8583 Code: 43 - Stolen Card / Hot-Carded)"
        )

    # --- ACTION: deny_fraud (Suspicion cleared) ---
    elif action_lower == "deny_fraud":
        if not transaction_id:
            return (
                f"Error: Transaction ID is required to deny fraud.\n\n"
                f"[SYSTEM_LOG] Request Rejected | Transaction ID missing"
            )
            
        txns = account.get("transactions", [])
        target_txn = next((t for t in txns if t.get("transaction_id") == transaction_id), None)
        
        if not target_txn:
            return (
                f"Error: I couldn't find transaction ID '{transaction_id}' in your statement history.\n\n"
                f"[SYSTEM_LOG] Request Rejected | Transaction ID not found: {transaction_id}"
            )
            
        # Reject clearing alert on non-flagged transactions
        if not target_txn.get("flagged_suspicious", False):
            return (
                f"Error: This transaction is already authorized and in a safe status. There are no active fraud alerts to clear.\n\n"
                f"[SYSTEM_LOG] Request Ignored | Transaction is not flagged as suspicious (ISO 8583 Code: 00 - Already Approved)"
            )
            
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        log_entry = {
            "timestamp": timestamp,
            "action_type": "SUSPICION_CLEARED_BY_CUSTOMER",
            "details": f"Customer confirmed transaction {transaction_id} was authorized. Flag cleared."
        }
        
        # Clear suspicion flag
        collection.update_one(
            {"_id": account["_id"]},
            {
                "$set": {"transactions.$[elem].flagged_suspicious": False},
                "$push": {"action_logs": log_entry}
            },
            array_filters=[{"elem.transaction_id": transaction_id}]
        )
        
        return (
            f"[AIVA IVR Dialogue]\n"
            f"\"Perfect! Thank you for confirming that you authorized this purchase. I have cleared the alert, and your card ending in {card_masked} remains active and fully ready for use. Is there anything else I can do for you today?\"\n\n"
            f"[SYSTEM_LOG] Fraud alert resolved by customer | Transaction ID: {transaction_id} marked as Authorized (ISO 8583 Code: 00 - Approved)"
        )

    else:
        return (
            f"Error: Unknown action '{query_or_action}'. Please select a valid credit card action.\n\n"
            f"[SYSTEM_LOG] Request Rejected | Invalid action: {query_or_action}"
        )

# ----------------- MCP Server Entry Point -----------------
@mcp.tool()
def handle_credit_card_flow(
    account_number: str,
    card_number: str,
    query_or_action: str,
    transaction_id: str = None,
    security_answer: str = None
) -> str:
    """
    Unified database gateway tool for AIVA Credit Card services. Handles Failed Transactions,
    Blocked Cards, and Fraud Suspicion queries and updates.

    Parameters:
    - account_number: Customer's Wells Fargo Account Number (e.g. '9876543210')
    - card_number: Credit card number ending digits or full number (e.g. '1111')
    - query_or_action: Action to perform:
      - 'get_transactions': Returns transactions history.
      - 'select_transaction': Retrieves details and probable action for a specific transaction (or unblock security question if whole card is blocked).
      - 'request_limit_increase': Temporarily increases limit for a failed transaction.
      - 'unblock_card': Unblocks a blocked credit card (requires security_answer).
      - 'confirm_fraud': Confirms fraud (blocks card, disputes transaction, orders replacement).
      - 'deny_fraud': Clears fraud suspicion (marks transaction as authorized).
    - transaction_id: (Optional) Transaction ID being reviewed.
    - security_answer: (Optional) Answer to unblock a card.
    """
    return execute_banking_logic(
        account_number=account_number,
        card_number=card_number,
        query_or_action=query_or_action,
        transaction_id=transaction_id,
        security_answer=security_answer
    )

# ----------------- FastAPI REST Gateway Endpoint -----------------
@app.post("/api/credit-card")
def api_process_credit_card(request: CreditCardRequest = Body(...)):
    """
    HTTP POST proxy endpoint for Postman testing. Executes the exact same core
    banking logic as the MCP stdio tool.
    """
    try:
        response_text = execute_banking_logic(
            account_number=request.account_number,
            card_number=request.card_number,
            query_or_action=request.query_or_action,
            transaction_id=request.transaction_id,
            security_answer=request.security_answer
        )
        
        # If response starts with "Error:", raise a bad request status
        if response_text.startswith("Error:"):
            raise HTTPException(status_code=400, detail=response_text)
            
        return {
            "status": "success",
            "message": response_text
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Core server error occurred: {str(e)}")

# CLI dispatcher
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--mcp":
        print("Starting AIVA Credit Card MCP Server in STDIO mode...")
        mcp.run()
    else:
        print(f"Starting AIVA Credit Card HTTP REST Gateway for Postman testing on http://{SERVER_HOST}:{SERVER_PORT}...")
        uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
