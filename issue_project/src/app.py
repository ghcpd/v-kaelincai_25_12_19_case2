"""
Flask Application - User Registration API
"""
from flask import Flask, request, jsonify, render_template
from src.validators import validate_registration_data

app = Flask(__name__)


@app.route("/")
def index():
    """Render registration page"""
    return render_template("register.html")


@app.route("/api/register", methods=["POST"])
def register():
    """
    User registration API endpoint
    
    Expected request body:
    {
        "username": "string",
        "email": "string",
        "birth_date": "YYYY-MM-DD"
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request data"
        }), 400
    
    username = data.get("username", "")
    email = data.get("email", "")
    birth_date = data.get("birth_date", "")
    
    # Validate data
    validation_result = validate_registration_data(username, email, birth_date)
    
    if not validation_result["valid"]:
        return jsonify({
            "success": False,
            "message": "Registration data validation failed",
            "errors": validation_result["errors"]
        }), 400
    
    # Simulate successful registration
    return jsonify({
        "success": True,
        "message": "Registration successful!",
        "user_id": 12345
    }), 201


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
