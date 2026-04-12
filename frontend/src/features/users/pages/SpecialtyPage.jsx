import "@/assets/css/users/specialty.css";
import { useState, useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import { getSpecialtyDetail } from "@features/shared/services/public-api-service";
import { isAuthenticated } from "@/utils/auth-helpers";
import LoadingSpinner from "@features/shared/components/LoadingSpinner"

export default function SpecialtyPage() {
  const { specialtyId } = useParams();
  const loggedIn = isAuthenticated();
  const [specialty, setSpecialty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!specialtyId) {
      setError("Không tìm thấy chuyên khoa.");
      setLoading(false);
      return;
    }

    let cancelled = false;
    const fetchSpecialty = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getSpecialtyDetail(specialtyId);
        if (!cancelled) setSpecialty(data);
      } catch (err) {
        console.error("Failed to fetch specialty:", err);
        if (!cancelled)
          setError("Không thể tải thông tin chuyên khoa. Vui lòng thử lại.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    fetchSpecialty();
    return () => { cancelled = true; };
  }, [specialtyId]);

  if (loading) {
    return (
      <main className="specialty">
        <LoadingSpinner fullPage label="Đang tải..." />
      </main>
    );
  }

  if (error) {
    return (
      <main className="specialty">
        <section className="specialty__hero">
          <div className="specialty__hero-inner">
            <p>{error}</p>
            <Link to="/dashboard" className="specialty__primary-cta">
              Quay lại Dashboard
            </Link>
          </div>
        </section>
      </main>
    );
  }

  return (
    <>
      <main className="specialty">
        <section className="specialty__hero">
          <div className="specialty__hero-inner">
            <Link to="/dashboard" className="specialty__back">
              <span aria-hidden="true">←</span> Quay lại Dashboard
            </Link>

            {!specialty ? (
              <div className="specialty__empty">
                <h1 className="specialty__title">Không tìm thấy chuyên khoa</h1>
                <p className="specialty__subtitle">
                  Vui lòng chọn một chuyên khoa từ Dashboard.
                </p>
                <Link to="/dashboard" className="specialty__primary-cta">
                  Xem các chuyên khoa
                </Link>
              </div>
            ) : (
              <div className="specialty__hero-grid">
                <div className="specialty__hero-content">
                  {specialty.level && (
                    <div className="specialty__pill">{specialty.level}</div>
                  )}
                  <h1 className="specialty__title">{specialty.name}</h1>
                  <p className="specialty__subtitle">{specialty.description}</p>

                  <div className="specialty__ctas">
                    {loggedIn ? (
                      <Link
                        to={`/specialties/${specialty.id}/book`}
                        className="specialty__primary-cta"
                      >
                        Đặt lịch khám
                      </Link>
                    ) : (
                      <Link
                        to={`/auth?returnUrl=${encodeURIComponent(`/specialties/${specialty.id}/book`)}`}
                        className="specialty__secondary-cta"
                      >
                        Đăng nhập để đặt lịch
                      </Link>
                    )}
                  </div>
                </div>

                <aside
                  className="specialty__hero-card"
                  aria-label="At a glance"
                >
                  <div className="specialty__hero-card-row">
                    <span className="specialty__hero-card-label">
                      Các bước tiếp theo
                    </span>
                    <span className="specialty__hero-card-value">
                      Chọn ngày → bác sĩ → giờ → xác nhận
                    </span>
                  </div>
                  <div className="specialty__hero-card-row">
                    <span className="specialty__hero-card-label">Truy cập</span>
                    <span className="specialty__hero-card-value">
                      Dashboard
                    </span>
                  </div>
                </aside>
              </div>
            )}
          </div>
        </section>

        {specialty && (
          <section className="specialty__section" id="doctors">
            <div className="specialty__section-inner">
              <div className="specialty__section-header">
                <h2 className="specialty__section-title">
                  Trước khi bạn đặt lịch khám
                </h2>
                <p className="specialty__section-subtitle">
                  Vui lòng xem các lưu ý sau để việc đặt lịch diễn ra thuận lợi.
                </p>
              </div>

              <ol className="specialty__rules-list">
                <li className="specialty__rule-card">
                  <h3 className="specialty__rule-title">
                    1. Chọn ngày và giờ trước
                  </h3>
                  <p className="specialty__rule-body">
                    Hãy chọn ngày và giờ phù hợp trước khi chọn bác sĩ để hệ
                    thống hiển thị đúng những bác sĩ đang còn lịch trống.
                  </p>
                </li>

                <li className="specialty__rule-card">
                  <h3 className="specialty__rule-title">
                    2. Lịch làm việc của bác sĩ có thể thay đổi
                  </h3>
                  <p className="specialty__rule-body">
                    Bác sĩ và khung giờ bạn chọn là yêu cầu ban đầu. Chúng tôi
                    sẽ xác nhận lịch cuối cùng dựa trên tình trạng làm việc thực
                    tế của bác sĩ.
                  </p>
                </li>

                <li className="specialty__rule-card">
                  <h3 className="specialty__rule-title">
                    3. Mỗi khung giờ chỉ cho một lịch hẹn
                  </h3>
                  <p className="specialty__rule-body">
                    Mỗi lượt đặt lịch chỉ áp dụng cho một bệnh nhân và một khung
                    giờ. Vui lòng đặt lịch riêng cho từng thành viên trong gia
                    đình.
                  </p>
                </li>

                <li className="specialty__rule-card">
                  <h3 className="specialty__rule-title">
                    4. Cung cấp thông tin chính xác
                  </h3>
                  <p className="specialty__rule-body">
                    Vui lòng kiểm tra kỹ thông tin cá nhân, liên hệ và ghi chú y
                    tế để bác sĩ có thể chuẩn bị tốt nhất cho buổi khám.
                  </p>
                </li>

                <li className="specialty__rule-card">
                  <h3 className="specialty__rule-title">
                    5. Không sử dụng cho trường hợp khẩn cấp
                  </h3>
                  <p className="specialty__rule-body">
                    Nếu bạn có triệu chứng nặng hoặc cấp cứu, vui lòng đến khoa
                    cấp cứu gần nhất thay vì đặt lịch khám trực tuyến.
                  </p>
                </li>
              </ol>
            </div>
          </section>
        )}
      </main>
    </>
  );
}
