# TasteBud - Recipe Discovery Web App

A smart recipe finder that helps users cook with ingredients they already have at home.

## Project Setup
This project exists in two repositories:
1. Assignment submission: https://github.com/cs1060/Shreejakikkisetti-hw3 (private, for grading)
2. Deployment: Create your own private repository and deploy to Vercel

## Features
- Ingredient-based recipe search
- Dynamic recipe matching with percentage
- Auto-complete ingredient suggestions
- Step-by-step recipe instructions
- Ingredient substitution recommendations
- Save/Like recipes feature
- Real-time ingredient auto-suggestions
- Detailed recipe instructions with measurements

## Local Development
1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open http://localhost:8080 in your browser

## Deployment Instructions
1. Create a new private repository in your personal GitHub account
2. Push the code to your new repository
3. Go to [Vercel](https://vercel.com) and sign up/login with GitHub
4. Click "New Project"
5. Import your private repository
6. Vercel will auto-detect the Python settings
7. Click "Deploy"

## Example Usage

Here are some ways to test and use TasteBud:

### 1. Finding Recipes with Available Ingredients
Let's say you have these ingredients in your kitchen:
- Chicken
- Rice
- Garlic
- Onion

Simply type these ingredients into the search bar (one at a time) and click "Add". TasteBud will show you recipes that match your ingredients, sorted by how well they match. You might discover recipes like "Chicken Fried Rice" or "Garlic Chicken with Rice".

### 2. Saving Your Favorite Recipes
Found a recipe you love? Here's how to save it:
1. Click on any recipe to view its details
2. Click the heart icon (🤍) to save it
3. Access your saved recipes anytime by clicking "Saved Recipes" in the navigation bar
4. To remove a recipe from your favorites, click the heart icon again (❤️)

### 3. Finding Ingredient Substitutions
Out of an ingredient? TasteBud can help:
1. Open any recipe
2. Click on any ingredient in the list
3. Click "Find Substitute"
4. You'll see alternative ingredients you can use instead

For example:
- No eggs? Try mashed banana or applesauce
- Out of butter? Use olive oil or coconut oil
- No milk? Almond milk or soy milk work great

### 4. Recipe Search Examples
Try these search combinations:
- For breakfast: "eggs, bread, butter"
- For a quick dinner: "pasta, tomatoes, garlic"
- For dessert: "flour, sugar, vanilla"
- For vegetarian options: "tofu, rice, vegetables"

### 5. Using the Step-by-Step Instructions
When viewing a recipe:
1. Start with the ingredient list to ensure you have everything
2. Click "Start Cooking" to begin
3. Use the arrow keys or swipe to navigate between steps
4. Each step is timed to help you stay on track

### Tips
- Add ingredients one at a time for better matching
- The more ingredients you add, the more precise your matches will be
- Save recipes before starting to cook for easy access later
- Check the substitutions feature if you're missing an ingredient
- Look at the match percentage to see how well a recipe fits your available ingredients

## Technologies Used
- Backend: Python Flask
- Frontend: HTML5, Tailwind CSS, Vanilla JavaScript
- Deployment: Vercel
- Data Storage: JSON files

## Author
Shreeja Kikkisetti
