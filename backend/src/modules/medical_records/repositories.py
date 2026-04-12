from src.extensions import db
from src.modules.medical_records.models import MedicalRecord


def get_medical_record_by_id(record_id):
    return db.session.get(MedicalRecord, int(record_id))


def get_medical_records_by_role(role_name, profile_id, page=1, limit=10):
    query = MedicalRecord.query

    if role_name == "PATIENT":
        query = query.filter(MedicalRecord.patient_profile_id == profile_id)
    elif role_name == "DOCTOR":
        query = query.filter(MedicalRecord.doctor_profile_id == profile_id)

    query = query.order_by(MedicalRecord.created_date.desc())

    return query.paginate(page=page, per_page=limit, error_out=False)


def add_instance(instance):
    db.session.add(instance)


def flush_session():
    db.session.flush()


def commit_session():
    db.session.commit()


def delete_instance(instance):
    db.session.delete(instance)
