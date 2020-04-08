import json
from six.moves.urllib.request import urlopen,Request
from functools import wraps
import sys

from flask import Flask, request, jsonify, _request_ctx_stack
from flask_cors import cross_origin
from jose import jwt
from flask_mysqldb import MySQL

AUTH0_DOMAIN = 'AUTH0_Domain'
API_AUDIENCE = "#YOUR_API_AUDIENCE"
ALGORITHMS = ["RS256"]

APP = Flask(__name__)

APP.config['MYSQL_HOST'] = '127.0.0.1'
APP.config['MYSQL_USER'] = 'root'
APP.config['MYSQL_PASSWORD'] = 'dropapp_root'
APP.config['MYSQL_DB'] = 'dropapp_dev'
APP.config['MYSQL_PORT'] = 32000

mysql = MySQL(APP)

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@APP.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        ###This part modifies the original auth0 documentation to make a request for the email
        req = Request("https://"+AUTH0_DOMAIN+"/userinfo")
        req.add_header('Authorization',"Bearer "+ token)
        user_info = urlopen(req).read()
        content = json.loads(user_info)
        kwargs['email']=content['email']
        ###Standar code resumes
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated

def query(sql,options):
    cur = mysql.connection.cursor()
    cur.execute(sql,(options))
    mysql.connection.commit()
    data = jsonify(cur.fetchall())
    cur.close()
    return data

def get_credentials(email):
    querystring = "select cu.id,cu.naam,cu.email,o.label as organisation_label,o.id as organisation_id from cms_users as cu left join organisations as o on cu.organisation_id=o.id where cu.email=%s"
    userdata = query(querystring,[email])
    userdata=userdata.json
    extracted = ["userid","username","email","organisation_name","organisation_id"]
    if len(userdata)!=1:
        return False,"Either the user is not in the database or there are multiple entries",{}
    return True,"",dict(zip(extracted,userdata[0]))



@APP.route("/api/private")
@cross_origin(origin="localhost", headers=["Content-Type", "Authorization"])
@requires_auth
def get_BoxAid(*args,**kwargs):
    valid,msg,userdata = get_credentials("jane.doe@boxaid.co")
    if not valid:
        return jsonify(message=msg)
    if not valid:
        response = "You are authenticated but not authorized to access this resource"
        return jsonify(message=response)
    return userdata

@APP.route("/")
def HELLO():
    return "This is a landing page"
# This doesn't need authentication
@APP.route("/api/public")
@cross_origin(origin = "localhost",headers=["Content-Type", "Authorization"])
def public():
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return jsonify(message=response)
