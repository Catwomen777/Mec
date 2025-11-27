from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError 
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from config import DevelopmentConfig
import os



SECRET_KEY = os.environ.get("SECRET_KEY") or "super secret secret"

def encode_token(customer_id):
    try:
    

        payload = {
        'exp': datetime.now(tz=timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(tz=timezone.utc),
        'sub': str(customer_id)
    }
        secret = current_app.config.get("SECRET_KEY", SECRET_KEY)
        token = jwt.encode(payload, secret, algorithm="HS256")
        return token
   
    except Exception as e:
        return str(e)
    
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get('Authorization')

        # If missing entirely → unauthorized
        if not auth_header:
            return jsonify({'message': 'Token is missing!'}), 401

        # Split the header (e.g. "Bearer <token>")
        parts = auth_header.split()

        # Wrong format
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'message': 'Token is missing!'}), 401

        token = parts[1]

        try:
            secret = current_app.config.get("SECRET_KEY") or "super-secret-key"
            data = jwt.decode(token, secret, algorithms=['HS256'])
            request.customer_id = int(data.get('sub'))
        
        except ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401

        except JWTError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated
