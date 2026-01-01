from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, login_required, current_user
from models import db, User
from auth import auth
from payments import payments
from ai import can_chat, get_ai_reply
import os

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth)
app.register_blueprint(payments)

@app.route("/")
def home():
    return render_template("pricing.html")

@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html")

@app.route("/api/chat", methods=["POST"])
@login_required
def api_chat():
    if not can_chat(current_user):
        return jsonify({"error": "Free limit reached. Upgrade."})

    reply = get_ai_reply(request.json["message"])
    current_user.messages_today += 1
    db.session.commit()
    return jsonify({"reply": reply})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
