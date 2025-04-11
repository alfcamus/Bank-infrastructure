from flask import Flask, request, jsonify
from functools import wraps
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper decorator for JSON APIs
def json_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
            return jsonify({
                'success': True,
                'data': response
            })
        except Exception as e:
            logger.error(f"API error: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    return decorated_function

# Health check endpoint
@app.route('/health', methods=['GET'])
@json_api
def health_check():
    """Simple health check endpoint"""
    return {'status': 'healthy', 'version': '1.0.0'}

# Example CRUD endpoint
@app.route('/api/items/<item_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@json_api
def items(item_id):
    """Example endpoint with multiple methods"""
    if request.method == 'GET':
        # Retrieve item logic
        return {'item_id': item_id, 'method': 'GET'}
    
    elif request.method == 'POST':
        # Create item logic
        data = request.get_json()
        return {'item_id': item_id, 'data': data, 'method': 'POST'}
    
    elif request.method == 'PUT':
        # Update item logic
        data = request.get_json()
        return {'item_id': item_id, 'data': data, 'method': 'PUT'}
    
    elif request.method == 'DELETE':
        # Delete item logic
        return {'item_id': item_id, 'method': 'DELETE'}

# Error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)