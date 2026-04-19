import "@css/users/profile.css";

import { useAppointmentDetailPage } from "@features/receptionist/hooks/use-appointment-detail";
import Navbar from "@features/users/components/Navbar";
import { useNavigate, useParams } from "react-router-dom";

const InfoRow = ({ label, value }) => (
  <p>
    <strong>{label}:</strong> {value}
  </p>
);

const DetailSection = ({ title, children }) => (
  <div className="record-page__section">
    <h2 className="record-page__section-title">{title}</h2>
    {children}
  </div>
);

const EditMode = ({ formData, setFormData, onSave, onCancel }) => (
  <>
    <DetailSection title="Cập nhật trạng thái">
      <select
        value={formData.status}
        onChange={(e) => setFormData({ ...formData, status: e.target.value })}
      >
        <option value="PENDING">PENDING</option>
        <option value="APPROVED">APPROVED</option>
        <option value="COMPLETED">COMPLETED</option>
        <option value="CANCEL">CANCEL</option>
      </select>
    </DetailSection>

    <DetailSection title="Ghi chú">
      <textarea
        value={formData.note}
        onChange={(e) => setFormData({ ...formData, note: e.target.value })}
        rows={4}
        style={{ width: "100%", padding: "0.5rem" }}
      />
    </DetailSection>

    <div className="record-page__section">
      <button onClick={onSave} style={{ marginRight: "1rem" }}>
        Lưu
      </button>
      <button onClick={onCancel}>Hủy</button>
    </div>
  </>
);

const ViewMode = ({ detail, onEdit }) => (
  <>
    <DetailSection title="Ghi chú">
      <p className="record-page__section-content">{detail.note}</p>
    </DetailSection>

    <div className="record-page__section">
      <button onClick={onEdit}>Chỉnh sửa</button>
    </div>
  </>
);

const AppointmentContent = ({
  detail,
  isEditing,
  formData,
  setFormData,
  onSave,
  onCancel,
  onEdit,
}) => {
  const data = {
    service: detail?.service || "—",
    name: detail?.name || `Lịch hẹn #${detail?.id || "—"}`,
    date: detail?.appointmentDate
      ? new Date(detail.appointmentDate).toLocaleString("vi-VN")
      : "—",
    patientName: detail?.patientName || "—",
    doctorName: detail?.doctorName || "—",
    specialty: detail?.specialty?.name || detail?.specialty || "—",
    status: detail?.status || "—",
    note: detail?.note || "—",
  };

  return (
    <div className="record-page__content">
      <DetailSection title="Thông tin chung">
        <InfoRow label="Dịch vụ" value={data.service} />
        <InfoRow label="Tên lịch" value={data.name} />
        <InfoRow label="Ngày hẹn" value={data.date} />
        {!isEditing && <InfoRow label="Trạng thái" value={data.status} />}
      </DetailSection>

      <DetailSection title="Thông tin bệnh nhân">
        <InfoRow label="Bệnh nhân" value={data.patientName} />
        <InfoRow label="Bác sĩ" value={data.doctorName} />
        <InfoRow label="Chuyên khoa" value={data.specialty} />
      </DetailSection>

      {isEditing ? (
        <EditMode
          formData={formData}
          setFormData={setFormData}
          onSave={onSave}
          onCancel={onCancel}
        />
      ) : (
        <ViewMode detail={data} onEdit={onEdit} />
      )}
    </div>
  );
};

const AppointmentDetailPage = () => {
  const { appointmentId } = useParams();
  const navigate = useNavigate();

  const {
    appointmentDetail,
    loading,
    error,
    isEditing,
    formData,
    setFormData,
    handleSave,
    handleEdit,
    handleCancel,
  } = useAppointmentDetailPage(appointmentId);

  if (loading) return <p>Đang tải chi tiết lịch hẹn...</p>;
  if (error)
    return (
      <div className="error-state">
        <p>{error}</p>
      </div>
    );

  return (
    <>
      <Navbar />
      <main className="profile-main" style={{ marginTop: "2rem" }}>
        <button
          type="button"
          className="record-page__back"
          onClick={() => navigate(-1)}
        >
          &#8592; Quay
        </button>
        <h1 className="profile-main__title">Chi tiết lịch hẹn</h1>
        <div className="record-page__card">
          <AppointmentContent
            detail={appointmentDetail}
            isEditing={isEditing}
            formData={formData}
            setFormData={setFormData}
            onSave={handleSave}
            onCancel={handleCancel}
            onEdit={handleEdit}
          />
        </div>
      </main>
    </>
  );
};

export default AppointmentDetailPage;
