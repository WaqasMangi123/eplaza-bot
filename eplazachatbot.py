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
                    "description": "AirPods Max with Good Quality and Active Noise Cancellation.",
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
                    "brand": "Apple",
                    "description": "Wireless. Effortless. Magical. With plenty of talk and listen time, voice-activated Siri access, and wireless charging case. Simply take them out and they are ready to use with all your devices",
                    "category": "earbuds_headphones",
                    "features": ["USB-C", "Wireless Charging", "Siri Access", "Premium Apple"]
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
                    "name": "Samsung Galaxy A16 (256GB)",
                    "price": 61999,
                    "brand": "Samsung",
                    "description": "Discover Samsung Galaxy A16 in Black with 256GB internal storage and explore essential features with Galaxy AI",
                    "category": "smartphones",
                    "features": ["256GB Storage", "Galaxy AI", "Large Storage", "AI Features"]
                },
                {
                    "name": "iPhone 11 Pro Max",
                    "price": 110900,
                    "brand": "Apple",
                    "description": "(Non PTA)Apple looks keen to bring iPhone 11 that is the high-end Pro Max version of the series along with its two other variants",
                    "category": "smartphones",
                    "features": ["Non-PTA", "Pro Max", "High-end", "Premium iOS"]
                },
                {
                    "name": "Vivo V27",
                    "price": 89999,
                    "brand": "Vivo",
                    "description": "Experience the power of 5G with the vivo V27. Featuring MediaTek Dimensity 7200 processor, 4600mAh battery supported with maximum 66W fast charging",
                    "category": "smartphones",
                    "features": ["5G Ready", "66W Fast Charging", "Dimensity 7200", "Good Camera"]
                }
            ],
            
            "fragrances": [
                {
                    "name": "Calvin Klein In2U For Women",
                    "price": 10730,
                    "brand": "Calvin Klein",
                    "description": "Calvin Klein In2U For Women Edt 100Ml",
                    "category": "fragrances",
                    "features": ["Women's Fragrance", "EDT", "100ML", "Designer Brand"]
                },
                {
                    "name": "Dior Sauvage Perfume",
                    "price": 12499,
                    "brand": "Dior",
                    "description": "Dior timeless Sauvage perfume",
                    "category": "fragrances",
                    "features": ["Timeless", "Designer Brand", "Premium", "Long-lasting"]
                },
                {
                    "name": "J. EXCLUSIVE",
                    "price": 4300,
                    "brand": "J.",
                    "description": "Exclusive is a refreshing fragrance for the uber-youth of Pakistan. Its success in the urban centers of Pakistan has made it a household name",
                    "category": "fragrances",
                    "features": ["Youth Fragrance", "Refreshing", "Urban Popular", "Household Name"]
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
            
            "skincare": [
                {
                    "name": "DEEP Cleansing Beard & Face Wash",
                    "price": 999,
                    "brand": "Nivea",
                    "description": "Tough enough for facial hair, but gentle enough for daily use. Formulated with Natural Charcoal, thoroughly cleanses your Beard & Face, masculine Vanilla & Bourbon scent. 100ml",
                    "category": "skincare",
                    "features": ["For Men", "Natural Charcoal", "Beard Care", "Vanilla Bourbon"]
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
                    "name": "Garnier - Men Acno Fight Face Wash",
                    "price": 849,
                    "brand": "Garnier",
                    "description": "Garnier - Men Acno Fight Face Wash - 100ml Fight acne and reveal brighter looking skin. A gentle yet effective face wash for blackheads and acne. 6-in-1 cleaning formula",
                    "category": "skincare",
                    "features": ["6-in-1 Formula", "Acne Fighting", "Blackhead Care", "Gentle"]
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
                    "name": "St London Velvet Lipstick -52 (Blush Pink)",
                    "price": 1410,
                    "brand": "St London",
                    "description": "ST London is a color cosmetic brand that captures the glamorous side of a woman and gives a complete beauty makeover with its wide range from foundations, blush-ons, bronzers, eye liners",
                    "category": "beauty_cosmetics",
                    "features": ["Velvet Texture", "Blush Pink", "Complete Range", "Glamorous"]
                }
            ],
            
            "smartwatches": [
                {
                    "name": "Official Huawei Watch Fit 3",
                    "price": 39999,
                    "brand": "Huawei",
                    "description": "Sleek Design Vibrant Display Comfortable Wear Heart Rate Monitoring SpO2 Tracking Advanced Sleep Analysis Stress Management Workout Modes Smart Notifications Long Battery Life",
                    "category": "smartwatches",
                    "features": ["Official Huawei", "Heart Rate", "SpO2", "Advanced Sleep", "Long Battery"]
                },
                {
                    "name": "Apple Watch Series 10",
                    "price": 109999,
                    "brand": "Apple",
                    "description": "Apple Watch Series 10 46mm Silver Aluminium Case With Denim Sports Band. Thinnest Apple Watch ever, with our biggest display New depth and water temperature sensors",
                    "category": "smartwatches",
                    "features": ["Thinnest Ever", "Biggest Display", "Water Sensors", "Denim Band"]
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
            'earbuds': 'earbuds_headphones',
            'headphones': 'earbuds_headphones',
            'airpods': 'earbuds_headphones',
            'phone': 'smartphones',
            'smartphone': 'smartphones',
            'mobile': 'smartphones',
            'perfume': 'fragrances',
            'fragrance': 'fragrances',
            'skincare': 'skincare',
            'face wash': 'skincare',
            'makeup': 'beauty_cosmetics',
            'cosmetics': 'beauty_cosmetics',
            'watch': 'smartwatches',
            'smartwatch': 'smartwatches'
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
