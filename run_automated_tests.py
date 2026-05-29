#!/usr/bin/env python3
"""
AIVA Credit Card MCP Server - Integration Test Runner and HTML Report Generator
"""
import urllib.request
import json
import sys
import os
from datetime import datetime

# Import seed script functions
try:
    import seed_db
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import seed_db

URL = "http://localhost:8000/api/credit-card"

def make_post_request(payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        URL,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            return 200, json.loads(res_body)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        try:
            return e.code, json.loads(err_body)
        except:
            return e.code, {"status": "error", "message": f"HTTP {e.code}: {e.reason}", "raw": err_body}
    except Exception as e:
        return 500, {"status": "error", "message": str(e)}


# ------------------ SVG SEQUENCE DIAGRAMS (Plain Strings) ------------------

SVG_FLOW1 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 640" style="width:100%;height:auto;display:block;">
  <defs>
    <marker id="arr1" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 Z" fill="context-stroke"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1100" height="640" fill="#060914" rx="12"/>
  <pattern id="pg1" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.025)" stroke-width="1"/>
  </pattern>
  <rect width="1100" height="640" fill="url(#pg1)" rx="12"/>

  <!-- Title Banner -->
  <rect x="0" y="0" width="1100" height="44" fill="rgba(209,18,38,0.12)" rx="12"/>
  <rect x="0" y="32" width="1100" height="12" fill="rgba(209,18,38,0.12)"/>
  <text x="550" y="28" text-anchor="middle" fill="#f2a900" font-size="15"
        font-family="Plus Jakarta Sans, sans-serif" font-weight="700" letter-spacing="1">
    AIVA Credit Card MCP - Flow 1: Failed Transaction &amp; Limit Increase
  </text>

  <!-- Lifelines -->
  <line x1="130" y1="120" x2="130" y2="540" stroke="rgba(255,255,255,0.13)" stroke-dasharray="6,5" stroke-width="1.5"/>
  <line x1="390" y1="120" x2="390" y2="540" stroke="rgba(59,130,246,0.3)"  stroke-dasharray="6,5" stroke-width="1.5"/>
  <line x1="650" y1="120" x2="650" y2="540" stroke="rgba(16,185,129,0.3)"  stroke-dasharray="6,5" stroke-width="1.5"/>
  <line x1="920" y1="120" x2="920" y2="540" stroke="rgba(245,158,11,0.3)"  stroke-dasharray="6,5" stroke-width="1.5"/>

  <!-- Actor Headers -->
  <rect x="60" y="52" width="140" height="64" rx="10" fill="#101427" stroke="#d11226" stroke-width="1.5"/>
  <text x="130" y="74" text-anchor="middle" fill="#f1f5f9" font-size="13" font-family="Plus Jakarta Sans,sans-serif" font-weight="700">Caller</text>
  <text x="130" y="92" text-anchor="middle" fill="#94a3b8" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">(Vedant)</text>

  <rect x="310" y="52" width="160" height="64" rx="10" fill="#101427" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="390" y="74" text-anchor="middle" fill="#f1f5f9" font-size="13" font-family="Plus Jakarta Sans,sans-serif" font-weight="700">CrewAI Agent</text>
  <text x="390" y="92" text-anchor="middle" fill="#94a3b8" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">(AIVA Assistant)</text>

  <rect x="572" y="52" width="156" height="64" rx="10" fill="#101427" stroke="#10b981" stroke-width="1.5"/>
  <text x="650" y="74" text-anchor="middle" fill="#f1f5f9" font-size="13" font-family="Plus Jakarta Sans,sans-serif" font-weight="700">MCP Gateway</text>
  <text x="650" y="92" text-anchor="middle" fill="#94a3b8" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">(FastAPI Gateway)</text>

  <rect x="845" y="52" width="150" height="64" rx="10" fill="#101427" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="920" y="74" text-anchor="middle" fill="#f1f5f9" font-size="13" font-family="Plus Jakarta Sans,sans-serif" font-weight="700">MongoDB Atlas</text>
  <text x="920" y="92" text-anchor="middle" fill="#94a3b8" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">(nextgen-creditcards-ivr)</text>

  <!-- Execution bars -->
  <rect x="385" y="135" width="10" height="370" fill="#3b82f6" opacity="0.25" rx="2"/>
  <rect x="645" y="155" width="10" height="330" fill="#10b981" opacity="0.25" rx="2"/>

  <!-- Steps -->
  <text x="22" y="168" fill="#f2a900" font-size="10" font-family="monospace" font-weight="bold">1</text>
  <line x1="130" y1="162" x2="383" y2="162" stroke="#f1f5f9" stroke-width="2" marker-end="url(#arr1)"/>
  <text x="258" y="154" text-anchor="middle" fill="#f1f5f9" font-size="11" font-family="Plus Jakarta Sans,sans-serif">"My watch purchase of $300 failed"</text>

  <line x1="395" y1="190" x2="643" y2="190" stroke="#f2a900" stroke-width="2" marker-end="url(#arr1)"/>
  <text x="519" y="182" text-anchor="middle" fill="#f2a900" font-size="10.5" font-family="monospace">get_transactions("770321003", "7003")</text>

  <line x1="655" y1="210" x2="913" y2="210" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arr1)"/>
  <text x="782" y="202" text-anchor="middle" fill="#3b82f6" font-size="10" font-family="monospace">find_one({account_number: "770321003"})</text>

  <line x1="913" y1="230" x2="657" y2="230" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="5,4" marker-end="url(#arr1)"/>
  <text x="782" y="224" text-anchor="middle" fill="#3b82f6" font-size="10" font-family="monospace">Returns account statement data</text>

  <line x1="643" y1="254" x2="397" y2="254" stroke="#f2a900" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#arr1)"/>
  <text x="519" y="246" text-anchor="middle" fill="#f2a900" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">Statement history (TXN_FAIL_001 failed)</text>

  <text x="22" y="290" fill="#f2a900" font-size="10" font-family="monospace" font-weight="bold">2</text>
  <line x1="383" y1="284" x2="137" y2="284" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="5,4" marker-end="url(#arr1)"/>
  <text x="258" y="276" text-anchor="middle" fill="#cbd5e1" font-size="11" font-family="Plus Jakarta Sans,sans-serif">"Which transaction do you have a doubt on?"</text>

  <line x1="130" y1="310" x2="383" y2="310" stroke="#f1f5f9" stroke-width="2" marker-end="url(#arr1)"/>
  <text x="258" y="302" text-anchor="middle" fill="#f1f5f9" font-size="11" font-family="Plus Jakarta Sans,sans-serif">"The luxury watch one (ID: TXN_FAIL_001)"</text>

  <text x="22" y="340" fill="#f2a900" font-size="10" font-family="monospace" font-weight="bold">3</text>
  <line x1="395" y1="334" x2="643" y2="334" stroke="#f2a900" stroke-width="2" marker-end="url(#arr1)"/>
  <text x="519" y="326" text-anchor="middle" fill="#f2a900" font-size="10.5" font-family="monospace">select_transaction("TXN_FAIL_001")</text>

  <line x1="643" y1="360" x2="397" y2="360" stroke="#f2a900" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#arr1)"/>
  <text x="519" y="352" text-anchor="middle" fill="#f2a900" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">Failed (exceeded limit). Probable Action: temporary increase</text>

  <!-- Branch Block for Happy vs Rejection/Error Path -->
  <rect x="40" y="380" width="1020" height="120" rx="8" fill="rgba(255,255,255,0.01)" stroke="rgba(255,255,255,0.08)" stroke-width="1.5"/>
  <text x="50" y="396" fill="#f2a900" font-size="10" font-family="Plus Jakarta Sans,sans-serif" font-weight="bold">ALT FRAGMENT: CREDIT LIMIT INCREASE RETRY OPTIONS</text>

  <!-- Happy path -->
  <text x="50" y="415" fill="#10b981" font-size="10" font-weight="bold">Option A: Happy Path (Valid Request)</text>
  <line x1="395" y1="430" x2="643" y2="430" stroke="#10b981" stroke-width="2" marker-end="url(#arr1)"/>
  <text x="519" y="422" text-anchor="middle" fill="#10b981" font-size="10" font-family="monospace">request_limit_increase("TXN_FAIL_001")</text>

  <line x1="643" y1="450" x2="397" y2="450" stroke="#10b981" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#arr1)"/>
  <text x="519" y="442" text-anchor="middle" fill="#10b981" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">Success: Credit limit increased to $2,000.00 (Logged in DB)</text>

  <!-- Unhappy/Invalid path -->
  <line x1="40" y1="460" x2="1060" y2="460" stroke="rgba(255,255,255,0.08)" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="50" y="475" fill="#d11226" font-size="10" font-weight="bold">Option B: Invalid Path (Invalid transaction ID e.g. "TXN_FAIL_999")</text>
  <line x1="395" y1="485" x2="643" y2="485" stroke="#d11226" stroke-width="2" marker-end="url(#arr1)"/>
  <text x="519" y="477" text-anchor="middle" fill="#d11226" font-size="10" font-family="monospace">request_limit_increase("TXN_FAIL_999")</text>

  <line x1="643" y1="505" x2="397" y2="505" stroke="#d11226" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#arr1)"/>
  <text x="519" y="497" text-anchor="middle" fill="#d11226" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">Error: Transaction ID was not found in account history</text>
