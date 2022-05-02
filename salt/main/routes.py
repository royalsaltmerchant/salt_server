from flask import request, Blueprint, jsonify
import logging, json, os
from salt.serializers import TrackAssetSchema
import boto3
from botocore.exceptions import ClientError
import stripe

main = Blueprint('main', __name__)

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

track_asset_schema = TrackAssetSchema()
track_assets_schema = TrackAssetSchema(many=True)

@main.route('/api/signed_URL_download', methods=['POST'])
def create_presigned_url():
    s3_client = boto3.client('s3')
    try:
        data = json.loads(request.data)
        bucket_name = data['bucket_name']
        object_name = data['object_name']
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=86400)
    except ClientError as e:
        logging.error(e)
        return None

    return response

@main.route('/api/signed_URL_upload', methods=['POST'])
def create_presigned_post():
    s3_client = boto3.client('s3')
    try:
        data = json.loads(request.data)
        bucket_name = data['bucket_name']
        object_name = data['object_name']
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=None,
                                                     Conditions=None,
                                                     ExpiresIn=3600)
    except ClientError as e:
        logging.error(e)
        return None

    return response

@main.route('/api/stripe_intent', methods=['POST'])
def create_payment():
    data = json.loads(request.data)
    # Create a PaymentIntent with the order amount and currency
    intent = stripe.PaymentIntent.create(
        amount=data['amount'],
        currency='usd',
        receipt_email=data['email'],
        description=data['description']
    )

    try:
        return jsonify({'publishable_key': os.environ.get('STRIPE_PUBLISHABLE_KEY'), 'client_secret': intent.client_secret})
    except Exception as e:
        return jsonify(error=str(e)), 403

