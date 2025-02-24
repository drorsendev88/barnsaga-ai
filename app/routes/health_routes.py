from flask import Blueprint, jsonify

health_routes = Blueprint("health_routes", __name__)

@health_routes.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "OK"}), 200