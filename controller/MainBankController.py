from flask import Flask, request, jsonify
from functools import wraps
from service.ClientService import ClientService
from service.AccountService import AccountService
import logging
from model.Account import Account
from model.Client import Client
# Initialize Flask app
app = Flask(__name__)
client_service = ClientService()
account_service = AccountService()
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
    client_service.add_client({'name': "Artur", "pesel": "12345678913"})
    return {'status': 'healthy', 'version': '1.0.0'}


# todo: add client logic

# Example CRUD endpoint
@app.route('/api/clients/client', methods=['GET', 'POST', 'PUT', 'DELETE'])
@json_api
def clients():
    """Example endpoint with multiple methods"""
    if request.method == 'GET':
        # Retrieve item 
        client_id = request.args.get('id')
        client = client_service.get_client(client_id)
        return {'client': client.to_dict(), 'method': 'GET'}

    elif request.method == 'POST':
        # Create item logic
        data = request.get_json()
        client = Client(None, data["name"], data["pesel"], None)
        client_service.add_client(client)

    elif request.method == 'PUT':
        # Update item logic
        data = request.get_json()
        return {'item_id': client_id, 'data': data, 'method': 'PUT'}

    elif request.method == 'DELETE':
        # Delete item logic
        return {'item_id': client_id, 'method': 'DELETE'}
    
@app.route('/api/accounts/account', methods=['GET', 'POST', 'PUT', 'DELETE'])
@json_api
def accounts():
    """Example endpoint with multiple methods"""
    if request.method == 'GET':
        # Retrieve item 
        client_id = request.args.get('client_id')
        account = account_service.get_account_by_client_id(client_id)
        return {'account': account.to_dict(), 'method': 'GET'}

    elif request.method == 'POST':
        # Create item logic
        data = request.get_json()
        account = Account(data["client_id"], None, data["balance"], data["account_type"], None)
        account_service.add_account(account)

    elif request.method == 'PUT':
        # Update item logic
        data = request.get_json()
        return {'item_id': client_id, 'data': data, 'method': 'PUT'}

    elif request.method == 'DELETE':
        account_id = request.args.get('id')
        account_service.delete_account(account_id)


# Error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
