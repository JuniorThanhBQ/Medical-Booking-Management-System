import "@css/doctor/registration.css";

import { useDoctorRegistration } from "@features/doctor/hooks/use-doctor-registration";
import { Link } from "react-router-dom";

export default function DoctorRegistration() {
  const {
    formData,
    error,
    loading,
    success,
    handleChange,
    handleFileChange,
    handleSubmit,
  } = useDoctorRegistration();

  if (success) {
    return (
      <div className="registration-success-wrapper">
        <div className="registration-success">
          <h2>Đăng ký thành công!</h2>
          <p>
            Chúng tôi đã nhận được hồ sơ của bạn và sẽ liên hệ trong thời gian
            sớm nhất.
          </p>
          <Link to="/" className="btn-back-home">
            Quay về trang chủ
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="doctor-registration-page">
      <div className="doctor-registration-header">
        <Link to="/" className="back-link">
          &#8592; Trở về trang chủ
        </Link>
      </div>

      <div className="doctor-registration-content">
        <div className="doctor-registration-form-section">
          <h2>Ứng Tuyển Vị Trí Bác Sĩ</h2>
          <form onSubmit={handleSubmit} className="doctor-registration-form">
            <div className="form-group">
              <label htmlFor="fullName">Họ và tên</label>
              <input
                type="text"
                id="fullName"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group half-width">
                <label htmlFor="dob">Ngày sinh</label>
                <input
                  type="date"
                  id="dob"
                  name="dob"
                  value={formData.dob}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group half-width">
                <label htmlFor="gender">Giới tính</label>
                <select
                  id="gender"
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  required
                >
                  <option value="MALE">Nam</option>
                  <option value="FEMALE">Nữ</option>
                  <option value="OTHER">Khác</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="address">Địa chỉ hiện tại</label>
              <input
                type="text"
                id="address"
                name="address"
                value={formData.address}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group half-width">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group half-width">
                <label htmlFor="phone">Số điện thoại</label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="reason">Lý do và vị trí ứng tuyển</label>
              <textarea
                id="reason"
                name="reason"
                rows="4"
                value={formData.reason}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="cv">Đính kèm CV (PDF, Tối đa 5MB)</label>
              <input
                type="file"
                id="cv"
                name="cv"
                accept=".pdf"
                onChange={handleFileChange}
                required
              />
            </div>

            {error && <p className="form-error">{error}</p>}

            <button type="submit" disabled={loading} className="btn-submit">
              {loading ? "Đang gửi hồ sơ..." : "Gửi Đơn Ứng Tuyển"}
            </button>
          </form>
        </div>

        <div className="doctor-registration-info-section">
          <div className="info-card">
            <h3>Yêu Cầu Tuyển Dụng</h3>
            <p className="info-intro">
              Chào mừng bạn đến với Medical Appointment B3. Vui lòng đọc kỹ các
              tiêu chuẩn và quy định dưới đây trước khi nộp hồ sơ.
            </p>

            <div className="info-block">
              <div className="info-icon">&#10004;</div>
              <div className="info-text">
                <h4>1. Tiêu chuẩn chuyên môn</h4>
                <p>
                  Yêu cầu có bằng bác sĩ chuyên khoa, Thạc sĩ hoặc Tiến sĩ y
                  khoa. Chữ ký số và chứng chỉ hành nghề phải còn hiệu lực pháp
                  lý tại Việt Nam.
                </p>
              </div>
            </div>

            <div className="info-block">
              <div className="info-icon">&#128274;</div>
              <div className="info-text">
                <h4>2. Đạo đức và pháp lý</h4>
                <p>
                  Cam kết tuân thủ tuyệt đối quy định về bảo mật thông tin hồ sơ
                  bệnh án. Không chia sẻ dữ liệu bệnh nhân dưới mọi hình thức
                  khi chưa được phép.
                </p>
              </div>
            </div>

            <div className="info-block">
              <div className="info-icon">&#128336;</div>
              <div className="info-text">
                <h4>3. Quy Trình xét hồ sơ</h4>
                <p>
                  Hồ sơ của bạn sẽ được gửi gửi về HR bệnh viện để xem xét thông
                  tin. Trong quá trình này, nếu bạn cần thay đổi hồ sơ thì gửi
                  trực tiếp qua mail cung cấp ở cuối trang.
                </p>
              </div>
            </div>

            <div className="info-block">
              <div className="info-icon">&#128336;</div>
              <div className="info-text">
                <h4>4. Phản hồi và chờ phỏng vấn</h4>
                <p>
                  Nếu hồ sơ của bạn đạt yêu cầu. Chúng tôi sẽ liên hệ lại qua
                  địa chỉ email bạn đã điền để sắp xếp lịch phỏng vấn trực tiếp
                  hoặc qua video call với HR và quản trị viên.
                </p>
              </div>
            </div>

            <div className="info-footer">
              <p>
                Mọi thắc mắc xin vui lòng liên hệ tới gmail:{" "}
                <strong>thanh.vantrung2005@gmail.com</strong>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
