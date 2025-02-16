from flask import Flask, render_template, request, jsonify, session
import json
import os
from difflib import SequenceMatcher
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Get the absolute path to the data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Load recipe data
def load_recipes():
    try:
        with open(os.path.join(DATA_DIR, 'recipes.json'), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_common_ingredients():
    try:
        with open(os.path.join(DATA_DIR, 'common_ingredients.json'), 'r') as f:
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

# Ingredient substitutions database
ingredient_substitutions = {
    'flour': ['almond flour', 'coconut flour', 'oat flour', 'whole wheat flour'],
    'sugar': ['honey', 'maple syrup', 'stevia', 'coconut sugar', 'agave nectar'],
    'eggs': ['applesauce', 'mashed banana', 'flax egg', 'chia egg', 'commercial egg replacer'],
    'butter': ['olive oil', 'coconut oil', 'applesauce', 'mashed avocado', 'greek yogurt'],
    'milk': ['almond milk', 'soy milk', 'oat milk', 'coconut milk', 'cashew milk'],
    'cream': ['coconut cream', 'cashew cream', 'silken tofu', 'evaporated milk'],
    'vanilla extract': ['vanilla bean', 'vanilla powder', 'maple syrup', 'almond extract'],
    'baking powder': ['mix of baking soda and cream of tartar', 'club soda', 'self-rising flour'],
    'soy sauce': ['coconut aminos', 'tamari', 'worcestershire sauce', 'fish sauce'],
    'garlic': ['garlic powder', 'shallots', 'garlic chives', 'asafoetida'],
    'onion': ['shallots', 'leeks', 'celery', 'onion powder'],
    'tomatoes': ['red bell peppers', 'pumpkin puree', 'carrots', 'beets'],
    'cheese': ['nutritional yeast', 'tofu', 'cashew cheese', 'coconut cheese'],
    'rice': ['quinoa', 'cauliflower rice', 'bulgur', 'couscous'],
    'pasta': ['zucchini noodles', 'spaghetti squash', 'shirataki noodles', 'chickpea pasta'],
    'beef': ['mushrooms', 'lentils', 'jackfruit', 'tempeh'],
    'chicken': ['tofu', 'chickpeas', 'seitan', 'tempeh'],
    'fish': ['hearts of palm', 'jackfruit', 'tofu', 'tempeh'],
    'breadcrumbs': ['crushed crackers', 'oats', 'ground nuts', 'crushed cornflakes']
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipes = load_recipes()
    recipe = next((r for r in recipes if str(r['id']) == str(recipe_id)), None)
    if recipe:
        liked_recipes = session.get('liked_recipes', [])
        return render_template('recipe.html', recipe=recipe, liked_recipes=liked_recipes)
    return 'Recipe not found', 404

@app.route('/api/recipes/search', methods=['POST'])
def search_recipes():
    data = request.get_json()
    user_ingredients = set(ingredient.lower() for ingredient in data.get('ingredients', []))
    
    recipes = load_recipes()
    matching_recipes = []
    
    for recipe in recipes:
        recipe_ingredients = set(ingredient.lower() for ingredient in recipe['ingredients'])
        match_percentage = calculate_match_percentage(user_ingredients, recipe['ingredients'])
        
        recipe_copy = recipe.copy()
        recipe_copy['match_percentage'] = match_percentage
        matching_recipes.append(recipe_copy)
    
    # Sort recipes by match percentage
    matching_recipes.sort(key=lambda x: x['match_percentage'], reverse=True)
    
    return jsonify(matching_recipes)

@app.route('/api/common-ingredients')
def get_common_ingredients():
    ingredients = load_common_ingredients()
    return jsonify(ingredients)

@app.route('/api/recipes/liked')
def get_liked_recipes():
    recipes = load_recipes()
    liked_recipes = session.get('liked_recipes', [])
    liked_recipes = [r for r in recipes if str(r['id']) in liked_recipes]
    return jsonify(liked_recipes)

@app.route('/api/recipes/<recipe_id>/like', methods=['POST'])
def like_recipe(recipe_id):
    try:
        # Convert recipe_id to string for consistent comparison
        recipe_id = str(recipe_id)
        
        # Initialize liked_recipes in session if not present
        if 'liked_recipes' not in session:
            session['liked_recipes'] = []
        
        # Verify recipe exists
        recipes = load_recipes()
        recipe_exists = any(str(r['id']) == recipe_id for r in recipes)
        if not recipe_exists:
            return jsonify({"error": "Recipe not found"}), 404
            
        liked_recipes = session['liked_recipes']
        if recipe_id in liked_recipes:
            liked_recipes.remove(recipe_id)
            session['liked_recipes'] = liked_recipes
            return jsonify({"status": "unliked"})
        else:
            liked_recipes.append(recipe_id)
            session['liked_recipes'] = liked_recipes
            return jsonify({"status": "liked"})
    except Exception as e:
        print(f"Error in like_recipe: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ingredients/suggest')
def suggest_ingredients():
    query = request.args.get('q', '').lower()
    common_ingredients = load_common_ingredients()
    suggestions = [i for i in common_ingredients if query in i.lower()][:5]
    return jsonify(suggestions)

@app.route('/api/ingredients/substitutions')
def get_substitutions():
    ingredient = request.args.get('ingredient', '').lower()
    
    # Try exact match first
    if ingredient in ingredient_substitutions:
        return jsonify(ingredient_substitutions[ingredient])
    
    # Try partial match
    for key in ingredient_substitutions:
        if key in ingredient or ingredient in key:
            return jsonify(ingredient_substitutions[key])
    
    # If no match found, return empty list
    return jsonify([])

@app.route('/api/substitutions', methods=['POST'])
def get_substitutions_post():
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
    port = int(os.environ.get('PORT', 8084))  # Default to 8084, but allow override via environment
    app.run(debug=True, port=port)
