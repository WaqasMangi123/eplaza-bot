from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import datetime
import os
import re
from typing import Dict, List, Any

app = Flask(__name__)
CORS(app)

class ProductChatbot:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY', 'your_openrouter_api_key_here')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "deepseek/deepseek-r1"
        
        self.products = self._load_product_data()
        self.conversations = {}
        self.system_prompt = self._create_system_prompt()
        
    def _load_product_data(self) -> Dict[str, List[Dict]]:
        products = {
            "earbuds_headphones": [
                {
                    "name": "AirPods Max",
                    "price": 149000,
                    "brand": "Apple",
                    "description": "AirPods Max with Good Quality.",
                    "category": "earbuds_headphones",
                    "features": ["Active Noise Cancellation", "Premium Quality", "Over-ear design"]
                },
                {
                    "name": "Apple AirPods 4",
                    "price": 95999,
                    "brand": "Apple",
                    "description": "Apple AirPods 4 Active Noise Cancellation.",
                    "category": "earbuds_headphones",
                    "features": ["Active Noise Cancellation", "True Wireless", "Touch Controls"]
                },
                {
                    "name": "FASTER ROBOX EARBUDS ANC+ENC",
                    "price": 5799,
                    "brand": "Faster",
                    "description": "FASTER ROBOX EARBUDS ANC+ENC Color: Black silver.",
                    "category": "earbuds_headphones",
                    "features": ["ANC", "ENC", "Affordable", "Good Sound Quality"]
                },
                {
                    "name": "Lenovo XT88 True Wireless Earbuds",
                    "price": 3799,
                    "brand": "Lenovo",
                    "description": "Bluetooth Version: 5.3, Range: 10m, Playtime: 4.5 hours, Charging Time: 1.5 hours",
                    "category": "earbuds_headphones",
                    "features": ["Bluetooth 5.3", "Budget-friendly", "4.5h playtime", "Quick charging"]
                },
                {
                    "name": "AirPods Pro 2 (2nd Gen)",
                    "price": 5000,
                    "brand": "Local",
                    "description": "Premium copy with all features, great sound quality, long battery life, touch control, pop-up window, lightning port, up to 4.5 hours battery, multiple ear tips",
                    "category": "earbuds_headphones",
                    "features": ["Touch Control", "Pop-up Window", "Lightning Port", "Multiple Ear Tips"]
                },
                {
                    "name": "AirPods Pro Black (2nd Gen)",
                    "price": 5200,
                    "brand": "Local",
                    "description": "Adaptive EQ, High Bass, Superior audio quality, Pop Up connection, Play and pause control, Bluetooth Version 5.3, Lightning port, Up to 4-6 hours battery, Small Medium Large ear tips, Motion-detecting accelerometer, Dual beamforming microphones",
                    "category": "earbuds_headphones",
                    "features": ["Adaptive EQ", "High Bass", "Motion Detection", "Dual Microphones"]
                },
                {
                    "name": "Rover Pro Earbuds",
                    "price": 14924,
                    "brand": "Zero",
                    "description": "Rover Pro Earbuds Aerofit Design with Quad Mic & ENC.",
                    "category": "earbuds_headphones",
                    "features": ["Aerofit Design", "Quad Mic", "ENC", "Premium"]
                },
                {
                    "name": "Quantum Earbuds",
                    "price": 19000,
                    "brand": "Zero",
                    "description": "Quantum Earbuds Active Noise Cancellation.",
                    "category": "earbuds_headphones",
                    "features": ["Active Noise Cancellation", "Premium Build", "High Quality"]
                },
                {
                    "name": "Samsung Galaxy Buds 3 AI",
                    "price": 25990,
                    "brand": "Samsung",
                    "description": "Samsung Galaxy Buds 3 AI True Wireless Bluetooth Earbuds, Sound Optimization, Real-Time Interpreter, Noise Cancelling, Redesigned Fit, Touch Control, Silver",
                    "category": "earbuds_headphones",
                    "features": ["AI Features", "Real-time Interpreter", "Sound Optimization", "Noise Cancelling"]
                },
                {
                    "name": "AirPods Pro (USB-C) (2nd generation)",
                    "price": 84999,
                    "brand": "I phone",
                    "description": "Wireless. Effortless. Magical. With plenty of talk and listen time, voice-activated Siri access, and wireless charging case. Simply take them out and they are ready to use with all your devices",
                    "category": "earbuds_headphones",
                    "features": ["USB-C", "Wireless Charging", "Siri Access", "Premium Apple"]
                }
            ],
            
            "beauty_cosmetics": [
                {
                    "name": "Brow Luxe Tool Kit",
                    "price": 1995,
                    "brand": "Luscious",
                    "description": "Shape, define, fill, and set brows with this high-performance tool kit. Travel-friendly, mirrored tool kit with 2 x Brow Powders, Brow Setting Wax, Mini Tweezers, 2 x Brow Brushes, 3 x Stencils, Step-by-step Guide",
                    "category": "beauty_cosmetics",
                    "features": ["Complete Kit", "Professional Tools", "Travel-friendly", "Step-by-step Guide"]
                },
                {
                    "name": "Angel Eyes Primer",
                    "price": 1695,
                    "brand": "Luscious",
                    "description": "Up to 16 hours of no-crease, no-smudge, and no-fade makeup. THE GUARDIAN ANGEL FOR YOUR EYE MAKEUP",
                    "category": "beauty_cosmetics",
                    "features": ["16-hour wear", "No-crease", "No-smudge", "Long-lasting"]
                },
                {
                    "name": "Softlight Brightening Face Powders",
                    "price": 2195,
                    "brand": "Luscious",
                    "description": "Sheer, color-correcting loose powders for instant complexion refresh. Featherlight and translucent for airbrushed finish, infused with soft-focus pigments to cancel dullness, control shine",
                    "category": "beauty_cosmetics",
                    "features": ["Color-correcting", "Loose Powder", "Soft-focus", "Shine Control"]
                },
                {
                    "name": "Softlight Powder Foundation",
                    "price": 2650,
                    "brand": "Luscious",
                    "description": "Our bestselling powder foundation loved by customers, celebrities and pro makeup artists",
                    "category": "beauty_cosmetics",
                    "features": ["Bestselling", "Celebrity Choice", "Professional", "Powder Foundation"]
                },
                {
                    "name": "Fair & Lovely Glow & Lovely Face Wash",
                    "price": 250,
                    "brand": "Fair&Lovely",
                    "description": "This face wash gives you the double action of deep cleansing and multivitamins brightening for an instant glow",
                    "category": "beauty_cosmetics",
                    "features": ["Deep Cleansing", "Brightening", "Multivitamins", "Instant Glow"]
                },
                {
                    "name": "Tea Tree Clearing Facewash",
                    "price": 999,
                    "brand": "Orior",
                    "description": "Get refreshed, mattifying, and visibly clearer skin with Tea Tree Face Wash. Designed to target stubborn acne and skin texture issues, infused with Tea Tree Oil and Aloe Vera extracts",
                    "category": "beauty_cosmetics",
                    "features": ["Tea Tree Oil", "Aloe Vera", "Anti-acne", "Mattifying"]
                },
                {
                    "name": "Allure Women's Perfume",
                    "price": 5990,
                    "brand": "Edenrobe",
                    "description": "Allure Women's Perfume - EBWF-ALLURE 50ML",
                    "category": "beauty_cosmetics",
                    "features": ["Women's Fragrance", "50ML", "Premium Quality", "Long-lasting scent"]
                },
                {
                    "name": "St London Velvet Lipstick -52 (Blush Pink)",
                    "price": 1410,
                    "brand": "St London",
                    "description": "ST London is a color cosmetic brand that captures the glamorous side of a woman and gives a complete beauty makeover with its wide range from foundations, blush-ons, bronzers, eye liners",
                    "category": "beauty_cosmetics",
                    "features": ["Velvet Texture", "Blush Pink", "Complete Range", "Glamorous"]
                },
                {
                    "name": "Essence Long Lasting Lipstick 01",
                    "price": 1170,
                    "brand": "Reana",
                    "description": "Essence Long Lasting Lipstick 01",
                    "category": "beauty_cosmetics",
                    "features": ["Long Lasting", "Quality Brand", "Affordable", "Good Pigmentation"]
                }
            ],
            
            "smartphones": [
                {
                    "name": "Realme C35",
                    "price": 39999,
                    "brand": "Realme",
                    "description": "Realme C35 is equipped with 50MP AI Triple Camera, 16.7cm(6.6'') FHD Fullscreen and 5000mAh Massive Battery",
                    "category": "smartphones",
                    "features": ["50MP Camera", "6.6 inch Display", "5000mAh Battery", "Budget-friendly"]
                },
                {
                    "name": "Samsung Galaxy A32",
                    "price": 75999,
                    "brand": "Samsung",
                    "description": "The display screen of the new Samsung A32 will be 6.4 inches Super AMOLED capacitive touchscreen, 16M colors",
                    "category": "smartphones",
                    "features": ["Super AMOLED", "6.4 inch", "Premium Display", "Reliable Performance"]
                },
                {
                    "name": "Vivo V27",
                    "price": 89999,
                    "brand": "Vivo",
                    "description": "Experience the power of 5G with the vivo V27. Featuring MediaTek Dimensity 7200 processor, 4600mAh battery supported with maximum 66W fast charging",
                    "category": "smartphones",
                    "features": ["5G Ready", "66W Fast Charging", "Dimensity 7200", "Good Camera"]
                },
                {
                    "name": "Oppo A34 5G",
                    "price": 58824,
                    "brand": "Oppo",
                    "description": "Oppo A34 5G price in Pakistan is expected to be from PKR 58,824. This mobile is rumoured to be an excellent phone with Qualcomm Snapdragon 765 (11 nm) processor, 4 GB of RAM, and 128 GB of storage",
                    "category": "smartphones",
                    "features": ["5G", "Snapdragon 765", "4GB RAM", "128GB Storage"]
                },
                {
                    "name": "Samsung Galaxy S8",
                    "price": 79999,
                    "brand": "Samsung",
                    "description": "Samsung Galaxy S8 is very slim and smart phone and it available in Midnight Black, Orchid Gray, Arctic Silver, Coral Blue and Maple Gold colors",
                    "category": "smartphones",
                    "features": ["Slim Design", "Multiple Colors", "Premium Build", "Smart Features"]
                },
                {
                    "name": "Samsung Galaxy A16 (256GB)",
                    "price": 61999,
                    "brand": "Samsung",
                    "description": "Discover Samsung Galaxy A16 in Black with 256GB internal storage and explore essential features with Galaxy AI",
                    "category": "smartphones",
                    "features": ["256GB Storage", "Galaxy AI", "Large Storage", "AI Features"]
                },
                {
                    "name": "Infinix Hot 50i",
                    "price": 30999,
                    "brand": "Infinix",
                    "description": "OS Android 14 (Go edition) UI XOS 14 Dimensions 165.7 x 77.1 x 8.1mm Weight 184 g SIM Dual Sim, Dual Standby (Nano-SIM) Colors Sleek Black, Sage Green, Titanium Grey",
                    "category": "smartphones",
                    "features": ["Android 14", "Dual SIM", "Budget Phone", "Multiple Colors"]
                },
                {
                    "name": "iPhone 11 Pro Max",
                    "price": 110900,
                    "brand": "I phone",
                    "description": "(Non PTA)Apple looks keen to bring iPhone 11 that is the high-end Pro Max version of the series along with its two other variants",
                    "category": "smartphones",
                    "features": ["Non-PTA", "Pro Max", "High-end", "Premium iOS"]
                },
                {
                    "name": "Xiaomi Redmi 13",
                    "price": 34999,
                    "brand": "Redmi",
                    "description": "Xiaomi is launching the latest Redmi 13 series, which seems to be very close to hitting the market. Amazing and mind-blowing features",
                    "category": "smartphones",
                    "features": ["Latest Series", "Amazing Features", "Budget-friendly", "Xiaomi Quality"]
                },
                {
                    "name": "Samsung Galaxy A50",
                    "price": 45000,
                    "brand": "Samsung",
                    "description": "Android 9.0 (Pie) UI One UI Dimensions 158.5 x 74.7 x 7.7 mm Weight 166 g SIM Dual Sim, Dual Standby (Nano-SIM) Colors Black, White, Blue, Coral",
                    "category": "smartphones",
                    "features": ["Android 9.0", "One UI", "Dual SIM", "Multiple Colors"]
                }
            ],
            
            "clothing_men": [
                {
                    "name": "Light Random Wash Boxy Fit Tee",
                    "price": 2999,
                    "brand": "Breakout",
                    "description": "A soft cotton tee in a boxy silhouette, finished with a light random wash for subtle texture. Clean and minimal in washed grey",
                    "category": "clothing_men",
                    "features": ["Cotton", "Boxy Fit", "Casual", "Washed Grey"]
                },
                {
                    "name": "Half Sleeves Mill Dyed Shirt",
                    "price": 4595,
                    "brand": "Cambridge",
                    "description": "Elevate your casual style with this mill-dyed half-sleeve shirt, crafted from 100% cotton woven fabric. Designed in a regular fit for all-day comfort. Lightweight and breathable, perfect summer essential",
                    "category": "clothing_men",
                    "features": ["100% Cotton", "Regular Fit", "Breathable", "Summer Essential"]
                },
                {
                    "name": "Classic Polo - Burgundy",
                    "price": 3395,
                    "brand": "Cambridge",
                    "description": "Upgrade your casual wardrobe with this classic polo shirt, crafted from premium cotton fabric. Designed with half sleeves and a ribbed collar for a timeless look",
                    "category": "clothing_men",
                    "features": ["Premium Cotton", "Classic Design", "Ribbed Collar", "Timeless"]
                },
                {
                    "name": "Skull Printed Oversized White T-Shirt for Men",
                    "price": 6599,
                    "brand": "Go Devil",
                    "description": "Skull Printed Oversized White T-Shirt for Men All size available",
                    "category": "clothing_men",
                    "features": ["Oversized Fit", "Skull Print", "All Sizes", "Statement Piece"]
                },
                {
                    "name": "Graphic Raglan T-Shirt",
                    "price": 3090,
                    "brand": "Outfitters",
                    "description": "Get ready to take on the day in style with our Graphic Raglan Heavyweight Raised Seam T-Shirt! Made from relaxed, breathable cotton, perfect for any casual occasion",
                    "category": "clothing_men",
                    "features": ["Heavyweight", "Raised Seam", "Breathable Cotton", "Casual"]
                },
                {
                    "name": "Graphic T-shirt",
                    "price": 2890,
                    "brand": "Outfitters",
                    "description": "Unleash your style with our Graphic T-shirt! This relaxed cotton tee brings the perfect blend of comfort and personality to your wardrobe. Soft fabric with eye-catching graphics",
                    "category": "clothing_men",
                    "features": ["Relaxed Fit", "Eye-catching Graphics", "Soft Fabric", "Personality"]
                },
                {
                    "name": "Polo Collar Shirt",
                    "price": 3060,
                    "brand": "Ideas",
                    "description": "Color of the article may vary from the uploaded picture",
                    "category": "clothing_men",
                    "features": ["Polo Collar", "Classic Style", "Versatile", "Quality Brand"]
                },
                {
                    "name": "Regular Fit Polo",
                    "price": 2690,
                    "brand": "Ideas",
                    "description": "Color of the article may vary from the uploaded picture",
                    "category": "clothing_men",
                    "features": ["Regular Fit", "Polo Style", "Comfortable", "Quality"]
                },
                {
                    "name": "Graphic T-Shirt",
                    "price": 1090,
                    "brand": "Zelbury",
                    "description": "T-Shirts - Men Ready to Wear - Zellbury All sizes Available",
                    "category": "clothing_men",
                    "features": ["All Sizes", "Ready to Wear", "Affordable", "Graphic Design"]
                },
                {
                    "name": "Textured T-Shirt",
                    "price": 1690,
                    "brand": "Zelbury",
                    "description": "T-Shirts - Men Ready to Wear - Zellbury All Sizes Available",
                    "category": "clothing_men",
                    "features": ["Textured", "All Sizes", "Ready to Wear", "Quality"]
                }
            ],
            
            "fragrances": [
                {
                    "name": "Musk Rouge (100 ML)",
                    "price": 5280,
                    "brand": "Bonanza",
                    "description": "Fragrance",
                    "category": "fragrances",
                    "features": ["100ML", "Musk Scent", "Long-lasting", "Premium"]
                },
                {
                    "name": "Calvin Klein In2U For Women",
                    "price": 10730,
                    "brand": "Calvin klein",
                    "description": "Calvin Klein In2U For Women Edt 100Ml",
                    "category": "fragrances",
                    "features": ["Women's Fragrance", "EDT", "100ML", "Designer Brand"]
                },
                {
                    "name": "Calvin Klein Unisex",
                    "price": 15400,
                    "brand": "Ck",
                    "description": "Calvin Klein Unisex One Reflections Edt 100ml",
                    "category": "fragrances",
                    "features": ["Unisex", "One Reflections", "100ML", "Designer"]
                },
                {
                    "name": "OUD",
                    "price": 10200,
                    "brand": "Dior",
                    "description": "Christian Dior Oud Ispahan Esprit de Parfum 80ml",
                    "category": "fragrances",
                    "features": ["Oud Scent", "80ML", "Esprit de Parfum", "Luxury"]
                },
                {
                    "name": "Sauvage Perfume",
                    "price": 12499,
                    "brand": "Dior",
                    "description": "Dior timeless Sauvage perfume",
                    "category": "fragrances",
                    "features": ["Timeless", "Designer Brand", "Premium", "Long-lasting"]
                },
                {
                    "name": "ZARAR GOLD",
                    "price": 4400,
                    "brand": "J.",
                    "description": "Perfume is sensitive to light and temperature. Exposure to light and heat can alter its composition and fragrance. Store your perfume in a cool, dark place, away from direct sunlight",
                    "category": "fragrances",
                    "features": ["Gold Collection", "Light Sensitive", "Premium Care", "Long-lasting"]
                },
                {
                    "name": "J.EXCLUSIVE",
                    "price": 4300,
                    "brand": "J.",
                    "description": "Exclusive is a refreshing fragrance for the uber-youth of Pakistan. Its success in the urban centers of Pakistan has made it a household name",
                    "category": "fragrances",
                    "features": ["Youth Fragrance", "Refreshing", "Urban Popular", "Household Name"]
                },
                {
                    "name": "EDGE",
                    "price": 5800,
                    "brand": "J.",
                    "description": "With the introduction of Edge, J. truly went over the edge by introducing a scent so bold that it evokes the sense of timeless freedom and calmness",
                    "category": "fragrances",
                    "features": ["Bold Scent", "Timeless", "Freedom", "Calmness"]
                },
                {
                    "name": "JANAN SPORT",
                    "price": 6580,
                    "brand": "J.",
                    "description": "Discover the new exquisite variant of our popular Janan family Janan Sport",
                    "category": "fragrances",
                    "features": ["Sport Variant", "Janan Family", "Exquisite", "Active"]
                },
                {
                    "name": "One Million EDT For Men",
                    "price": 34104,
                    "brand": "Paco Rabanne",
                    "description": "Paco Rabanne One Million EDT For Men 200Ml",
                    "category": "fragrances",
                    "features": ["EDT", "200ML", "Men's Fragrance", "Designer Luxury"]
                }
            ],
            
            "clothing_women": [
                {
                    "name": "Women T Shirt",
                    "price": 2499,
                    "brand": "Hangteen",
                    "description": "Care Instructions: Machine or hand-wash up to 30C/86F, Gentle cycle, Do not dry in direct sunlight, Do not bleach, Do not iron directly on prints/embroidery",
                    "category": "clothing_women",
                    "features": ["Easy Care", "Machine Washable", "Print Friendly", "Gentle"]
                },
                {
                    "name": "Embroidered Keyhole Blouse",
                    "price": 5250,
                    "brand": "Beech Tree",
                    "description": "Embroidered Band Collar Button-Through Top With Keyhole Detail On Neck, Smocking On Sleeve Cuffs Along With Puff Sleeves. Fabric: China Woven. Casual Fit Size",
                    "category": "clothing_women",
                    "features": ["Embroidered", "Keyhole Design", "Puff Sleeves", "China Woven"]
                },
                {
                    "name": "Multi Printed Shirt for Women",
                    "price": 2149,
                    "brand": "Gul Ahmed",
                    "description": "Button down printed shirt with Wide sleeves Regular Fit Model height is 5 feet 5 inches. Model is wearing Small size",
                    "category": "clothing_women",
                    "features": ["Multi Print", "Wide Sleeves", "Regular Fit", "Button Down"]
                },
                {
                    "name": "Collar Shirt",
                    "price": 3690,
                    "brand": "Gul Ahmed",
                    "description": "Button Down Printed Shirt With Sleeves Regular Fit Model height is 5 feet 5 inches. Model is wearing Small size",
                    "category": "clothing_women",
                    "features": ["Collar Design", "Printed", "Regular Fit", "Quality Brand"]
                },
                {
                    "name": "Women Mid-Length Top",
                    "price": 5297,
                    "brand": "Engine",
                    "description": "Fabric: Georgette This mid-length button-down top in lightweight georgette offers a breezy and elegant silhouette. Ideal for both casual and semi-formal occasions",
                    "category": "clothing_women",
                    "features": ["Georgette", "Mid-length", "Elegant", "Versatile"]
                },
                {
                    "name": "Mid-Length Top",
                    "price": 5499,
                    "brand": "Engine",
                    "description": "Fabric: Poplin This women printed mid-length top is crafted from smooth and breathable poplin fabric, offering a chic and comfortable fit",
                    "category": "clothing_women",
                    "features": ["Poplin", "Printed", "Breathable", "Chic"]
                },
                {
                    "name": "Brown Stripe Button Down Shirt",
                    "price": 3950,
                    "brand": "Sowears",
                    "description": "Stay stylish and comfortable in our Brown Stripe Button Down Shirt. Made from a mix of Cotton and Lawn fabric, perfect for any occasion. Classic stripe design",
                    "category": "clothing_women",
                    "features": ["Brown Stripe", "Cotton Lawn", "Classic Design", "Versatile"]
                },
                {
                    "name": "Moon Stone Shirt In Black",
                    "price": 6950,
                    "brand": "Soweras",
                    "description": "Moon Stone Shirt in Black, a timeless piece that combines elegance with intricate craftsmanship. Crafted from delicate lace net fabric with floral pattern",
                    "category": "clothing_women",
                    "features": ["Lace Net", "Floral Pattern", "Elegant", "Timeless"]
                },
                {
                    "name": "Ink Veil Embroidered Shirt",
                    "price": 5950,
                    "brand": "Sowears",
                    "description": "The Ink Veil Embroidered Shirt is a perfect blend of elegance and comfort. Crafted from premium cotton, black tunic-style shirt with intricate white embroidery",
                    "category": "clothing_women",
                    "features": ["Premium Cotton", "Embroidered", "Tunic Style", "Elegant"]
                },
                {
                    "name": "Orient Plum Button Down Shirt",
                    "price": 3950,
                    "brand": "Sowears",
                    "description": "Product Detail: This button down shirt in soft viscose features box pleat detailing at the back for a flattering look. Stay comfortable and stylish",
                    "category": "clothing_women",
                    "features": ["Viscose", "Box Pleat", "Flattering", "Comfortable"]
                }
            ],
            
            "skincare": [
                {
                    "name": "Rice Face Wash & Scrub",
                    "price": 800,
                    "brand": "Co Natural",
                    "description": "Our Rice Face Wash & Scrub is a 2-in-1 cleanser and exfoliator that gently buffs away dirt, dead skin, and impurities, leaving your skin brighter, smoother, and softer",
                    "category": "skincare",
                    "features": ["2-in-1", "Rice Extract", "Exfoliating", "Brightening"]
                },
                {
                    "name": "DEEP Cleansing Beard & Face Wash",
                    "price": 999,
                    "brand": "Nivea",
                    "description": "Tough enough for facial hair, but gentle enough for daily use. Formulated with Natural Charcoal, thoroughly cleanses your Beard & Face, masculine Vanilla & Bourbon scent. 100ml",
                    "category": "skincare",
                    "features": ["For Men", "Natural Charcoal", "Beard Care", "Vanilla Bourbon"]
                },
                {
                    "name": "MEN Protect & Care Aloe Vera Deep Cleansing Face Wash",
                    "price": 1499,
                    "brand": "Nivea",
                    "description": "Get your skin the protection and care it deserves! The face wash with Aloe Vera and Pro-Vitamin B5 thoroughly cleanses your skin, leaving it healthy-looking and refreshed. 100ml",
                    "category": "skincare",
                    "features": ["Aloe Vera", "Pro-Vitamin B5", "Men's Care", "Deep Cleansing"]
                },
                {
                    "name": "Advanced Freckle Face Wash",
                    "price": 860,
                    "brand": "Vince",
                    "description": "Advanced Freckle Face Wash",
                    "category": "skincare",
                    "features": ["Freckle Care", "Advanced Formula", "Specialized", "Affordable"]
                },
                {
                    "name": "Whitening Scrub Face Wash",
                    "price": 895,
                    "brand": "Vince",
                    "description": "Whitening Scrub Face Wash",
                    "category": "skincare",
                    "features": ["Whitening", "Scrub Action", "Face Care", "Affordable"]
                },
                {
                    "name": "Men Neat & Clear Face Wash with BHA & Kaolin Clay",
                    "price": 250,
                    "brand": "Golden's Pearl",
                    "description": "Men Neat & Clear Face Wash with BHA & Kaolin Clay 75ml",
                    "category": "skincare",
                    "features": ["BHA", "Kaolin Clay", "Men's Care", "Budget-friendly"]
                },
                {
                    "name": "PONDS ACNE CLEAR 10 FIGHT FACIAL FOAM",
                    "price": 310,
                    "brand": "Ponds",
                    "description": "PONDS ACNE CLEAR 10 FIGHT FACIAL FOAM fights acne effectively",
                    "category": "skincare",
                    "features": ["Acne Fighting", "Facial Foam", "10x Action", "Trusted Brand"]
                },
                {
                    "name": "Ponds Charcoal Face Wash",
                    "price": 870,
                    "brand": "Ponds",
                    "description": "Ponds Charcoal Face Wash -100gm Pond Pure Detox with Activated Charcoal Face Wash. Deep-cleansing formula designed to purify and detoxify your skin",
                    "category": "skincare",
                    "features": ["Activated Charcoal", "Deep Cleansing", "Detox", "Purifying"]
                },
                {
                    "name": "Men Fair & Lovely Glow Handsome Instant Brightness Rapid Action Face Wash",
                    "price": 480,
                    "brand": "Fair & Lovely",
                    "description": "Men Fair and Lovely Rapid Action Instant Fairness facewash designed for MEN skin for 1-wash instant fair look. Eliminates impurities, ICY menthol leaves skin cool and fresh",
                    "category": "skincare",
                    "features": ["Instant Brightness", "ICY Menthol", "Rapid Action", "Men's Care"]
                },
                {
                    "name": "Garnier - Men Acno Fight Face Wash",
                    "price": 849,
                    "brand": "Garnier",
                    "description": "Garnier - Men Acno Fight Face Wash - 100ml Fight acne and reveal brighter looking skin. A gentle yet effective face wash for blackheads and acne. 6-in-1 cleaning formula",
                    "category": "skincare",
                    "features": ["6-in-1 Formula", "Acne Fighting", "Blackhead Care", "Gentle"]
                }
            ],
            
            "smartwatches": [
                {
                    "name": "S9 Ultra Smartwatch",
                    "price": 2999,
                    "brand": "Infurion",
                    "description": "S9 Ultra Smartwatch Wireless INFURION Charging Bluetooth Call Sleep Monitoring Men Women Watch Ultra Smart Watch Series 8",
                    "category": "smartwatches",
                    "features": ["Wireless Charging", "Bluetooth Calls", "Sleep Monitoring", "Ultra Series"]
                },
                {
                    "name": "D20 New T900 Ultra 2 Smartwatch",
                    "price": 2999,
                    "brand": "Okaas",
                    "description": "OKS D20 New T900 Ultra 2 Smartwatch Bluetooth Call Sleeping Monitoring Smart Watch Series 8 2.09 inch Full Touch Watch for Men Women",
                    "category": "smartwatches",
                    "features": ["2.09 inch Display", "Full Touch", "Bluetooth Call", "Sleep Monitor"]
                },
                {
                    "name": "Official Huawei Watch Fit 3",
                    "price": 39999,
                    "brand": "Huawei",
                    "description": "Sleek Design Vibrant Display Comfortable Wear Heart Rate Monitoring SpO2 Tracking Advanced Sleep Analysis Stress Management Workout Modes Smart Notifications Long Battery Life",
                    "category": "smartwatches",
                    "features": ["Official Huawei", "Heart Rate", "SpO2", "Advanced Sleep", "Long Battery"]
                },
                {
                    "name": "Official Huawei Band 6",
                    "price": 15999,
                    "brand": "Huawei",
                    "description": "Huawei Band 6 Smart Watch",
                    "category": "smartwatches",
                    "features": ["Official Huawei", "Band Style", "Smart Features", "Affordable"]
                },
                {
                    "name": "DT900 ULTRA Smart watch",
                    "price": 8500,
                    "brand": "Local",
                    "description": "DT900 ULTRA Smart watch With 7 Straps. Multiple strap options for different occasions",
                    "category": "smartwatches",
                    "features": ["7 Straps Included", "Ultra Design", "Multiple Options", "Value Pack"]
                },
                {
                    "name": "Galaxy Fit3",
                    "price": 75999,
                    "brand": "Samsung",
                    "description": "Galaxy Watch FE (Bluetooth, 40mm)",
                    "category": "smartwatches",
                    "features": ["Samsung Official", "40mm", "Bluetooth", "Galaxy Ecosystem"]
                },
                {
                    "name": "Spigen Apple Watch Series 10",
                    "price": 7799,
                    "brand": "Apple",
                    "description": "Spigen Apple Watch Series 10 46mm Rugged Armor Pro Case With Band. Rugged design with unique carbon fiber accents absorbs shock, keeping your Apple Watch safe",
                    "category": "smartwatches",
                    "features": ["Rugged Protection", "Carbon Fiber", "46mm", "Shock Absorption"]
                },
                {
                    "name": "Apple Watch Series 10",
                    "price": 109999,
                    "brand": "Apple",
                    "description": "Apple Watch Series 10 46mm Silver Aluminium Case With Denim Sports Band. Thinnest Apple Watch ever, with our biggest display New depth and water temperature sensors",
                    "category": "smartwatches",
                    "features": ["Thinnest Ever", "Biggest Display", "Water Sensors", "Denim Band"]
                },
                {
                    "name": "Prestige Smartwatch",
                    "price": 23500,
                    "brand": "Sveston",
                    "description": "Colour Black+Silver",
                    "category": "smartwatches",
                    "features": ["Prestige Design", "Black Silver", "Premium Look", "Stylish"]
                },
                {
                    "name": "Maxfit Smartwatch",
                    "price": 13999,
                    "brand": "Sveston",
                    "description": "Colour Black+Blue",
                    "category": "smartwatches",
                    "features": ["Maxfit Design", "Black Blue", "Fitness Focus", "Colorful"]
                }
            ],
            
            "jeans_denim": [
                {
                    "name": "Original Straight Fit Cargo Denim",
                    "price": 3710,
                    "brand": "Outfitters",
                    "description": "Black straight-fit cargo denim crafted from cotton, featuring two side pockets, two back pockets, and two cargo pockets. Designed with dart details on the knees and adjustable strap details. 100% Cotton",
                    "category": "jeans_denim",
                    "features": ["100% Cotton", "Cargo Pockets", "Adjustable Straps", "Dart Details"]
                },
                {
                    "name": "Baggy Fit Denim",
                    "price": 3450,
                    "brand": "Outfitters",
                    "description": "Baggy fit denim jeans made from 100% cotton in a light blue wash. Designed with an elastic waistband for added comfort and a relaxed, easy silhouette. 100% Cotton",
                    "category": "jeans_denim",
                    "features": ["Baggy Fit", "Light Blue", "Elastic Waistband", "100% Cotton"]
                },
                {
                    "name": "Slim Relaxed Fit Cargo Denim",
                    "price": 3710,
                    "brand": "Breakout",
                    "description": "Slim relaxed fit cargo denim in cotton, featuring two side, two back, and two cargo pockets for functionality and comfort",
                    "category": "jeans_denim",
                    "features": ["Slim Relaxed", "Cargo Style", "Functional Pockets", "Cotton"]
                },
                {
                    "name": "Mid Length Rtr Girls Stretch Denim Shorts",
                    "price": 499,
                    "brand": "Deeds",
                    "description": "Flex / Stretchable belt High Rise Zip fly Two back pocket Fabric DNA Denim / Jeans 80% Cotton 18% Polyester 2% Elastin",
                    "category": "jeans_denim",
                    "features": ["Stretchable", "High Rise", "80% Cotton", "Girls Shorts"]
                },
                {
                    "name": "Mid Length Ripped Denim Skirt",
                    "price": 499,
                    "brand": "Deeds",
                    "description": "Rigid Zip fly Two back pocket Two front pockets Fabric DNA Denim / Jeans 100% Cotton",
                    "category": "jeans_denim",
                    "features": ["Ripped Style", "Denim Skirt", "100% Cotton", "Front & Back Pockets"]
                },
                {
                    "name": "Skinny Ripped Denim",
                    "price": 1199,
                    "brand": "Deeds",
                    "description": "Two Side Pockets Coin Pocket Two Back Bone-Pockets Stretchable Skinny fit Ripped Premium quality Branded Buttons",
                    "category": "jeans_denim",
                    "features": ["Skinny Fit", "Ripped Style", "Stretchable", "Premium Buttons"]
                },
                {
                    "name": "Skinny fit Vintage Grey Cotton Pant",
                    "price": 999,
                    "brand": "Deeds",
                    "description": "Made in Pakistan Skinny Fit Two Side Pockets Two Back Bone-Pockets Stretchable Fabric: 98% Cotton 2% Elastane",
                    "category": "jeans_denim",
                    "features": ["Vintage Grey", "98% Cotton", "2% Elastane", "Made in Pakistan"]
                },
                {
                    "name": "Light Grey Slim Fit Jeans",
                    "price": 5000,
                    "brand": "Diners",
                    "description": "Diners Denim is Soft and smooth, this denim has an extra-fine weave and is engineered with added stretch for easy mobility. Trouser Type: Casual Color: Light Grey",
                    "category": "jeans_denim",
                    "features": ["Light Grey", "Extra-fine Weave", "Added Stretch", "Casual Type"]
                },
                {
                    "name": "Loose Relaxed Jeans",
                    "price": 6490,
                    "brand": "Outfitters",
                    "description": "Add some edge to your wardrobe with our Faded Black Loose Relaxed Fit Jeans. Made from durable cotton, these jeans offer comfort and versatility. Perfect for any casual or dressy occasion",
                    "category": "jeans_denim",
                    "features": ["Loose Relaxed", "Faded Black", "Durable Cotton", "Versatile"]
                },
                {
                    "name": "Straight Jeans",
                    "price": 5490,
                    "brand": "Outfitters",
                    "description": "These Straight Jeans are the perfect blend of style and comfort. Made with high-quality cotton, they provide a snug fit that will flatter your figure while keeping you comfortable all day long",
                    "category": "jeans_denim",
                    "features": ["Straight Fit", "High-quality Cotton", "Snug Fit", "All Day Comfort"]
                },
                {
                    "name": "Slim Cropped Jeans",
                    "price": 5990,
                    "brand": "Outfitters",
                    "description": "Strut your stuff in these Slim Cropped Jeans that hit all the right notes! The perfect blend fabric hugs your curves while giving you room to groove. These cropped beauties are ready to play nice with your favorite tops",
                    "category": "jeans_denim",
                    "features": ["Slim Cropped", "Perfect Blend Fabric", "Curve Hugging", "Trendy Style"]
                }
            ]
        }
        
        return products
    
    def _create_system_prompt(self) -> str:
        product_catalog = "COMPLETE PRODUCT CATALOG:\n\n"
        
        for category, products in self.products.items():
            category_name = category.replace('_', ' ').title()
            product_catalog += f"=== {category_name.upper()} ===\n"
            
            for product in products:
                product_catalog += f"• {product['name']}\n"
                product_catalog += f"  Price: Rs. {product['price']:,}\n"
                product_catalog += f"  Brand: {product['brand']}\n"
                product_catalog += f"  Description: {product['description']}\n"
                product_catalog += f"  Features: {', '.join(product['features'])}\n\n"
        
        return f"""You are an expert product consultant and sales assistant for an e-commerce store. You have COMPLETE access to our entire product database.

{product_catalog}

IMPORTANT RESPONSE FORMAT:
When recommending products, you MUST use this EXACT format:

• [Product Name]
  Price: Rs. [Exact Price]
  Brand: [Brand Name]  
  Description: [Brief description]
  Features: [Feature1, Feature2, Feature3]

RULES:
- Always mention specific product names and exact prices from the catalog
- Use the bullet point format above for product recommendations
- Be friendly and conversational
- Suggest 2-4 products maximum per response
- Ask follow-up questions to help customers

Remember: You know ALL our products intimately. Always provide specific product recommendations with exact details from the catalog!"""

    def _find_relevant_products(self, user_input: str) -> List[Dict]:
        """Find products relevant to user query"""
        user_input_lower = user_input.lower()
        relevant_products = []
        
        # Brand filtering
        brand_keywords = {
            'apple': ['Apple'],
            'samsung': ['Samsung'],
            'dior': ['Dior'],
            'nivea': ['Nivea'],
            'ponds': ['Ponds'],
            'garnier': ['Garnier'],
            'huawei': ['Huawei'],
            'realme': ['Realme'],
            'vivo': ['Vivo']
        }
        
        for keyword, brands in brand_keywords.items():
            if keyword in user_input_lower:
                for category_products in self.products.values():
                    for product in category_products:
                        if product['brand'] in brands:
                            relevant_products.append(product)
        
        # Category filtering
