from flask import Flask, render_template, request, jsonify
import json
import os
from difflib import SequenceMatcher

app = Flask(__name__)

# Load recipe data
def load_recipes():
    try:
        with open('data/recipes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_liked_recipes():
    try:
        with open('data/liked_recipes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_liked_recipes(liked_recipes):
    with open('data/liked_recipes.json', 'w') as f:
        json.dump(liked_recipes, f, indent=2)

def load_common_ingredients():
    try:
        with open('data/common_ingredients.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Calculate ingredient match percentage
def calculate_match_percentage(available_ingredients, recipe_ingredients):
    available_ingredients = [i.lower().strip() for i in available_ingredients]
    recipe_ingredients = [i.lower().strip() for i in recipe_ingredients]
    
    matches = sum(1 for i in recipe_ingredients if any(
        SequenceMatcher(None, i, avail).ratio() > 0.8 
        for avail in available_ingredients
    ))
    return int((matches / len(recipe_ingredients)) * 100)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipes = load_recipes()
    recipe = next((r for r in recipes if r['id'] == recipe_id), None)
    
    if recipe is None:
        return "Recipe not found", 404
        
    return render_template('recipe.html', recipe=recipe)

@app.route('/api/recipes/search', methods=['POST'])
def search_recipes():
    data = request.get_json()
    if not data or 'ingredients' not in data:
        return jsonify({'error': 'No ingredients provided'}), 400
    
    ingredients = data['ingredients']
    recipes = load_recipes()
    
    matching_recipes = []
    for recipe in recipes:
        match_percentage = calculate_match_percentage(ingredients, recipe['ingredients'])
        if match_percentage > 0:
            recipe_copy = recipe.copy()
            recipe_copy['match_percentage'] = match_percentage
            matching_recipes.append(recipe_copy)
    
    matching_recipes.sort(key=lambda x: x['match_percentage'], reverse=True)
    return jsonify(matching_recipes)

@app.route('/api/recipes/<int:recipe_id>/like', methods=['POST'])
def like_recipe(recipe_id):
    liked_recipes = load_liked_recipes()
    if recipe_id not in liked_recipes:
        liked_recipes.append(recipe_id)
        save_liked_recipes(liked_recipes)
        return jsonify({"status": "liked"})
    return jsonify({"status": "already_liked"})

@app.route('/api/recipes/<int:recipe_id>/unlike', methods=['POST'])
def unlike_recipe(recipe_id):
    liked_recipes = load_liked_recipes()
    if recipe_id in liked_recipes:
        liked_recipes.remove(recipe_id)
        save_liked_recipes(liked_recipes)
        return jsonify({"status": "unliked"})
    return jsonify({"status": "not_liked"})

@app.route('/api/recipes/liked')
def get_liked_recipes():
    liked_recipe_ids = load_liked_recipes()
    recipes = load_recipes()
    liked_recipes = [r for r in recipes if r['id'] in liked_recipe_ids]
    return jsonify(liked_recipes)

@app.route('/api/ingredients/suggest')
def suggest_ingredients():
    query = request.args.get('q', '').lower()
    common_ingredients = load_common_ingredients()
    suggestions = [i for i in common_ingredients if query in i.lower()][:5]
    return jsonify(suggestions)

@app.route('/api/substitutions', methods=['POST'])
def get_substitutions():
    data = request.get_json()
    if not data or 'ingredient' not in data:
        return jsonify({'error': 'No ingredient provided'}), 400
        
    # Synthetic substitution data
    substitutions = {
        'butter': ['oil', 'applesauce', 'mashed banana'],
        'eggs': ['mashed banana', 'applesauce', 'flax seeds'],
        'milk': ['almond milk', 'soy milk', 'oat milk'],
        'flour': ['almond flour', 'coconut flour', 'oat flour'],
        'sugar': ['honey', 'maple syrup', 'stevia'],
        'oil': ['applesauce', 'mashed banana', 'greek yogurt']
    }
    
    ingredient = data['ingredient'].lower().strip()
    return jsonify(substitutions.get(ingredient, []))

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Create sample recipe data if it doesn't exist
    if not os.path.exists('data/recipes.json'):
        sample_recipes = [
            {
                "id": 1,
                "name": "Classic Pancakes",
                "description": "Light and fluffy pancakes perfect for breakfast",
                "ingredients": [
                    "2 cups all-purpose flour",
                    "2 1/4 cups milk",
                    "2 large eggs",
                    "3 tablespoons sugar",
                    "2 1/2 teaspoons baking powder",
                    "1/2 teaspoon salt",
                    "3 tablespoons melted butter"
                ],
                "steps": [
                    "In a large bowl, whisk together flour, sugar, baking powder, and salt",
                    "In another bowl, whisk milk, eggs, and melted butter until well combined",
                    "Pour wet ingredients into dry ingredients and whisk until just mixed (some small lumps are okay)",
                    "Heat a non-stick pan or griddle over medium heat",
                    "Pour about 1/4 cup batter for each pancake and cook until bubbles form on top",
                    "Flip and cook other side until golden brown (about 1-2 minutes)"
                ],
                "time": "20 minutes",
                "difficulty": "Easy",
                "servings": 4
            },
            {
                "id": 2,
                "name": "Vegetable Stir-Fry",
                "description": "Quick and healthy vegetable stir-fry with a savory sauce",
                "ingredients": [
                    "2 cups broccoli florets",
                    "2 medium carrots, sliced",
                    "1 large bell pepper, sliced",
                    "1 medium onion, sliced",
                    "3 cloves garlic, minced",
                    "1/4 cup soy sauce",
                    "2 tablespoons vegetable oil",
                    "1 tablespoon fresh ginger, grated",
                    "1 tablespoon cornstarch",
                    "1/4 cup water",
                    "1/2 teaspoon sesame oil (optional)"
                ],
                "steps": [
                    "Cut all vegetables into similar-sized pieces for even cooking",
                    "Mix soy sauce, cornstarch, and water in a small bowl; set aside",
                    "Heat vegetable oil in a wok or large pan over medium-high heat",
                    "Add garlic and ginger, stir-fry for 30 seconds until fragrant",
                    "Add onions and carrots, stir-fry for 2 minutes",
                    "Add broccoli and bell peppers, cook for 3-4 minutes until crisp-tender",
                    "Pour sauce mixture over vegetables, stir until thickened (about 1 minute)",
                    "Drizzle with sesame oil if using, serve hot over rice"
                ],
                "time": "25 minutes",
                "difficulty": "Easy",
                "servings": 4
            },
            {
                "id": 3,
                "name": "Chocolate Chip Cookies",
                "description": "Classic chewy chocolate chip cookies with crispy edges",
                "ingredients": [
                    "2 1/4 cups all-purpose flour",
                    "1 cup unsalted butter, softened",
                    "3/4 cup granulated sugar",
                    "3/4 cup packed brown sugar",
                    "2 large eggs",
                    "1 teaspoon vanilla extract",
                    "1 teaspoon baking soda",
                    "1/2 teaspoon salt",
                    "2 cups semi-sweet chocolate chips",
                    "1/2 cup chopped nuts (optional)"
                ],
                "steps": [
                    "Preheat oven to 375°F (190°C) and line baking sheets with parchment paper",
                    "In a bowl, whisk together flour, baking soda, and salt",
                    "In a large bowl, cream together softened butter, brown sugar, and granulated sugar until fluffy (about 2-3 minutes)",
                    "Beat in eggs one at a time, then stir in vanilla extract",
                    "Gradually mix in the dry ingredients until just combined",
                    "Fold in chocolate chips and nuts if using",
                    "Drop rounded tablespoons of dough onto prepared baking sheets, 2 inches apart",
                    "Bake for 9-11 minutes or until edges are lightly browned",
                    "Let cool on baking sheets for 5 minutes before transferring to wire racks"
                ],
                "time": "30 minutes",
                "difficulty": "Medium",
                "servings": 24
            }
        ]
        
        with open('data/recipes.json', 'w') as f:
            json.dump(sample_recipes, f, indent=2)
    
    # Create initial liked recipes file if it doesn't exist
    if not os.path.exists('data/liked_recipes.json'):
        with open('data/liked_recipes.json', 'w') as f:
            json.dump([], f)
    
    # Create common ingredients file if it doesn't exist
    if not os.path.exists('data/common_ingredients.json'):
        common_ingredients = [
            "flour", "sugar", "salt", "butter", "eggs", "milk", 
            "olive oil", "garlic", "onion", "pepper", "tomatoes",
            "chicken", "beef", "rice", "pasta", "cheese", "carrots",
            "potatoes", "celery", "mushrooms", "bell peppers",
            "soy sauce", "vinegar", "honey", "lemon", "lime",
            "cinnamon", "vanilla", "baking powder", "baking soda"
        ]
        with open('data/common_ingredients.json', 'w') as f:
            json.dump(common_ingredients, f, indent=2)
    
    app.run(debug=True, port=8080)
