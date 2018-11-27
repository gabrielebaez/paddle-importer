from dotenv import load_dotenv, find_dotenv
import requests
import json
import os

load_dotenv(find_dotenv())


def base_url(route, resource):
    return f"https://vendors.paddle.com/api/2.0/{route}/{resource}?\
            vendor_id={os.getenv('VENDOR_ID')}&\
            vendor_auth_code={os.getenv('VENDOR_AUTH_CODE')}"


def get_products():
    url = base_url('product', 'get_products')
    r = requests.post(url)
    r = r.json()

    def _format(data):
        return {
            "id": data['id'],
            "name": data['name'],
            "description": data['description'] if data['description'] is not None else '',
            "base_price": data['base_price'],
            "sale_price": data['sale_price'] if data['sale_price'] is not None else '',
            "screenshots": data['screenshots'] if 'screenshots' in data else '',
            "icon": data['icon']
        }

    return [_format(i) for i in r['response']['products']]


def get_users():
    url = base_url('subscription','users')
    r = requests.post(url)
    r = r.json()

    def _format(data):
        return {
            "user_id": data["user_id"],
            'user_email': data['user_email'],
            "marketing_consent": data["marketing_consent"],
            "state": data["state"],
            "signup_date": data["signup_date"],
            "last_payment_amount": data["last_payment"]["amount"],
            "last_payment_currency": data["last_payment"]["currency"],
            "last_payment_date": data["last_payment"]["date"],
            "next_payment_amount": data["next_payment"]["amount"],
            "next_payment_currency": data['next_payment']['currency'],
            "next_payment_date": data['next_payment']['date']
        }

    return [_format(i) for i in r['response']]


def get_payments():

    url = base_url('subscription','payments')
    r = requests.post(url)
    r = r.json()

    def _format(data):
        return {
            "id": data["id"],
            "subscription_id": data["subscription_id"],
            "amount": data["amount"],
            "currency": data["currency"],
            "payout_date": data["payout_date"],
            "is_paid": data["is_paid"],
            "is_one_off_charge": data["is_one_off_charge"],
            "receipt_url": data["receipt_url"] if 'receip_url' in data else ''
        }

    return [_format(i) for i in r['response']]


if __name__ == '__main__':
    for i in get_payments():
        print(i)
