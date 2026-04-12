import { useEffect, useMemo, useState } from "react";
import { fetchAppointmentsInDay } from "../services/appointments-api.js";
import { getStatusLabel } from "@/configs/const";
import { TYPE_OPTIONS, REASON_OPTIONS } from "@/configs/const";
import AppointmentsPreviewModal from "./AppointmentModal";



export default function LeaveRequestsCard({
  newRequest,
  updateNewRequest,
  leaveRequests,
  onSubmit,
}) {
  const selectedDateForPreview = useMemo(() => newRequest.fromDate ?? "", [newRequest.fromDate]);

  const [isAppointmentsModalOpen, setIsAppointmentsModalOpen] = useState(false);
  const [appointmentsDate, setAppointmentsDate] = useState("");


  useEffect(() => {
    if (!isAppointmentsModalOpen) return;

    function onKeyDown(event) {
      if (event.key === "Escape") setIsAppointmentsModalOpen(false);
    }

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [isAppointmentsModalOpen]);

  function openAppointmentsPreview(date) {
    if (!date) return;

    setAppointmentsDate(date);
    setIsAppointmentsModalOpen(true);
  }

  return (
    <div className="schedule-page__card">
      <div className="schedule-page__card-header">
        <h2 className="schedule-page__card-title">Yêu cầu nghỉ phép / đổi lịch</h2>
        <p className="schedule-page__card-description">
          Tạo yêu cầu để quản trị viên phê duyệt trước khi lịch làm việc thay đổi.
        </p>
      </div>

      <form className="schedule-page__form" onSubmit={onSubmit}>
        <div className="schedule-page__form-row">
          <label className="schedule-page__form-label">
            Loại yêu cầu
            <select
              className="schedule-page__select"
              value={newRequest.type ?? "time_off"}
              onChange={(event) =>
                updateNewRequest({
                  type: event.target.value,
                })
              }
            >
              {TYPE_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
        </div>

        {newRequest.type === "time_off" && (
        <div className="schedule-page__form-row">
          <label className="schedule-page__form-label">
            Lý do nghỉ
            <select
              className="schedule-page__select"
              value={newRequest.reason ?? "vacation"}
              onChange={(event) =>
                updateNewRequest({
                  reason: event.target.value,
                })
              }
            >
              {REASON_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
        </div>)}

        <div className="schedule-page__form-row schedule-page__form-row-inline">
          <label className="schedule-page__form-label">
            Từ ngày
            <input
              type="date"
              className="schedule-page__input"
              value={newRequest.fromDate ?? ""}
              onChange={(event) =>
                updateNewRequest({
                  fromDate: event.target.value,
                })
              }
              required
            />
          </label>
          <label className="schedule-page__form-label">
            Đến ngày
            <input
              type="date"
              className="schedule-page__input"
              value={newRequest.toDate ?? ""}
              onChange={(event) =>
                updateNewRequest({
                  toDate: event.target.value,
                })
              }
              required
            />
          </label>
        </div>

        <div className="schedule-page__form-row">
          <button
            type="button"
            className="schedule-page__secondary-button"
            disabled={!selectedDateForPreview}
            onClick={() => openAppointmentsPreview(selectedDateForPreview)}
          >
            Xem lịch hẹn trong ngày đã chọn
          </button>
        </div>

        <div className="schedule-page__form-row">
          <label className="schedule-page__form-label">
            Lý do khác
            <textarea
              className="schedule-page__textarea"
              rows={3}
              placeholder="Mô tả lý do..."
              value={newRequest.reason ?? ""}
              onChange={(event) =>
                updateNewRequest({
                  reason: event.target.value,
                })
              }
            />
          </label>
        </div>

        

        <button type="submit" className="schedule-page__primary-button">
          Xác nhận
        </button>
      </form>

      {leaveRequests.length > 0 && (
        <ul className="schedule-page__list schedule-page__list--compact">
          {leaveRequests.map((request) => (
            <li key={request.id} className="schedule-page__list-item">
              <div className="schedule-page__list-main">
                <div>
                  <p className="schedule-page__list-title">
                    {request.type === "time_off" && "Nghỉ phép"}
                    {request.type === "partial_day" && "Nghỉ một phần ngày"}
                    {request.type === "shift_change" && "Đổi ca / thay đổi lịch"}
                  </p>
                  <p className="schedule-page__list-meta">
                    {request.fromDate} - {request.toDate}
                  </p>
                  <p className="schedule-page__list-meta schedule-page__list-meta--muted">
                    {request.reason}
                  </p>
                </div>
                <span
                  className={`schedule-page__badge schedule-page__badge--status-${request.status}`}
                >
                  {request.status === "pending" && "Đang chờ duyệt"}
                  {request.status === "approved" && "Đã phê duyệt"}
                  {request.status === "rejected" && "Từ chối"}
                </span>
              </div>
              {request.adminComment && (
                <p className="schedule-page__admin-comment">
                  Ghi chú từ quản trị viên: {request.adminComment}
                </p>
              )}
            </li>
          ))}
        </ul>
      )}

      <AppointmentsPreviewModal
        date={appointmentsDate}
        isOpen={isAppointmentsModalOpen}
        onClose={() => setIsAppointmentsModalOpen(false)}
      />

    </div>
  );
}

