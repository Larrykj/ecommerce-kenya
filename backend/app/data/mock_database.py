"""
Mock Database with Real Product Data
Provides realistic data for development and deployment without external dependencies
"""
from typing import List, Dict, Optional
from datetime import datetime
import random

# Mock Users Database
MOCK_USERS = [
    {
        "id": "user_001",
        "email": "john@example.com",
        "username": "john_doe",
        "full_name": "John Doe",
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyK5vGpW1pSa",  # password: demo123
        "phone_number": "254712345678",
        "county": "Nairobi",
        "city": "Westlands",
        "preferred_language": "en",
        "preferred_categories": ["electronics", "fashion"],
        "is_active": True,
        "is_verified": True,
        "created_at": "2024-01-15T10:00:00Z"
    },
    {
        "id": "user_002",
        "email": "mary@example.com",
        "username": "mary_smith",
        "full_name": "Mary Smith",
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyK5vGpW1pSa",
        "phone_number": "254723456789",
        "county": "Mombasa",
        "city": "Mombasa",
        "preferred_language": "sw",
        "preferred_categories": ["beauty", "home"],
        "is_active": True,
        "is_verified": True,
        "created_at": "2024-02-01T14:30:00Z"
    }
]

# Mock Products Database - Real Kenyan E-commerce Products
MOCK_PRODUCTS = [
    # Electronics
    {
        "id": "prod_001",
        "name": "Samsung Galaxy A54 5G",
        "name_sw": "Samsung Galaxy A54 5G",
        "description": "6.4-inch display, 128GB storage, 8GB RAM, 5G ready",
        "description_sw": "Ekran ya inchi 6.4, uhifadhi wa GB 128, RAM GB 8, tayari kwa 5G",
        "price": 34999.00,
        "currency": "KES",
        "category": "electronics",
        "images": ["https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500"],
        "stock": 45,
        "vendor_id": "vendor_001",
        "vendor_name": "TechHub Kenya",
        "rating": 4.5,
        "review_count": 128,
        "county": "Nairobi",
        "is_active": True,
        "tags": ["smartphone", "5G", "samsung"],
        "created_at": "2024-01-10T09:00:00Z"
    },
    {
        "id": "prod_002",
        "name": "Infinix Note 30 Pro",
        "name_sw": "Infinix Note 30 Pro",
        "description": "6.78-inch display, 256GB storage, 12GB RAM, Fast charging",
        "description_sw": "Ekran ya inchi 6.78, uhifadhi wa GB 256, RAM GB 12, malipo ya haraka",
        "price": 28999.00,
        "currency": "KES",
        "category": "electronics",
        "images": ["https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500"],
        "stock": 32,
        "vendor_id": "vendor_002",
        "vendor_name": "Mobile World Kenya",
        "rating": 4.3,
        "review_count": 95,
        "county": "Nairobi",
        "is_active": True,
        "tags": ["smartphone", "infinix", "fast-charging"],
        "created_at": "2024-01-15T10:00:00Z"
    },
    {
        "id": "prod_003",
        "name": "Tecno Spark 20 Pro",
        "name_sw": "Tecno Spark 20 Pro",
        "description": "6.6-inch display, 128GB storage, 8GB RAM, AI triple camera",
        "description_sw": "Ekran ya inchi 6.6, uhifadhi wa GB 128, RAM GB 8, kamera tatu za AI",
        "price": 19999.00,
        "currency": "KES",
        "category": "electronics",
        "images": ["https://images.unsplash.com/photo-1605236453806-6ff36851218e?w=500"],
        "stock": 67,
        "vendor_id": "vendor_003",
        "vendor_name": "Kenya Phone Shop",
        "rating": 4.2,
        "review_count": 156,
        "county": "Nairobi",
        "is_active": True,
        "tags": ["smartphone", "tecno", "camera"],
        "created_at": "2024-01-20T11:00:00Z"
    },
    {
        "id": "prod_004",
        "name": "JBL Tune 510BT Headphones",
        "name_sw": "Vipokezi vya JBL Tune 510BT",
        "description": "Wireless Bluetooth headphones, 40mm drivers, 32 hours battery",
        "description_sw": "Vipokezi vya Bluetooth zisizo na waya, madraiva ya mm 40, betri ya masaa 32",
        "price": 5999.00,
        "currency": "KES",
        "category": "electronics",
        "images": ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"],
        "stock": 89,
        "vendor_id": "vendor_001",
        "vendor_name": "TechHub Kenya",
        "rating": 4.6,
        "review_count": 203,
        "county": "Nairobi",
        "is_active": True,
        "tags": ["headphones", "audio", "wireless"],
        "created_at": "2024-01-05T08:00:00Z"
    },
    # Fashion
    {
        "id": "prod_005",
        "name": "Men's Kanga Outfit Set",
        "name_sw": "Seti ya Kanga ya Wanaume",
        "description": "Traditional kanga 2-piece set, 100% cotton, various colors",
        "description_sw": "Seti ya pamba ya jadi ya vipande 2, pamba 100%, rangi mbalimbali",
        "price": 2499.00,
        "currency": "KES",
        "category": "fashion",
        "images": ["https://images.unsplash.com/photo-1490578474895-699cd4e2cf59?w=500"],
        "stock": 124,
        "vendor_id": "vendor_004",
        "vendor_name": "Umoja Fashion House",
        "rating": 4.7,
        "review_count": 89,
        "county": "Mombasa",
        "is_active": True,
        "tags": ["traditional", "men", "cotton"],
        "created_at": "2024-01-12T13:00:00Z"
    },
    {
        "id": "prod_006",
        "name": "Women's Kitenge Dress",
        "name_sw": "Gauni la Kitenge la Wanawake",
        "description": "Beautiful kitenge maxi dress, African print, comfortable fit",
        "description_sw": "Gauni zuri la kitenge, chapa ya Kiafrika, kufaa vizuri",
        "price": 3299.00,
        "currency": "KES",
        "category": "fashion",
        "images": ["https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=500"],
        "stock": 56,
        "vendor_id": "vendor_004",
        "vendor_name": "Umoja Fashion House",
        "rating": 4.8,
        "review_count": 142,
        "county": "Mombasa",
        "is_active": True,
        "tags": ["dress", "women", "african-print"],
        "created_at": "2024-01-18T15:00:00Z"
    },
    {
        "id": "prod_007",
        "name": "Leather Sandals",
        "name_sw": "Viatu vya Ngozi",
        "description": "Handmade leather sandals, comfortable, durable",
        "description_sw": "Viatu vya ngozi vilivyotengenezwa kwa mkono, vizuri, thabiti",
        "price": 1999.00,
        "currency": "KES",
        "category": "fashion",
        "images": ["https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500"],
        "stock": 78,
        "vendor_id": "vendor_005",
        "vendor_name": "Craftsman Kenya",
        "rating": 4.4,
        "review_count": 67,
        "county": "Nairobi",
        "is_active": True,
        "tags": ["footwear", "leather", "handmade"],
        "created_at": "2024-01-08T10:00:00Z"
    },
    # Home & Living
    {
        "id": "prod_008",
        "name": "Kikoy Blanket",
        "name_sw": "Blanketi ya Kikoy",
        "description": "Traditional kikoy blanket, soft cotton, colorful patterns",
        "description_sw": "Blanketi ya jadi ya kikoy, pamba laini, miundo yenye rangi",
        "price": 4499.00,
        "currency": "KES",
        "category": "home",
        "images": ["https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500"],
        "stock": 43,
        "vendor_id": "vendor_006",
        "vendor_name": "Home Decor Kenya",
        "rating": 4.6,
        "review_count": 112,
        "county": "Nairobi",
        "is_active": True,
        "tags": ["blanket", "traditional", "home"],
        "created_at": "2024-01-14T11:00:00Z"
    },
    {
        "id": "prod_009",
        "name": "Maasai Beaded Cushions",
        "name_sw": "Mto wa Maasai wa Beads",
        "description": "Handmade Maasai beaded cushions, set of 2, colorful",
        "description_sw": "Mto wa Maasai wa beads uliotengenezwa kwa mkono, seti ya 2, zenye rangi",
        "price": 3499.00,
        "currency": "KES",
        "category": "home",
        "images": ["https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=500"],
        "stock": 28,
        "vendor_id": "vendor_005",
        "vendor_name": "Craftsman Kenya",
        "rating": 4.9,
        "review_count": 78,
        "county": "Nairobi",
        "is_active": True,
        "tags": ["cushions", "maasai", "decorative"],
        "created_at": "2024-01-16T12:00:00Z"
    },
    # Beauty & Health
    {
        "id": "prod_010",
        "name": "Shea Butter Soap Set",
        "name_sw": "Seti ya Sabuni ya Shea Butter",
        "description": "Natural shea butter soap, 6 bars, moisturizing",
        "description_sw": "Sabuni ya asili ya shea butter, baa 6, ya unyevu",
        "price": 899.00,
        "currency": "KES",
        "category": "beauty",
        "images": ["https://images.unsplash.com/photo-1600428821653-c3fbe6c01f5b?w=500"],
        "stock": 156,
        "vendor_id": "vendor_007",
        "vendor_name": "Natural Beauty Kenya",
        "rating": 4.5,
        "review_count": 234,
        "county": "Nairobi",
        "is_active": True,
        "tags": ["soap", "natural", "moisturizing"],
        "created_at": "2024-01-11T09:00:00Z"
    },
    {
        "id": "prod_011",
        "name": "Aloe Vera Face Mask",
        "name_sw": "Masks ya Uso ya Aloe Vera",
        "description": "Natural aloe vera face mask, 100ml, hydrating",
        "description_sw": "Masks ya asili ya uso ya aloe vera, 100ml, ya maji",
        "price": 1299.00,
        "currency": "KES",
        "category": "beauty",
        "images": ["https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=500"],
        "stock": 92,
        "vendor_id": "vendor_007",
        "vendor_name": "Natural Beauty Kenya",
        "rating": 4.6,
        "review_count": 145,
        "county": "Nairobi",
        "is_active": True,
        "tags": ["skincare", "natural", "face-mask"],
        "created_at": "2024-01-19T14:00:00Z"
    },
    # Food & Groceries
    {
        "id": "prod_012",
        "name": "Pure Kenyan Honey 500g",
        "name_sw": "Asali ya Kenya Safi 500g",
        "description": "Organic Kenyan honey, pure, no additives, 500g jar",
        "description_sw": "Asali ya Kenya ya asili, safi, bila viongezi, jar ya 500g",
        "price": 899.00,
        "currency": "KES",
        "category": "food",
        "images": ["https://images.unsplash.com/photo-1587049352851-8d4e89133924?w=500"],
        "stock": 201,
        "vendor_id": "vendor_008",
        "vendor_name": "Farm Fresh Kenya",
        "rating": 4.8,
        "review_count": 312,
        "county": "Nairobi",
        "is_active": True,
        "tags": ["honey", "organic", "local"],
        "created_at": "2024-01-07T08:00:00Z"
    },
    {
        "id": "prod_013",
        "name": "Coffee Beans 1kg",
        "name_sw": "Vizao vya Kahawa 1kg",
        "description": "Premium Kenyan coffee beans, medium roast, 1kg bag",
        "description_sw": "Vizao vya kahawa vya Kenya vya hali ya juu, choma wastani, begi la 1kg",
        "price": 1499.00,
        "currency": "KES",
        "category": "food",
        "images": ["https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=500"],
        "stock": 87,
        "vendor_id": "vendor_008",
        "vendor_name": "Farm Fresh Kenya",
        "rating": 4.9,
        "review_count": 267,
        "county": "Nairobi",
        "is_active": True,
        "tags": ["coffee", "premium", "local"],
        "created_at": "2024-01-13T10:00:00Z"
    },
    # Sports
    {
        "id": "prod_014",
        "name": "Football Jersey - Harambee Stars",
        "name_sw": "Jersey ya Mpira - Harambee Stars",
        "description": "Official replica Harambee Stars jersey, polyester, various sizes",
        "description_sw": "Jersey rasmi ya replica ya Harambee Stars, polyester, saizi mbalimbali",
        "price": 3999.00,
        "currency": "KES",
        "category": "sports",
        "images": ["https://images.unsplash.com/photo-1580087256394-dc596e6c8f0f?w=500"],
        "stock": 54,
        "vendor_id": "vendor_009",
        "vendor_name": "Sports World Kenya",
        "rating": 4.7,
        "review_count": 189,
        "county": "Nairobi",
        "is_active": True,
        "tags": ["football", "jersey", "kenya"],
        "created_at": "2024-01-17T13:00:00Z"
    },
    {
        "id": "prod_015",
        "name": "Running Shoes",
        "name_sw": "Viatu vya Kukimbia",
        "description": "Comfortable running shoes, breathable, cushioned sole",
        "description_sw": "Viatu vizuri vya kukimbia, vya kupumua, sehe ya chini ya laini",
        "price": 6999.00,
        "currency": "KES",
        "category": "sports",
        "images": ["https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"],
        "stock": 41,
        "vendor_id": "vendor_009",
        "vendor_name": "Sports World Kenya",
        "rating": 4.4,
        "review_count": 98,
        "county": "Nairobi",
        "is_active": True,
        "tags": ["running", "shoes", "athletic"],
        "created_at": "2024-01-21T15:00:00Z"
    },
]

