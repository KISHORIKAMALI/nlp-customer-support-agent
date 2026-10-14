# Mock Database & Tools for Customer Support
# Supports order status, payment status, refund status, delivery status,
# product specs, support ticket creation, and human escalation.

import datetime

# Mock Customer & Orders Database
CUSTOMERS_DB = {
    "CUST001": {"name": "Alex Johnson", "email": "alex.j@example.com", "tier": "Gold"},
    "CUST002": {"name": "Priya Sharma", "email": "priya.s@example.com", "tier": "Standard"},
    "CUST003": {"name": "Michael Brown", "email": "mbrown@example.com", "tier": "Platinum"}
}

ORDERS_DB = {
    "ORD1001": {
        "order_id": "ORD1001",
        "customer_id": "CUST001",
        "product_id": "PROD_LP_101",
        "product_name": "ProBook X15 Laptop",
        "order_status": "In Transit",
        "carrier": "FedEx Express",
        "tracking_number": "FDX-9988221",
        "order_date": "2026-10-10",
        "expected_delivery": "2026-10-16",
        "current_location": "Regional Hub - Chicago Sorting Facility",
        "transit_delay": True,
        "transit_delay_reason": "Severe weather conditions at transit corridor. Delayed by 2 days.",
        "cancellation_eligible": False, # Because already in transit; requires recall or doorstep refusal
        "amount": 1299.99,
        "payment_method": "Credit Card"
    },
    "ORD1002": {
        "order_id": "ORD1002",
        "customer_id": "CUST002",
        "product_id": "PROD_LP_102",
        "product_name": "UltraBook Air 13",
        "order_status": "Delivered",
        "carrier": "BlueDart",
        "tracking_number": "BLU-4411009",
        "order_date": "2026-10-01",
        "delivery_date": "2026-10-04",
        "amount": 1099.00,
        "payment_method": "UPI",
        "cancellation_eligible": False
    },
    "ORD1003": {
        "order_id": "ORD1003",
        "customer_id": "CUST001",
        "product_id": "PROD_ACC_201",
        "product_name": "PowerPod 65W GaN Fast Charger",
        "order_status": "Processing",
        "carrier": "Pending Allocation",
        "tracking_number": None,
        "order_date": "2026-10-13",
        "expected_delivery": "2026-10-18",
        "amount": 49.99,
        "payment_method": "Credit Card",
        "cancellation_eligible": True # Not yet shipped
    },
    "ORD1004": {
        "order_id": "ORD1004",
        "customer_id": "CUST003",
        "product_id": "PROD_AUD_301",
        "product_name": "NoiseShield Pro Wireless ANC Headphones",
        "order_status": "Return Initiated",
        "refund_status": "Rejected",
        "refund_rejection_reason": "Inspection failed: Missing original charging cable and serial number on headphone chassis did not match warranty registration card.",
        "amount": 199.99,
        "order_date": "2026-09-20",
        "return_received_date": "2026-10-08",
        "cancellation_eligible": False
    }
}

PAYMENTS_DB = {
    "TXN9001": {
        "transaction_id": "TXN9001",
        "order_id": "ORD1001",
        "amount": 1299.99,
        "status": "Successful",
        "gateway": "Stripe",
        "payment_method": "Visa ending in 4242",
        "timestamp": "2026-10-10 14:22:10"
    },
    "TXN9002": {
        "transaction_id": "TXN9002",
        "order_id": "ORD1004",
        "amount": 199.99,
        "status": "Refund Denied",
        "gateway": "PayPal",
        "payment_method": "PayPal Balance",
        "rejection_code": "INSPECTION_MISMATCH",
        "timestamp": "2026-10-09 11:05:40"
    }
}

PRODUCTS_DB = {
    "PROD_LP_101": {
        "product_id": "PROD_LP_101",
        "name": "ProBook X15 Laptop",
        "category": "Laptops",
        "price": 1299.99,
        "specs": "Intel Core i7-13700H, 16GB DDR5 RAM, 1TB SSD, 15.6 inch OLED 120Hz display",
        "warranty": "1 Year Standard Manufacturer Warranty",
        "return_window_days": 14
    },
    "PROD_LP_102": {
        "product_id": "PROD_LP_102",
        "name": "UltraBook Air 13",
        "category": "Laptops",
        "price": 1099.00,
        "specs": "Apple M2 8-core CPU, 8GB Unified Memory, 512GB SSD, 13.6-inch Retina",
        "warranty": "1 Year Standard Hardware Warranty",
        "return_window_days": 14
    },
    "PROD_ACC_201": {
        "product_id": "PROD_ACC_201",
        "name": "PowerPod 65W GaN Fast Charger",
        "category": "Accessories",
        "price": 49.99,
        "specs": "65W USB-C PD 3.0 / PPS, 2x USB-C + 1x USB-A ports, Foldable plug",
        "warranty": "2 Years Replacement Warranty",
        "return_window_days": 30
    },
    "PROD_AUD_301": {
        "product_id": "PROD_AUD_301",
        "name": "NoiseShield Pro Wireless ANC Headphones",
        "category": "Audio",
        "price": 199.99,
        "specs": "Active Noise Cancellation, 40hr Battery, Hi-Res LDAC, Multipoint Bluetooth",
        "warranty": "1 Year Warranty",
        "return_window_days": 30
    }
}

SUPPORT_TICKETS = []
ESCALATIONS = []


# ================= TOOL DEFINITIONS ================= #

