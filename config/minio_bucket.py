import base64
import io
import uuid
from fastapi import HTTPException
from minio import Minio
from dotenv import load_dotenv
from PIL import Image
import os

load_dotenv()

MINIO_FILE_PATH =  os.environ.get('MINIO_FILE_PATH')
MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')
MINIO_URL = os.environ.get('MINIO_URL')
MINIO_BUCKET_NAME = os.environ.get('MINIO_IMAGES_BUCKET_NAME')

MINIO_CLIENT = Minio(
    endpoint=MINIO_URL, 
    access_key=MINIO_ACCESS_KEY, 
    secret_key=MINIO_SECRET_KEY, 
    secure=True
    )



def upload_image_minio(base64_string: str) -> str:
    image_info, image_base64_data = base64_string.split(',')
    image_data = base64.b64decode(image_base64_data)
    
    if len(image_data) > 20 * 1024 * 1024:
        raise HTTPException(413, 'Imagem maior que 20MB')

    if not image_info.startswith('data:image/png'):
        raise HTTPException(400, 'Arquivo não é uma imagem .png')

    image_uuid = str(uuid.uuid4())
    image_filename = f"{image_uuid}.png"

    with Image.open(io.BytesIO(image_data)) as img:
        in_mem_file = io.BytesIO()
        img.save(in_mem_file, format='PNG')
        in_mem_file.seek(0)
        MINIO_CLIENT.put_object(MINIO_BUCKET_NAME, image_filename, in_mem_file, length=in_mem_file.getbuffer().nbytes)

    return f"https://{MINIO_URL}/{MINIO_BUCKET_NAME}/{image_filename}"