# Mock Vendors
MOCK_VENDORS = [
    {
        "id": "vendor_001",
        "name": "TechHub Kenya",
        "county": "Nairobi",
        "city": "Westlands",
        "rating": 4.6,
        "product_count": 25,
        "verified": True
    },
    {
        "id": "vendor_002",
        "name": "Mobile World Kenya",
        "county": "Nairobi",
        "city": "CBD",
        "rating": 4.4,
        "product_count": 18,
        "verified": True
    },
    {
        "id": "vendor_003",
        "name": "Kenya Phone Shop",
        "county": "Nairobi",
        "city": "Kasarani",
        "rating": 4.3,
        "product_count": 32,
        "verified": True
    },
    {
        "id": "vendor_004",
        "name": "Umoja Fashion House",
        "county": "Mombasa",
        "city": "Mombasa",
        "rating": 4.8,
        "product_count": 45,
        "verified": True
    },
    {
        "id": "vendor_005",
        "name": "Craftsman Kenya",
        "county": "Nairobi",
        "city": "Karen",
        "rating": 4.7,
        "product_count": 28,
        "verified": True
    },
    {
        "id": "vendor_006",
        "name": "Home Decor Kenya",
        "county": "Nairobi",
        "city": "Lavington",
        "rating": 4.5,
        "product_count": 22,
        "verified": True
    },
    {
        "id": "vendor_007",
        "name": "Natural Beauty Kenya",
        "county": "Nairobi",
        "city": "Parklands",
        "rating": 4.6,
        "product_count": 38,
        "verified": True
    },
    {
        "id": "vendor_008",
        "name": "Farm Fresh Kenya",
        "county": "Nairobi",
        "city": "Runda",
        "rating": 4.9,
        "product_count": 52,
        "verified": True
    },
    {
        "id": "vendor_009",
        "name": "Sports World Kenya",
        "county": "Nairobi",
        "city": "Kilimani",
        "rating": 4.5,
        "product_count": 31,
        "verified": True
    },
]