def get_order_status(order_id: str) -> dict:
    """Fetch status, transit state, dates and eligibility for a given order ID."""
    order_id = order_id.strip().upper()
    if order_id in ORDERS_DB:
        order = ORDERS_DB[order_id]
        return {
            "success": True,
            "order_id": order["order_id"],
            "product_name": order["product_name"],
            "order_status": order["order_status"],
            "carrier": order.get("carrier"),
            "tracking_number": order.get("tracking_number"),
            "expected_delivery": order.get("expected_delivery"),
            "current_location": order.get("current_location"),
            "transit_delay": order.get("transit_delay", False),
            "transit_delay_reason": order.get("transit_delay_reason"),
            "cancellation_eligible": order.get("cancellation_eligible", False)
        }
    return {
        "success": False,
        "error": f"Order ID '{order_id}' was not found in the order management system. Available test IDs: ORD1001, ORD1002, ORD1003, ORD1004."
    }

def get_payment_status(transaction_id: str) -> dict:
    """Check payment gateway transaction status."""
    transaction_id = transaction_id.strip().upper()
    if transaction_id in PAYMENTS_DB:
        txn = PAYMENTS_DB[transaction_id]
        return {
            "success": True,
            "transaction_id": txn["transaction_id"],
            "order_id": txn["order_id"],
            "amount": txn["amount"],
            "status": txn["status"],
            "payment_method": txn["payment_method"],
            "timestamp": txn["timestamp"]
        }
    return {
        "success": False,
        "error": f"Transaction ID '{transaction_id}' not found."
    }

def get_refund_status(order_id: str) -> dict:
    """Retrieve refund progress, amount, and reasons if rejected."""
    order_id = order_id.strip().upper()
    # Default to checking ORD1004 if customer is inquiring about rejection without ID
    if order_id not in ORDERS_DB:
        # Check if there is an active refund in the system
        for oid, ord_data in ORDERS_DB.items():
            if ord_data.get("refund_status"):
                order_id = oid
                break

    if order_id in ORDERS_DB:
        order = ORDERS_DB[order_id]
        status = order.get("refund_status", "No refund initiated")
        reason = order.get("refund_rejection_reason", "N/A")
        return {
            "success": True,
            "order_id": order["order_id"],
            "product_name": order["product_name"],
            "amount": order["amount"],
            "refund_status": status,
            "rejection_reason": reason,
            "action_required": "Contact customer support with proof of original accessories or request a secondary reinspection." if status == "Rejected" else None
        }
    return {
        "success": False,
        "error": f"No refund records found for order ID '{order_id}'."
    }

def get_delivery_status(order_id: str) -> dict:
    """Retrieve live courier shipping and transit telematics."""
    order_id = order_id.strip().upper()
    if order_id in ORDERS_DB:
        order = ORDERS_DB[order_id]
        return {
            "success": True,
            "order_id": order["order_id"],
            "carrier": order.get("carrier"),
            "tracking_number": order.get("tracking_number"),
            "order_status": order.get("order_status"),
            "current_location": order.get("current_location", "Warehouse facility"),
            "transit_delay": order.get("transit_delay", False),
            "transit_delay_reason": order.get("transit_delay_reason", "None"),
            "expected_delivery": order.get("expected_delivery")
        }
    return {
        "success": False,
        "error": f"Delivery records not found for order '{order_id}'."
    }

def get_product_information(product_id_or_keyword: str) -> dict:
    """Fetch product specifications, return windows and warranty info."""
    query = product_id_or_keyword.strip().upper()
    if query in PRODUCTS_DB:
        return {"success": True, "product": PRODUCTS_DB[query]}
    # Search by keyword match
    for pid, pdata in PRODUCTS_DB.items():
        if query.lower() in pdata["name"].lower() or query.lower() in pdata["category"].lower():
            return {"success": True, "product": pdata}
    return {
        "success": False,
        "error": f"Product '{product_id_or_keyword}' not found in catalog."
    }

def create_support_ticket(order_id: str = None, issue_summary: str = "", customer_email: str = "customer@example.com", priority: str = "Medium") -> dict:
    """Create a tracked customer support ticket in CRM."""
    ticket_id = f"TCK-{len(SUPPORT_TICKETS) + 101}"
    ticket = {
        "ticket_id": ticket_id,
        "order_id": order_id,
        "issue_summary": issue_summary,
        "customer_email": customer_email,
        "priority": priority,
        "status": "Open",
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    SUPPORT_TICKETS.append(ticket)
    return {
        "success": True,
        "ticket_id": ticket_id,
        "status": "Created",
        "message": f"Support ticket {ticket_id} logged successfully with priority '{priority}'."
    }

def request_human_agent(reason: str, context_summary: str = "", order_id: str = None) -> dict:
    """Escalate customer session to a live human representative."""
    escalation_id = f"ESC-{len(ESCALATIONS) + 501}"
    escalation = {
        "escalation_id": escalation_id,
        "order_id": order_id,
        "reason": reason,
        "context_summary": context_summary,
        "agent_team": "Tier-2 Human Escalation Desk",
        "estimated_wait_time": "2 to 3 minutes",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    ESCALATIONS.append(escalation)
    return {
        "success": True,
        "escalated": True,
        "escalation_id": escalation_id,
        "reason": reason,
        "estimated_wait_time": "2 to 3 minutes",
        "message": f"Transferring to a human customer care specialist (Escalation ID: {escalation_id}). Estimated wait: 2-3 mins."
    }

ALL_TOOLS = {
    "get_order_status": get_order_status,
    "get_payment_status": get_payment_status,
    "get_refund_status": get_refund_status,
    "get_delivery_status": get_delivery_status,
    "get_product_information": get_product_information,
    "create_support_ticket": create_support_ticket,
    "request_human_agent": request_human_agent
}
