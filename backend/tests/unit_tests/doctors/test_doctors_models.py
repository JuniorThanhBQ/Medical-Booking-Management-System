from datetime import time

import pytest
from sqlalchemy.exc import IntegrityError

from src.modules.doctors.models import DayOfWeek, WorkDate, WorkSchedule
from tests.test_base import test_app, test_session


@pytest.fixture
def base_work_schedule(test_session):
    schedule = WorkSchedule(
        title="Morning Shift",
        description="Regular morning shift",
        start_time=time(8, 0),
        end_time=time(12, 0)
    )
    test_session.add(schedule)
    test_session.commit()
    return schedule


class TestDayOfWeekEnum:
    def test_enum_day_valid(self):
        assert DayOfWeek.MONDAY.value == 1
        assert DayOfWeek.SUNDAY.value == 7

    def test_enum_day_invalid(self):
        with pytest.raises(ValueError):
            DayOfWeek(99)


class TestWorkScheduleModel:
    def test_schedule_create(self, test_session):
        schedule = WorkSchedule(
            title="Afternoon Shift",
            start_time=time(13, 0),
            end_time=time(17, 0)
        )
        test_session.add(schedule)
        test_session.commit()

        fetched_schedule = test_session.query(WorkSchedule).filter_by(title="Afternoon Shift").first()
        assert fetched_schedule is not None
        assert fetched_schedule.start_time == time(13, 0)

    def test_schedule_missing(self, test_session):
        schedule = WorkSchedule(
            start_time=time(8, 0),
            end_time=time(12, 0)
        )
        test_session.add(schedule)
        with pytest.raises(IntegrityError):
            test_session.commit()

    def test_schedule_string(self, base_work_schedule):
        assert str(base_work_schedule) == "Morning Shift"

    def test_schedule_cascade(self, test_session, base_work_schedule):
        work_date = WorkDate(
            day_of_week=DayOfWeek.MONDAY,
            work_schedule_id=base_work_schedule.id
        )
        test_session.add(work_date)
        test_session.commit()

        test_session.delete(base_work_schedule)
        test_session.commit()

        remaining_dates = test_session.query(WorkDate).count()
        assert remaining_dates == 0

    def test_schedule_update(self, test_session, base_work_schedule):
        base_work_schedule.start_time = time(9, 0)
        test_session.commit()

        updated_schedule = test_session.query(WorkSchedule).filter_by(id=base_work_schedule.id).first()
        assert updated_schedule.start_time == time(9, 0)


class TestWorkDateModel:
    def test_work_date_create(self, test_session, base_work_schedule):
        work_date = WorkDate(
            day_of_week=DayOfWeek.TUESDAY,
            work_schedule_id=base_work_schedule.id
        )
        test_session.add(work_date)
        test_session.commit()

        fetched_date = test_session.query(WorkDate).filter_by(day_of_week=DayOfWeek.TUESDAY).first()
        assert fetched_date is not None

    def test_work_date_missing(self, test_session):
        work_date = WorkDate(day_of_week=DayOfWeek.WEDNESDAY)
        test_session.add(work_date)
        with pytest.raises(IntegrityError):
            test_session.commit()

    def test_work_date_string(self, base_work_schedule):
        work_date = WorkDate(
            day_of_week=DayOfWeek.THURSDAY,
            work_schedule_id=base_work_schedule.id
        )
        assert str(work_date) == "THURSDAY"
