# import os, json, boto3, logging, botocore
# import secrets
# from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from salt import mail

email_sender = 'testerdemosalt@gmail.com'

def send_reset_email(user):
    token = user.get_reset_token()
    email = user.email
    msg = Message('SFAudioGuild Password Reset', sender=email_sender, recipients=[email])
    msg.body = f"To reset your password, visit the following link: https://app.sfaudioguild.com/reset_password/{token}    .... if you did not make this request, simply ignore this email and no changes will be made"
    mail.send(msg)

def send_update_coins_email(user, coins):
    email = user.email
    msg = Message('SFAudioGuild Coin Count Update', sender=email_sender, recipients=[email])
    msg.body = f"Your coin count has changed! You now have {coins} coins."
    mail.send(msg)