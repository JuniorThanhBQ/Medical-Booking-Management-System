import "@css/doctor/registration.css";

import apis, { endpoints } from "@configs/apis";
import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "sonner";
export default function DoctorRegistration() {
  const [formData, setFormData] = useState({
    fullName: "",
    dob: "",
    gender: "MALE",
    address: "",
    email: "",
    phone: "",
    reason: "",
  });
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const hasShownToast = useRef(false);

  useEffect(() => {
    if (!hasShownToast.current) {
      toast.info("Khuyến khích gửi hồ sơ trực tiếp qua mail.");
      hasShownToast.current = true;
    }
  }, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type !== "application/pdf") {
        setError("Chỉ chấp nhận file định dạng PDF.");
        setFile(null);
        e.target.value = null;
        return;
      }
      if (selectedFile.size > 5 * 1024 * 1024) {
        setError("Kích thước file không được vượt quá 5MB.");
        setFile(null);
        e.target.value = null;
        return;
      }
      setError("");
      setFile(selectedFile);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Vui lòng đính kèm CV (PDF).");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const submitData = new FormData();
      submitData.append("fullName", formData.fullName);
      submitData.append("dateOfBirth", formData.dob);
      submitData.append("gender", formData.gender);
      submitData.append("address", formData.address);
      submitData.append("email", formData.email);
      submitData.append("phone", formData.phone);
      submitData.append("reason", formData.reason);
      submitData.append("CV", file);

      await apis.post(endpoints["doctor_registration"], submitData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setSuccess(true);
    } catch (err) {
      setError("Có lỗi xảy ra khi gửi thông tin. Vui lòng thử lại sau.");
    } finally {
      setLoading(false);
    }
  };

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
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M19 12H5M12 19l-7-7 7-7" />
          </svg>
          Trở về trang chủ
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
              <div className="info-icon">
                <svg
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
              </div>
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
              <div className="info-icon">
                <svg
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                </svg>
              </div>
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
              <div className="info-icon">
                <svg
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
              </div>
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
              <div className="info-icon">
                <svg
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
              </div>
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
