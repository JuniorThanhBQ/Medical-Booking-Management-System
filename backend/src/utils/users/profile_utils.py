from src.libs.cloudinary import cloudinary_upload_process
from src.utils.utils import parse_gender


def add_profile_updates(obj, data, mapping):
    for payload_key, attr in mapping.items():
        if payload_key in data:
            if isinstance(obj, dict):
                obj[attr] = data[payload_key]
            else:
                setattr(obj, attr, data[payload_key])


def update_extended_profile(profile, data):
    if "medicalHistory" in data and profile["profile_type"] == "patient":
        profile["medical_history"] = data["medicalHistory"]

    if data.get("avatar"):
        profile["avatar"] = cloudinary_upload_process(data["avatar"])

    if "gender" in data:
        profile["gender"] = parse_gender(data.get("gender"), default=profile["gender"])
