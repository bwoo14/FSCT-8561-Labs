from pathlib import Path
from PIL import Image, ExifTags
import base64

# Get path of images directory
image_dir = Path("Images")

# # Confirm images found
# print("Images found:", len(list(image_dir.glob("*.png"))))

# Testing with one image first
# image_path = image_dir / "Brain-Channel.png"
image_path = image_dir / "Music.png"
with Image.open(image_path) as img:
	# Get exif data
	exif = img.getexif()

	# Print number of tags and each tag
	print("EXIF tags:", len(exif))
	for tag_id, value in exif.items():
		print(ExifTags.TAGS.get(tag_id, tag_id), ":", value)


# image_path = image_dir / "Brain.png"
image_path = image_dir / "Chemicals.png"

# Checking for extra info using the Image.info to get metadata
with Image.open(image_path) as img:
	for key, value in img.info.items():
		if isinstance(value, str):
			print(key, ":", value)

# Checking XMP data stored in PNG files
image_path = image_dir / "Dopamine.png"
with Image.open(image_path) as img:
	xmp = img.info.get("XML:com.adobe.xmp") or img.info.get("xmp")
	if isinstance(xmp, bytes):
		xmp = xmp.decode("utf-8", errors="replace")
	print(xmp if xmp else "No XMP found")


import base64
example = "RVhGSUw6IFR1bm5lbCBjb21wcmVzc2VkIGRhdGFiYXNlIGR1bXAgdmlhIEROUyBDb3ZlcnQgQ2hhbm5lbC4="
print(base64.b64decode(example).decode("utf-8"))