</svg>"""

SVG_FLOW2 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 640" style="width:100%;height:auto;display:block;">
  <defs>
    <marker id="arr2" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 Z" fill="context-stroke"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1100" height="640" fill="#060914" rx="12"/>
  <pattern id="pg2" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.025)" stroke-width="1"/>
  </pattern>
  <rect width="1100" height="640" fill="url(#pg2)" rx="12"/>

  <!-- Title Banner -->
  <rect x="0" y="0" width="1100" height="44" fill="rgba(209,18,38,0.12)" rx="12"/>
  <rect x="0" y="32" width="1100" height="12" fill="rgba(209,18,38,0.12)"/>
  <text x="550" y="28" text-anchor="middle" fill="#f2a900" font-size="15"
        font-family="Plus Jakarta Sans, sans-serif" font-weight="700" letter-spacing="1">
    AIVA Credit Card MCP - Flow 2: Blocked Card Recovery
  </text>

  <!-- Lifelines -->
  <line x1="130" y1="120" x2="130" y2="540" stroke="rgba(255,255,255,0.13)" stroke-dasharray="6,5" stroke-width="1.5"/>
  <line x1="390" y1="120" x2="390" y2="540" stroke="rgba(59,130,246,0.3)"  stroke-dasharray="6,5" stroke-width="1.5"/>
  <line x1="650" y1="120" x2="650" y2="540" stroke="rgba(16,185,129,0.3)"  stroke-dasharray="6,5" stroke-width="1.5"/>
  <line x1="920" y1="120" x2="920" y2="540" stroke="rgba(245,158,11,0.3)"  stroke-dasharray="6,5" stroke-width="1.5"/>

  <!-- Actor Headers -->
  <rect x="60" y="52" width="140" height="64" rx="10" fill="#101427" stroke="#d11226" stroke-width="1.5"/>
  <text x="130" y="74" text-anchor="middle" fill="#f1f5f9" font-size="13" font-family="Plus Jakarta Sans,sans-serif" font-weight="700">Caller</text>
  <text x="130" y="92" text-anchor="middle" fill="#94a3b8" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">(Maria Gonzalez)</text>

  <rect x="310" y="52" width="160" height="64" rx="10" fill="#101427" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="390" y="74" text-anchor="middle" fill="#f1f5f9" font-size="13" font-family="Plus Jakarta Sans,sans-serif" font-weight="700">CrewAI Agent</text>
  <text x="390" y="92" text-anchor="middle" fill="#94a3b8" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">(AIVA Assistant)</text>

  <rect x="572" y="52" width="156" height="64" rx="10" fill="#101427" stroke="#10b981" stroke-width="1.5"/>
  <text x="650" y="74" text-anchor="middle" fill="#f1f5f9" font-size="13" font-family="Plus Jakarta Sans,sans-serif" font-weight="700">MCP Gateway</text>
  <text x="650" y="92" text-anchor="middle" fill="#94a3b8" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">(FastAPI Gateway)</text>

  <rect x="845" y="52" width="150" height="64" rx="10" fill="#101427" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="920" y="74" text-anchor="middle" fill="#f1f5f9" font-size="13" font-family="Plus Jakarta Sans,sans-serif" font-weight="700">MongoDB Atlas</text>
  <text x="920" y="92" text-anchor="middle" fill="#94a3b8" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">(nextgen-creditcards-ivr)</text>

  <!-- Execution bars -->
  <rect x="385" y="135" width="10" height="370" fill="#3b82f6" opacity="0.25" rx="2"/>
  <rect x="645" y="155" width="10" height="330" fill="#10b981" opacity="0.25" rx="2"/>

  <!-- Steps -->
  <text x="22" y="168" fill="#f2a900" font-size="10" font-family="monospace" font-weight="bold">1</text>
  <line x1="130" y1="162" x2="383" y2="162" stroke="#f1f5f9" stroke-width="2" marker-end="url(#arr2)"/>
  <text x="258" y="154" text-anchor="middle" fill="#f1f5f9" font-size="11" font-family="Plus Jakarta Sans,sans-serif">"Why is my card declined?"</text>

  <line x1="395" y1="190" x2="643" y2="190" stroke="#f2a900" stroke-width="2" marker-end="url(#arr2)"/>
  <text x="519" y="182" text-anchor="middle" fill="#f2a900" font-size="10.5" font-family="monospace">select_transaction("+15550102", "8121")</text>

  <line x1="655" y1="210" x2="913" y2="210" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arr2)"/>
  <text x="782" y="202" text-anchor="middle" fill="#3b82f6" font-size="10" font-family="monospace">find_one({account_number: "+15550102"})</text>

  <line x1="913" y1="230" x2="657" y2="230" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="5,4" marker-end="url(#arr2)"/>
  <text x="782" y="224" text-anchor="middle" fill="#3b82f6" font-size="10" font-family="monospace">Returns account status: Blocked</text>

  <line x1="643" y1="254" x2="397" y2="254" stroke="#f2a900" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#arr2)"/>
  <text x="519" y="246" text-anchor="middle" fill="#f2a900" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">Card ending in 8121 is BLOCKED. Prompts: "What was your first pet's name?"</text>

  <text x="22" y="290" fill="#f2a900" font-size="10" font-family="monospace" font-weight="bold">2</text>
  <line x1="383" y1="284" x2="137" y2="284" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="5,4" marker-end="url(#arr2)"/>
  <text x="258" y="276" text-anchor="middle" fill="#cbd5e1" font-size="11" font-family="Plus Jakarta Sans,sans-serif">"To unblock, what was the name of your first pet?"</text>

  <!-- Alt block for Security verification (A=Rocky/Error, B=Buddy/Success) -->
  <rect x="40" y="310" width="1020" height="190" rx="8" fill="rgba(255,255,255,0.01)" stroke="rgba(255,255,255,0.08)" stroke-width="1.5"/>
  <text x="50" y="326" fill="#f2a900" font-size="10" font-family="Plus Jakarta Sans,sans-serif" font-weight="bold">ALT FRAGMENT: SECURITY QUESTION VERIFICATION</text>

  <!-- Unhappy/Invalid answer path -->
  <text x="50" y="345" fill="#d11226" font-size="10" font-weight="bold">Option A: Incorrect Answer (Invalid Answer Rejection)</text>
  <line x1="130" y1="360" x2="383" y2="360" stroke="#f1f5f9" stroke-width="2" marker-end="url(#arr2)"/>
  <text x="258" y="352" text-anchor="middle" fill="#f1f5f9" font-size="11" font-family="Plus Jakarta Sans,sans-serif">Customer says: "Rocky"</text>

  <line x1="395" y1="375" x2="643" y2="375" stroke="#d11226" stroke-width="2" marker-end="url(#arr2)"/>
  <text x="519" y="367" text-anchor="middle" fill="#d11226" font-size="10" font-family="monospace">unblock_card(security_answer="Rocky")</text>

  <line x1="643" y1="400" x2="397" y2="400" stroke="#d11226" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#arr2)"/>
  <text x="519" y="392" text-anchor="middle" fill="#d11226" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">Error: Security verification failed. Card remains BLOCKED (Logged in DB)</text>

  <!-- Happy answer path -->
  <line x1="40" y1="420" x2="1060" y2="420" stroke="rgba(255,255,255,0.08)" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="50" y="435" fill="#10b981" font-size="10" font-weight="bold">Option B: Correct Answer (Happy Path Success)</text>
  <line x1="130" y1="450" x2="383" y2="450" stroke="#f1f5f9" stroke-width="2" marker-end="url(#arr2)"/>
  <text x="258" y="442" text-anchor="middle" fill="#f1f5f9" font-size="11" font-family="Plus Jakarta Sans,sans-serif">Customer says: "Buddy"</text>

  <line x1="395" y1="470" x2="643" y2="470" stroke="#10b981" stroke-width="2" marker-end="url(#arr2)"/>
  <text x="519" y="462" text-anchor="middle" fill="#10b981" font-size="10" font-family="monospace">unblock_card(security_answer="Buddy")</text>

  <line x1="643" y1="490" x2="397" y2="490" stroke="#10b981" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#arr2)"/>
  <text x="519" y="482" text-anchor="middle" fill="#10b981" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">Success: Verification passed. Card status set to ACTIVE (Logged in DB)</text>
</svg>"""

SVG_FLOW3 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 640" style="width:100%;height:auto;display:block;">
  <defs>
    <marker id="arr3" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 Z" fill="context-stroke"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1100" height="640" fill="#060914" rx="12"/>
  <pattern id="pg3" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.025)" stroke-width="1"/>
  </pattern>
  <rect width="1100" height="640" fill="url(#pg3)" rx="12"/>

  <!-- Title Banner -->
  <rect x="0" y="0" width="1100" height="44" fill="rgba(209,18,38,0.12)" rx="12"/>
  <rect x="0" y="32" width="1100" height="12" fill="rgba(209,18,38,0.12)"/>
  <text x="550" y="28" text-anchor="middle" fill="#f2a900" font-size="15"
        font-family="Plus Jakarta Sans, sans-serif" font-weight="700" letter-spacing="1">
    AIVA Credit Card MCP - Flow 3: Fraud Suspicion &amp; Containment
  </text>

  <!-- Lifelines -->
  <line x1="130" y1="120" x2="130" y2="540" stroke="rgba(255,255,255,0.13)" stroke-dasharray="6,5" stroke-width="1.5"/>
  <line x1="390" y1="120" x2="390" y2="540" stroke="rgba(59,130,246,0.3)"  stroke-dasharray="6,5" stroke-width="1.5"/>
  <line x1="650" y1="120" x2="650" y2="540" stroke="rgba(16,185,129,0.3)"  stroke-dasharray="6,5" stroke-width="1.5"/>
  <line x1="920" y1="120" x2="920" y2="540" stroke="rgba(245,158,11,0.3)"  stroke-dasharray="6,5" stroke-width="1.5"/>

  <!-- Actor Headers -->
  <rect x="60" y="52" width="140" height="64" rx="10" fill="#101427" stroke="#d11226" stroke-width="1.5"/>
  <text x="130" y="74" text-anchor="middle" fill="#f1f5f9" font-size="13" font-family="Plus Jakarta Sans,sans-serif" font-weight="700">Caller</text>
  <text x="130" y="92" text-anchor="middle" fill="#94a3b8" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">(Emily Watson)</text>

  <rect x="310" y="52" width="160" height="64" rx="10" fill="#101427" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="390" y="74" text-anchor="middle" fill="#f1f5f9" font-size="13" font-family="Plus Jakarta Sans,sans-serif" font-weight="700">CrewAI Agent</text>
  <text x="390" y="92" text-anchor="middle" fill="#94a3b8" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">(AIVA Assistant)</text>

  <rect x="572" y="52" width="156" height="64" rx="10" fill="#101427" stroke="#10b981" stroke-width="1.5"/>
  <text x="650" y="74" text-anchor="middle" fill="#f1f5f9" font-size="13" font-family="Plus Jakarta Sans,sans-serif" font-weight="700">MCP Gateway</text>
  <text x="650" y="92" text-anchor="middle" fill="#94a3b8" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">(FastAPI Gateway)</text>

  <rect x="845" y="52" width="150" height="64" rx="10" fill="#101427" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="920" y="74" text-anchor="middle" fill="#f1f5f9" font-size="13" font-family="Plus Jakarta Sans,sans-serif" font-weight="700">MongoDB Atlas</text>
  <text x="920" y="92" text-anchor="middle" fill="#94a3b8" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">(nextgen-creditcards-ivr)</text>

  <!-- Execution bars -->
  <rect x="385" y="135" width="10" height="370" fill="#3b82f6" opacity="0.25" rx="2"/>
  <rect x="645" y="155" width="10" height="330" fill="#10b981" opacity="0.25" rx="2"/>

  <!-- Steps -->
  <text x="22" y="168" fill="#f2a900" font-size="10" font-family="monospace" font-weight="bold">1</text>
  <line x1="130" y1="162" x2="383" y2="162" stroke="#f1f5f9" stroke-width="2" marker-end="url(#arr3)"/>
  <text x="258" y="154" text-anchor="middle" fill="#f1f5f9" font-size="11" font-family="Plus Jakarta Sans,sans-serif">"I have a query about a suspicious $2500 charge"</text>

  <line x1="395" y1="190" x2="643" y2="190" stroke="#f2a900" stroke-width="2" marker-end="url(#arr3)"/>
  <text x="519" y="182" text-anchor="middle" fill="#f2a900" font-size="10.5" font-family="monospace">get_transactions("+15550104", "5528")</text>

  <line x1="655" y1="210" x2="913" y2="210" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arr3)"/>
  <text x="782" y="202" text-anchor="middle" fill="#3b82f6" font-size="10" font-family="monospace">find_one({account_number: "+15550104"})</text>

  <line x1="913" y1="230" x2="657" y2="230" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="5,4" marker-end="url(#arr3)"/>
  <text x="782" y="224" text-anchor="middle" fill="#3b82f6" font-size="10" font-family="monospace">Returns account data (TXN_FRAUD_001 is flagged)</text>

  <line x1="643" y1="254" x2="397" y2="254" stroke="#f2a900" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#arr3)"/>
  <text x="519" y="246" text-anchor="middle" fill="#f2a900" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">Recent history (TXN_FRAUD_001 is FLAGGED). Prompts: "Did you make this?"</text>

  <text x="22" y="290" fill="#f2a900" font-size="10" font-family="monospace" font-weight="bold">2</text>
  <line x1="383" y1="284" x2="137" y2="284" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="5,4" marker-end="url(#arr3)"/>
  <text x="258" y="276" text-anchor="middle" fill="#cbd5e1" font-size="11" font-family="Plus Jakarta Sans,sans-serif">"Did you authorize this $2,500.00 charge at Electronics Depot?"</text>

  <!-- Alt block for Fraud Confirmation / Deny -->
  <rect x="40" y="310" width="1020" height="190" rx="8" fill="rgba(255,255,255,0.01)" stroke="rgba(255,255,255,0.08)" stroke-width="1.5"/>
  <text x="50" y="326" fill="#f2a900" font-size="10" font-family="Plus Jakarta Sans,sans-serif" font-weight="bold">ALT FRAGMENT: CUSTOMER RESPONSE TO FRAUD SUSPICION</text>

  <!-- Option A: Confirm Fraud -->
  <text x="50" y="345" fill="#d11226" font-size="10" font-weight="bold">Option A: Confirm Fraud (Fraud Containment Flow)</text>
  <line x1="130" y1="360" x2="383" y2="360" stroke="#f1f5f9" stroke-width="2" marker-end="url(#arr3)"/>
  <text x="258" y="352" text-anchor="middle" fill="#f1f5f9" font-size="11" font-family="Plus Jakarta Sans,sans-serif">"No, I did not make that charge!"</text>

  <line x1="395" y1="375" x2="643" y2="375" stroke="#d11226" stroke-width="2" marker-end="url(#arr3)"/>
  <text x="519" y="367" text-anchor="middle" fill="#d11226" font-size="10" font-family="monospace">confirm_fraud("TXN_FRAUD_001")</text>

  <line x1="643" y1="400" x2="397" y2="400" stroke="#d11226" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#arr3)"/>
  <text x="519" y="392" text-anchor="middle" fill="#d11226" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">Success: Card Blocked, dispute filed, replacement ordered (Logged in DB)</text>

  <!-- Option B: Deny Fraud -->
  <line x1="40" y1="420" x2="1060" y2="420" stroke="rgba(255,255,255,0.08)" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="50" y="435" fill="#10b981" font-size="10" font-weight="bold">Option B: Deny Fraud (Alternate Path - Customer Authorizes)</text>
  <line x1="130" y1="450" x2="383" y2="450" stroke="#f1f5f9" stroke-width="2" marker-end="url(#arr3)"/>
  <text x="258" y="442" text-anchor="middle" fill="#f1f5f9" font-size="11" font-family="Plus Jakarta Sans,sans-serif">"Yes, I authorized that purchase"</text>

  <line x1="395" y1="470" x2="643" y2="470" stroke="#10b981" stroke-width="2" marker-end="url(#arr3)"/>
  <text x="519" y="462" text-anchor="middle" fill="#10b981" font-size="10" font-family="monospace">deny_fraud("TXN_FRAUD_001")</text>

  <line x1="643" y1="490" x2="397" y2="490" stroke="#10b981" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#arr3)"/>
  <text x="519" y="482" text-anchor="middle" fill="#10b981" font-size="10.5" font-family="Plus Jakarta Sans,sans-serif">Success: Fraud flag cleared. Card remains ACTIVE (Logged in DB)</text>
