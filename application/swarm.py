import base64
from werkzeug.utils import secure_filename
import requests
from constants import *
from PIL import Image, ImageFilter
import io
<<<<<<< HEAD
=======


dictionary_format = {
    'png': 'png',
    'jpeg': 'jpeg',
    'jpg': 'jpeg'
}
>>>>>>> 1754ce064c766b838b139e75de2185e8a5b72a1b


def get_base64_image(swarm_hash: str = "4b23ff7749ccc59b72a309c470ac75be187d1ce6d587970e06a3af3884a4bb06"):
    request = requests.get(f"https://gateway.ethswarm.org/files/{swarm_hash}")
    return base64.b64encode(request.content).decode('ascii')


<<<<<<< HEAD
def upload_image_private(data, title):
    filename = secure_filename(data.filename)

    headers = {"content-type": f"image/jpeg"}
=======
def upload_image_swarm(data, title):
    image_format = dictionary_format[secure_filename(data.filename).split('.')[-1].lower()]

    headers = {"content-type": f"image/{image_format}"}
>>>>>>> 1754ce064c766b838b139e75de2185e8a5b72a1b
    url = f"{SWARM_URL_NODE}files?name={title}"
    result = requests.post(url, data=data, headers=headers)

    url_blurry = f"{SWARM_URL_NODE}files?name=blurry_{title}"
    blurry_image = Image.open(data).filter(ImageFilter.BoxBlur(30))
    output = io.BytesIO()
<<<<<<< HEAD
    blurry_image.save(output, format=f'jpeg')
=======
    blurry_image.save(output, format=f'{image_format}')
>>>>>>> 1754ce064c766b838b139e75de2185e8a5b72a1b
    hex_data = output.getvalue()
    result_blurry = requests.post(url_blurry, data=hex_data, headers=headers)

    swarm_hash = result.json()["reference"]
    swarm_hash_blurry = result_blurry.json()["reference"]
    return swarm_hash, swarm_hash_blurry
<<<<<<< HEAD


def upload_image_public(data, title):
    filename = secure_filename(data.filename)
    url = f"{SWARM_URL_NODE}files?name={title}"
    headers = {"content-type": f"image/jpeg"}
    result = requests.post(url, data=data, headers=headers)
    swarm_hash = result.json()["reference"]
    return swarm_hash, swarm_hash

=======
>>>>>>> 1754ce064c766b838b139e75de2185e8a5b72a1b
