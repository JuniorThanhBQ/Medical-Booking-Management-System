from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from src.modules.auth_profiles.models import (AuditLog, CtaLabel,
                                              DoctorProfile, GenderRole,
                                              PatientProfile, Profile,
                                              Specialty, User, UserRole)
from tests.test_base import test_app, test_session


@pytest.fixture
def base_user(test_session):
    user = User(
        username="johndoe",
        password="hashed_password",
        first_name="John",
        last_name="Doe",
        email="john@example.com"
    )
    test_session.add(user)
    test_session.commit()
    return user


class TestEnumModels:
    def test_enum_valid(self):
        assert UserRole.DOCTOR.value == 1
        assert GenderRole.MALE.value == 1
        assert CtaLabel.CK1.value == 1

    def test_enum_invalid(self):
        with pytest.raises(ValueError):
            UserRole(99)


class TestUserModel:
    def test_user_crud(self, test_session, base_user):
        fetched = test_session.query(User).filter_by(username="johndoe").first()
        assert fetched is not None

        fetched.first_name = "Jane"
        test_session.commit()
        assert fetched.first_name == "Jane"

        test_session.delete(fetched)
        test_session.commit()
        assert test_session.query(User).count() == 0

    def test_user_miss_fields(self, test_session):
        user = User(password="123", first_name="A", last_name="B", email="b@b.com")
        test_session.add(user)
        with pytest.raises(IntegrityError):
            test_session.commit()

    def test_user_role_assign(self, test_session, base_user):
        assert base_user.role == UserRole.PATIENT
        base_user.role = UserRole.ADMIN
        test_session.commit()
        assert base_user.role == UserRole.ADMIN

    def test_user_unique_email(self, test_session, base_user):
        dup_user = User(
            username="other", password="123",
            first_name="A", last_name="B", email=base_user.email
        )
        test_session.add(dup_user)
        with pytest.raises(IntegrityError):
            test_session.commit()

    def test_user_string(self, base_user):
        assert str(base_user) == "Doe John"


class TestProfileModel:
    def test_profile_crud(self, test_session, base_user):
        profile = Profile(user_id=base_user.id, address="123 Street", phone="0123456789")
        test_session.add(profile)
        test_session.commit()

        fetched = test_session.query(Profile).first()
        assert fetched.address == "123 Street"

        fetched.phone = "9876543210"
        test_session.commit()
        assert fetched.phone == "9876543210"

        test_session.delete(fetched)
        test_session.commit()
        assert test_session.query(Profile).count() == 0

    def test_profile_mapper(self, test_session, base_user):
        profile = Profile(user_id=base_user.id)
        test_session.add(profile)
        test_session.commit()
        assert profile.profile_type == "profile"

    def test_profile_fk_cascade(self, test_session, base_user):
        profile = Profile(user_id=base_user.id)
        test_session.add(profile)
        test_session.commit()

        test_session.delete(base_user)
        test_session.commit()
        assert test_session.query(Profile).count() == 0

    def test_profile_uselist(self, test_session, base_user):
        p1 = Profile(user_id=base_user.id)
        test_session.add(p1)
        test_session.commit()

        p2 = Profile(user_id=base_user.id)
        test_session.add(p2)
        with pytest.raises(IntegrityError):
            test_session.commit()

    def test_profile_birth(self, test_session, base_user):
        profile = Profile(user_id=base_user.id, birthday=date(1990, 1, 1))
        test_session.add(profile)
        test_session.commit()
        assert profile.birthday.year == 1990

    def test_profile_string(self, test_session, base_user):
        profile = Profile(user_id=base_user.id)
        test_session.add(profile)
        test_session.commit()
        assert str(profile) == "Doe John"


class TestSpecialtyModel:
    def test_specialty_crud(self, test_session):
        specialty = Specialty(name="Cardiology", level="High")
        test_session.add(specialty)
        test_session.commit()

        assert specialty.id is not None
        assert specialty.cta_label == CtaLabel.CK1

        specialty.level = "Medium"
        test_session.commit()
        assert specialty.level == "Medium"

        test_session.delete(specialty)
        test_session.commit()
        assert test_session.query(Specialty).count() == 0

    def test_specialty_unique(self, test_session):
        s1 = Specialty(name="Neuro", level="1")
        s2 = Specialty(name="Neuro", level="2")
        test_session.add_all([s1, s2])

        with pytest.raises(IntegrityError):
            test_session.commit()

    def test_specialty_string(self):
        specialty = Specialty(name="Dental", level="1")
        assert str(specialty) == "Dental"


class TestInheritedProfiles:
    def test_doctor_profile(self, test_session, base_user):
        specialty = Specialty(name="Surgeon", level="1")
        test_session.add(specialty)
        test_session.commit()

        doctor = DoctorProfile(
            user_id=base_user.id,
            title="Dr.",
            bio="Expert",
            specialty_id=specialty.id
        )
        test_session.add(doctor)
        test_session.commit()

        assert doctor.profile_type == "doctor"
        assert doctor.specialty.name == "Surgeon"

        doctor.title = "Prof."
        test_session.commit()
        assert doctor.title == "Prof."

    def test_patient_profile(self, test_session, base_user):
        patient = PatientProfile(
            user_id=base_user.id,
            medical_history="No severe conditions"
        )
        test_session.add(patient)
        test_session.commit()

        assert patient.profile_type == "patient"
        assert patient.medical_history == "No severe conditions"


class TestAuditLogModel:
    def test_audit_log_crud(self, test_session, base_user):
        log = AuditLog(
            action_name="LOGIN",
            description="User logged in",
            user_id=base_user.id
        )
        test_session.add(log)
        test_session.commit()

        fetched = test_session.query(AuditLog).first()
        assert fetched.action_name == "LOGIN"
        assert fetched.user.username == "johndoe"
