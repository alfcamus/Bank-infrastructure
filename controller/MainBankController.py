from flask import Flask, request, jsonify
from functools import wraps
from service.ClientService import ClientService
from service.AccountService import AccountService
from service.TransactionService import TransactionService
import logging
from model.Account import Account
from model.Client import Client
from model.Transaction import Transaction

# Initialize Flask app
app = Flask(__name__)
account_service = AccountService()
client_service = ClientService(account_service)
transaction_service = TransactionService()
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# TODO for frontend app: add simple authentication in backend ->
# use sha-256 to hash password on registration
# main id: client id, but for purpose of registration generate login
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

    elif request.method == "POST" and request.args.get("check_password"):
        data = request.get_json()
        if client_service.check_password(data ["login"], data ["password"]):
            return {"success": "True"}
        else:
            return {"success": "False"}
        
    elif request.method == 'POST':
        # Create item logic
        data = request.get_json()
        client = Client(None, data["name"], data["surname"], data["pesel"], None, None, data["password"])
        client_service.add_client(client)

    elif request.method == 'PUT':
        # Update item logic
        data = request.get_json()
        return {'item_id': client_id, 'data': data, 'method': 'PUT'}

    elif request.method == 'DELETE':
        client_id = request.args.get('id')
        client_service.delete_client(client_id)


@app.route('/api/accounts/account', methods=['GET', 'POST', 'PUT', 'DELETE'])
@json_api
def accounts():
    """Example endpoint with multiple methods"""
    if request.method == 'GET':
        # Retrieve item 
        client_id = request.args.get('client_id')
        account = account_service.get_accounts_by_client_id(client_id)
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


@app.route('/api/transactions/transaction', methods=['GET', 'POST'])
@json_api
def transactions():
    """Example endpoint with multiple methods"""
    if request.method == 'GET':
        # Retrieve item 
        transaction_id = request.args.get('id')
        transaction = transaction_service.get_transaction_by_id(transaction_id)
        return {'account': transaction.to_dict(), 'method': 'GET'}

    elif request.method == 'POST':
        # Create item logic
        data = request.get_json()
        transaction = Transaction(data["source_account"], data["value"], data["transfer_type"], None)
        transaction_service.add_transaction(transaction)


# Error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(500)
def not_found(error):
    return jsonify({'success': False, 'error': 'Not found'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
