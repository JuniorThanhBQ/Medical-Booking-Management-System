import { useState, useEffect } from 'react';
import { SUPPORTED_COUNTRIES, GENDER_OPTIONS } from '@/configs/const';
import { splitName, splitBirthday, formatProfileUpdate, MONTH_OPTIONS } from '../utils/profile-utils';

const EditProfileForm = ({ profile, onSave }) => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    phone: '',
    email: '',
    birthDay: '',
    birthMonth: '',
    birthYear: '',
    gender: '',
  });

  useEffect(() => {
    const { firstName, lastName } = splitName(profile.name);
    const { day, month, year } = splitBirthday(profile.birthday);
    
    setFormData({
      firstName,
      lastName,
      phone: profile.phone || '',
      email: profile.email || '',
      birthDay: day,
      birthMonth: month,
      birthYear: year,
      gender: profile.gender || '',
    });
  }, [profile]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const updatedProfile = formatProfileUpdate(formData);
    onSave(updatedProfile);
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
              value={formData.firstName}
              onChange={handleChange}
            />
          </div>
          <div className="profile-form__group">
            <label className="profile-form__label">Tên</label>
            <input
              type="text"
              name="lastName"
              className="profile-form__input"
              value={formData.lastName}
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
              value={formData.phone}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="profile-form__group">
          <label className="profile-form__label">Địa chỉ email</label>
          <input
            type="email"
            name="email"
            className="profile-form__input"
            value={formData.email}
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
              value={formData.birthDay}
              onChange={handleChange}
              min="1"
              max="31"
            />
            <select
              name="birthMonth"
              className="profile-form__select"
              value={formData.birthMonth}
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
              value={formData.birthYear}
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
            value={formData.gender}
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
