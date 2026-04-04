import { getStatusClassName } from "../../../users/utils/profile-utils.js";
import { getStatusLabel } from "@/configs/const";
import { MedicalFileIcon, DoctorIcon } from "@/assets/icons";


const MedicalDetailPanel = ({ item }) => {
  const rxItems = item.prescriptionText
    ? item.prescriptionText.split("\n").map((s) => s.trim()).filter(Boolean)
    : [];

  return (
    <div className="profile-activity__detail">
      <div className="profile-activity__medical-header">
        <div className="profile-activity__medical-header-icon">
          <MedicalFileIcon />
        </div>
        <div className="profile-activity__medical-header-info">
          <p className="profile-activity__medical-record-id">{item.recordId ?? item.id}</p>
          <p className="profile-activity__medical-header-date">
            {item.dateTimeLabel ?? (item.createdAt ? new Date(item.createdAt).toLocaleDateString("vi-VN") : "")}
          </p>
        </div>
      </div>

      <div className="profile-activity__detail-body">
        <div className="profile-activity__status-row">
          <span className={`profile-activity__pill ${getStatusClassName(item.status)}`}>
            {getStatusLabel(item.status)}
          </span>
        </div>

        <div className="profile-activity__medical-doctor">
          <div className="profile-activity__medical-doctor-avatar">
            <DoctorIcon />
          </div>
          <div>
            <p className="profile-activity__medical-doctor-name">{item.doctorName}</p>
            <p className="profile-activity__medical-specialty">{item.specialty}</p>
          </div>
        </div>

        <div className="profile-activity__medical-card">
          <p className="profile-activity__medical-card-label">Chẩn đoán</p>
          <p className="profile-activity__medical-card-value">{item.diagnosis}</p>
        </div>

        <div className="profile-activity__medical-section">
          <p className="profile-activity__medical-section-label">Ghi chú lâm sàng</p>
          <p className="profile-activity__medical-notes">{item.notes}</p>
        </div>

        {rxItems.length > 0 && (
          <div className="profile-activity__medical-section">
            <p className="profile-activity__medical-section-label">Đơn thuốc</p>
            <ul className="profile-activity__medical-rx-list">
              {rxItems.map((rx, i) => (
                <li key={i} className="profile-activity__medical-rx-item">{rx}</li>
              ))}
            </ul>
          </div>
        )}

        {item.treatmentOrders && (
          <div className="profile-activity__medical-section">
            <p className="profile-activity__medical-section-label">Chỉ định điều trị</p>
            <p className="profile-activity__medical-notes">{item.treatmentOrders}</p>
          </div>
        )}
      </div>
    </div>
  );
};

const ActivityDetailPanel = ({ item }) => {
  if (!item) return <></>;

  if (item.type === "medical_records") {
    return (
      <MedicalDetailPanel item={item} />
    );
  }

  return (
    <div className="profile-activity__detail">
      <div className="profile-activity__hero">
        {item.hero?.kind === "image" && item.hero?.src ? (
          <img src={item.hero.src} />
        ) : (
          <div className="profile-activity__hero-fallback" />
        )}
      </div>

      <div className="profile-activity__detail-body">
        <div className="profile-activity__status-row">
          <span className={`profile-activity__pill ${getStatusClassName(item.status)}`}>
            {getStatusLabel(item.status)}
          </span>
        </div>

        <h3 className="profile-activity__detail-title">
          {item.dateTimeLabel ?? (item.date && item.startTime ? `${item.date} ${item.startTime}` : item.date ?? "")}
        </h3>
        <p className="profile-activity__datetime">
          {item.durationLabel ?? (item.startTime && item.endTime ? `${item.startTime} – ${item.endTime}` : "")}
        </p>
      </div>
    </div>
  );
};

export default ActivityDetailPanel;
