import "@css/users/doctor-detail.css";

import LoadingSpinner from "@features/shared/components/LoadingSpinner";
import { getDoctorDetail } from "@features/shared/services/public-api-service";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import Navbar from "../components/Navbar";

const DAY_MAPPING = {
  MONDAY: "Thứ Hai",
  TUESDAY: "Thứ Ba",
  WEDNESDAY: "Thứ Tư",
  THURSDAY: "Thứ Năm",
  FRIDAY: "Thứ Sáu",
  SATURDAY: "Thứ Bảy",
  SUNDAY: "Chủ Nhật",
};

const DoctorDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [doctor, setDoctor] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getDoctorDetail(id)
      .then((data) => {
        setDoctor(data);
        setError(null);
      })
      .catch(() => setError("Không thể tải thông tin bác sĩ."))
      .finally(() => setLoading(false));
  }, [id]);

  const getInitials = (lastName = "", firstName = "") => {
    const l = lastName.charAt(0).toUpperCase();
    const f = firstName.charAt(0).toUpperCase();
    return `${l}${f}`;
  };

  if (loading) return <LoadingSpinner fullPage label="Đang tải thông tin..." />;

  if (error) {
    return (
      <>
        <Navbar />
        <main className="doctor-detail-error">
          <p>{error}</p>
          <button className="btn-secondary" onClick={() => navigate(-1)}>
            Quay lại
          </button>
        </main>
      </>
    );
  }

  if (!doctor) return null;

  const { firstName, lastName, profile, workSchedule, email } = doctor;
  const fullName = `${profile?.title || "BS"} ${lastName} ${firstName}`;

  return (
    <>
      <Navbar />
      <main className="doctor-detail-page">
        <div className="doctor-detail-container">
          <button className="btn-back" onClick={() => navigate(-1)}>
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M19 12H5M12 19l-7-7 7-7" />
            </svg>
            Quay lại
          </button>

          <div className="doctor-profile-card">
            <div className="doctor-profile-header">
              <div className="doctor-avatar">
                {doctor.avatar ? (
                  <img src={doctor.avatar} alt={fullName} />
                ) : (
                  <span>{getInitials(lastName, firstName)}</span>
                )}
              </div>
              <div className="doctor-header-info">
                <h1 className="doctor-name">{fullName}</h1>
                <p className="doctor-bio">
                  {profile?.bio ||
                    "Chuyên gia y tế tận tâm với nhiều năm kinh nghiệm."}
                </p>
                <div className="doctor-tags">
                  <span className="doctor-tag">
                    {profile?.gender === "MALE"
                      ? "Nam"
                      : profile?.gender === "FEMALE"
                        ? "Nữ"
                        : "Khác"}
                  </span>
                </div>
              </div>
            </div>

            <div className="doctor-contact-grid">
              <div className="contact-item">
                <div className="contact-icon">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                    <polyline points="22,6 12,13 2,6" />
                  </svg>
                </div>
                <div>
                  <p className="contact-label">Email liên hệ</p>
                  <p className="contact-value">{email}</p>
                </div>
              </div>

              <div className="contact-item">
                <div className="contact-icon">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" />
                  </svg>
                </div>
                <div>
                  <p className="contact-label">Số điện thoại</p>
                  <p className="contact-value">
                    {profile?.phone || "Chưa cập nhật"}
                  </p>
                </div>
              </div>
            </div>

            <div className="doctor-actions">
              <button
                className="btn-primary"
                onClick={() => navigate(`/specialties/${profile?.specialtyId}`)}
              >
                Khám phá Chuyên Khoa
              </button>
            </div>
          </div>

          {workSchedule && (
            <div className="doctor-schedule-card">
              <div className="schedule-header">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                  <line x1="16" y1="2" x2="16" y2="6" />
                  <line x1="8" y1="2" x2="8" y2="6" />
                  <line x1="3" y1="10" x2="21" y2="10" />
                </svg>
                <h2>Lịch Làm Việc</h2>
              </div>

              <div className="schedule-content">
                <div className="schedule-info">
                  <p className="schedule-title">{workSchedule.title}</p>
                  <p className="schedule-time">
                    {workSchedule.startTime} - {workSchedule.endTime}
                  </p>
                  <p className="schedule-desc">{workSchedule.description}</p>
                </div>

                <div className="schedule-days">
                  <p className="days-label">Các ngày trực trong tuần:</p>
                  <div className="days-badges">
                    {workSchedule.workDate?.map((day) => (
                      <span key={day} className="day-badge">
                        {DAY_MAPPING[day] || day}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </>
  );
};

export default DoctorDetail;
