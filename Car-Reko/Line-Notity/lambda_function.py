import urllib.request
import json
import ssl
import sys
import urllib.parse
import datetime
import os

# The LINE Notify API key.
LINE_TOKEN = os.environ.get("LINE_NOTIFY_API_KEY")

# The LINE Notify URL.
LINE_NOTIFY_URL = "https://notify-api.line.me/api/notify"

# The S3 prefix for the uploaded images.
S3_PREFIX = os.environ.get("S3_PREFIX")

# The S3 prefix for the uploaded QR code images.
S3_UPLOAD_IMG_PREFIX = os.environ.get("S3_UPLOAD_IMG_PREFIX")


def line_notify_image(msg, pic_url):
    """Sends a LINE Notify message with an image.

    Args:
        msg: The message to send.
        pic_url: The URL of the image to send.
    """

    method = "POST"
    headers = {"Authorization": "Bearer %s" % LINE_TOKEN}

    # The payload to send to the LINE Notify API.
    payload = {
        "message": msg,
        "imageThumbnail": pic_url,
        "imageFullsize": pic_url,
    }

    try:
        # Encode the payload as UTF-8.
        payload = urllib.parse.urlencode(payload).encode("utf-8")

        # Create a request object.
        req = urllib.request.Request(
            url=LINE_NOTIFY_URL,
            data=payload,
            method=method,
            headers=headers,
        )

        # Send the request.
        urllib.request.urlopen(req)
    except Exception as e:
        print("Exception Error: ", e)
        sys.exit(1)


def line_notify(msg):
    """Sends a LINE Notify message.

    Args:
        msg: The message to send.
    """

    method = "POST"
    headers = {"Authorization": "Bearer %s" % LINE_TOKEN}

    payload = {"message": msg}

    try:
        # Encode the payload as UTF-8.
        payload = urllib.parse.urlencode(payload).encode("utf-8")

        # Create a request object.
        req = urllib.request.Request(
            url=LINE_NOTIFY_URL,
            data=payload,
            method=method,
            headers=headers,
        )

        # Send the request.
        urllib.request.urlopen(req)
    except Exception as e:
        print("Exception Error: ", e)
        sys.exit(1)


def lambda_handler(event, context):
    """The Lambda handler function.

    Args:
        event: The event object.
        context: The context object.

    Returns:
        A dictionary with the response message.
    """

    status_code = 200

    # Get the message text and file name from the event object.
    msg = event["text"]
    file_name = event["file_name"]

    # If the event type is "qrcode", use the S3_UPLOAD_IMG_PREFIX for the image URL.
    # Otherwise, use the S3_PREFIX.
    if event["type"] == "qrcode":
        pic_url_temp = S3_PREFIX + file_name
    else:
        pic_url_temp = S3_UPLOAD_IMG_PREFIX + file_name

    # Send the LINE Notify message with the image.
    line_notify_image(msg, pic_url_temp)

    return {
        "message": msg,
    }

