"""
Main Flask application module for AcademiaVeritas project.

This module initializes the Flask application, registers blueprints,
and configures the application for production use.
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config  # Ensure config.py exists and defines a 'config' dictionary or object
from routes.auth_routes import auth_bp, google_bp_institution, google_bp_verifier

from routes.certificate_routes import cert_bp


def create_app(config_name=None):
    """
    Application factory pattern for creating Flask app instances.
    
    Args:
        config_name (str): Configuration environment name
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.getenv('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])

    # Initialize CORS
    cors_origins = app.config.get('CORS_ORIGINS', '*')
    CORS(app, origins=cors_origins)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(cert_bp)
    app.register_blueprint(google_bp_institution, url_prefix="/api/institution/google")
    app.register_blueprint(google_bp_verifier, url_prefix="/api/verifier/google")
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Method not allowed'}), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'AcademiaVeritas API is running'
        }), 200
    
    return app


# Create the application instance
app = create_app()


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )
