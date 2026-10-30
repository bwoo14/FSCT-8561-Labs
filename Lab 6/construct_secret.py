from pathlib import Path
from PIL import Image, ExifTags
import base64

# Get path of images directory
image_dir = Path("Images")


def metadata(png):

	image_path = image_dir / png

	print(f"Examining: {png}")
	print()
	print("EXIF...")
	with Image.open(image_path) as img:
		# Get exif data
		exif = img.getexif()

		# Print number of tags and each tag
		print("EXIF tags:", len(exif))
		for tag_id, value in exif.items():
			print(ExifTags.TAGS.get(tag_id, tag_id), ":", value)


	print()
	print("Metadata...")
# Checking for extra info using the Image.info to get metadata
	# with Image.open(image_path) as img:
	# 	for key, value in img.info.items():
	# 		if isinstance(value, str):
	# 			print(key, ":", value)


				
	with Image.open(image_path) as img:
		for key, value in img.info.items():
			if isinstance(value, bytes):
				try:
					decoded_text = value.decode("utf-8", errors="ignore")
					print(f"{key} (bytes decoded): {value}")
					print("IM RIGHT HERE")
				except Exception:
					print(f"{key}: <binary data>")
			else:
				print(f"{key} : {value}")


	print()
	print("XMP")
# Checking XMP data stored in PNG files
	with Image.open(image_path) as img:
		xmp = img.info.get("XML:com.adobe.xmp") or img.info.get("xmp")
		if isinstance(xmp, bytes):
			xmp = xmp.decode("utf-8", errors="replace")
		print(xmp if xmp else "No XMP found")

	print("="*20)

import base64
# example = "RVhGSUw6IFR1bm5lbCBjb21wcmVzc2VkIGRhdGFiYXNlIGR1bXAgdmlhIEROUyBDb3ZlcnQgQ2hhbm5lbC4="
# print(base64.b64decode(example).decode("utf-8"))


metadata("Activation.png")
metadata("Brain-Channel.png")
metadata("Brain.png")
metadata("Chemicals.png")
metadata("Dopamine.png")
metadata("Music.png")