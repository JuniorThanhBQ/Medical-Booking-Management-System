import "@css/receptionist/appointment-card.css";

import { useState } from "react";

const AppointmentCard = ({
  appointment,
  onUpdateStatus,
  onDelete,
  onViewDetail,
}) => {
  const [showActions, setShowActions] = useState(false);
  const [newStatus, setNewStatus] = useState(appointment.status);
  const [newNote, setNewNote] = useState(appointment.note || "");

  const handleUpdate = () => {
    onUpdateStatus(appointment.id, newStatus, newNote);
    setShowActions(false);
  };

  return (
    <div className="appointment-card">
      <div className="appointment-card__clickable" onClick={onViewDetail}>
        <h3 className="appointment-card__title">{appointment.name}</h3>

        <div className="appointment-card__info">
          <div className="appointment-card__row">
            <strong>Bệnh nhân:</strong> {appointment.patientName}
          </div>
          <div className="appointment-card__row">
            <strong>Bác sĩ:</strong> {appointment.doctorName}
          </div>
          <div className="appointment-card__row">
            <strong>Ngày hẹn:</strong>{" "}
            {new Date(appointment.appointmentDate).toLocaleString("vi-VN")}
          </div>
          <div className="appointment-card__row">
            <strong>Trạng thái:</strong>{" "}
            <span
              className={`appointment-card__status status--${appointment.status.toLowerCase()}`}
            >
              {appointment.status}
            </span>
          </div>
        </div>

        {appointment.note && (
          <div className="appointment-card__note">
            <strong>Ghi chú:</strong> {appointment.note}
          </div>
        )}
      </div>

      <div className="appointment-card__actions-wrapper">
        <button
          className="appointment-card__actions-trigger"
          onClick={() => setShowActions(!showActions)}
        >
          {showActions ? "✕ Đóng chỉnh sửa" : "⚙ Quản lý lịch hẹn"}
        </button>

        {showActions && (
          <div className="appointment-card__form">
            <div className="appointment-card__field">
              <label>Thay đổi trạng thái</label>
              <select
                className="appointment-card__select"
                value={newStatus}
                onChange={(e) => setNewStatus(e.target.value)}
              >
                <option value="PENDING">🕒 PENDING</option>
                <option value="APPROVED">✅ APPROVED</option>
                <option value="COMPLETED">✔ COMPLETED</option>
                <option value="CANCEL">❌ CANCEL</option>
              </select>
            </div>

            <div className="appointment-card__field">
              <label>Ghi chú nội bộ</label>
              <textarea
                className="appointment-card__textarea"
                value={newNote}
                onChange={(e) => setNewNote(e.target.value)}
                rows={2}
                placeholder="Nhập ghi chú mới..."
              />
            </div>

            <div className="appointment-card__footer">
              <button className="btn btn--primary" onClick={handleUpdate}>
                Cập nhật
              </button>
              <button
                className="btn btn--danger"
                onClick={() => onDelete(appointment.id)}
              >
                Xóa lịch
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AppointmentCard;
