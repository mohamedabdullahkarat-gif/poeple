import exifread
import hashlib
from PIL import Image

async def extract_exif(path):
    with open(path, "rb") as f:
        tags = exifread.process_file(f)
    exif_data = {}
    for tag in ["Image Model","EXIF DateTimeOriginal","GPS GPSLatitude"]:
        if tag in tags:
            exif_data[tag] = str(tags[tag])
    return exif_data

async def image_hash(path):
    with open(path,"rb") as f:
        return hashlib.md5(f.read()).hexdigest()

async def ai_generated_heuristic(path):
    exif = extract_exif(path)
    img = Image.open(path)
    w,h = img.size
    score=0
    if not exif:
        score+=60
    if w*h < 500*500:
        score+=20
    return min(score,100)
