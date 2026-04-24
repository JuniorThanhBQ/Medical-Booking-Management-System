import {
  formatProfileUpdate,
  MONTH_OPTIONS,
  splitBirthday,
  splitName,
} from "@utils/profile-utils.js";
import { useMemo, useState } from "react";
import { toast } from "sonner";

import { GENDER_OPTIONS, SUPPORTED_COUNTRIES } from "@/configs/const";

const EditProfileForm = ({ profile, onSave }) => {
  const initialFormData = useMemo(() => {
    const { firstName, lastName } = splitName(profile?.name || "");
    const { day, month, year } = splitBirthday(
      profile?.dayOfBirth || profile?.dateOfBirth || "",
    );

    return {
      firstName,
      lastName,
      phone: profile?.phone || "",
      email: profile?.email || "",
      birthDay: day,
      birthMonth: month,
      birthYear: year,
      // Backend stores gender in uppercase (MALE/FEMALE/OTHER) but the
      // <select> options use lowercase values — normalize so the current
      // gender is actually selected instead of falling back to "Chọn".
      gender: (profile?.gender || "").toLowerCase(),
    };
  }, [profile]);

  const [formData, setFormData] = useState(null);
  const currentFormData = formData ?? initialFormData;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...(prev ?? initialFormData), [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const updatedProfile = formatProfileUpdate(currentFormData);
      await onSave({
        ...updatedProfile,
        dayOfBirth: updatedProfile.dateOfBirth,
        firstName: currentFormData.firstName,
        lastName: currentFormData.lastName,
      });
      toast.info("Đã ghi nhận thông tin.");
    } catch {
      toast.error("Đã xảy ra lỗi khi lưu thay đổi!");
    }
  };

  return (
    <section className="profile-edit-section">
      <form className="profile-form" onSubmit={handleSubmit}>
        <div className="profile-form__row">
          <div className="profile-form__group">
            <label className="profile-form__label">Họ</label>
            <input
              type="text"
              name="firstName"
              className="profile-form__input"
              value={currentFormData.firstName}
              onChange={handleChange}
            />
          </div>
          <div className="profile-form__group">
            <label className="profile-form__label">Tên</label>
            <input
              type="text"
              name="lastName"
              className="profile-form__input"
              value={currentFormData.lastName}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="profile-form__group">
          <label className="profile-form__label">Số điện thoại</label>
          <div className="profile-form__phone-container">
            <select className="profile-form__select profile-form__country-select">
              {SUPPORTED_COUNTRIES.map((country) => (
                <option key={country.code} value={country.phoneCode}>
                  {country.phoneCode}
                </option>
              ))}
            </select>
            <input
              type="tel"
              name="phone"
              className="profile-form__input"
              style={{ flex: 1 }}
              value={currentFormData.phone}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="profile-form__group">
          <label className="profile-form__label">Địa chỉ email</label>
          <input
            disabled
            type="email"
            name="email"
            className="profile-form__input"
            value={currentFormData.email}
            onChange={handleChange}
          />
        </div>

        <div className="profile-form__group">
          <label className="profile-form__label">Ngày sinh</label>
          <div className="profile-form__date-row">
            <input
              type="number"
              name="birthDay"
              placeholder="Ngày"
              className="profile-form__input"
              value={currentFormData.birthDay}
              onChange={handleChange}
              min="1"
              max="31"
            />
            <select
              name="birthMonth"
              className="profile-form__select"
              value={currentFormData.birthMonth}
              onChange={handleChange}
            >
              <option value="">Tháng</option>
              {MONTH_OPTIONS.map((month) => (
                <option key={month.value} value={month.value}>
                  {month.label}
                </option>
              ))}
            </select>
            <input
              type="number"
              name="birthYear"
              placeholder="Năm"
              className="profile-form__input"
              value={currentFormData.birthYear}
              onChange={handleChange}
              min="1900"
              max={new Date().getFullYear()}
            />
          </div>
        </div>

        <div className="profile-form__group">
          <label className="profile-form__label">Giới tính</label>
          <select
            name="gender"
            className="profile-form__select"
            value={currentFormData.gender}
            onChange={handleChange}
          >
            <option value="">Chọn</option>
            {GENDER_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <button type="submit" className="profile-form__submit">
          Lưu thay đổi
        </button>
      </form>
    </section>
  );
};

export default EditProfileForm;
