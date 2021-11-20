# import os, json, boto3, logging, botocore
# import secrets
# from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from salt import mail

# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)

#     i.save(picture_path)

#     return picture_fn

# def save_picture(form_picture):
#     S3_BUCKET = os.environ.get('S3_BUCKET')
#     client = boto3.client('s3')
#     file_name = form_picture.filename

#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(file_name)
#     picture_hex = random_hex + f_ext
#     picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_hex)

#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)

#     client.upload_file(picture_path, S3_BUCKET, picture_hex)

#     return picture_hex

# def get_image_file(current_image_file):
#     s3 = boto3.resource('s3')
#     S3_BUCKET = os.environ.get('S3_BUCKET')
#     my_bucket = s3.Bucket(S3_BUCKET)

#     try: 
#         filtered_image_file = list(my_bucket.objects.filter(Prefix=current_image_file))
#         image_file_key = filtered_image_file[0].key
#         AWS_image_file = f'https://{S3_BUCKET}.s3.amazonaws.com/{image_file_key}'
#     except:
#         AWS_image_file = f'https://{S3_BUCKET}.s3.amazonaws.com/daruma.jpg'

#     return AWS_image_file


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('SFAudioGuild Password Reset', sender='testerdemosalt@gmail.com', recipients=[user.email])
    msg.body = f"To reset your password, visit the following link: https://app.sfaudioguild.com/reset_password/{token}    .... if you did not make this request, simply ignore this email and no changes will be made"
    mail.send(msg)