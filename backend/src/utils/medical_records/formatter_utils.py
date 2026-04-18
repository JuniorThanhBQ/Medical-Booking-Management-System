def format_medical_record(record):
    appointment = record.appointment
    doctor_user = record.doctor.user
    patient_user = record.patient.user
    specialty = record.doctor.specialty

    return {
        "id": str(record.id),
        "service": appointment.medical_service.name if appointment and appointment.medical_service else None,
        "appointmentId": str(appointment.id) if appointment else None,
        "patientName": f"{patient_user.last_name} {patient_user.first_name}",
        "doctorName": f"{doctor_user.last_name} {doctor_user.first_name}",
        "specialty": specialty.name if specialty else None,
        "status": appointment.status.name if appointment and appointment.status else None,
        "diagnosis": record.diagnosis,
        "createdAt": record.created_date.isoformat() + "Z" if record.created_date else None,
    }
