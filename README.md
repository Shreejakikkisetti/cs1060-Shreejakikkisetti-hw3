# TasteBud

A smart recipe discovery and cooking assistant web application.

## Description

TasteBud helps users discover recipes based on ingredients they already have at home. It features:
- Ingredient-based recipe search
- Step-by-step recipe walkthrough with swipe navigation
- AI-powered ingredient substitution recommendations
- Clean, ad-free interface
- Save favorite recipes
- Ingredient auto-suggestions

## Live Demo

The application is deployed on Netlify and can be accessed at:
[https://tastebud-recipe-finder.netlify.app](https://tastebud-recipe-finder.netlify.app)

## Local Development Setup

1. Create a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python3 app.py
   ```

4. Open your web browser and visit:
   ```
   http://localhost:5000
   ```

## Deployment

This application is configured for deployment on Netlify. To deploy your own instance:

1. Fork this repository

2. Connect your GitHub repository to Netlify:
   - Sign up for a Netlify account
   - Click "New site from Git"
   - Choose your repository
   - Build settings will be automatically configured via netlify.toml

3. The site will be automatically built and deployed

## Technologies Used

- Backend: Python/Flask
- Frontend: HTML5, CSS3 (Tailwind CSS), JavaScript
- Data: JSON (synthetic data for demonstration)
- Deployment: Netlify

## Features

- **Ingredient Search**: Find recipes based on ingredients you have
- **Smart Matching**: Shows match percentage for each recipe
- **Step-by-Step Guide**: Swipeable interface for easy recipe following
- **Substitutions**: AI-powered ingredient substitution suggestions
- **Responsive Design**: Works on desktop and mobile devices
- **Save Favorites**: Like and save your favorite recipes
- **Auto-complete**: Smart ingredient suggestions while typing

## Notes

- This is a prototype focusing on the core user journey
- Data is synthetic and not connected to a real database
- Some features may display "Not implemented" messages
- Error handling is minimal for this prototype version
