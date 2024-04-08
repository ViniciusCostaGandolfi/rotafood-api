import base64
import io
import uuid
from fastapi import HTTPException
from minio import Minio
from PIL import Image
from config import settings

MINIO_CLIENT = Minio(
    endpoint=settings.MINIO_URL,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
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
        MINIO_CLIENT.put_object(settings.MINIO_IMAGES_BUCKET_NAME, image_filename, in_mem_file, length=in_mem_file.getbuffer().nbytes)

    return f"https://{settings.MINIO_URL}/{settings.MINIO_IMAGES_BUCKET_NAME}/{image_filename}"
