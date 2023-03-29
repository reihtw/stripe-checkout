import os
import stripe
from flask import Flask, render_template, url_for


app = Flask(__name__)

app.config['STRIPE_PUBLIC_KEY'] = os.environ.get('STRIPE_PUBLIC_KEY')
app.config['STRIPE_SECRET_KEY'] = os.environ.get('STRIPE_SECRET_KEY')

stripe.api_key = app.config['STRIPE_SECRET_KEY']


@app.route('/')
def index():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1MqdzqG8kcwul3slCN4AfLW0',
            'quantity': 1,
        }],
        mode='subscription',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True)
    )

    return render_template(
        'index.html',
        checkout_session_id=session['id'],
        checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
    )


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
