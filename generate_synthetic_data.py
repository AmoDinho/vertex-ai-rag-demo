#!/usr/bin/env python3
"""
Generate synthetic ecommerce reviews with support ticket data for RAG demo.
Creates 5000 realistic records in JSONL format.
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any
import faker

# Initialize Faker for realistic data generation
fake = faker.Faker()

# Product categories and their typical items
PRODUCT_CATEGORIES = {
    "Electronics": [
        ("Wireless Bluetooth Headphones", "High-quality wireless headphones with noise cancellation", 150, 250),
        ("Smartphone", "Latest generation smartphone with advanced camera", 800, 1200),
        ("Laptop", "Professional laptop for work and gaming", 1000, 2500),
        ("Smart Watch", "Fitness tracking smartwatch with health monitoring", 200, 400),
        ("Tablet", "High-resolution tablet for productivity and entertainment", 300, 800),
        ("Gaming Console", "Next-gen gaming console with 4K support", 500, 600),
        ("Wireless Speaker", "Portable Bluetooth speaker with premium sound", 80, 200),
        ("Camera", "Digital camera with professional features", 600, 1500),
    ],
    "Clothing": [
        ("Cotton T-Shirt", "Comfortable 100% cotton t-shirt in various colors", 15, 35),
        ("Denim Jeans", "Classic fit denim jeans with premium quality", 50, 120),
        ("Sneakers", "Comfortable athletic sneakers for daily wear", 80, 180),
        ("Winter Jacket", "Insulated winter jacket for cold weather", 100, 300),
        ("Dress Shirt", "Professional dress shirt for office wear", 40, 90),
        ("Running Shoes", "Performance running shoes with advanced cushioning", 120, 250),
        ("Hoodie", "Cozy pullover hoodie for casual wear", 45, 85),
        ("Formal Suit", "Professional business suit for formal occasions", 300, 800),
    ],
    "Home & Garden": [
        ("Coffee Maker", "Programmable coffee maker with thermal carafe", 80, 200),
        ("Vacuum Cleaner", "Powerful vacuum cleaner for all floor types", 150, 400),
        ("Air Purifier", "HEPA air purifier for clean indoor air", 200, 500),
        ("Garden Tool Set", "Complete gardening tools for outdoor maintenance", 60, 150),
        ("Kitchen Knife Set", "Professional chef knife set with storage block", 100, 300),
        ("Bed Sheets", "Luxury cotton bed sheets for comfortable sleep", 50, 150),
        ("Dining Table", "Elegant dining table for family gatherings", 400, 1200),
        ("Outdoor Grill", "Gas grill for backyard barbecue cooking", 300, 800),
    ],
    "Books": [
        ("Programming Guide", "Comprehensive guide to modern programming", 30, 60),
        ("Fiction Novel", "Best-selling fiction novel by renowned author", 15, 25),
        ("Cookbook", "Collection of gourmet recipes for home cooking", 25, 45),
        ("Self-Help Book", "Personal development and motivation guide", 20, 35),
        ("History Book", "Detailed historical account of significant events", 35, 55),
        ("Science Textbook", "Educational textbook for advanced science topics", 80, 150),
        ("Art Book", "Beautiful collection of artistic works and techniques", 40, 80),
        ("Travel Guide", "Comprehensive travel guide with insider tips", 25, 40),
    ]
}

# Review templates based on rating
REVIEW_TEMPLATES = {
    1: [
        "Absolutely terrible product. {issue}. Would not recommend to anyone.",
        "Worst purchase I've ever made. {issue}. Complete waste of money.",
        "One star is too generous. {issue}. Returning immediately.",
        "Extremely disappointed. {issue}. Poor quality and terrible service.",
    ],
    2: [
        "Not satisfied with this purchase. {issue}. Expected much better quality.",
        "Below average product. {issue}. Wouldn't buy again.",
        "Disappointed with the quality. {issue}. Not worth the price.",
        "Poor experience overall. {issue}. Many better alternatives available.",
    ],
    3: [
        "Average product, nothing special. {issue} but it's acceptable.",
        "Okay for the price. {issue} but does the job.",
        "Middle of the road. {issue} but has some good points too.",
        "Decent enough. {issue} though overall it's fine.",
    ],
    4: [
        "Good product overall. {positive} though {minor_issue}.",
        "Happy with this purchase. {positive} but {minor_issue}.",
        "Solid choice. {positive} despite {minor_issue}.",
        "Pleased with the quality. {positive} although {minor_issue}.",
    ],
    5: [
        "Excellent product! {positive}. Highly recommend!",
        "Perfect! {positive}. Couldn't be happier with this purchase.",
        "Outstanding quality. {positive}. Will definitely buy again.",
        "Amazing! {positive}. Exceeded all my expectations.",
    ]
}

ISSUES = [
    "Arrived damaged", "Poor build quality", "Doesn't work as advertised", 
    "Cheap materials", "Broke after one use", "Shipping took forever",
    "Wrong item received", "Missing parts", "Poor customer service",
    "Overpriced for what you get"
]

POSITIVE_ASPECTS = [
    "Great build quality", "Works perfectly", "Fast shipping", 
    "Excellent customer service", "Good value for money", "Easy to use",
    "High-quality materials", "Better than expected", "Perfect fit",
    "Amazing features"
]

MINOR_ISSUES = [
    "could be slightly cheaper", "shipping was a bit slow", 
    "instructions could be clearer", "packaging could be better",
    "color was slightly different than expected", "setup took some time"
]

# Support ticket scenarios
TICKET_SCENARIOS = {
    "QUERY": {
        "comments": [
            "Customer asking about product compatibility",
            "Question about warranty coverage and terms",
            "Inquiry about product specifications and features",
            "Request for usage instructions and setup guide",
            "Question about product availability and restocking",
        ],
        "duration_range": (15, 120),  # 15 minutes to 2 hours
        "resolutions": ["QUERY_RESOLVED"]
    },
    "REFUND": {
        "comments": [
            "Product not as described, requesting full refund",
            "Item arrived damaged, seeking refund",
            "Changed mind about purchase, want to return",
            "Product quality below expectations, refund requested",
            "Wrong item received, requesting refund",
        ],
        "duration_range": (180, 2880),  # 3 hours to 2 days
        "resolutions": ["REFUND_APPROVED", "REFUND_REJECTED"]
    },
    "REPLACEMENT": {
        "comments": [
            "Product defective on arrival, need replacement",
            "Item stopped working after few days, requesting replacement",
            "Received wrong color/size, need correct replacement",
            "Product has manufacturing defect, replacement needed",
            "Item missing accessories, requesting complete replacement",
        ],
        "duration_range": (240, 4320),  # 4 hours to 3 days
        "resolutions": ["REPLACEMENT_APPROVED", "REPLACEMENT_REJECTED"]
    },
    "DISPUTE": {
        "comments": [
            "Charged twice for same order, disputing duplicate charge",
            "Product description misleading, disputing charges",
            "Service fee not disclosed, raising billing dispute",
            "Unauthorized charge on account, formal dispute",
            "Product return processed but refund not received",
        ],
        "duration_range": (720, 10080),  # 12 hours to 1 week
        "resolutions": ["DISPUTE_RESOLVED", "DISPUTE_REJECTED"]
    }
}

def generate_sku() -> str:
    """Generate a realistic SKU."""
    prefix = random.choice(["PRD", "ITM", "SKU", "ELK", "CLT", "HGD", "BOK"])
    return f"{prefix}-{random.randint(10000, 99999)}"

def generate_review_description(rating: int, product_name: str) -> str:
    """Generate a realistic review based on rating."""
    template = random.choice(REVIEW_TEMPLATES[rating])
    
    if rating <= 2:
        issue = random.choice(ISSUES)
        return template.format(issue=issue)
    elif rating == 3:
        issue = random.choice(ISSUES + MINOR_ISSUES)
        return template.format(issue=issue)
    elif rating == 4:
        positive = random.choice(POSITIVE_ASPECTS)
        minor_issue = random.choice(MINOR_ISSUES)
        return template.format(positive=positive, minor_issue=minor_issue)
    else:  # rating == 5
        positive = random.choice(POSITIVE_ASPECTS)
        return template.format(positive=positive)

def generate_support_ticket_data() -> Dict[str, Any]:
    """Generate realistic support ticket data."""
    ticket_type = random.choice(list(TICKET_SCENARIOS.keys()))
    scenario = TICKET_SCENARIOS[ticket_type]
    
    # Generate ticket number
    ticket_number = f"TKT-{random.randint(100000, 999999)}"
    
    # Generate status based on probability
    status_weights = {"OPEN": 0.1, "IN_PROGRESS": 0.2, "RESOLVED": 0.5, "CLOSED": 0.2}
    status = random.choices(
        list(status_weights.keys()), 
        weights=list(status_weights.values())
    )[0]
    
    # Generate comment
    comment = random.choice(scenario["comments"])
    
    # Generate resolution (only for resolved/closed tickets)
    resolution = None
    if status in ["RESOLVED", "CLOSED"]:
        resolution = random.choice(scenario["resolutions"])
    
    # Generate duration based on status and type
    min_duration, max_duration = scenario["duration_range"]
    if status == "OPEN":
        duration = random.randint(min_duration, min_duration * 3)
    elif status == "IN_PROGRESS":
        duration = random.randint(min_duration * 2, max_duration // 2)
    else:  # RESOLVED or CLOSED
        duration = random.randint(max_duration // 2, max_duration)
    
    return {
        "supportTicketNumber": ticket_number,
        "supportTicketStatus": status,
        "supportTicketComment": comment,
        "supportTicketType": ticket_type,
        "supportTicketResolution": resolution,
        "ticketDuration": duration
    }

def generate_record() -> Dict[str, Any]:
    """Generate a single review record with support ticket data."""
    # Select random product category and item
    category = random.choice(list(PRODUCT_CATEGORIES.keys()))
    product_info = random.choice(PRODUCT_CATEGORIES[category])
    product_name, product_description, min_price, max_price = product_info
    
    # Generate price
    price = round(random.uniform(min_price, max_price), 2)
    
    # Generate rating (weighted towards higher ratings)
    rating_weights = [0.05, 0.1, 0.15, 0.35, 0.35]  # 1-5 star distribution
    rating = random.choices([1, 2, 3, 4, 5], weights=rating_weights)[0]
    
    # Generate dates
    days_ago = random.randint(1, 365)
    date_purchased = fake.date_between(start_date='-1y', end_date='today')
    
    # Generate customer data
    customer_name = fake.name()
    user_id = f"user_{random.randint(10000, 99999)}"
    
    # Generate slug
    slug = product_name.lower().replace(" ", "-").replace("&", "and")
    
    # Generate support ticket data
    ticket_data = generate_support_ticket_data()
    
    return {
        "reviewId": str(uuid.uuid4()),
        "sku": generate_sku(),
        "productName": product_name,
        "productDescription": product_description,
        "price": price,
        "currency": "USD",
        "datePurchased": date_purchased.isoformat(),
        "userId": user_id,
        "customerName": customer_name,
        "slug": slug,
        "reviewDescription": generate_review_description(rating, product_name),
        "reviewRating": rating,
        **ticket_data
    }

def generate_synthetic_dataset(num_records: int = 5000) -> List[Dict[str, Any]]:
    """Generate the complete synthetic dataset."""
    print(f"Generating {num_records} synthetic ecommerce reviews...")
    
    records = []
    for i in range(num_records):
        if (i + 1) % 500 == 0:
            print(f"Generated {i + 1} records...")
        
        record = generate_record()
        records.append(record)
    
    return records

def save_to_jsonl(records: List[Dict[str, Any]], filename: str):
    """Save records to JSONL format."""
    print(f"Saving {len(records)} records to {filename}...")
    
    with open(filename, 'w', encoding='utf-8') as f:
        for record in records:
            json.dump(record, f, ensure_ascii=False)
            f.write('\n')
    
    print(f"Successfully saved {len(records)} records to {filename}")

def main():
    """Main function to generate and save the dataset."""
    # Generate 5000 synthetic records
    records = generate_synthetic_dataset(5000)
    
    # Save to reviews.jsonl
    save_to_jsonl(records, '/Users/amomoloko/github/vertex-ai-rag-demo/reviews.jsonl')
    
    # Print sample record for verification
    print("\nSample record:")
    print(json.dumps(records[0], indent=2))
    
    # Print statistics
    print(f"\nDataset Statistics:")
    print(f"Total records: {len(records)}")
    
    # Rating distribution
    ratings = [r['reviewRating'] for r in records]
    for rating in range(1, 6):
        count = ratings.count(rating)
        print(f"{rating}-star reviews: {count} ({count/len(records)*100:.1f}%)")
    
    # Ticket type distribution
    ticket_types = [r['supportTicketType'] for r in records]
    for ticket_type in ['QUERY', 'REFUND', 'REPLACEMENT', 'DISPUTE']:
        count = ticket_types.count(ticket_type)
        print(f"{ticket_type} tickets: {count} ({count/len(records)*100:.1f}%)")

if __name__ == "__main__":
    main()
