from datetime import datetime, date, time, timedelta
from types import SimpleNamespace

from tests.test_base import test_app
from src.utils.doctor.formatter_utils import (
    format_speciality_output,
    parse_and_validate_date,
)
from src.utils.doctor.time_slots_utils import (
    check_is_conflicting,
    is_valid_working_day,
    format_work_schedule,
)


def test_format_speciality_output():
    s = SimpleNamespace(
        id=1,
        name='Tim mạch',
        description='desc',
        level='Cơ sở',
        images=None
    )
    out = format_speciality_output(s)

    assert out['id'] == 1
    assert out['name'] == 'Tim mạch'
    assert out['images'] is None


def test_format_speciality_output_with_object():
    class SpecialtyObj:
        def __init__(self):
            self.id = 2
            self.name = 'Da liễu'
            self.description = 'Chuyên khoa da liễu'
            self.level = 'Nâng cao'
            self.images = None

    s = SpecialtyObj()
    out = format_speciality_output(s)

    assert out['id'] == 2
    assert out['name'] == 'Da liễu'
    assert out['level'] == 'Nâng cao'
    assert out['images'] is None


def test_parse_and_validate_date_valid():
    today = date.today().isoformat()
    d, err = parse_and_validate_date(today)

    assert err is None


def test_parse_and_validate_date_invalid_format():
    d, err = parse_and_validate_date('bad')

    assert d is None


def test_check_is_conflicting_overlap():
    slot_start = datetime(2026, 4, 1, 9, 0)

    vt = SimpleNamespace(
        duration_minutes=30,
        buffer_before=5,
        buffer_after=5
    )

    ms = SimpleNamespace(visit_type=vt)

    appt = SimpleNamespace(
        appointment_date=datetime(2026, 4, 1, 9, 15),
        medical_service=ms
    )

    assert check_is_conflicting(slot_start, 30, [appt]) is True


def test_check_is_conflicting_no_overlap():
    slot_start = datetime(2026, 4, 1, 8, 0)

    appt = SimpleNamespace(
        appointment_date=datetime(2026, 4, 1, 9, 15),
        medical_service=None
    )

    assert check_is_conflicting(slot_start, 30, [appt]) is False


def test_is_valid_working_day_false_when_no_profile():
    doctor = SimpleNamespace(profile=None)

    ok, sched = is_valid_working_day(doctor, date.today())

    assert ok is False


def test_format_work_schedule():
    wd = SimpleNamespace(
        day_of_week=SimpleNamespace(name='MONDAY')
    )

    ws = SimpleNamespace(
        title='T',
        description='D',
        start_time=time(8, 0),
        end_time=time(12, 0),
        work_dates=[wd]
    )

    out = format_work_schedule(ws)

    assert out['title'] == 'T'
    assert 'Monday' in out['workDate'][0]