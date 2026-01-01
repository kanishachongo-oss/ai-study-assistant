import stripe
from flask import Blueprint, redirect
from flask_login import current_user
from models import db

payments = Blueprint("payments", __name__)

stripe.api_key = "STRIPE_SECRET_KEY"

@payments.route("/subscribe")
def subscribe():
    session = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        line_items=[{
            "price": "STRIPE_PRICE_ID",
            "quantity": 1
        }],
        success_url="https://YOUR_APP_URL/success",
        cancel_url="https://YOUR_APP_URL/pricing"
    )
    return redirect(session.url)


@payments.route("/success")
def success():
    current_user.is_paid = True
    db.session.commit()
    return redirect("/chat")