category_keywords = {
    # Audio & Electronics
    'earbuds': 'earbuds_headphones',
    'headphones': 'earbuds_headphones',
    'airpods': 'earbuds_headphones',
    'audio': 'earbuds_headphones',
    'wireless': 'earbuds_headphones',
    
    # Smartphones
    'phone': 'smartphones',
    'smartphone': 'smartphones',
    'mobile': 'smartphones',
    'iphone': 'smartphones',
    'android': 'smartphones',
    'samsung': 'smartphones',
    'galaxy': 'smartphones',
    
    # Beauty & Cosmetics
    'makeup': 'beauty_cosmetics',
    'cosmetics': 'beauty_cosmetics',
    'beauty': 'beauty_cosmetics',
    'lipstick': 'beauty_cosmetics',
    'foundation': 'beauty_cosmetics',
    'powder': 'beauty_cosmetics',
    'eyeshadow': 'beauty_cosmetics',
    'brow': 'beauty_cosmetics',
    'primer': 'beauty_cosmetics',
    
    # Skincare
    'skincare': 'skincare',
    'face wash': 'skincare',
    'facewash': 'skincare',
    'cleanser': 'skincare',
    'scrub': 'skincare',
    'cleansing': 'skincare',
    'moisturizer': 'skincare',
    
    # Fragrances
    'perfume': 'fragrances',
    'fragrance': 'fragrances',
    'cologne': 'fragrances',
    'scent': 'fragrances',
    'oud': 'fragrances',
    'musk': 'fragrances',
    
    # Men's Clothing
    'mens shirt': 'clothing_men',
    'mens tshirt': 'clothing_men',
    'mens t-shirt': 'clothing_men',
    'mens polo': 'clothing_men',
    'mens clothing': 'clothing_men',
    'men shirt': 'clothing_men',
    'men tshirt': 'clothing_men',
    'men polo': 'clothing_men',
    'polo shirt': 'clothing_men',
    'graphic tee': 'clothing_men',
    
    # Women's Clothing
    'womens shirt': 'clothing_women',
    'womens top': 'clothing_women',
    'womens blouse': 'clothing_women',
    'womens clothing': 'clothing_women',
    'women shirt': 'clothing_women',
    'women top': 'clothing_women',
    'women blouse': 'clothing_women',
    'blouse': 'clothing_women',
    'embroidered': 'clothing_women',
    
    # Smartwatches
    'watch': 'smartwatches',
    'smartwatch': 'smartwatches',
    'smart watch': 'smartwatches',
    'apple watch': 'smartwatches',
    'fitness tracker': 'smartwatches',
    'wearable': 'smartwatches',
    
    # Jeans & Denim
    'jeans': 'jeans_denim',
    'denim': 'jeans_denim',
    'pants': 'jeans_denim',
    'cargo': 'jeans_denim',
    'skinny jeans': 'jeans_denim',
    'straight jeans': 'jeans_denim',
    'baggy jeans': 'jeans_denim',
    'denim shorts': 'jeans_denim',
    'denim skirt': 'jeans_denim'
}
        
        for keyword, category in category_keywords.items():
            if keyword in user_input_lower and category in self.products:
                relevant_products.extend(self.products[category])
        
        # Price filtering
        budget_match = re.search(r'under\s+(\d+)', user_input_lower)
        if budget_match:
            max_price = int(budget_match.group(1))
            if max_price < 1000:
                max_price *= 1000  # Convert to full amount
            relevant_products = [p for p in relevant_products if p['price'] <= max_price]
        
        # If no specific filters, return popular products
        if not relevant_products:
            for category_products in self.products.values():
                relevant_products.extend(category_products[:2])  # Take 2 from each category
        
        # Remove duplicates and limit results
        seen_names = set()
        unique_products = []
        for product in relevant_products:
            if product['name'] not in seen_names:
                unique_products.append(product)
                seen_names.add(product['name'])
                if len(unique_products) >= 6:
                    break
        
        return unique_products

    def _format_product_response(self, products: List[Dict], intro_text: str = "") -> str:
        """Format products in the exact format expected by frontend"""
        if not products:
            return "I can help you find great products! Try asking about specific brands like Apple, Samsung, or categories like earbuds, smartphones."
        
        response = intro_text
        if intro_text and not intro_text.endswith('\n'):
            response += "\n\n"
        
        for product in products[:4]:  # Limit to 4 products
            response += f"• {product['name']}\n"
            response += f"  Price: Rs. {product['price']:,}\n"
            response += f"  Brand: {product['brand']}\n"
            response += f"  Description: {product['description']}\n"
            response += f"  Features: {', '.join(product['features'])}\n\n"
        
        return response.strip()

    def process_query(self, user_input: str, session_id: str = "default") -> str:
        """Process user query with smart product recommendations"""
        
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        user_input_lower = user_input.lower().strip()
        
        # Handle greetings
        greetings = ['hi', 'hello', 'hey', 'sup', 'hii', 'helo']
        if user_input_lower in greetings:
            response = "Hi there! I'm your product expert. I know all about our earbuds, smartphones, clothing, fragrances, skincare, smartwatches, and jeans. What can I help you find today?"
            self.conversations[session_id].append({'user': user_input, 'assistant': response})
            return response
        
        # Handle very short inputs
        if len(user_input.strip()) < 2:
            response = "I'm here to help you find the perfect products! Ask me about anything - comparisons, recommendations, or specific items you're looking for."
            self.conversations[session_id].append({'user': user_input, 'assistant': response})
            return response

        # Handle specific brand queries
        if 'apple' in user_input_lower:
            apple_products = self._find_relevant_products(user_input)
            response = self._format_product_response(
                apple_products, 
                "Here are some excellent Apple products:"
            )
            response += "\n\nWhich Apple product interests you most?"
            self.conversations[session_id].append({'user': user_input, 'assistant': response})
            return response
        
        if 'samsung' in user_input_lower:
            samsung_products = self._find_relevant_products(user_input)
            response = self._format_product_response(
                samsung_products,
                "Here are some great Samsung products:"
            )
            response += "\n\nWould you like more details about any of these Samsung products?"
            self.conversations[session_id].append({'user': user_input, 'assistant': response})
            return response
        
        # Handle category queries
        if any(word in user_input_lower for word in ['earbuds', 'headphones', 'airpods']):
            earbuds_products = self._find_relevant_products(user_input)
            response = self._format_product_response(
                earbuds_products,
                "Here are the best earbuds we have:"
            )
            response += "\n\nWhat's your budget range for earbuds?"
            self.conversations[session_id].append({'user': user_input, 'assistant': response})
            return response
        
        if any(word in user_input_lower for word in ['phone', 'smartphone', 'mobile']):
            phone_products = self._find_relevant_products(user_input)
            response = self._format_product_response(
                phone_products,
                "Here are some excellent smartphones:"
            )
            response += "\n\nAre you looking for any specific features in a smartphone?"
            self.conversations[session_id].append({'user': user_input, 'assistant': response})
            return response
        
        # Handle budget queries
        budget_match = re.search(r'under\s+(\d+)', user_input_lower)
        if budget_match:
            budget_products = self._find_relevant_products(user_input)
            budget = int(budget_match.group(1))
            if budget < 1000:
                budget *= 1000
            response = self._format_product_response(
                budget_products,
                f"Here are great products under Rs. {budget:,}:"
            )
            response += f"\n\nAll these fit perfectly within your Rs. {budget:,} budget!"
            self.conversations[session_id].append({'user': user_input, 'assistant': response})
            return response
        
        # Handle general recommendation queries
        if any(word in user_input_lower for word in ['best', 'recommend', 'suggest', 'show', 'good']):
            general_products = self._find_relevant_products(user_input)
            response = self._format_product_response(
                general_products,
                "Here are some of our best products:"
            )
            response += "\n\nWhat category interests you most?"
            self.conversations[session_id].append({'user': user_input, 'assistant': response})
            return response

        # Try AI API if available, but provide fallback
        try:
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history
            recent_history = self.conversations[session_id][-4:] if len(self.conversations[session_id]) > 4 else self.conversations[session_id]
            for msg in recent_history:
                messages.append({"role": "user", "content": msg['user']})
                messages.append({"role": "assistant", "content": msg['assistant']})
            
            messages.append({"role": "user", "content": user_input})
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 500,
                "top_p": 0.9
            }
            
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            
            if 'choices' in result and result['choices'] and result['choices'][0]['message']['content'].strip():
                ai_response = result['choices'][0]['message']['content'].strip()
                
                # If AI response doesn't have proper format, enhance it
                if '• ' not in ai_response or 'Price: Rs.' not in ai_response:
                    relevant_products = self._find_relevant_products(user_input)
                    ai_response = self._format_product_response(
                        relevant_products,
                        ai_response if len(ai_response) > 20 else "Here are some products that might interest you:"
                    )
                
                self.conversations[session_id].append({'user': user_input, 'assistant': ai_response})
                
                # Clean up conversation history
                if len(self.conversations[session_id]) > 10:
                    self.conversations[session_id] = self.conversations[session_id][-8:]
                
                return ai_response
                
        except Exception as e:
            print(f"AI API error: {str(e)}")
            # Fall through to fallback response

        # Fallback response with actual products
        fallback_products = self._find_relevant_products(user_input)
        response = self._format_product_response(
            fallback_products,
            "I can help you find great products!"
        )
        response += "\n\nTry asking about specific brands like Apple, Samsung, or categories like earbuds, smartphones!"
        
        self.conversations[session_id].append({'user': user_input, 'assistant': response})
        return response

