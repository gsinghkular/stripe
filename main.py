import stripe
from flask import Flask, render_template, jsonify, request
import os

static_dir = str(os.path.abspath(os.path.join(__file__, "..", "static")))
app = Flask(
    __name__, static_folder=static_dir, static_url_path="", template_folder=static_dir
)

stripe.api_key = os.getenv("API_KEY")

cust_id = "cus_Ndq0VytuQy0ldm"


# serve index.html
@app.route("/", methods=["GET"])
def index():
    intent = stripe.SetupIntent.create(
        usage="off_session",
        payment_method_types=["card"],
        #     payment_method_options={
        #     "card": {
        #         "mandate_options": {
        #             "reference": "some_reference",
        #             "description": "description",
        #             "amount": 200000,
        #             "currency": "usd",
        #             "amount_type": "maximum",
        #             "start_date": 1680474930,
        #             "interval": "sporadic",
        #             "supported_types": ["india"],
        #         },
        #     }
        # },
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


def mandate(mid):
    # update stripe setup intent to attach mandate
    res = stripe.SetupIntent.modify(
        mid,
        payment_method_options={
            "card": {
                "mandate_options": {
                    "reference": "some_reference",
                    "description": "description",
                    "amount": 200000,
                    "currency": "usd",
                    "amount_type": "maximum",
                    "start_date": 1680474930,
                    "interval": "sporadic",
                    "supported_types": ["india"],
                },
            }
        },
    )
    return res
