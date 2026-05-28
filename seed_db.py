#!/usr/bin/env python3
import sys
import os
from datetime import datetime, timedelta
import pymongo
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME", "Veda_Rituals")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "wf-creditcards-ivr")

if not MONGO_URI:
    print("ERROR: MONGO_URI environment variable not set in .env file.", file=sys.stderr)
    sys.exit(1)

def get_iso_date(days_offset=0, hours_offset=0):
    dt = datetime.now() - timedelta(days=days_offset, hours=hours_offset)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def seed_database():
    print(f"Connecting to MongoDB cluster...")
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        # Verify connectivity
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"ERROR: Failed to connect to MongoDB: {e}", file=sys.stderr)
        sys.exit(1)
        
    collection = db[COLLECTION_NAME]
    
    print(f"Dropping existing collection '{COLLECTION_NAME}' if it exists...")
    collection.drop()
    
    # 1. Failed Transaction Flow (Sarah Jenkins)
    # Account: 10-digit Wells Fargo account number: 9876543210
    # Card ending in 1111
    account_1 = {
        "account_number": "9876543210",
        "customer_name": "Sarah Jenkins",
        "phone_number": "+14155551111",
        "card_details": {
            "card_number_full": "4111-2222-3333-1111",
            "card_number_masked": "1111",
            "status": "Active",
            "credit_limit": 1000.00,
            "daily_spent": 900.00,
            "available_balance": 100.00,
            "expiry_date": "10/29",
            "security_question": "What was the name of your first pet?",
            "security_answer": "Buddy"
        },
        "transactions": [
            {
                "transaction_id": "TXN_FAIL_001",
                "amount": 300.00,
                "merchant": "Luxury Watches Inc",
                "date": get_iso_date(days_offset=0, hours_offset=1),
                "status": "Failed",
                "failure_reason": "Daily Limit Exceeded",
                "flagged_suspicious": False,
                "is_disputed": False,
                "category": "Luxury & Retail",
                "auth_code": None
            },
            {
                "transaction_id": "TXN_SARAH_001",
                "amount": 900.00,
                "merchant": "Best Buy Stores",
                "date": get_iso_date(days_offset=0, hours_offset=4),
                "status": "Success",
                "failure_reason": None,
                "flagged_suspicious": False,
                "is_disputed": False,
                "category": "Electronics",
                "auth_code": "AU_984710"
            },
            {
                "transaction_id": "TXN_SARAH_002",
                "amount": 42.50,
                "merchant": "Starbucks Coffee",
                "date": get_iso_date(days_offset=1),
                "status": "Success",
                "failure_reason": None,
                "flagged_suspicious": False,
                "is_disputed": False,
                "category": "Food & Dining",
                "auth_code": "AU_128394"
            },
            {
                "transaction_id": "TXN_SARAH_003",
                "amount": 120.00,
                "merchant": "Target Stores",
                "date": get_iso_date(days_offset=2),
                "status": "Success",
                "failure_reason": None,
                "flagged_suspicious": False,
                "is_disputed": False,
                "category": "Shopping",
                "auth_code": "AU_529104"
            }
        ],
        "action_logs": []
    }

    # 2. Blocked Card Flow (Michael Chen)
    # Account: 10-digit Wells Fargo account number: 5432109876
    # Card ending in 2222
    account_2 = {
        "account_number": "5432109876",
        "customer_name": "Michael Chen",
        "phone_number": "+14155552222",
        "card_details": {
            "card_number_full": "4111-2222-3333-2222",
            "card_number_masked": "2222",
            "status": "Blocked",
            "credit_limit": 5000.00,
            "daily_spent": 150.00,
            "available_balance": 4850.00,
            "expiry_date": "04/28",
            "security_question": "What was the name of your first pet?",
            "security_answer": "Buddy"
        },
        "transactions": [
            {
                "transaction_id": "TXN_MIKE_001",
                "amount": 150.00,
                "merchant": "Chevron Gas Station",
                "date": get_iso_date(days_offset=1),
                "status": "Success",
                "failure_reason": None,
                "flagged_suspicious": False,
                "is_disputed": False,
                "category": "Gas",
                "auth_code": "AU_837194"
            },
            {
                "transaction_id": "TXN_MIKE_002",
                "amount": 25.40,
                "merchant": "Whole Foods Market",
                "date": get_iso_date(days_offset=2),
                "status": "Success",
                "failure_reason": None,
                "flagged_suspicious": False,
                "is_disputed": False,
                "category": "Grocery",
                "auth_code": "AU_529183"
            }
        ],
        "action_logs": []
    }

    # 3. Fraud Suspicion Flow (Elena Rostova)
    # Account: 10-digit Wells Fargo account number: 8765432109
    # Card ending in 3333
    account_3 = {
        "account_number": "8765432109",
        "customer_name": "Elena Rostova",
        "phone_number": "+14155553333",
        "card_details": {
            "card_number_full": "4111-2222-3333-3333",
            "card_number_masked": "3333",
            "status": "Active",
            "credit_limit": 15000.00,
            "daily_spent": 2500.00,
            "available_balance": 12500.00,
            "expiry_date": "12/28",
            "security_question": "What was the name of your first pet?",
            "security_answer": "Buddy"
        },
        "transactions": [
            {
                "transaction_id": "TXN_FRAUD_001",
                "amount": 2500.00,
                "merchant": "Electronics Depot",
                "date": get_iso_date(days_offset=0, hours_offset=2),
                "status": "Success",
                "failure_reason": None,
                "flagged_suspicious": True,
                "is_disputed": False,
                "category": "Electronics",
                "auth_code": "AU_738192"
            },
            {
                "transaction_id": "TXN_ELENA_001",
                "amount": 45.00,
                "merchant": "Uber Trips",
                "date": get_iso_date(days_offset=1),
                "status": "Success",
                "failure_reason": None,
                "flagged_suspicious": False,
                "is_disputed": False,
                "category": "Transportation",
                "auth_code": "AU_481029"
            },
            {
                "transaction_id": "TXN_ELENA_002",
                "amount": 89.20,
                "merchant": "Amazon.com",
                "date": get_iso_date(days_offset=3),
                "status": "Success",
                "failure_reason": None,
                "flagged_suspicious": False,
                "is_disputed": False,
                "category": "Shopping",
                "auth_code": "AU_392810"
            }
        ],
        "action_logs": []
    }

    print("Inserting mock customer account records...")
    result = collection.insert_many([account_1, account_2, account_3])
    print(f"Successfully seeded {len(result.inserted_ids)} records in '{DB_NAME}.{COLLECTION_NAME}'!")
    
    # Verify by printing seeded records
    print("\nVerified records in collection:")
    for doc in collection.find():
        print(f"- Customer: {doc['customer_name']} | Account No: {doc['account_number']} | Card Masked: {doc['card_details']['card_number_masked']} | Status: {doc['card_details']['status']}")

if __name__ == "__main__":
    seed_database()