# Mock Orders
MOCK_ORDERS = []

# Mock Interactions (for recommendations)
MOCK_INTERACTIONS = [
    {"user_id": "user_001", "product_id": "prod_001", "interaction_type": "view", "timestamp": "2024-01-20T10:00:00Z"},
    {"user_id": "user_001", "product_id": "prod_004", "interaction_type": "purchase", "timestamp": "2024-01-21T14:00:00Z"},
    {"user_id": "user_002", "product_id": "prod_005", "interaction_type": "purchase", "timestamp": "2024-01-22T09:00:00Z"},
    {"user_id": "user_002", "product_id": "prod_006", "interaction_type": "view", "timestamp": "2024-01-23T11:00:00Z"},
]


class MockDatabase:
    """Mock database class to simulate database operations"""
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict]:
        """Find user by email"""
        for user in MOCK_USERS:
            if user["email"] == email:
                return user.copy()
        return None
    
    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[Dict]:
        """Find user by ID"""
        for user in MOCK_USERS:
            if user["id"] == user_id:
                return user.copy()
        return None
    
    @staticmethod
    def create_user(user_data: Dict) -> Dict:
        """Create a new user"""
        new_user = {
            "id": f"user_{len(MOCK_USERS) + 1:03d}",
            "email": user_data["email"],
            "username": user_data["username"],
            "full_name": user_data.get("full_name", ""),
            "password_hash": user_data["password_hash"],
            "phone_number": user_data.get("phone_number", ""),
            "county": user_data.get("county", "Nairobi"),
            "city": user_data.get("city", ""),
            "preferred_language": user_data.get("preferred_language", "en"),
            "preferred_categories": user_data.get("preferred_categories", []),
            "is_active": True,
            "is_verified": False,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        MOCK_USERS.append(new_user)
        return new_user.copy()
    
    @staticmethod
    def get_products(
        category: Optional[str] = None,
        county: Optional[str] = None,
        search: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict]:
        """Get products with filters"""
        products = MOCK_PRODUCTS.copy()
        
        # Apply filters
        if category:
            products = [p for p in products if p["category"] == category]
        
        if county:
            products = [p for p in products if p["county"] == county]
        
        if search:
            search_lower = search.lower()
            products = [
                p for p in products
                if search_lower in p["name"].lower() or 
                   search_lower in p["description"].lower() or
                   any(search_lower in tag.lower() for tag in p.get("tags", []))
            ]
        
        if min_price:
            products = [p for p in products if p["price"] >= min_price]
        
        if max_price:
            products = [p for p in products if p["price"] <= max_price]
        
        # Apply pagination
        return products[offset:offset + limit]
    
    @staticmethod
    def get_product_by_id(product_id: str) -> Optional[Dict]:
        """Get product by ID"""
        for product in MOCK_PRODUCTS:
            if product["id"] == product_id:
                return product.copy()
        return None
    
    @staticmethod
    def get_trending_products(county: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Get trending products (sorted by rating and review count)"""
        products = MOCK_PRODUCTS.copy()
        
        if county:
            products = [p for p in products if p["county"] == county]
        
        # Sort by rating * review_count (engagement metric)
        products.sort(key=lambda p: p["rating"] * p["review_count"], reverse=True)
        
        return products[:limit]
    
    @staticmethod
    def get_vendors(county: Optional[str] = None) -> List[Dict]:
        """Get vendors"""
        vendors = MOCK_VENDORS.copy()
        
        if county:
            vendors = [v for v in vendors if v["county"] == county]
        
        return vendors
    
    @staticmethod
    def get_user_interactions(user_id: str) -> List[Dict]:
        """Get user interactions for recommendations"""
        return [i for i in MOCK_INTERACTIONS if i["user_id"] == user_id]
    
    @staticmethod
    def add_interaction(user_id: str, product_id: str, interaction_type: str):
        """Add a new interaction"""
        MOCK_INTERACTIONS.append({
            "user_id": user_id,
            "product_id": product_id,
            "interaction_type": interaction_type,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    
    @staticmethod
    def create_order(order_data: Dict) -> Dict:
        """Create a new order"""
        order = {
            "id": f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{len(MOCK_ORDERS) + 1:03d}",
            **order_data,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        MOCK_ORDERS.append(order)
        return order.copy()

# Global instance
mock_db = MockDatabase()

