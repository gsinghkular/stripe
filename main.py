import stripe
from flask import Flask, render_template, jsonify, request
import os, uuid
import dotenv
import logging
from time import time

logger = logging.getLogger(__name__)

dotenv.load_dotenv()
static_dir = str(os.path.abspath(os.path.join(__file__, "..", "static")))
app = Flask(
    __name__, static_folder=static_dir, static_url_path="", template_folder=static_dir
)

stripe.api_key = os.getenv("API_KEY")

cust_id = "cus_OSHqrO1zJLBu8e"


# serve index.html
@app.route("/", methods=["GET"])
def index():
    intent = stripe.SetupIntent.create(
        usage="off_session",
        customer=cust_id,
        payment_method="pm_1NfNIZJtnhTdnQ4KISPaznsf",
        payment_method_types=["card"],
            payment_method_options={
            "card": {
                "mandate_options": {
                    "reference": uuid.uuid4(),
                    "description": "description",
                    "amount": 200_00,
                    "currency": "usd",
                    "amount_type": "maximum",
                    "start_date": int(time()),
                    "interval": "sporadic",
                    "supported_types": ["india"],
                },
            }
        },
    )
    return render_template("index.html", client_secret=intent.client_secret)


# create stripe customer
@app.route("/create-customer", methods=["GET"])
def create_customer():
    customer = stripe.Customer.create()
    return {"customer_id": customer.id}


# an endpoint setup-complete that returns all GET parameters as json
@app.route("/setup-complete", methods=["GET"])
def setup_complete():
    return jsonify(request.args)


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_ENDPOINT_SECRET")
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400
    # Handle the checkout.session.completed event
    type = event["type"]
    if event["type"] == "checkout.session.completed":
        print("Payment was successful.")
        logger.info(request.get_json())
        # TODO: run some custom code here

    return "Success", 200

"""
    intent = stripe.SetupIntent.create(
        usage="off_session",
        customer=cust_id,
        payment_method="pm_1NfOP4JtnhTdnQ4KqcDxlMeQ",
        payment_method_types=["card"],
            payment_method_options={
            "card": {
                "mandate_options": {
                    "reference": uuid.uuid4(),
                    "description": "description",
                    "amount": 200_00,
                    "currency": "usd",
                    "amount_type": "maximum",
                    "start_date": int(time()),
                    "interval": "sporadic",
                    "supported_types": ["india"],
                },
            }
        },
    )
"""
