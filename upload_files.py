import os
import cloudinary
import cloudinary.uploader
from PIL import Image

cloudinary.config(
  cloud_name="dqyjgvbdt",
  api_key="221244285745569",
  api_secret="CHikmDtShw10zVkhSiJXXOQaxQQ"
)

MEDIA_DIR = "MEDIA_DIR"

for root, dirs, files in os.walk(MEDIA_DIR):
    for file in files:
        file_path = os.path.join(root, file)

        # Create a compressed version
        compressed_path = os.path.join(root, f"compressed_{file}")
        img = Image.open(file_path)
        img = img.resize((1200, 800))  # reduce size
        img.save(compressed_path, optimize=True, quality=80)

        # ✅ Upload compressed file
        response = cloudinary.uploader.upload(
            compressed_path,
            folder="django_media/",
        )
        print(f"Uploaded {compressed_path} → {response['secure_url']}")
