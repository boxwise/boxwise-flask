"""Construction of routes for flask app"""
import os

from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from boxwise_flask.auth_helper import AuthError, requires_auth
from boxwise_flask.graph_ql.resolvers import schema

# Blueprint to serve React on production
frontend_bp = Blueprint(
    "frontend_bp",
    __name__,
    static_folder=os.getenv("FLASK_STATIC_FOLDER", "static"),
    static_url_path=os.getenv("FLASK_STATIC_URL_PATH", "/static"),
)


@frontend_bp.route("/mobile")
def index():
    return frontend_bp.send_static_file("index.html")


# Blueprint for API
api_bp = Blueprint("api_bp", __name__)


@api_bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@api_bp.route("/")
def HELLO():
    return "This is a landing page"


# This doesn't need authentication
@api_bp.route("/api/public", methods=["GET"])
@cross_origin(origin="localhost", headers=["Content-Type", "Authorization"])
def public():
    response = (
        "Hello from a public endpoint! You don't need to be authenticated to see this."
    )
    return jsonify(message=response)


# This needs authentication
@api_bp.route("/api/private", methods=["GET"])
@cross_origin(origin="localhost", headers=["Content-Type", "Authorization"])
@requires_auth
def private():
    response = (
        "Hello from a private endpoint! You need to be authenticated to see this."
    )
    return jsonify(message=response)


@api_bp.route("/graphql", methods=["GET"])
def graphql_playgroud():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@api_bp.route("/graphql", methods=["POST"])
@cross_origin(origin="localhost", headers=["Content-Type", "Authorization"])
@requires_auth
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request

    debug_graphql = True  # bool(os.getenv("DEBUG_GRAPHQL", False))
    success, result = graphql_sync(
        schema, data, context_value=request, debug=debug_graphql
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
