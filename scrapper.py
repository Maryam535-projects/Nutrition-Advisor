import requests
from bs4 import BeautifulSoup
import json
import time
import re
from fake_useragent import UserAgent

class NutritionScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.cache = {}
        self.load_cache()
    
    def load_cache(self):
        try:
            with open('nutrition_cache.json', 'r') as f:
                self.cache = json.load(f)
        except:
            self.cache = {}
    
    def save_cache(self):
        with open('nutrition_cache.json', 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get_nutrition_data(self, food_item):
        """Get nutrition data for a food item"""
        food_key = food_item.lower().strip()
        
        # Check cache first
        if food_key in self.cache:
            return self.cache[food_key]
        
        # Try different data sources
        nutrition_data = self.scrape_usda(food_key) or \
                        self.scrape_myfitnesspal(food_key) or \
                        self.scrape_wikipedia(food_key) or \
                        self.generate_ai_data(food_key)
        
        if nutrition_data:
            self.cache[food_key] = nutrition_data
            self.save_cache()
        
        return nutrition_data
    
    def scrape_usda(self, food_item):
        """Scrape USDA nutrition data (simulated)"""
        try:
            # Simulated USDA scraping
            usda_data = {
                'apple': {'calories': 52, 'carbs': 14, 'protein': 0.3, 'fat': 0.2},
                'banana': {'calories': 89, 'carbs': 23, 'protein': 1.1, 'fat': 0.3},
                'chicken breast': {'calories': 165, 'carbs': 0, 'protein': 31, 'fat': 3.6},
                'broccoli': {'calories': 34, 'carbs': 7, 'protein': 2.8, 'fat': 0.4},
                'rice': {'calories': 130, 'carbs': 28, 'protein': 2.7, 'fat': 0.3}
            }
            
            for key in usda_data:
                if key in food_item:
                    return usda_data[key]
            
            return None
        except:
            return None
    
    def scrape_myfitnesspal(self, food_item):
        """Scrape MyFitnessPal data (simulated)"""
        # This is simulated - actual implementation would use proper web scraping
        return None
    
    def scrape_wikipedia(self, food_item):
        """Scrape Wikipedia for nutrition info"""
        try:
            url = f"https://en.wikipedia.org/wiki/{food_item.replace(' ', '_')}"
            headers = {'User-Agent': self.ua.random}
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for nutrition tables
                tables = soup.find_all('table', {'class': 'infobox'})
                for table in tables:
                    text = table.get_text().lower()
                    if 'nutrition' in text or 'calories' in text:
                        # Parse nutrition data
                        nutrition = self.parse_nutrition_table(table)
                        if nutrition:
                            return nutrition
            
            return None
        except:
            return None
    
    def parse_nutrition_table(self, table):
        """Parse nutrition table from Wikipedia"""
        # Simplified parsing - actual implementation would be more robust
        rows = table.find_all('tr')
        nutrition = {}
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                key = cells[0].get_text().strip().lower()
                value = cells[1].get_text().strip()
                
                if 'calorie' in key:
                    numbers = re.findall(r'\d+', value)
                    if numbers:
                        nutrition['calories'] = int(numbers[0])
                elif 'carb' in key:
                    numbers = re.findall(r'\d+', value)
                    if numbers:
                        nutrition['carbs'] = int(numbers[0])
                elif 'protein' in key:
                    numbers = re.findall(r'\d+', value)
                    if numbers:
                        nutrition['protein'] = int(numbers[0])
                elif 'fat' in key:
                    numbers = re.findall(r'\d+', value)
                    if numbers:
                        nutrition['fat'] = int(numbers[0])
        
        return nutrition if nutrition else None
    
    def generate_ai_data(self, food_item):
        """Generate nutrition data using AI rules"""
        # Food category mapping
        categories = {
            'fruit': {'calories': 50, 'carbs': 12, 'protein': 0.5, 'fat': 0.2},
            'vegetable': {'calories': 25, 'carbs': 5, 'protein': 2, 'fat': 0.3},
            'protein': {'calories': 150, 'carbs': 0, 'protein': 25, 'fat': 5},
            'grain': {'calories': 100, 'carbs': 20, 'protein': 3, 'fat': 1},
            'dairy': {'calories': 80, 'carbs': 5, 'protein': 4, 'fat': 5},
            'snack': {'calories': 200, 'carbs': 25, 'protein': 2, 'fat': 10}
        }
        
        # Determine category
        category = self.categorize_food(food_item)
        base_data = categories.get(category, categories['fruit'])
        
        # Add some variation
        import random
        return {
            'calories': base_data['calories'] + random.randint(-10, 20),
            'carbs': base_data['carbs'] + random.randint(-2, 5),
            'protein': base_data['protein'] + random.randint(-1, 3),
            'fat': base_data['fat'] + random.randint(0, 2),
            'category': category,
            'source': 'ai_generated'
        }
    
    def categorize_food(self, food_item):
        """Categorize food item"""
        food_lower = food_item.lower()
        
        categories = {
            'fruit': ['apple', 'banana', 'orange', 'berry', 'grape', 'melon', 'mango'],
            'vegetable': ['broccoli', 'spinach', 'carrot', 'tomato', 'lettuce', 'cabbage'],
            'protein': ['chicken', 'beef', 'fish', 'egg', 'meat', 'pork', 'tofu'],
            'grain': ['rice', 'bread', 'pasta', 'wheat', 'oats', 'cereal'],
            'dairy': ['milk', 'cheese', 'yogurt', 'butter', 'cream'],
            'snack': ['chips', 'chocolate', 'cookie', 'cake', 'candy']
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in food_lower:
                    return category
        
        return 'other'
    
    def search_foods(self, query):
        """Search for foods matching query"""
        results = []
        query_lower = query.lower()
        
        for food, data in self.cache.items():
            if query_lower in food.lower():
                results.append({
                    'name': food.title(),
                    'calories': data.get('calories', 0),
                    'category': data.get('category', 'unknown').title()
                })
        
        return results[:10]

# Example usage
if __name__ == '__main__':
    scraper = NutritionScraper()
    
    # Test scraping
    foods = ['apple', 'chicken breast', 'broccoli', 'pizza']
    
    for food in foods:
        data = scraper.get_nutrition_data(food)
        print(f"{food}: {data}")