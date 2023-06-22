import json 
from requests import post
from flask import current_app


def is_human(captcha_response):
    payload = {'response': captcha_response, 'secret': current_app.config['RECAPTCHA_SECRET_KEY']}
    response = post("https://www.google.com/recaptcha/api/siteverify", data=payload)
    response_text = json.loads(response.text)
    return response_text['success']