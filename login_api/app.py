#! /usr/bin/env python3.6
import os
from flask import Flask, redirect, request, render_template

import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51ONrt3SBco5jw1ZOEqfYCsb28jeel942DhqURr5sTiGrALuJxl4dRgKNP6HQfil28rUCJVHrZx9rgjUIzZySVT2Y00RQg3CCsR'

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:4242'

@app.route('/')
def hello():
    return render_template('checkout.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try: 
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1PH1B5SBco5jw1ZOlHwmNr6V',
                    'quantity': 1,
                },
            ],
            currency='inr',
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(port=4242, debug=True)