from flask import Flask, jsonify
from netlify_lambda_wsgi import make_aws_lambda_wsgi_handler

app = Flask(__name__)

# Import your Flask app
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app import app as flask_app

# Create handler for AWS Lambda
handler = make_aws_lambda_wsgi_handler(flask_app)
