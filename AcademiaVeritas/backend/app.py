"""
Main Flask application module for AcademiaVeritas project.
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from routes.auth_routes import auth_bp, google_bp_institution, google_bp_verifier
from routes.certificate_routes import cert_bp

def create_app(config_name=None):
    """Application factory for creating Flask app instances."""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.getenv('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    # Set SECRET_KEY for Flask-Dance
    app.secret_key = app.config['SECRET_KEY']

    # Initialize CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', '*'))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(cert_bp)
    app.register_blueprint(google_bp_institution)
    app.register_blueprint(google_bp_verifier)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy'}), 200
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )

