from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from src.modules.booking.models import (Appointment, MedicalRecord, StatusRole,
                                        db)
from src.modules.users.services import create_token, token_required

api = Blueprint("booking_api", __name__)


@api.route("/appointment", methods=["POST"])
@token_required
def create_appointment(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Thiếu dữ liệu"}), 400

    name = data.get("name")
    description = data.get("description")
    status = data.get("status")
    doctor_id = data.get("doctorprofile_id")
    patient_id = data.get("patientprofile_id")
    medicalrecord_id = data.get("medicalrecord_id")

    if not name:
        return jsonify({"message": "name bị bỏ trống."}), 400

    if not description:
        return jsonify({"message": "description bị bỏ trống."}), 400

    if not doctor_id:
        return jsonify({"message": "Thiếu doctorprofile_id"}), 400

    if not patient_id:
        return jsonify({"message": "Thiếu patientprofile_id"}), 400

    if not medicalrecord_id:
        return jsonify({"message": "Thiếu medicalrecord_id"}), 400

    doctor = DoctorProfile.query.get(doctor_id)
    if not doctor:
        return jsonify({"message": "Doctor không tồn tại"}), 404

    patient = PatientProfile.query.get(patient_id)
    if not patient:
        return jsonify({"message": "Patient không tồn tại"}), 404

    medical = MedicalRecord.query.get(medicalrecord_id)
    if not medical:
        return jsonify({"message": "Medical record không tồn tại"}), 404

    new_appointment = Appointment(
        name=name,
        description=description,
        status=StatusRole[status] if status else StatusRole.PENDING,
        doctorprofile_id=doctor_id,
        patientprofile_id=patient_id,
        medicalrecord_id=medicalrecord_id,
    )

    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({"message": "Đăng ký lịch khám thành công thành công"}), 201


@api.route("/appointments", methods=["GET"])
@token_required
def get_appointments(current_user):
    appointments = Appointment.query.all()

    result = []
    for a in appointments:
        result.append(
            {
                "id": a.id,
                "name": a.name,
                "description": a.description,
                "status": a.status.name,
                "doctor": a.doctor.id if a.doctor else None,
                "patient": a.patient.id if a.patient else None,
            }
        )

    return jsonify(result)


@api.route("/appointments/<int:id>", methods=["GET"])
@token_required
def get_appointment(id, current_user):
    a = Appointment.query.get(id)

    if not a:
        return jsonify({"message": "Không tìm thấy"}), 404

    return jsonify(
        {
            "id": a.id,
            "name": a.name,
            "description": a.description,
            "status": a.status.name,
            "doctor": a.doctor.id if a.doctor else None,
            "patient": a.patient.id if a.patient else None,
            "medical_record": a.medicalrecord.id if a.medicalrecord else None,
        }
    )


@api.route("/appointments/<int:id>", methods=["DELETE"])
@token_required
def delete_appointment(id, current_user):
    a = Appointment.query.get(id)

    if not a:
        return jsonify({"message": "Không tìm thấy"}), 404

    db.session.delete(a)
    db.session.commit()

    return jsonify({"message": "Xoá thành công"})
