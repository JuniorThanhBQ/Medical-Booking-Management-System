import "@css/shared/hero.css";

import useAuth from "@contexts/auth/AuthContext";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

import { ArrowRightIcon } from "@/assets/icons";

const STATS = [
  { value: "24/7", label: "Tiếp nhận lịch khám 24/7" },
  { value: "100%", label: "Tận tâm trong từng ca bệnh" },
  { value: "CS1", label: "Một cơ sở làm trọng tâm dịch vụ" },
  { value: "5.0", label: "Đi theo xu hướng công nghệ hiện đại" },
];

export default function HeroSection() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleBookingClick = (e) => {
    if (!user) {
      e.preventDefault();
      toast.info("Nhắc nhở: Bạn sẽ cần đăng nhập để đặt lịch.", {
        onAutoClose: () => {
          navigate("/dashboard");
        },
      });
    } else {
      toast.success(`Chào mừng ${user.profile.firstName} đã quay lại!`, {});
    }
  };

  return (
    <section className="hero" id="hero">
      <div className="hero__bg">
        <img
          src="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=1600&auto=format&fit=crop&q=85"
          alt=""
          fetchPriority="high"
          decoding="async"
        />
        <div className="hero__overlay" />
      </div>

      <div className="hero__body">
        <div className="hero__content">
          <span className="hero__badge">Đa khoa</span>

          <h1 className="hero__title">
            Open
            <br />
            Medical
            <br />
            Appointment
          </h1>

          <p className="hero__desc">
            Đội ngũ bác sĩ giàu kinh nghiệm, chăm sóc toàn diện với đa dạng dịch
            vụ từ chẩn đoán chính xác đến phác đồ điều trị. Châm ngôn của chúng
            tôi là lương y như từ mẫu.
          </p>

          <div className="hero__ctas">
            <a
              href="/dashboard"
              className="hero__btn-primary"
              onClick={handleBookingClick}
            >
              Đặt lịch tư vấn
            </a>
            <a href="#services" className="hero__btn-ghost">
              Xem tất cả dịch vụ
              <ArrowRightIcon size={15} />
            </a>
          </div>
        </div>
      </div>

      <div className="hero__stats-strip">
        <div className="hero__stats-inner lp-container">
          {STATS.map((s) => (
            <div key={s.label} className="hero__stat">
              <span className="hero__stat-value">{s.value}</span>
              <span className="hero__stat-label">{s.label}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
