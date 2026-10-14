# Intent Detection, Entity Extraction, and Contextual Query Rewriting

import re
from typing import Dict, Any, List

INTENT_RULES = {
    "human_agent_request": [
        r"\b(human|agent|person|representative|operator|talk to someone|speak to a human|customer service agent)\b"
    ],
    "refund_request": [
        r"\b(refund|refunds|money back|reimbursement|rejected refund|refund status|why was my refund|how long will the refund take)\b"
    ],
    "cancellation": [
        r"\b(cancel|cancellation|stop order|abort order|cancel it)\b"
    ],
    "return_request": [
        r"\b(return|returns|return policy|damaged|defective|send back|rma|return window)\b"
    ],
    "order_status": [
        r"\b(order status|where is my order|track|tracking|has not arrived|hasn't arrived|delivery date|where is it|ord\d+)\b"
    ],
    "payment_problem": [
        r"\b(payment|charged|debited|transaction|txn|card declined|double charge|billing)\b"
    ],
    "product_information": [
        r"\b(spec|specs|specification|price|features|probook|ultrabook|charger|headphones|battery life|display)\b"
    ],
    "technical_problem": [
        r"\b(won't power on|not working|screen blank|broken|crash|troubleshoot|flicker|wifi)\b"
    ],
    "warranty": [
        r"\b(warranty|guarantee|extended warranty|coverage|protection plan)\b"
    ],
    "complaint": [
        r"\b(unacceptable|horrible|angry|dispute|scam|bad service|complaint|escalate)\b"
    ]
}

def detect_intent(query: str) -> Dict[str, Any]:
    """
    Detect user intent using multi-class pattern matching and semantic classification.
    Returns primary intent, confidence score, and detected entities.
    """
    query_lower = query.lower()
    scores = {}

    for intent, patterns in INTENT_RULES.items():
        score = 0
        for pattern in patterns:
            matches = re.findall(pattern, query_lower)
            if matches:
                score += len(matches) * 0.4
        if score > 0:
            scores[intent] = min(round(score + 0.35, 2), 0.98)

    # Extract entities (Order ID, Product ID, Transaction ID)
    order_matches = re.findall(r'\b(ORD\d+)\b', query, re.IGNORECASE)
    txn_matches = re.findall(r'\b(TXN\d+)\b', query, re.IGNORECASE)
    prod_matches = re.findall(r'\b(PROD_[A-Z]+_\d+)\b', query, re.IGNORECASE)

    extracted_entities = {
        "order_id": order_matches[0].upper() if order_matches else None,
        "transaction_id": txn_matches[0].upper() if txn_matches else None,
        "product_id": prod_matches[0].upper() if prod_matches else None
    }

    if not scores:
        primary_intent = "general_inquiry"
        confidence = 0.50
    else:
        # Check human agent priority
        if "human_agent_request" in scores:
            primary_intent = "human_agent_request"
            confidence = scores["human_agent_request"]
        else:
            primary_intent = max(scores, key=scores.get)
            confidence = scores[primary_intent]

    return {
        "primary_intent": primary_intent,
        "confidence": confidence,
        "all_detected_intents": scores,
        "entities": extracted_entities
    }

def rewrite_query_with_context(current_query: str, conversation_history: List[Dict[str, str]]) -> str:
    """
    Reformulate ambiguous or pronoun-heavy follow-up queries using prior dialogue context.
    Example:
    History: "Can I cancel ORD1001 and get a refund?" -> Bot: "..."
    Follow-up: "How long will the refund take?"
    Rewritten: "How long will the refund take for order ORD1001 refund timeline"
    """
    if not conversation_history:
        return current_query

    # Extract context entities from previous turn
    last_user_msg = ""
    last_assistant_msg = ""
    active_order_id = None

    for msg in reversed(conversation_history):
        content = msg.get("content", "")
        ord_found = re.findall(r'\b(ORD\d+)\b', content, re.IGNORECASE)
        if ord_found and not active_order_id:
            active_order_id = ord_found[0].upper()
        if msg.get("role") == "user" and not last_user_msg:
            last_user_msg = content
        elif msg.get("role") == "assistant" and not last_assistant_msg:
            last_assistant_msg = content

    rewritten = current_query.strip()
    
    # Check if query is a follow up referencing 'it', 'refund', 'that', 'order' without an order ID
    pronouns = [r"\bit\b", r"\bthat\b", r"\bthis\b", r"\bthe refund\b", r"\bthe order\b"]
    has_pronoun = any(re.search(p, current_query.lower()) for p in pronouns)

    if active_order_id and (has_pronoun or "refund" in current_query.lower() or "cancel" in current_query.lower()):
        if active_order_id not in rewritten:
            rewritten = f"{rewritten} (context: order {active_order_id})"

    # If follow-up asks "how long will the refund take?", expand with refund timelines and methods
    if "how long" in current_query.lower() and "refund" in current_query.lower():
        rewritten = f"{rewritten} refund processing timeline credit card bank transfer methods"

    return rewritten