</svg>"""


# ------------------ AUTOMATED TEST RUNNER ------------------

def run_test_suite():
    results = {}
    test_cases_results = []

    def run_tc(name, payload, expected_status, expected_contains=None):
        print(f"Running: {name}...")
        code, res = make_post_request(payload)
        
        passed = True
        failure_reason = ""
        
        if code != expected_status:
            passed = False
            failure_reason = f"Expected HTTP status {expected_status}, got {code}"
        
        if passed and expected_contains:
            res_str = json.dumps(res)
            if expected_contains not in res_str:
                passed = False
                failure_reason = f"Expected text '{expected_contains}' not found in response."
                
        status_str = "PASS" if passed else "FAIL"
        print(f"Result: {status_str} (HTTP {code})")
        if not passed:
            print(f"Reason: {failure_reason}")
            print(f"Response: {json.dumps(res)}\n")
            
        tc_res = {
            "name": name,
            "payload": payload,
            "status": status_str,
            "code": code,
            "response": res,
            "failure_reason": failure_reason
        }
        test_cases_results.append(tc_res)
        return passed, res

    # ------------------ SEED DATABASE ------------------
    print("Step 1: Automatically seeding database for fresh integration test...")
    seed_db.seed_database()
    print("Database successfully seeded!\n")

    # ------------------ FLOW 1: FAILED TRANSACTION ------------------
    print("Step 2: Testing Flow 1 - Failed Transaction (Vedant)")

    payload_1a = {"account_number": "770321003", "card_number": "7003", "query_or_action": "get_transactions"}
    passed, res = run_tc("Flow 1.A: Fetch Statement (Vedant)", payload_1a, 200, "Vedant")
    results["flow1_stepA_req"] = json.dumps(payload_1a, indent=2)
    results["flow1_stepA_res"] = json.dumps(res, indent=2)

    payload_1b = {"account_number": "770321003", "card_number": "7003", "query_or_action": "select_transaction", "transaction_id": "TXN_FAIL_001"}
    passed, res = run_tc("Flow 1.B: Select Failed Transaction TXN_FAIL_001", payload_1b, 200, "Daily Limit Exceeded")
    results["flow1_stepB_req"] = json.dumps(payload_1b, indent=2)
    results["flow1_stepB_res"] = json.dumps(res, indent=2)

    payload_1c = {"account_number": "770321003", "card_number": "7003", "query_or_action": "request_limit_increase", "transaction_id": "TXN_FAIL_001"}
    passed, res = run_tc("Flow 1.C: Request Limit Increase (Vedant)", payload_1c, 200, "limit increase has been approved")
    results["flow1_stepC_req"] = json.dumps(payload_1c, indent=2)
    results["flow1_stepC_res"] = json.dumps(res, indent=2)

    # NEW Flow 1.D: Request daily limit increase on blocked card (expected rejection)
    payload_1d = {"account_number": "+15550102", "card_number": "8121", "query_or_action": "request_limit_increase", "transaction_id": "TXN_MARIA_001"}
    passed, res = run_tc("Flow 1.D (NEW): Limit Increase on Blocked Card (Expected Rejection)", payload_1d, 400, "security hold on this card")

    # ------------------ FLOW 2: BLOCKED CARD ------------------
    print("\nStep 3: Testing Flow 2 - Blocked Card (Maria Gonzalez)")

    payload_2a = {"account_number": "+15550102", "card_number": "8121", "query_or_action": "select_transaction"}
    passed, res = run_tc("Flow 2.A: Status Check on Blocked Card (Maria Gonzalez)", payload_2a, 200, "currently blocked")
    results["flow2_stepA_req"] = json.dumps(payload_2a, indent=2)
    results["flow2_stepA_res"] = json.dumps(res, indent=2)

    payload_2b = {"account_number": "+15550102", "card_number": "8121", "query_or_action": "unblock_card", "security_answer": "Rocky"}
    passed, res = run_tc("Flow 2.B: Unblock with WRONG Answer 'Rocky' (Expected Rejection)", payload_2b, 400, "verification failed")
    results["flow2_stepB_req"] = json.dumps(payload_2b, indent=2)
    results["flow2_stepB_res"] = json.dumps(res, indent=2)

    payload_2c = {"account_number": "+15550102", "card_number": "8121", "query_or_action": "unblock_card", "security_answer": "Buddy"}
    passed, res = run_tc("Flow 2.C: Unblock with CORRECT Answer 'Buddy'", payload_2c, 200, "successfully unblocked")
    results["flow2_stepC_req"] = json.dumps(payload_2c, indent=2)
    results["flow2_stepC_res"] = json.dumps(res, indent=2)

    # NEW Flow 2.D: Sequential 3-Strike Lockout Validation (Re-seeds first to clear Maria Gonzalez's Active card status)
    print("\nStep 3.D: Testing Flow 2 Lockout - sequential 3 wrong answers -> correct rejected")
    seed_db.seed_database()
    
    # Attempt 1 (Wrong)
    p_lock_1 = {"account_number": "+15550102", "card_number": "8121", "query_or_action": "unblock_card", "security_answer": "Max"}
    run_tc("Flow 2.D1: Unblock wrong attempt 1", p_lock_1, 400, "remains blocked")
    # Attempt 2 (Wrong)
    p_lock_2 = {"account_number": "+15550102", "card_number": "8121", "query_or_action": "unblock_card", "security_answer": "Charlie"}
    run_tc("Flow 2.D2: Unblock wrong attempt 2", p_lock_2, 400, "remains blocked")
    # Attempt 3 (Wrong -> Locks out unblocking)
    p_lock_3 = {"account_number": "+15550102", "card_number": "8121", "query_or_action": "unblock_card", "security_answer": "Rocky"}
    run_tc("Flow 2.D3: Unblock wrong attempt 3 (Trigger Lockout)", p_lock_3, 400, "locked due to too many failed attempts")
    # Attempt 4 (Correct -> Must be rejected because of active lockout status!)
    p_lock_4 = {"account_number": "+15550102", "card_number": "8121", "query_or_action": "unblock_card", "security_answer": "Buddy"}
    run_tc("Flow 2.D4: Unblock correct attempt 4 (Verify Lockout Enforced)", p_lock_4, 400, "locked self-service unblocking")

    # ------------------ FLOW 3: FRAUD CONFIRMED ------------------
    print("\nStep 4: Testing Flow 3 - Fraud Suspicion & Containment (Emily Watson)")
    # Re-seed database so Emily Watson's card is active and unresolved again
    seed_db.seed_database()

    payload_3a = {"account_number": "+15550104", "card_number": "5528", "query_or_action": "get_transactions"}
    passed, res = run_tc("Flow 3.A: Fetch Statement (Emily Watson)", payload_3a, 200, "Emily Watson")
    results["flow3_stepA_req"] = json.dumps(payload_3a, indent=2)
    results["flow3_stepA_res"] = json.dumps(res, indent=2)

    payload_3b = {"account_number": "+15550104", "card_number": "5528", "query_or_action": "select_transaction", "transaction_id": "TXN_FRAUD_001"}
    passed, res = run_tc("Flow 3.B: Select Suspicious Transaction TXN_FRAUD_001", payload_3b, 200, "suspicious")
    results["flow3_stepB_req"] = json.dumps(payload_3b, indent=2)
    results["flow3_stepB_res"] = json.dumps(res, indent=2)

    payload_3c = {"account_number": "+15550104", "card_number": "5528", "query_or_action": "confirm_fraud", "transaction_id": "TXN_FRAUD_001"}
    passed, res = run_tc("Flow 3.C: Confirm Fraud & Dispute Transaction", payload_3c, 200, "immediately blocked your card")
    results["flow3_stepC_req"] = json.dumps(payload_3c, indent=2)
    results["flow3_stepC_res"] = json.dumps(res, indent=2)

    # NEW Flow 3.D: Duplicate Dispute Prevention
    payload_3d_dup = {"account_number": "+15550104", "card_number": "5528", "query_or_action": "confirm_fraud", "transaction_id": "TXN_FRAUD_001"}
    run_tc("Flow 3.D (NEW): Duplicate dispute submission (Expected Block)", payload_3d_dup, 200, "already disputed")

    # NEW Flow 3.E: Compromised Card unblocking attempt (Expected Block)
    payload_3e_unb = {"account_number": "+15550104", "card_number": "5528", "query_or_action": "unblock_card", "security_answer": "Buddy"}
    run_tc("Flow 3.E (NEW): Unblock attempt on Stolen Card (Expected Rejection)", payload_3e_unb, 400, "permanently deactivated due to a reported fraud dispute")

    # ------------------ FLOW 4: FRAUD DENIED (RESET STATE FIRST) ------------------
    print("\nStep 5: Testing Flow 3 Alternate - Fraud Denied (Re-seeding Emily Watson's state)")
    seed_db.seed_database() # re-seed to make Emily Watson's card Active and flagged charge unresolved again!
    print("Database successfully re-seeded for alternate flow!")

    payload_3d = {"account_number": "+15550104", "card_number": "5528", "query_or_action": "deny_fraud", "transaction_id": "TXN_FRAUD_001"}
    passed, res = run_tc("Flow 3.D: Deny Fraud & Authorize Transaction (Alternate Path)", payload_3d, 200, "Authorized")
    # Store this response in results so we can display it in the HTML report
    results["flow3_stepD_req"] = json.dumps(payload_3d, indent=2)
    results["flow3_stepD_res"] = json.dumps(res, indent=2)

    # NEW Flow 4.B: Clear fraud alert on non-flagged transaction (Expected Block)
    payload_4b = {"account_number": "770321003", "card_number": "7003", "query_or_action": "deny_fraud", "transaction_id": "TXN_VEDANT_001"}
    run_tc("Flow 4.B (NEW): Clear alert on non-flagged transaction (Expected Rejection)", payload_4b, 400, "already authorized and in a safe status")




    # ------------------ PRINT CONSOLE PASS/FAIL SUMMARY ------------------
    print("\n" + "="*60)
    print("                INTEGRATION TEST RUN SUMMARY")
    print("="*60)
    
    passed_tests = [tc for tc in test_cases_results if tc["status"] == "PASS"]
    failed_tests = [tc for tc in test_cases_results if tc["status"] == "FAIL"]
    
    print(f"\nTotal Run: {len(test_cases_results)} | PASSED: {len(passed_tests)} | FAILED: {len(failed_tests)}")
    
    print("\n[SUCCESS] PASSED TEST CASES:")
    if passed_tests:
        for idx, tc in enumerate(passed_tests, 1):
            print(f"  {idx}. {tc['name']} (HTTP {tc['code']})")
    else:
        print("  None")
        
    print("\n[FAILURE] FAILED TEST CASES:")
    if failed_tests:
        for idx, tc in enumerate(failed_tests, 1):
            print(f"  {idx}. {tc['name']} (HTTP {tc['code']})")
            print(f"     Reason: {tc['failure_reason']}")
    else:
        print("  None - All test cases successfully passed!")
    print("="*60 + "\n")


    # ------------------ GENERATE HTML DOCUMENT ------------------
    print("Step 6: Compiling HTML documentation with actual runtime requests & responses...")
    generate_html_report(results, test_cases_results)
    print("Automated HTML Report updated successfully at integration_docs.html!\n")


def generate_html_report(res, test_cases):
    """
    Generates the integration_docs.html file.
    Uses string concatenation (NOT f-strings) for all parts containing curly braces
    to avoid Python interpreting SVG/CSS/JS text as f-string expressions.
    """

    # ── HELPER: code block pair (request + response side by side)
    def code_pair(req_json, res_json, res_border_color="var(--blue)"):
        return (
            '<div class="pre-grid">'
            '<div class="pre-block">'
            '<div class="pre-block-label">&#9654; Request JSON</div>'
            '<button class="copy-btn" onclick="copyCode(this)">Copy</button>'
            '<pre><code>' + req_json + '</code></pre>'
            '</div>'
            '<div class="pre-block" style="border-left:3px solid ' + res_border_color + '">'
            '<div class="pre-block-label">&#9664; Live Response JSON</div>'
            '<button class="copy-btn" onclick="copyCode(this)">Copy</button>'
            '<pre><code>' + res_json + '</code></pre>'
            '</div>'
            '</div>'
        )

    CSS = """
    :root {
        --bg: #080a13; --card-bg: rgba(16,20,39,0.7); --border: rgba(255,255,255,0.07);
        --red: #d11226; --gold: #f2a900; --blue: #3b82f6;
        --text: #f1f5f9; --muted: #94a3b8; --green: #10b981; --warn: #f59e0b;
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        font-family: 'Plus Jakarta Sans', sans-serif; background: var(--bg); color: var(--text);
        line-height: 1.6; overflow-x: hidden;
        background-image: radial-gradient(circle at 10% 20%, rgba(209,18,38,0.08) 0%, transparent 45%),
                          radial-gradient(circle at 90% 80%, rgba(242,169,0,0.04) 0%, transparent 45%);
    }
    header { background: linear-gradient(135deg,rgba(16,20,39,0.95),rgba(8,10,19,0.98)); border-bottom:1px solid var(--border); padding:3rem 1.5rem; text-align:center; position:relative; }
    header::after { content:''; position:absolute; bottom:0; left:0; width:100%; height:3px; background:linear-gradient(to right,var(--red),var(--gold)); }
    header h1 { font-family:'Outfit',sans-serif; font-size:clamp(1.8rem,4vw,2.8rem); font-weight:800; background:linear-gradient(135deg,#fff 0%,#e2e8f0 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:0.5rem; }
    header p { color:var(--muted); font-size:1.1rem; max-width:700px; margin:0 auto; }
    .badge { background:rgba(209,18,38,0.15); border:1px solid var(--red); color:#ff808b; padding:0.35rem 0.8rem; border-radius:50px; font-size:0.78rem; font-weight:600; display:inline-block; margin-bottom:1rem; text-transform:uppercase; letter-spacing:1px; }
    .container { max-width:1200px; margin:0 auto; padding:3rem 1.5rem; }
    .section-title { font-family:'Outfit',sans-serif; font-size:1.8rem; font-weight:700; margin:2.5rem 0 1.75rem; display:flex; align-items:center; gap:0.75rem; border-bottom:1px solid var(--border); padding-bottom:0.75rem; }
    .section-title::before { content:''; display:inline-block; width:5px; height:28px; background:var(--gold); border-radius:4px; }
    
    .intro-block { background:linear-gradient(135deg,rgba(209,18,38,0.07),rgba(242,169,0,0.03)); border:1px solid rgba(242,169,0,0.18); border-radius:16px; padding:2rem; margin-bottom:2.5rem; }
    .intro-block h3 { font-family:'Outfit',sans-serif; color:var(--gold); margin-bottom:0.75rem; font-size:1.3rem; font-weight:600; }
    .intro-block p { color:#cbd5e1; font-size:1rem; line-height:1.7; }
    
    .grid-3 { display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:1.5rem; margin-bottom:4rem; }
    .card { background:var(--card-bg); border:1px solid var(--border); border-radius:16px; padding:2rem; transition:transform 0.3s,box-shadow 0.3s,border-color 0.3s; position:relative; overflow:hidden; backdrop-filter:blur(10px); }
    .card::before { content:''; position:absolute; top:0; left:0; width:4px; height:100%; border-radius:4px 0 0 4px; }
    .card-failed::before { background:var(--warn); } .card-blocked::before { background:var(--red); } .card-fraud::before { background:var(--green); }
    .card:hover { transform:translateY(-5px); border-color:rgba(255,255,255,0.15); box-shadow:0 12px 30px -5px rgba(0,0,0,0.4); }
    .card-icon { font-size:2rem; margin-bottom:1rem; }
    .card h3 { font-family:'Outfit',sans-serif; font-size:1.25rem; font-weight:600; margin-bottom:0.6rem; }
    .card p { color:var(--muted); font-size:0.92rem; margin-bottom:1.25rem; min-height:48px; }
    .card-meta { background:rgba(255,255,255,0.03); border-radius:10px; padding:0.8rem 1rem; font-size:0.83rem; border:1px solid rgba(255,255,255,0.04); }
    .card-meta div { display:flex; justify-content:space-between; margin-bottom:0.3rem; }
    .card-meta div:last-child { margin-bottom:0; }
    .meta-label { color:var(--muted); font-weight:500; } .meta-val { color:var(--text); font-family:monospace; font-weight:bold; }
    
    .diagram-container { background:var(--card-bg); border:1px solid var(--border); border-radius:16px; padding:2rem; margin-bottom:4rem; backdrop-filter:blur(10px); }
    .diagram-toolbar { display:flex; justify-content:space-between; align-items:center; margin-bottom:1.25rem; background: rgba(255,255,255,0.02); padding: 0.75rem 1.25rem; border-radius: 8px; border: 1px solid var(--border); }
    .diagram-label { font-size:0.85rem; font-weight:700; color:var(--gold); text-transform:uppercase; letter-spacing:1px; }
    .expand-btn { background:rgba(242,169,0,0.12); border:1px solid rgba(242,169,0,0.35); color:var(--gold); padding:0.4rem 1rem; border-radius:8px; font-size:0.85rem; font-weight:600; cursor:pointer; transition:all 0.2s; display:flex; align-items:center; gap:0.4rem; }
    .expand-btn:hover { background:rgba(242,169,0,0.22); border-color:var(--gold); }
    .svg-thumb { width:100%; overflow-x:auto; background:rgba(0,0,0,0.25); border-radius:10px; border:1px dashed rgba(255,255,255,0.08); padding:0.5rem; }
    
    .diag-tab { padding:0.75rem 1.25rem; cursor:pointer; border-bottom:2px solid transparent; font-weight:500; font-size:0.9rem; color:var(--muted); transition:all 0.2s; white-space:nowrap; }
    .diag-tab:hover { color:var(--text); }
    .diag-tab.active { color:var(--gold); border-bottom-color:var(--gold); font-weight:600; }
    .diag-content { display:none; }
    .diag-content.active { display:block; }
    
    .conv-tab { padding:0.75rem 1.25rem; cursor:pointer; border-bottom:2px solid transparent; font-weight:500; font-size:0.9rem; color:var(--muted); transition:all 0.2s; white-space:nowrap; }
    .conv-tab:hover { color:var(--text); }
    .conv-tab.active { color:var(--gold); border-bottom-color:var(--gold); font-weight:600; }
    .conv-content { display:none; }
    .conv-content.active { display:block; }
    
    .timeline { display: flex; flex-direction: column; gap: 1.5rem; }
    .timeline-step { display: flex; flex-direction: column; background: rgba(255,255,255,0.01); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; }
    .timeline-step-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 0.5rem; margin-bottom: 1rem; }
    .timeline-step-num { font-family: monospace; color: var(--gold); font-weight: 700; font-size: 0.8rem; background: rgba(242,169,0,0.1); border: 1px solid var(--gold); padding: 0.15rem 0.5rem; border-radius: 4px; }
    .timeline-step-title { font-family: 'Outfit', sans-serif; font-size: 1.05rem; font-weight: 600; color: var(--text); }
    
    .chat-container { display: flex; flex-direction: column; gap: 1.25rem; }
    .chat-row { display: flex; flex-direction: column; gap: 0.35rem; }
    
    .chat-bubble { padding: 0.85rem 1.25rem; border-radius: 12px; font-size: 0.9rem; line-height: 1.55; max-width: 85%; }
    .chat-bubble-user { background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.25); color: #93c5fd; align-self: flex-start; border-bottom-left-radius: 2px; }
    .chat-bubble-agent { background: rgba(242,169,0,0.06); border: 1px solid rgba(242,169,0,0.2); color: #fde047; align-self: center; text-align: center; border-radius: 20px; font-weight: 500; font-size: 0.85rem; max-width: 95%; padding: 0.6rem 1.25rem; }
    .chat-bubble-mcp { background: rgba(16,185,129,0.06); border: 1px solid rgba(16,185,129,0.2); color: #a7f3d0; align-self: flex-end; border-bottom-right-radius: 2px; width: 85%; font-family: monospace; font-size: 0.82rem; }
    .chat-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.15rem; display: flex; align-items: center; gap: 0.35rem; }
    .chat-label-user { color: var(--blue); align-self: flex-start; }
    .chat-label-agent { color: var(--gold); align-self: center; }
    .chat-label-mcp { color: var(--green); align-self: flex-end; }

    /* ── FULLSCREEN MODAL - pure CSS/JS, no cloneNode ── */
    .modal {
        display: none;
        position: fixed;
        inset: 0;
        z-index: 10000;
        background: rgba(4,6,12,0.98);
        backdrop-filter: blur(25px);
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        overflow-y: auto;
        overflow-x: hidden;
    }
    .modal.open { display: flex; }
    .modal-toolbar {
        position: sticky; top: 0; width: 100%; z-index: 10001;
        background: rgba(8,10,19,0.95); border-bottom:1px solid var(--border);
        padding: 0.85rem 2rem; display: flex; align-items: center;
        justify-content: space-between; backdrop-filter: blur(10px);
        flex-shrink: 0;
    }
    .modal-toolbar-title { font-family:'Outfit',sans-serif; font-size:1.1rem; font-weight:700; color:var(--gold); }
    .modal-toolbar-hints { display:flex; gap:1.5rem; align-items:center; }
    .modal-hint { color:var(--muted); font-size:0.8rem; }
    .modal-close-btn {
        background: rgba(209,18,38,0.15); border: 1px solid var(--red); color:#ff808b;
        font-size: 0.9rem; font-weight: 700; padding: 0.5rem 1.25rem;
        border-radius: 8px; cursor: pointer; transition: all 0.2s; letter-spacing: 0.5px;
    }
    .modal-close-btn:hover { background: var(--red); color: #fff; transform: scale(1.02); }
    
    .modal-svg-area {
        padding: 2rem;
        width: 100%;
        max-width: 1300px;
        margin: auto;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-grow: 1;
    }
    .modal-svg-area svg { width: 100%; height: auto; display: block; max-height: 85vh; }

    .api-section { background:var(--card-bg); border:1px solid var(--border); border-radius:16px; padding:2.5rem; margin-bottom:4rem; backdrop-filter:blur(10px); }
    .endpoint-badge { background:#060914; border:1px solid var(--border); border-left:4px solid var(--green); border-radius:8px; padding:0.9rem 1.25rem; font-family:monospace; font-size:0.95rem; display:flex; align-items:center; gap:0.75rem; margin-bottom:2rem; overflow-x:auto; }
    .method { background:var(--green); color:#061f14; padding:0.2rem 0.7rem; border-radius:4px; font-weight:bold; font-size:0.82rem; }
    .url { color:var(--text); font-weight:bold; }
    
    .tabs { display:flex; border-bottom:1px solid var(--border); margin-bottom:2rem; gap:0.25rem; overflow-x:auto; }
    .tab { padding:0.75rem 1.25rem; cursor:pointer; border-bottom:2px solid transparent; font-weight:500; font-size:0.9rem; color:var(--muted); transition:all 0.2s; white-space:nowrap; }
    .tab:hover { color:var(--text); }
    .tab.active { color:var(--gold); border-bottom-color:var(--gold); font-weight:600; }
    .tab-content { display:none; }
    .tab-content.active { display:block; }
    
    .step-heading { margin-top:2rem; margin-bottom:0.5rem; color:var(--gold); font-size:1.05rem; font-weight:600; display:flex; align-items:center; gap:0.5rem; }
    .step-num { background:rgba(242,169,0,0.15); border:1px solid var(--gold); color:var(--gold); width:24px; height:24px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.72rem; font-weight:bold; }
    .step-desc { font-size:0.9rem; color:var(--muted); margin-bottom:0.75rem; }
    
    .pre-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(380px,1fr)); gap:1rem; margin-bottom:1.75rem; }
    @media (max-width:800px) { .pre-grid { grid-template-columns:1fr; } }
    .pre-block { position:relative; background:#03050c; border:1px solid var(--border); border-radius:12px; padding:1.25rem; overflow-x:auto; }
    .pre-block-label { font-size:0.75rem; color:var(--muted); margin-bottom:0.4rem; text-transform:uppercase; font-weight:700; letter-spacing:0.5px; }
    pre { margin:0; font-family:'Fira Code','Courier New',monospace; font-size:0.78rem; }
    code { display:block; white-space:pre; }
    .copy-btn { position:absolute; top:0.7rem; right:0.7rem; background:rgba(255,255,255,0.04); border:1px solid var(--border); color:var(--muted); padding:0.2rem 0.5rem; border-radius:4px; cursor:pointer; font-size:0.72rem; transition:all 0.2s; }
    .copy-btn:hover { background:rgba(255,255,255,0.08); color:var(--text); }
    
    .kt-card { background:rgba(255,255,255,0.01); border:1px solid var(--border); border-radius:16px; padding:2.5rem; margin-bottom:1.5rem; }
    .kt-card h3 { font-family:'Outfit',sans-serif; color:var(--gold); font-size:1.2rem; margin-bottom:1.25rem; }
    ol { padding-left:1.5rem; margin-bottom:1.5rem; }
    ol li { margin-bottom:0.5rem; color:var(--muted); }
    ol li strong { color:var(--text); }
    .code-line { display:block; background:#02040a; border-radius:6px; padding:0.5rem 0.85rem; font-family:monospace; font-size:0.85rem; margin-top:0.4rem; margin-bottom:0.75rem; color:var(--green); }
    
    footer { text-align:center; padding:2.5rem 1.5rem; border-top:1px solid var(--border); color:var(--muted); font-size:0.82rem; }
    table { width:100%; border-collapse:collapse; font-size:0.88rem; }
    th { text-align:left; padding:0.6rem 1rem; color:var(--gold); font-family:'Outfit',sans-serif; }
    td { padding:0.6rem 1rem; border-bottom:1px solid rgba(255,255,255,0.04); }
    tr:last-child td { border-bottom:none; }
    """

    JS = """
    function switchTab(evt, tabId) {
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        evt.currentTarget.classList.add('active');
    }
    function switchDiagramTab(evt, tabId) {
        document.querySelectorAll('.diag-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.diag-tab').forEach(el => el.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        evt.currentTarget.classList.add('active');
    }
    function switchConvTab(evt, tabId) {
        document.querySelectorAll('.conv-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.conv-tab').forEach(el => el.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        evt.currentTarget.classList.add('active');
    }
    function copyCode(btn) {
        const code = btn.parentElement.querySelector('pre').textContent.trim();
        const fallback = () => {
            const ta = document.createElement('textarea');
            ta.value = code; document.body.appendChild(ta); ta.select();
            document.execCommand('copy'); document.body.removeChild(ta);
            btn.textContent = '&#10003; Copied';
            setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
        };
        if (navigator.clipboard) {
            navigator.clipboard.writeText(code).then(() => {
                btn.textContent = '&#10003; Copied';
                btn.style.background = 'rgba(16,185,129,0.2)';
                btn.style.borderColor = 'var(--green)';
                setTimeout(() => { btn.textContent = 'Copy'; btn.style.background=''; btn.style.borderColor=''; }, 2000);
            }).catch(fallback);
        } else { fallback(); }
    }
    function openModal(modalId) {
        document.getElementById(modalId).classList.add('open');
        document.body.style.overflow = 'hidden';
    }
    function closeModal(modalId) {
        document.getElementById(modalId).classList.remove('open');
        document.body.style.overflow = '';
    }
    document.addEventListener('keydown', e => { 
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal').forEach(el => el.classList.remove('open'));
            document.body.style.overflow = '';
        }
    });
    """

    # Compute live suite status details
    test_suite_status = "ALL PASSED"
    status_color = "var(--green)"
    status_bg = "rgba(16,185,129,0.15)"
    
    passed_tests_html = []
    failed_tests_html = []
    
    for tc in test_cases:
        badge_style = "background:rgba(16,185,129,0.15); border:1px solid var(--green); color:var(--green);" if tc["status"] == "PASS" else "background:rgba(209,18,38,0.15); border:1px solid var(--red); color:#ff808b;"
        status_symbol = "✓" if tc["status"] == "PASS" else "✗"
        
        row = (
            '<div style="display:flex; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.2); border:1px solid var(--border); border-radius:8px; padding:0.6rem 1rem; font-size:0.88rem; margin-bottom:0.4rem;">'
            '<div style="display:flex; align-items:center; gap:0.75rem;">'
            '<span style="color:' + ("var(--green)" if tc["status"] == "PASS" else "var(--red)") + '; font-weight:bold; font-size:1.1rem;">' + status_symbol + '</span>'
            '<span style="font-weight:500;">' + tc["name"] + '</span>'
            '</div>'
            '<div style="display:flex; align-items:center; gap:1rem;">'
            '<span style="font-family:monospace; color:var(--muted); font-size:0.8rem;">HTTP ' + str(tc["code"]) + '</span>'
            '<span style="padding:0.2rem 0.6rem; border-radius:4px; font-size:0.72rem; font-weight:bold; ' + badge_style + '">' + tc["status"] + '</span>'
            '</div>'
            '</div>'
        )
        
        if tc["status"] == "PASS":
            passed_tests_html.append(row)
        else:
            test_suite_status = "FAILED"
            status_color = "var(--red)"
            status_bg = "rgba(209,18,38,0.15)"
            
            row_with_reason = (
                '<div style="margin-bottom:0.4rem;">' + row + 
                '<div style="background:rgba(209,18,38,0.05); border:1px dashed rgba(209,18,38,0.3); border-radius:0 0 8px 8px; padding:0.5rem 1rem; font-size:0.8rem; color:#ff808b; margin-top:-0.4rem; border-top:none;">'
                '<strong>Failure Reason:</strong> ' + tc["failure_reason"] + 
                '</div></div>'
            )
            failed_tests_html.append(row_with_reason)

    passed_section_content = "".join(passed_tests_html) if passed_tests_html else '<div style="color:var(--muted); font-size:0.88rem; padding: 0.5rem 0;">None</div>'
    failed_section_content = "".join(failed_tests_html) if failed_tests_html else '<div style="color:var(--muted); font-size:0.88rem; padding: 0.5rem 0;">None - All tests passed successfully!</div>'

    execution_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── Build HTML using string concatenation (safe from f-string brace issues) ──
    html_parts = []

    html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AIVA Credit Card MCP Server - Integration &amp; Testing Guide</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>""")
    html_parts.append(CSS)
    html_parts.append("""</style>
</head>
<body>
<header>
  <span class="badge">AIVA IVR Banking Integration Report</span>
  <h1>Credit Card MCP Server</h1>
  <p>Decoupled stateful gateway for Twilio, Whisper, ElevenLabs &amp; CrewAI conversational banking.</p>
</header>
<div class="container">

  <!-- SECTION 1: DEMO SCHEMA -->
  <h2 class="section-title">NextGen Bank Isolated Demo Schema</h2>
  <div class="intro-block">
    <h3>&#128737;&#65039; Live Demonstration Isolation Pattern</h3>
    <p>The database seeds <strong>three distinct customer accounts</strong> formatted identically to real
    <strong>NextGen Bank 10-digit Account Numbers</strong>. Each profile isolates exactly one business flow
    so Failed Transactions, Card Blocks, and Fraud Alerts can be demoed concurrently without state contamination.</p>
  </div>
  <div class="grid-3">
    <div class="card card-failed">
      <div class="card-icon">&#128201;</div>
      <h3>Flow 1 &mdash; Failed Transaction</h3>
      <p>Vedant's $300.00 watch purchase failed (daily limit $1,000 exceeded). AIVA resolves via temporary limit increase.</p>
      <div class="card-meta">
        <div><span class="meta-label">Customer</span><span class="meta-val">Vedant</span></div>
        <div><span class="meta-label">Account No</span><span class="meta-val">770321003</span></div>
        <div><span class="meta-label">Card Ends</span><span class="meta-val">&middot;&middot; 7003</span></div>
        <div><span class="meta-label">Action</span><span class="meta-val">request_limit_increase</span></div>
      </div>
    </div>
    <div class="card card-blocked">
      <div class="card-icon">&#128274;</div>
      <h3>Flow 2 &mdash; Blocked Card</h3>
      <p>Maria Gonzalez's card is Blocked. AIVA verifies his security pet-name question (&quot;Buddy&quot;) and sets card Active.</p>
      <div class="card-meta">
        <div><span class="meta-label">Customer</span><span class="meta-val">Maria Gonzalez</span></div>
        <div><span class="meta-label">Account No</span><span class="meta-val">+15550102</span></div>
        <div><span class="meta-label">Card Ends</span><span class="meta-val">&middot;&middot; 8121</span></div>
        <div><span class="meta-label">Action</span><span class="meta-val">unblock_card</span></div>
      </div>
    </div>
    <div class="card card-fraud">
      <div class="card-icon">&#128680;</div>
      <h3>Flow 3 &mdash; Fraud Suspicion</h3>
      <p>Emily Watson has an unrecognized $2,500.00 charge. AIVA blocks the card, disputes the transaction, orders replacement.</p>
      <div class="card-meta">
        <div><span class="meta-label">Customer</span><span class="meta-val">Emily Watson</span></div>
        <div><span class="meta-label">Account No</span><span class="meta-val">+15550104</span></div>
        <div><span class="meta-label">Card Ends</span><span class="meta-val">&middot;&middot; 5528</span></div>
        <div><span class="meta-label">Action</span><span class="meta-val">confirm_fraud / deny_fraud</span></div>
      </div>
    </div>

  </div>

  <!-- SECTION: CONVERSATIONAL WALKTHROUGH -->
  <h2 class="section-title">Conversational Banking Interaction Walkthrough</h2>
  <div class="api-section">
    <p style="color:var(--muted);margin-bottom:1.5rem;font-size:0.95rem;">
      Review the conversational banking experience step-by-step. Select a scenario tab below to see what the <strong>Customer</strong> says, how the <strong>CrewAI Agent</strong> reasons, and the exact <strong>MCP Server calls and responses</strong> generated in the background.
    </p>
    <div class="tabs" style="border-bottom: 1px solid var(--border); margin-bottom: 1.5rem;">
      <div class="conv-tab active" onclick="switchConvTab(event,'c-failed')">&#128201; Flow 1: Failed Transaction</div>
      <div class="conv-tab" onclick="switchConvTab(event,'c-blocked')">&#128274; Flow 2: Blocked Card</div>
      <div class="conv-tab" onclick="switchConvTab(event,'c-fraud-yes')">&#128680; Flow 3: Fraud Confirmed</div>
      <div class="conv-tab" onclick="switchConvTab(event,'c-fraud-no')">&#10003; Flow 4: Fraud Denied</div>
      
    </div>

    <!-- Conv Tab 1: Failed Transaction -->
    <div id="c-failed" class="conv-content active">
      <div class="timeline">
        <!-- Step 1 -->
        <div class="timeline-step">
          <div class="timeline-step-header">
            <span class="timeline-step-title">Step 1: Check Statement &amp; Fetch Transactions</span>
            <span class="timeline-step-num">Flow 1 - Step A</span>
          </div>
          <div class="chat-container">
            <div class="chat-row">
              <div class="chat-label chat-label-user">🗣️ Twilio IVR Customer (Vedant)</div>
              <div class="chat-bubble chat-bubble-user">"Hello, my card was declined today when I tried to buy a watch. Can you see why it failed?"</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Orchestration Logic</div>
              <div class="chat-bubble chat-bubble-agent">Identifies customer, validates card 7003 on account 770321003. Decides to fetch transactions list to inspect failed purchases. Calls <strong>get_transactions</strong>.</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-mcp">⚙️ MCP Gateway Call &amp; Core Banking Response</div>
              <div class="chat-bubble chat-bubble-mcp">
                <strong>Payload:</strong> {"account_number": "770321003", "card_number": "7003", "query_or_action": "get_transactions"}<br/><br/>
                <strong>Response:</strong> Statement history successfully loaded. Highlights <strong>TXN_FAIL_001</strong> ($300.00 at Luxury Watches Inc) with status <strong>Failed (Daily Limit Exceeded)</strong>. Available Credit is $100.00, Limit is $1,000.00.
              </div>
            </div>
          </div>
        </div>
        
        <!-- Step 2 -->
        <div class="timeline-step">
          <div class="timeline-step-header">
            <span class="timeline-step-title">Step 2: Pinpoint specific failed transaction</span>
            <span class="timeline-step-num">Flow 1 - Step B</span>
          </div>
          <div class="chat-container">
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Voice Response to Customer</div>
              <div class="chat-bubble chat-bubble-agent" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.1); color:var(--text);">"I see a failed transaction of $300.00 at Luxury Watches Inc because it exceeded your daily limit. Is this the charge you are referring to?"</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-user">🗣️ Twilio IVR Customer (Vedant)</div>
              <div class="chat-bubble chat-bubble-user">"Yes, that watch purchase is mine. Why did it decline?"</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Orchestration Logic</div>
              <div class="chat-bubble chat-bubble-agent">Selects the transaction ID to retrieve specific banking recommendations. Calls <strong>select_transaction</strong>.</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-mcp">⚙️ MCP Gateway Call &amp; Core Banking Response</div>
              <div class="chat-bubble chat-bubble-mcp">
                <strong>Payload:</strong> {"account_number": "770321003", "card_number": "7003", "query_or_action": "select_transaction", "transaction_id": "TXN_FAIL_001"}<br/><br/>
                <strong>Response:</strong> Failed transaction query loaded. <strong>Probable Action:</strong> Limit exceeded. Offer temporary credit limit increase to $2,000.00 so the customer can retry.
              </div>
            </div>
          </div>
        </div>

        <!-- Step 3 -->
        <div class="timeline-step">
          <div class="timeline-step-header">
            <span class="timeline-step-title">Step 3: Resolve via credit limit increase</span>
            <span class="timeline-step-num">Flow 1 - Step C</span>
          </div>
          <div class="chat-container">
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Voice Response to Customer</div>
              <div class="chat-bubble chat-bubble-agent" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.1); color:var(--text);">"Since you spent $900.00 earlier, this $300.00 purchase exceeded your daily limit of $1,000.00. I can temporarily increase your credit limit to $2,000.00 for the next 24 hours so you can successfully complete your purchase. Would you like me to do that?"</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-user">🗣️ Twilio IVR Customer (Vedant)</div>
              <div class="chat-bubble chat-bubble-user">"Yes, please do that. That would be perfect."</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Orchestration Logic</div>
              <div class="chat-bubble chat-bubble-agent">Executes credit limit increase by calling <strong>request_limit_increase</strong>.</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-mcp">⚙️ MCP Gateway Call &amp; Core Banking Response</div>
              <div class="chat-bubble chat-bubble-mcp">
                <strong>Payload:</strong> {"account_number": "770321003", "card_number": "7003", "query_or_action": "request_limit_increase", "transaction_id": "TXN_FAIL_001"}<br/><br/>
                <strong>Response:</strong> Credit limit successfully increased to $2,000.00 in database. Action logged in core logs.
              </div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Voice Response to Customer</div>
              <div class="chat-bubble chat-bubble-agent" style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.25); color:var(--green);">"Excellent! Your credit limit has been temporarily increased to $2,000.00. You are all set to retry the transaction now. Is there anything else I can assist you with?"</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Conv Tab 2: Blocked Card -->
    <div id="c-blocked" class="conv-content">
      <div class="timeline">
        <!-- Step 1 -->
        <div class="timeline-step">
          <div class="timeline-step-header">
            <span class="timeline-step-title">Step 1: Detect block status &amp; retrieve security challenge</span>
            <span class="timeline-step-num">Flow 2 - Step A</span>
          </div>
          <div class="chat-container">
            <div class="chat-row">
              <div class="chat-label chat-label-user">🗣️ Twilio IVR Customer (Maria Gonzalez)</div>
              <div class="chat-bubble chat-bubble-user">"Hi, I tried to use my credit card at a gas station, but it declined. Is there a block on my card?"</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Orchestration Logic</div>
              <div class="chat-bubble chat-bubble-agent">Queries card status by selecting statement. Omit transaction_id because card is completely blocked. Calls <strong>select_transaction</strong>.</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-mcp">⚙️ MCP Gateway Call &amp; Core Banking Response</div>
              <div class="chat-bubble chat-bubble-mcp">
                <strong>Payload:</strong> {"account_number": "+15550102", "card_number": "8121", "query_or_action": "select_transaction"}<br/><br/>
                <strong>Response:</strong> Status loaded: <strong>Blocked</strong>. <strong>Probable Action:</strong> Prompt security verification pet question: "What was the name of your first pet?".
              </div>
            </div>
          </div>
        </div>

        <!-- Step 2 -->
        <div class="timeline-step">
          <div class="timeline-step-header">
            <span class="timeline-step-title">Step 2: Challenge security answer (Wrong Answer)</span>
            <span class="timeline-step-num">Flow 2 - Step B</span>
          </div>
          <div class="chat-container">
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Voice Response to Customer</div>
              <div class="chat-bubble chat-bubble-agent" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.1); color:var(--text);">"Yes, I see your credit card ending in 8121 is currently blocked for security reasons. I can unblock it for you right now, but first, I need to verify your identity. Could you please tell me: What was the name of your first pet?"</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-user">🗣️ Twilio IVR Customer (Maria Gonzalez)</div>
              <div class="chat-bubble chat-bubble-user">"Oh, let me think... was it Rocky?"</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Orchestration Logic</div>
              <div class="chat-bubble chat-bubble-agent">Submits answer "Rocky" for database validation. Calls <strong>unblock_card</strong>.</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-mcp">⚙️ MCP Gateway Call &amp; Core Banking Response</div>
              <div class="chat-bubble chat-bubble-mcp">
                <strong>Payload:</strong> {"account_number": "+15550102", "card_number": "8121", "query_or_action": "unblock_card", "security_answer": "Rocky"}<br/><br/>
                <strong>Response:</strong> (HTTP 400) Verification failed. Card remains <strong>Blocked</strong>. FAILED_UNBLOCK_ATTEMPT logged.
              </div>
            </div>
          </div>
        </div>

        <!-- Step 3 -->
        <div class="timeline-step">
          <div class="timeline-step-header">
            <span class="timeline-step-title">Step 3: Try again &amp; unblock card (Correct Answer)</span>
            <span class="timeline-step-num">Flow 2 - Step C</span>
          </div>
          <div class="chat-container">
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Voice Response to Customer</div>
              <div class="chat-bubble chat-bubble-agent" style="background:rgba(209,18,38,0.1); border:1px solid rgba(209,18,38,0.25); color:#ff808b;">"I'm sorry, 'Rocky' doesn't match our records. For your security, the card remains blocked. Would you like to try another name?"</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-user">🗣️ Twilio IVR Customer (Maria Gonzalez)</div>
              <div class="chat-bubble chat-bubble-user">"Ah, my mistake! It was Buddy!"</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Orchestration Logic</div>
              <div class="chat-bubble chat-bubble-agent">Submits answer "Buddy" for database validation. Calls <strong>unblock_card</strong>.</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-mcp">⚙️ MCP Gateway Call &amp; Core Banking Response</div>
              <div class="chat-bubble chat-bubble-mcp">
                <strong>Payload:</strong> {"account_number": "+15550102", "card_number": "8121", "query_or_action": "unblock_card", "security_answer": "Buddy"}<br/><br/>
                <strong>Response:</strong> Verification passed. Card status successfully set to <strong>Active</strong>. CARD_UNBLOCKED logged in database.
              </div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Voice Response to Customer</div>
              <div class="chat-bubble chat-bubble-agent" style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.25); color:var(--green);">"Perfect! That matches our records. Your credit card ending in 8121 is now successfully unblocked and ACTIVE for immediate use. You are good to go!"</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Conv Tab 3: Fraud Confirmed -->
    <div id="c-fraud-yes" class="conv-content">
      <div class="timeline">
        <!-- Step 1 -->
        <div class="timeline-step">
          <div class="timeline-step-header">
            <span class="timeline-step-title">Step 1: Check Statement &amp; Fetch Suspicious Transaction</span>
            <span class="timeline-step-num">Flow 3 - Step A</span>
          </div>
          <div class="chat-container">
            <div class="chat-row">
              <div class="chat-label chat-label-user">🗣️ Twilio IVR Customer (Emily Watson)</div>
              <div class="chat-bubble chat-bubble-user">"I saw a notification for a huge charge of $2,500 that I did not make. Can you look into this?"</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Orchestration Logic</div>
              <div class="chat-bubble chat-bubble-agent">Loads statement history to inspect transactions. Calls <strong>get_transactions</strong>.</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-mcp">⚙️ MCP Gateway Call &amp; Core Banking Response</div>
              <div class="chat-bubble chat-bubble-mcp">
                <strong>Payload:</strong> {"account_number": "+15550104", "card_number": "5528", "query_or_action": "get_transactions"}<br/><br/>
                <strong>Response:</strong> Statement history successfully loaded. Identifies transaction <strong>TXN_FRAUD_001</strong> ($2,500.00 at Electronics Depot) as <strong>flagged_suspicious: true</strong>.
              </div>
            </div>
          </div>
        </div>

        <!-- Step 2 -->
        <div class="timeline-step">
          <div class="timeline-step-header">
            <span class="timeline-step-title">Step 2: Retrieve probable fraud containment actions</span>
            <span class="timeline-step-num">Flow 3 - Step B</span>
          </div>
          <div class="chat-container">
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Voice Response to Customer</div>
              <div class="chat-bubble chat-bubble-agent" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.1); color:var(--text);">"I see a charge for $2,500.00 at Electronics Depot on your statement which our fraud detection systems have flagged as highly suspicious. Let me query the details."</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Orchestration Logic</div>
              <div class="chat-bubble chat-bubble-agent">Queries transaction ID for recommended containment actions. Calls <strong>select_transaction</strong>.</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-mcp">⚙️ MCP Gateway Call &amp; Core Banking Response</div>
              <div class="chat-bubble chat-bubble-mcp">
                <strong>Payload:</strong> {"account_number": "+15550104", "card_number": "5528", "query_or_action": "select_transaction", "transaction_id": "TXN_FRAUD_001"}<br/><br/>
                <strong>Response:</strong> Fraud Suspicion confirmed. <strong>Probable Action:</strong> Ask customer if they authorized. If not, block card, file dispute, order replacement.
              </div>
            </div>
          </div>
        </div>

        <!-- Step 3 -->
        <div class="timeline-step">
          <div class="timeline-step-header">
            <span class="timeline-step-title">Step 3: Confirm Fraud &mdash; Containment &amp; Card Blocking</span>
            <span class="timeline-step-num">Flow 3 - Step C</span>
          </div>
          <div class="chat-container">
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Voice Response to Customer</div>
              <div class="chat-bubble chat-bubble-agent" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.1); color:var(--text);">"Could you please confirm if you authorized this $2,500.00 purchase at Electronics Depot?"</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-user">🗣️ Twilio IVR Customer (Emily Watson)</div>
              <div class="chat-bubble chat-bubble-user">"No, absolutely not! I have never heard of that store! That is fraud!"</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Orchestration Logic</div>
              <div class="chat-bubble chat-bubble-agent">Executes fraud containment. Blocks card, disputes transaction, and orders replacement. Calls <strong>confirm_fraud</strong>.</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-mcp">⚙️ MCP Gateway Call &amp; Core Banking Response</div>
              <div class="chat-bubble chat-bubble-mcp">
                <strong>Payload:</strong> {"account_number": "+15550104", "card_number": "5528", "query_or_action": "confirm_fraud", "transaction_id": "TXN_FRAUD_001"}<br/><br/>
                <strong>Response:</strong> Success! Emily Watson's card status updated to <strong>Blocked</strong>, transaction disputed, replacement card ordered, and FRAUD_CONFIRMED_CARD_BLOCKED logged.
              </div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Voice Response to Customer</div>
              <div class="chat-bubble chat-bubble-agent" style="background:rgba(209,18,38,0.1); border:1px solid rgba(209,18,38,0.25); color:#ff808b;">"Thank you for confirming. I have immediately blocked your card ending in 5528 to prevent any further charges. The $2,500.00 charge is now marked as disputed, and you will not be held responsible. A replacement card is on its way and will arrive in 3-5 business days."</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Conv Tab 4: Fraud Denied -->
    <div id="c-fraud-no" class="conv-content">
      <div class="timeline">
        <!-- Step 1 -->
        <div class="timeline-step">
          <div class="timeline-step-header">
            <span class="timeline-step-title">Step 1: Check Statement &amp; Suspicious Transaction</span>
            <span class="timeline-step-num">Flow 3 Alternate</span>
          </div>
          <div class="chat-container">
            <div class="chat-row">
              <div class="chat-label chat-label-user">🗣️ Twilio IVR Customer (Emily Watson)</div>
              <div class="chat-bubble chat-bubble-user">"I received a text alert about a $2,500 charge on my credit card. Is it blocked?"</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Orchestration Logic</div>
              <div class="chat-bubble chat-bubble-agent">Loads statement history and identifies <strong>TXN_FRAUD_001</strong> flagged suspicious as in Flow 3, Steps 1 and 2. Calls <strong>select_transaction</strong>.</div>
            </div>
          </div>
        </div>

        <!-- Step 2 -->
        <div class="timeline-step">
          <div class="timeline-step-header">
            <span class="timeline-step-title">Step 2: Customer Authorizes Charge &mdash; Clear Alert</span>
            <span class="timeline-step-num">Flow 3.D</span>
          </div>
          <div class="chat-container">
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Voice Response to Customer</div>
              <div class="chat-bubble chat-bubble-agent" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.1); color:var(--text);">"I see a purchase for $2,500.00 at Electronics Depot which has been flagged as suspicious. Did you authorize this charge?"</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-user">🗣️ Twilio IVR Customer (Emily Watson)</div>
              <div class="chat-bubble chat-bubble-user">"Oh yes, that was me! I bought a new editing computer today."</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Orchestration Logic</div>
              <div class="chat-bubble chat-bubble-agent">Clears suspicion flag in database and retains active card status. Calls <strong>deny_fraud</strong>.</div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-mcp">⚙️ MCP Gateway Call &amp; Core Banking Response</div>
              <div class="chat-bubble chat-bubble-mcp">
                <strong>Payload:</strong> {"account_number": "+15550104", "card_number": "5528", "query_or_action": "deny_fraud", "transaction_id": "TXN_FRAUD_001"}<br/><br/>
                <strong>Response:</strong> Success! Emily Watson's transaction marked AUTHORIZED, flagged_suspicious set to false, card remains active, and SUSPICION_CLEARED_BY_CUSTOMER logged.
              </div>
            </div>
            <div class="chat-row">
              <div class="chat-label chat-label-agent">🤖 CrewAI Voice Response to Customer</div>
              <div class="chat-bubble chat-bubble-agent" style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.25); color:var(--green);">"Perfect! Thank you for confirming. I have marked the $2,500.00 purchase as authorized, and cleared the fraud alert. Your card ending in 5528 remains Active and fully ready for use!"</div>
            </div>
          </div>
        </div>
      </div>

""")

    html_parts.append("""  <!-- SECTION 2: SEQUENCE DIAGRAMS -->
  <h2 class="section-title">High-Resolution Interaction Flows</h2>
  <div class="diagram-container">
    <p style="color:var(--muted);margin-bottom:1.5rem;font-size:0.95rem;">
      Toggle below to view interactive scenario-specific sequence diagrams. Click <strong>Expand Full Screen</strong> to maximize for a stunning walkthrough presentation.
    </p>
    <div class="tabs" style="border-bottom: 1px solid var(--border); margin-bottom: 1.5rem;">
      <div class="diag-tab active" onclick="switchDiagramTab(event,'d-failed')">&#128201; Flow 1: Failed Transaction</div>
      <div class="diag-tab" onclick="switchDiagramTab(event,'d-blocked')">&#128274; Flow 2: Blocked Card</div>
      <div class="diag-tab" onclick="switchDiagramTab(event,'d-fraud')">&#128680; Flow 3: Fraud Suspicion</div>
      
    </div>

    <!-- Tab 1: Failed Transaction Diagram -->
    <div id="d-failed" class="diag-content active">
      <div class="diagram-toolbar">
        <span class="diagram-label">&#128208; Failed Transaction &amp; credit limit increase sequence</span>
        <button class="expand-btn" onclick="openModal('diagram-modal-f1')">&#9974; Expand Full Screen</button>
      </div>
      <div class="svg-thumb">""")
    html_parts.append(SVG_FLOW1)
    html_parts.append("""      </div>
    </div>

    <!-- Tab 2: Blocked Card Diagram -->
    <div id="d-blocked" class="diag-content">
      <div class="diagram-toolbar">
        <span class="diagram-label">&#128208; Blocked Card recovery &amp; security verification</span>
        <button class="expand-btn" onclick="openModal('diagram-modal-f2')">&#9974; Expand Full Screen</button>
      </div>
      <div class="svg-thumb">""")
    html_parts.append(SVG_FLOW2)
    html_parts.append("""      </div>
    </div>

    <!-- Tab 3: Fraud Suspicion Diagram -->
    <div id="d-fraud" class="diag-content">
      <div class="diagram-toolbar">
        <span class="diagram-label">&#128208; Fraud suspicion containment or authorization</span>
        <button class="expand-btn" onclick="openModal('diagram-modal-f3')">&#9974; Expand Full Screen</button>
      </div>
      <div class="svg-thumb">""")
    html_parts.append(SVG_FLOW3)
    html_parts.append("""      </div>
    </div>

    </div>
  </div>

  <!-- SECTION 3: POSTMAN TESTING -->
  <h2 class="section-title">Postman HTTP REST Testing Guide</h2>
  <div class="api-section">
    <p style="color:var(--muted);margin-bottom:1.75rem;font-size:0.95rem;">
      FastAPI gateway on port <strong style="color:var(--gold)">8000</strong>.
      All tabs show <em>exact live request/response</em> captured at report-generation time.
    </p>
    <div class="endpoint-badge">
      <span class="method">POST</span>
      <span class="url">http://localhost:8000/api/credit-card</span>
    </div>
    <div class="tabs">
      <div class="tab active" onclick="switchTab(event,'t-failed')">&#128201; 1. Failed Txn</div>
      <div class="tab" onclick="switchTab(event,'t-blocked')">&#128274; 2. Blocked Card</div>
      <div class="tab" onclick="switchTab(event,'t-fraud-yes')">&#128680; 3. Fraud Confirmed</div>
      <div class="tab" onclick="switchTab(event,'t-fraud-no')">&#10003; 4. Fraud Denied</div>
      
    </div>

    <!-- Tab 1: Failed Transaction -->
    <div id="t-failed" class="tab-content active">
      <div class="step-heading"><span class="step-num">A</span>Fetch Transaction Statement</div>
      <p class="step-desc">Retrieve Vedant' transaction list and card status:</p>""")

    html_parts.append(code_pair(res["flow1_stepA_req"], res["flow1_stepA_res"]))

    html_parts.append("""      <div class="step-heading"><span class="step-num">B</span>Select Failed Transaction &mdash; Get Probable Action</div>
      <p class="step-desc">Select TXN_FAIL_001 to get the probable action (limit increase):</p>""")

    html_parts.append(code_pair(res["flow1_stepB_req"], res["flow1_stepB_res"]))

    html_parts.append("""      <div class="step-heading"><span class="step-num">C</span>Execute Temporary Limit Increase</div>
      <p class="step-desc">Increase daily limit to $2,000, log action in DB:</p>""")

    html_parts.append(code_pair(res["flow1_stepC_req"], res["flow1_stepC_res"], "var(--green)"))

    html_parts.append("""    </div>

    <!-- Tab 2: Blocked Card -->
    <div id="t-blocked" class="tab-content">
      <div class="step-heading"><span class="step-num">A</span>Check Blocked Status &amp; Get Security Question</div>
      <p class="step-desc">Card is Blocked &mdash; MCP returns the security question to verify:</p>""")

    html_parts.append(code_pair(res["flow2_stepA_req"], res["flow2_stepA_res"]))

    html_parts.append("""      <div class="step-heading"><span class="step-num">B</span>Verify Security Answer &mdash; Wrong Answer "Rocky" (Rejection)</div>
      <p class="step-desc">Incorrect answer test &mdash; card stays blocked, failed attempt logged:</p>""")

    html_parts.append(code_pair(res["flow2_stepB_req"], res["flow2_stepB_res"], "var(--red)"))

    html_parts.append("""      <div class="step-heading"><span class="step-num">C</span>Verify Security Answer &mdash; Correct Answer "Buddy" (Success)</div>
      <p class="step-desc">Correct answer &mdash; card unblocked, set to Active, action logged in DB:</p>""")

    html_parts.append(code_pair(res["flow2_stepC_req"], res["flow2_stepC_res"], "var(--green)"))

    html_parts.append("""    </div>

    <!-- Tab 3: Fraud Confirmed -->
    <div id="t-fraud-yes" class="tab-content">
      <div class="step-heading"><span class="step-num">A</span>Fetch Transaction Statement</div>
      <p class="step-desc">Query Emily Watson's transactions to surface the suspicious charge:</p>""")

    html_parts.append(code_pair(res["flow3_stepA_req"], res["flow3_stepA_res"]))

    html_parts.append("""      <div class="step-heading"><span class="step-num">B</span>Select Flagged Transaction &mdash; Get Probable Action</div>
      <p class="step-desc">Select TXN_FRAUD_001 &mdash; MCP surfaces fraud action options:</p>""")

    html_parts.append(code_pair(res["flow3_stepB_req"], res["flow3_stepB_res"]))

    html_parts.append("""      <div class="step-heading"><span class="step-num">C</span>Confirm Fraud &mdash; Block Card, Dispute &amp; Order Replacement</div>
      <p class="step-desc">Customer confirms fraud: card blocked immediately, dispute filed, replacement ordered, logged in DB:</p>""")

    html_parts.append(code_pair(res["flow3_stepC_req"], res["flow3_stepC_res"], "var(--green)"))

    html_parts.append("""    </div>

    <!-- Tab 4: Fraud Denied -->
    <div id="t-fraud-no" class="tab-content">
      <div class="step-heading"><span class="step-num">A</span>Fetch Transactions &mdash; Emily Watson's account is resolved</div>
      <p class="step-desc">Deny fraud request was processed on the active transaction:</p>""")

    html_parts.append(code_pair(res["flow3_stepD_req"], res["flow3_stepD_res"], "var(--green)"))

    html_parts.append("""    </div>

  </div>

    <!-- SECTION 4: API ACTION REFERENCE TABLE -->
  <h2 class="section-title">API Action Reference</h2>
  <div class="api-section" style="overflow-x:auto;">
    <table>
      <thead>
        <tr>
          <th>query_or_action</th><th>Required Extra Fields</th><th>Description</th><th>Flow</th>
        </tr>
      </thead>
      <tbody>
        <tr><td style="font-family:monospace;color:var(--blue)">get_transactions</td><td style="color:var(--muted)">account_number, card_number</td><td style="color:var(--muted)">Returns last 5-10 transactions + card summary</td><td>All flows (Step A)</td></tr>
        <tr><td style="font-family:monospace;color:var(--blue)">select_transaction</td><td style="color:var(--muted)">+ transaction_id (or omit if blocked)</td><td style="color:var(--muted)">Details + probable action; or security question if blocked</td><td>All flows (Step B)</td></tr>
        <tr><td style="font-family:monospace;color:var(--warn)">request_limit_increase</td><td style="color:var(--muted)">+ transaction_id (failed txn)</td><td style="color:var(--muted)">Increases daily credit limit to $2,000, logs action</td><td>Flow 1</td></tr>
        <tr><td style="font-family:monospace;color:var(--warn)">unblock_card</td><td style="color:var(--muted)">+ security_answer</td><td style="color:var(--muted)">Validates security answer; sets card Active, logs action</td><td>Flow 2</td></tr>
        <tr><td style="font-family:monospace;color:var(--red)">confirm_fraud</td><td style="color:var(--muted)">+ transaction_id</td><td style="color:var(--muted)">Blocks card, marks txn disputed, orders replacement, logs</td><td>Flow 3a</td></tr>
        <tr><td style="font-family:monospace;color:var(--green)">deny_fraud</td><td style="color:var(--muted)">+ transaction_id</td><td style="color:var(--muted)">Clears fraud flag, card stays Active, logs action</td><td>Flow 3b</td></tr>

      </tbody>
    </table>
  </div>

  <!-- SECTION 5: KNOWLEDGE TRANSFER -->
  <h2 class="section-title">Knowledge Transfer: Execution &amp; Integration</h2>
  <div class="kt-card">
    <h3>Running the Server Locally</h3>
    <ol>
      <li><strong>Navigate to project directory:</strong>
        <span class="code-line">cd C:/Users/bhatn/OneDrive/Documents/Projects/AntiGravity/aiva-creditcard-mcp</span>
      </li>
      <li><strong>Re-seed DB and regenerate this HTML report:</strong>
        <span class="code-line">python run_automated_tests.py</span>
      </li>
      <li><strong>Start HTTP Gateway for Postman/runtime testing:</strong>
        <span class="code-line">python server.py</span>
        API listens at <code style="color:var(--gold)">http://localhost:8000</code> &mdash; Swagger UI at <code style="color:var(--gold)">http://localhost:8000/docs</code>
      </li>
      <li><strong>Start STDIO MCP Mode for CrewAI integration:</strong>
        <span class="code-line">python server.py --mcp</span>
      </li>
    </ol>
    <h3 style="margin-top:2rem;">CrewAI MCP Configuration (mcp_config.json)</h3>
    <div class="pre-block" style="margin-top:0.75rem;">
      <button class="copy-btn" onclick="copyCode(this)">Copy</button>
      <pre><code>{
  "mcpServers": {
    "aiva-creditcard-mcp": {
      "command": "python",
      "args": ["C:/Users/bhatn/OneDrive/Documents/Projects/AntiGravity/aiva-creditcard-mcp/server.py", "--mcp"]
    }
  }
}</code></pre>
    </div>
  </div>

  <!-- SECTION 6: AUTOMATED INTEGRATION TEST REPORT (Moved to Last) -->
  <h2 class="section-title">Automated Integration Test Report</h2>
  <div class="intro-block" style="border-left: 4px solid """)
    html_parts.append(status_color)
    html_parts.append(""";">
    <h3 style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
      <span>&#128308; Live Integration Test Suite Status</span>
      <span class="badge" style="background:""")
    html_parts.append(status_bg)
    html_parts.append("; border:1px solid ")
    html_parts.append(status_color)
    html_parts.append("; color:")
    html_parts.append(status_color)
    html_parts.append("""; margin-bottom:0;">""")
    html_parts.append(test_suite_status)
    html_parts.append("""</span>
    </h3>
    <p style="color:#cbd5e1; font-size:0.95rem; margin-bottom:1.5rem;">
      Integration test suite executed on <strong style="color:var(--gold)">""")
    html_parts.append(execution_timestamp)
    html_parts.append("""</strong>. 
      All core business flows (Failed Transaction, Blocked Card, Fraud containment, and Fraud authorization) were validated on the local FastAPI proxy gateway.
    </p>
    
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(450px, 1fr)); gap:2rem; margin-top:1rem; border-top:1px solid var(--border); padding-top:1.5rem;">
      <div>
        <h4 style="color:var(--red); font-size:0.95rem; margin-bottom:0.75rem; font-family:'Outfit',sans-serif; font-weight:600; display:flex; align-items:center; gap:0.4rem;">
          <span>✗ Failed Test Cases</span>
        </h4>
        <div>""")
    html_parts.append(failed_section_content)
    html_parts.append("""        </div>
      </div>
      <div>
        <h4 style="color:var(--green); font-size:0.95rem; margin-bottom:0.75rem; font-family:'Outfit',sans-serif; font-weight:600; display:flex; align-items:center; gap:0.4rem;">
          <span>✓ Passed Test Cases</span>
        </h4>
        <div>""")
    html_parts.append(passed_section_content)
    html_parts.append("""        </div>
      </div>
    </div>
  </div>

</div><!-- /container -->

<!-- FULLSCREEN MODAL FOR FLOW 1 -->
<div id="diagram-modal-f1" class="modal">
  <div class="modal-toolbar">
    <span class="modal-toolbar-title">&#128208; AIVA Credit Card MCP &mdash; Flow 1: Failed Transaction Diagram</span>
    <div class="modal-toolbar-hints">
      <span class="modal-hint">Press Esc or click Close to exit</span>
      <button class="modal-close-btn" onclick="closeModal('diagram-modal-f1')">&#10005; Close</button>
    </div>
  </div>
  <div class="modal-svg-area">""")
    html_parts.append(SVG_FLOW1)
    html_parts.append("""  </div>
</div>

<!-- FULLSCREEN MODAL FOR FLOW 2 -->
<div id="diagram-modal-f2" class="modal">
  <div class="modal-toolbar">
    <span class="modal-toolbar-title">&#128208; AIVA Credit Card MCP &mdash; Flow 2: Blocked Card Diagram</span>
    <div class="modal-toolbar-hints">
      <span class="modal-hint">Press Esc or click Close to exit</span>
      <button class="modal-close-btn" onclick="closeModal('diagram-modal-f2')">&#10005; Close</button>
    </div>
  </div>
  <div class="modal-svg-area">""")
    html_parts.append(SVG_FLOW2)
    html_parts.append("""  </div>
</div>

<!-- FULLSCREEN MODAL FOR FLOW 3 -->
<div id="diagram-modal-f3" class="modal">
  <div class="modal-toolbar">
    <span class="modal-toolbar-title">&#128208; AIVA Credit Card MCP &mdash; Flow 3: Fraud Suspicion Diagram</span>
    <div class="modal-toolbar-hints">
      <span class="modal-hint">Press Esc or click Close to exit</span>
      <button class="modal-close-btn" onclick="closeModal('diagram-modal-f3')">&#10005; Close</button>
    </div>
  </div>
  <div class="modal-svg-area">""")
    html_parts.append(SVG_FLOW3)
    html_parts.append("""  </div>
</div>

<footer>
  <p>AIVA IVR Credit Card Integration Documentation &copy; 2026. NextGen Bank Credit Card Demo Reference Only.</p>
</footer>
<script>""")
    html_parts.append(JS)
    html_parts.append("""</script>
</body>
</html>
""")

    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "integration_docs.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("".join(html_parts))


if __name__ == "__main__":
    print("=== RUNNING PROGRAMMATIC INTEGRATION & REPORT GENERATION ===")
    run_test_suite()
    print("=== AUTOMATION COMPLETE ===")
