from datetime import date, datetime, timedelta


def format_speciality_output(specialty=None):
    return {
        "id": specialty.id,
        "name": specialty.name,
        "description": specialty.description,
        "level": specialty.level,
        "images": specialty.images if specialty.images else None
    }


def parse_and_validate_date(date_str, max_day_searching=30):
    try:
        if date_str:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            target_date = date.today()

        today = date.today()
        if target_date < today or target_date > (today + timedelta(days=max_day_searching)):
            return None, f"Chỉ xem được lịch trong vòng {max_day_searching} ngày tới"

        return target_date, None
    except ValueError:
        return None, "Định dạng không hợp lệ (YYYY-MM-DD)"
