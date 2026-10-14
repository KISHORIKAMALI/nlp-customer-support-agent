# Knowledge Base Documents for Customer Support System
# Covers: Return Policy, Refund Policy, Cancellation Policy, Warranty Policy,
# Delivery Policy, Payment Policy, Troubleshooting, Product Information, Customer Support/Escalation.

DOCUMENTS = [
    # 1. Return Policy
    {
        "id": "doc_return_01",
        "title": "Standard Return Policy and Eligibility",
        "category": "Return Policy",
        "source": "customer_handbook_2026.pdf#sec2.1",
        "content": (
            "Customers may initiate a return within 30 calendar days of delivery for most items. "
            "To be eligible for a return, the product must be in its original packaging, include all accessories, "
            "manuals, and registration cards, and show no signs of customer abuse. "
            "Electronics such as laptops, tablets, and mobile phones are eligible for return within a 14-day window from the delivery date. "
            "If an electronic item arrives physically damaged or defective out of the box, customers must notify support within 48 hours of delivery. "
            "Damaged items reported after 48 hours but within 14 days will be inspected for accidental vs transit damage before an RMA (Return Merchandise Authorization) is issued."
        )
    },
    {
        "id": "doc_return_02",
        "title": "Return Procedures for Damaged and Defective Products",
        "category": "Return Policy",
        "source": "customer_handbook_2026.pdf#sec2.2",
        "content": (
            "Can I return a damaged laptop? Yes, laptops delivered with transit damage, broken screens, or hardware defects "
            "can be returned for a full replacement or refund under our Damaged On Arrival (DOA) policy within 14 days. "
            "Customers should provide photographic evidence of the parcel and damaged device. Once verified, a prepaid return shipping label "
            "is generated automatically. Non-returnable items include gift cards, downloaded software licenses, and clearance liquidation goods."
        )
    },

    # 2. Refund Policy
    {
        "id": "doc_refund_01",
        "title": "Refund Timelines and Methods",
        "category": "Refund Policy",
        "source": "refund_guidelines_v3.md#timelines",
        "content": (
            "Once a returned item is received at our fulfillment warehouse, it undergoes physical quality inspection within 2 business days. "
            "Upon inspection approval, the refund is initiated automatically to the original payment method. "
            "Credit card and debit card refunds typically take 3 to 5 business days to reflect in the customer's account depending on their banking institution. "
            "UPI and digital wallet refunds take 24 to 48 hours. Direct bank transfers (ACH/NEFT) take 2 to 3 business days. "
            "Store credit refunds are credited instantly upon inspection sign-off."
        )
    },
    {
        "id": "doc_refund_02",
        "title": "Refund Rejections and Exceptions",
        "category": "Refund Policy",
        "source": "refund_guidelines_v3.md#rejections",
        "content": (
            "Why was my refund rejected? Refunds may be rejected for several specific reasons: "
            "1. The item returned was not the genuine product originally shipped (serial number mismatch). "
            "2. The return was initiated outside the valid return window (e.g., past 14 days for laptops or 30 days for general items). "
            "3. The product exhibits physical damage, liquid ingress, or tampering caused by user mishandling rather than transit defect. "
            "4. Required accessories, chargers, or documentation were missing from the return parcel. "
            "5. A previous chargeback or payment dispute was raised with the issuing bank, which locks the merchant transaction. "
            "If a refund is rejected, support provides the detailed inspection report and tracking number for returning the item back to the buyer."
        )
    },

    # 3. Cancellation Policy
    {
        "id": "doc_cancel_01",
        "title": "Order Cancellation Rules and Transit Status",
        "category": "Cancellation Policy",
        "source": "cancellation_rules_2026.md#orders",
        "content": (
            "Orders can be freely cancelled by the customer or support agent as long as the order status is 'Pending', 'Processing', or 'Order Placed'. "
            "Once an order transitions to 'Shipped' or 'In Transit', direct system cancellation is no longer possible because the parcel has been handed over to third-party couriers. "
            "If an order has not arrived and is delayed or in transit, the customer has two options: "
            "(a) Request a courier package recall / return-to-origin, which triggers a refund once carrier confirms intercept, or "
            "(b) Refuse delivery at their doorstep when the carrier arrives. "
            "If a shipment is officially marked as 'Lost in Transit' or severely delayed past guaranteed delivery threshold (>7 business days late), "
            "support can issue an immediate priority cancellation and full refund without waiting for parcel return."
        )
    },

    # 4. Warranty Policy
    {
        "id": "doc_warranty_01",
        "title": "Hardware Warranty Terms and Coverage",
        "category": "Warranty Policy",
        "source": "warranty_terms.pdf#coverage",
        "content": (
            "All new laptops, monitors, and smartphones sold through our store come with a 1-year standard manufacturer limited warranty. "
            "Refurbished electronic goods come with a 6-month certified hardware warranty. "
            "The warranty covers internal component failures, motherboard faults, screen dead-pixels exceeding manufacturer tolerance, and power adapter defects. "
            "The warranty DOES NOT cover accidental liquid spills, drops, screen cracks from user impact, unauthorized opening/repairs, or normal battery wear. "
            "Extended warranty plans (Protection+) cover accidental damage and can be purchased within 30 days of hardware purchase."
        )
    },

    # 5. Delivery Policy
    {
        "id": "doc_delivery_01",
        "title": "Delivery Speeds, Carriers, and Tracking",
        "category": "Delivery Policy",
        "source": "logistics_sla.pdf#delivery",
        "content": (
            "Standard delivery takes 3 to 5 business days across domestic zones. Express shipping guarantees delivery within 1 to 2 business days. "
            "Customers receive an automated SMS and email with a live carrier tracking link as soon as the shipping label is generated. "
            "If tracking has not updated for 72 consecutive hours, our logistics team automatically opens a carrier investigation ticket. "
            "High-value orders (exceeding $500 or equivalent) require an adult signature or one-time delivery OTP verification upon drop-off."
        )
    },

    # 6. Payment Policy
    {
        "id": "doc_payment_01",
        "title": "Accepted Payment Methods and Payment Failure Handling",
        "category": "Payment Policy",
        "source": "payment_gateway_faq.md#billing",
        "content": (
            "We accept major credit cards (Visa, MasterCard, Amex), debit cards, UPI, PayPal, Apple Pay, Google Pay, and Net Banking. "
            "In case a payment is debited from customer account but order confirmation failed ('Payment Pending' / 'Payment Failed'), "
            "the banking gateway will initiate an auto-reversal within 24 to 48 banking hours. "
            "Customers can check the exact transaction status using their payment reference transaction ID (TXN ID)."
        )
    },

    # 7. Troubleshooting
    {
        "id": "doc_troubleshoot_01",
        "title": "Common Hardware and Software Troubleshooting",
        "category": "Troubleshooting",
        "source": "device_troubleshooting_guide.md#laptops",
        "content": (
            "Laptop won't power on: Ensure power adapter LED is lit. Disconnect all peripherals, hold down power button for 30 seconds for hard EC reset, "
            "plug power back in, and press power button once. "
            "Display blank/flickering: Connect an external monitor via HDMI to verify if issue is with LCD panel or GPU. "
            "Wi-Fi disconnection: Reset network stack via Windows Device Manager or run network troubleshooter. "
            "If hardware diagnostics fail, support will guide through warranty repair or RMA replacement process."
        )
    },

    # 8. Product Information
    {
        "id": "doc_product_01",
        "title": "Product Catalog Specifications and Compatibility",
        "category": "Product Information",
        "source": "product_specs_catalog.json",
        "content": (
            "ProBook X15 Laptop (PROD_LP_101): Intel Core i7-13700H, 16GB DDR5 RAM, 1TB NVMe SSD, 15.6 inch 2.8K OLED Display, 72Wh battery. "
            "UltraBook Air 13 (PROD_LP_102): Apple M2 8-core, 8GB Unified RAM, 512GB SSD, 13.6 inch Liquid Retina, fanless silent chassis. "
            "PowerPod 65W GaN Fast Charger (PROD_ACC_201): Dual USB-C + Single USB-A, PD 3.0 / PPS support, compatible with MacBook, Dell, HP, ThinkPad, and smartphones. "
            "NoiseShield Pro Wireless ANC Headphones (PROD_AUD_301): 40mm titanium drivers, 40hr battery life, Bluetooth 5.3, multi-point pairing."
        )
    },

    # 9. Customer Support / Human Escalation Policy
    {
        "id": "doc_escalation_01",
        "title": "Escalation to Human Customer Service Representatives",
        "category": "Customer Support/Escalation",
        "source": "support_sop.pdf#tier2_escalation",
        "content": (
            "When should an inquiry escalate to a human agent? "
            "1. When the customer explicitly requests to speak with a human, representative, live agent, or supervisor. "
            "2. When automated verification detects conflicting records between order management, billing gateway, and carrier logs. "
            "3. High-severity complaints involving damaged goods above $500, suspected fraud, or unresolved refund rejections. "
            "4. When the reasoning confidence score falls below acceptable threshold (< 0.65). "
            "During escalation, the system creates a high-priority ticket, packages the full conversation context and verification summary, "
            "and routes to the Tier-2 Customer Care desk with an estimated wait time of under 3 minutes."
        )
    }
]
