from pathlib import Path
from PIL import Image, ExifTags
import base64
import csv


# List of cybersecurity-related keywords to flag in metadata
suspicious_names = [
    "vuln",
    "cve",
    "unpatched",
    "lateral",
    "mimikatz",
    "recon",
    "dns",
    "harvesting",
    "subdomain",
    "exploit",
    "sql injection",
    "payload",
    "waf",
    "persist",
    "reverse shell",
    "obfuscated",
    "cron job",
    "exfil",
    "database dump",
    "covert channel",
    "tunnel"
]


# Directory containing the target images
image_dir = Path("Images")


# Helper function to check if a value is encoded (Hex, Base64, etc.)
def detect_encoding(value):
    if isinstance(value, bytes):
        try:
            value.decode("utf-8")
            return "UTF-8"
        except UnicodeDecodeError:
            return "Binary"

    if isinstance(value, str):
        try:
            bytes.fromhex(value)
            return "Hex"
        except ValueError:
            pass

        try:
            base64.b64decode(value, validate=True)
            return "Base64 (possible)"
        except Exception:
            pass

        return "Plaintext"

    return type(value).name


# Helper function to check if text contains suspicious keywords
def is_sus(value):
    if not isinstance(value, str):
        return False
    for word in suspicious_names:
        if word in value.lower():
            return True
    return False


results = []
# Loop through all PNG images in the directory
for image_path in sorted(image_dir.glob("*.png")):
    with Image.open(image_path) as img:

        exif = img.getexif()
        exif_fields = [ExifTags.TAGS.get(tag_id, tag_id) for tag_id in exif.keys()]
        meta_fields = list(img.info.keys())

        # Combine all unique metadata fields found
        unique_fields = list(set(exif_fields + meta_fields))
        
        # Initialize result dictionary for the current image
        result = {
            "filename": image_path.name,
            "format": img.format,
            "metadata_fields": ", ".join(unique_fields),
            "suspected_field": "", # identify relevant EXIF, PNG, or XMP field
            "encoding": "", # indicate Base64, plaintext, etc.
            "risk_score": 0, # apply and justify yourscoring rules
            "reason": "", # explain evidence for this score
        }
        sus_fields = []

        # Inspect EXIF metadata tags
        for tag_id, value in exif.items():
            check_encode = detect_encoding(str(value))
            if check_encode != "Plaintext":
                sus_fields.append(ExifTags.TAGS.get(tag_id, tag_id))
                result["risk_score"] += 5 # +5 if metadata is encoded
                result["encoding"] += check_encode
                result["reason"] = "Encode detected"

            elif is_sus(value):
                sus_fields.append(ExifTags.TAGS.get(tag_id, tag_id))
                result["risk_score"] += 10 # + 10 if malicious keyword is detected
                result["reason"] = "Suspicious words in value detected"
            

        # Inspect PNG text metadata and other info dictionary keys
        for field in img.info.keys():
            check_encode = detect_encoding(str(img.info[field]))
            if check_encode != "Plaintext":
                if not(field in sus_fields and check_encode in result["encoding"]):
                    result["encoding"] += check_encode
                    sus_fields.append(field)
                    result["risk_score"] += 5 # +5 if metadata is encoded
                    result["reason"] = "Encode detected"
            elif is_sus(img.info[field]):
                sus_fields.append(field)
                result["risk_score"] += 10 # + 10 if malicious keyword is detected
                result["reason"] = "Suspicious words in value detected"

        result["suspected_field"] = ", ".join(sus_fields)
        
    
        results.append(result)

# Export all collected results to a CSV report
with open("metadata_report.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
print("Saved", len(results), "rows to metadata_report.csv")