import pytest
from sqlalchemy.exc import IntegrityError

from src.modules.medical_records.models import MedicalRecord, MedicalRecordType
from tests.test_base import test_app, test_session


class TestMedicalRecordTypeEnum:
    def test_medical_record_type_valid(self):
        assert MedicalRecordType.DONE.value == 1
        assert MedicalRecordType.FOLLOW_UP.value == 2

    def test_medical_record_type_invalid(self):
        with pytest.raises(ValueError):
            MedicalRecordType(99)


class TestMedicalRecordModel:
    def test_medical_record_lifecycle(self, test_session):
        medical_record = MedicalRecord(
            diagnosis="Viêm họng cấp",
            prescription_text="Paracetamol 500mg",
            treatment_orders="Nghỉ ngơi, uống nhiều nước",
            doctor_profile_id=1,
            patient_profile_id=2,
            note="Bệnh nhân có tiền sử dị ứng nhẹ"
        )
        test_session.add(medical_record)
        test_session.commit()

        fetched_record = test_session.query(MedicalRecord).filter_by(diagnosis="Viêm họng cấp").first()
        assert fetched_record is not None
        assert fetched_record.type == MedicalRecordType.DONE

        fetched_record.diagnosis = "Viêm họng mãn tính"
        test_session.commit()

        updated_record = test_session.get(MedicalRecord, medical_record.id)
        assert updated_record.diagnosis == "Viêm họng mãn tính"

        test_session.delete(updated_record)
        test_session.commit()

        assert test_session.get(MedicalRecord, medical_record.id) is None

    def test_medical_record_missing_fields(self, test_session):
        medical_record = MedicalRecord(diagnosis="Thiếu thông tin bắt buộc")
        test_session.add(medical_record)
        with pytest.raises(IntegrityError):
            test_session.commit()

    def test_medical_record_string_format(self):
        medical_record = MedicalRecord(
            patient_profile_id=10,
            diagnosis="Đau dạ dày"
        )
        expected_string = "Phiếu điều trị: 10 - Đau dạ dày"
        assert str(medical_record) == expected_string

    def test_medical_record_foreign_keys(self, test_session):
        medical_record = MedicalRecord(
            diagnosis="Kiểm tra khóa ngoại",
            prescription_text="Test",
            treatment_orders="Test",
            doctor_profile_id=100,
            patient_profile_id=200
        )
        test_session.add(medical_record)
        test_session.commit()

        fetched_record = test_session.query(MedicalRecord).filter_by(doctor_profile_id=100).first()
        assert fetched_record.patient_profile_id == 200

    def test_medical_record_default_type(self, test_session):
        medical_record = MedicalRecord(
            diagnosis="Kiểm tra giá trị mặc định",
            prescription_text="Test",
            treatment_orders="Test",
            doctor_profile_id=1,
            patient_profile_id=1
        )
        test_session.add(medical_record)
        test_session.commit()

        assert medical_record.type == MedicalRecordType.DONE
