"""
Credit Risk Intelligence System — Enterprise Entry Point
A modular Flask application with SHAP explainability and a premium dashboard.
"""

from flask import Flask
from config import SECRET_KEY, DEBUG, PORT
from routes.dashboard import dashboard_bp
from routes.predict import predict_bp
from routes.shap_api import shap_bp
from routes.simulate import simulate_bp
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    # Register Blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(shap_bp)
    app.register_blueprint(simulate_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=DEBUG, port=PORT)