# Initialize chatbot
chatbot = ProductChatbot()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'response': 'Please send a valid message!',
                'session_id': 'error',
                'timestamp': datetime.datetime.now().isoformat()
            }), 400
            
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', f'web_session_{datetime.datetime.now().timestamp()}')
        
        if not user_message:
            return jsonify({
                'response': 'Please ask me about our products! I can help with earbuds, smartphones, fragrances, and more.',
                'session_id': session_id,
                'timestamp': datetime.datetime.now().isoformat()
            })
        
        print(f"Processing query: '{user_message}' for session: {session_id}")
        
        # Process the query
        response_text = chatbot.process_query(user_message, session_id)
        
        print(f"Generated response: {response_text[:100]}...")
        
        return jsonify({
            'response': response_text,
            'session_id': session_id,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'response': 'I can help you find great products! Try asking about Apple, Samsung, earbuds, or smartphones.',
            'session_id': 'error_session',
            'timestamp': datetime.datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy', 
        'service': 'Product Recommendation AI',
        'timestamp': datetime.datetime.now().isoformat(),
        'products_loaded': sum(len(products) for products in chatbot.products.values())
    })

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Product Recommendation Chatbot API',
        'status': 'online',
        'endpoints': {
            'chat': '/api/chat (POST)',
            'health': '/health (GET)'
        },
        'usage': 'Send POST request to /api/chat with {"message": "your message", "session_id": "optional_session_id"}',
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Product Chatbot on port {port}")
    print(f"📦 Loaded {sum(len(products) for products in chatbot.products.values())} products")
    app.run(host='0.0.0.0', port=port, debug=False)
