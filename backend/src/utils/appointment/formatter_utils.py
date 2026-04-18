from datetime import datetime


def parse_appointment_datetime(str_appointment_date=None):
    try:
        appointment_datetime = datetime.strptime(
            str_appointment_date.replace("Z", "").split(".")[0],
            "%Y-%m-%dT%H:%M:%S"
        )

        return appointment_datetime, None

    except ValueError:
        return None, ({"message": "Định dạng ngày không hợp lệ"}, "ERROR_BAD_REQUEST")


def format_appointment(appointment=None, doctor=None, patient_user=None, patient_name=None, specialty=None):
    if patient_name is None:
        user = patient_user or appointment.patient_profile
        patient_name = f"{user.last_name} {user.first_name}"

    return {
        "id": appointment.id,
        "service": appointment.medical_service.name if appointment.medical_service else None,
        "name": appointment.name,
        "patientName": patient_name,
        "doctorName": f"{doctor.last_name} {doctor.first_name}" if doctor else None,
        "specialty": specialty if specialty else None,
        "appointmentDate": appointment.appointment_date.isoformat() + "Z",
        "status": appointment.status.name if appointment.status else None,
        "note": appointment.note,
        "createdAt": appointment.created_date.isoformat() + "Z",
        "updatedAt": appointment.updated_date.isoformat() + "Z",
    }
