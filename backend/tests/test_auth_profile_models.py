import pytest
from sqlalchemy.exc import IntegrityError

from src.modules.auth_profile.models import (AuditLog, CtaLabel, DoctorProfile,
                                             GenderRole, PatientProfile,
                                             Profile, Specialty, User,
                                             UserRole)
from tests.test_base import test_app, test_session


class TestUserRegistrationAndManagement:
    def test_successfully_register_a_new_patient(self, test_session):
        new_user = User(
            username="johndoe",
            password="SecurePassword123!",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
        )
        test_session.add(new_user)
        test_session.commit()

        audit_log = AuditLog(
            action_name="USER_REGISTER",
            description="New patient registered",
            user_id=new_user.id
        )
        test_session.add(audit_log)
        test_session.commit()

        saved_user = test_session.query(User).filter_by(email="john.doe@example.com").first()
        assert saved_user is not None
        assert saved_user.id is not None
        assert saved_user.username == "johndoe"
        assert saved_user.role == UserRole.PATIENT
        assert saved_user.is_active is True

        saved_log = test_session.query(AuditLog).filter_by(user_id=saved_user.id).first()
        assert saved_log is not None

    def test_fail_registration_with_duplicate_email(self, test_session):
        user1 = User(
            username="johndoe",
            password="pwd",
            first_name="John",
            last_name="Doe",
            email="duplicate@example.com"
        )
        test_session.add(user1)
        test_session.commit()

        user2 = User(
            username="janedoe",
            password="pwd",
            first_name="Jane",
            last_name="Doe",
            email="duplicate@example.com"
        )
        test_session.add(user2)

        with pytest.raises(IntegrityError):
            test_session.commit()
        test_session.rollback()

    def test_fail_registration_missing_required_fields(self, test_session):
        incomplete_user = User(
            username="incompleteuser",
            password="SecurePassword123!",
            email="incomplete@example.com"
        )
        test_session.add(incomplete_user)

        with pytest.raises(IntegrityError):
            test_session.commit()
        test_session.rollback()


class TestProfileManagement:
    @pytest.fixture
    def setup_user_and_specialty(self, test_session):
        user = User(username="doctor1", password="pwd", first_name="Dr", last_name="Who", email="dr@example.com",
                    role=UserRole.DOCTOR)
        specialty = Specialty(name="Cardiology", description="Heart stuff", level="Level 1", cta_label=CtaLabel.CK1)
        test_session.add_all([user, specialty])
        test_session.commit()
        return user, specialty

    def test_successfully_create_a_doctor_profile(self, test_session, setup_user_and_specialty):
        user, specialty = setup_user_and_specialty

        doc_profile = DoctorProfile(
            user_id=user.id,
            phone="+1234567890",
            gender=GenderRole.MALE,
            title="MD, PhD",
            bio="Experienced cardiologist.",
            specialty_id=specialty.id
        )
        test_session.add(doc_profile)
        test_session.commit()

        saved_profile = test_session.query(DoctorProfile).filter_by(user_id=user.id).first()
        assert saved_profile is not None
        assert saved_profile.profile_type == "doctor"
        assert saved_profile.title == "MD, PhD"
        assert saved_profile.specialty_id == specialty.id
        assert saved_profile.user.email == "dr@example.com"

    def test_enforce_1_to_1_user_to_profile_relationship(self, test_session, setup_user_and_specialty):
        user, _ = setup_user_and_specialty

        patient_profile = PatientProfile(user_id=user.id, medical_history="None")
        test_session.add(patient_profile)
        test_session.commit()

        doc_profile = DoctorProfile(user_id=user.id, title="MD", bio="Bio", specialty_id=1)
        test_session.add(doc_profile)

        with pytest.raises(IntegrityError):
            test_session.commit()
        test_session.rollback()


class TestSpecialtyManagementAndReferentialIntegrity:
    @pytest.fixture
    def setup_doctor_with_specialty(self, test_session):
        user = User(username="doc2", password="pwd", first_name="A", last_name="B", email="doc2@ex.com")
        specialty = Specialty(name="Neurology", description="Brain", level="L1")
        test_session.add_all([user, specialty])
        test_session.commit()

        doc_profile = DoctorProfile(user_id=user.id, title="MD", bio="...", specialty_id=specialty.id)
        test_session.add(doc_profile)
        test_session.commit()
        return user, specialty, doc_profile

    def test_fail_to_delete_specialty_assigned_to_doctors(self, test_session, setup_doctor_with_specialty):
        _, specialty, _ = setup_doctor_with_specialty

        test_session.delete(specialty)

        with pytest.raises(IntegrityError):
            test_session.commit()
        test_session.rollback()

    def test_cascade_deletion_of_user_to_profile(self, test_session, setup_doctor_with_specialty):
        user, _, doc_profile = setup_doctor_with_specialty
        user_id = user.id
        profile_id = doc_profile.id

        test_session.delete(user)
        test_session.commit()

        deleted_user = test_session.query(User).filter_by(id=user_id).first()
        deleted_profile = test_session.query(Profile).filter_by(id=profile_id).first()
        deleted_doc_profile = test_session.query(DoctorProfile).filter_by(id=profile_id).first()

        assert deleted_user is None
        assert deleted_profile is None
        assert deleted_doc_profile is None
