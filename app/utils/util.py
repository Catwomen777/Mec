from jose import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify


SECRET_KEY = "your_secret_key"

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(tz=timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(tz=timezone.utc),
        'sub': customer_id
    }
    
def encode_token(service_ticket_id):
    payload = {
        'exp': datetime.now(tz=timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(tz=timezone.utc),
        'sub': service_ticket_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'authorization' in request.headers:
            token = request.headers['authorization'].split(" ")[1]
            
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.customer_id = int(data['sub'])  
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(*args, **kwargs)
    
    return decorated
        
            