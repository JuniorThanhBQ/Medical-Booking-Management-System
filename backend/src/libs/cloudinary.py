import logging
import cloudinary.uploader

logger = logging.getLogger('flask_logger')


def cloudinary_upload_process(avatar):
    try:
        result = cloudinary.uploader.upload(
            avatar,
            folder="medical_appointment_b3"
        )
        return result.get("secure_url")

    except Exception as e:
        logger.error("Lỗi Cloudinary: %s", e, exc_info=True)
        raise ValueError("Lỗi trong xử lý hình ảnh") from e
