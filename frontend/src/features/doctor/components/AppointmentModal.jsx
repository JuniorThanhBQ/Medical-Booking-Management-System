import LoadingSpinner from "@features/shared/components/LoadingSpinner";
import { useEffect, useState } from "react";

import { fetchAppointmentsInDay } from "../services/appointments-api.js";

export default function AppointmentsPreviewModal({ date, isOpen, onClose }) {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isOpen) return;

    async function loadAppointments() {
      setLoading(true);
      setError("");

      try {
        const result = await fetchAppointmentsInDay({ date });
        setAppointments(Array.isArray(result) ? result : []);
      } catch {
        setAppointments([]);
        setError("Không thể tải lịch hẹn. Vui lòng thử lại.");
      } finally {
        setLoading(false);
      }
    }

    loadAppointments();
  }, [date, isOpen]);

  useEffect(() => {
    if (!isOpen) return;

    function onKeyDown(e) {
      if (e.key === "Escape") onClose();
    }

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="schedule-page__modal-backdrop"
      role="presentation"
      onClick={onClose}
    >
      <div
        className="schedule-page__modal"
        role="dialog"
        aria-modal="true"
        aria-label={`Lịch hẹn trong ngày ${date}`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="schedule-page__modal-header">
          <div>
            <p className="schedule-page__modal-title">Lịch hẹn trong ngày</p>
            <p className="schedule-page__modal-subtitle">{date}</p>
          </div>

          <button
            type="button"
            className="schedule-page__modal-close"
            onClick={onClose}
            aria-label="Đóng"
          >
            ×
          </button>
        </div>

        <div className="schedule-page__modal-body">
          {loading && <LoadingSpinner size="sm" label="Đang tải lịch hẹn..." />}

          {!loading && error && (
            <p className="schedule-page__modal-error">{error}</p>
          )}

          {!loading && !error && appointments.length === 0 && (
            <p className="schedule-page__modal-hint">
              Không có lịch hẹn trong ngày này.
            </p>
          )}

          {!loading && !error && appointments.length > 0 && (
            <ul className="schedule-page__appointments">
              {appointments.map((appt) => (
                <li key={appt.id} className="schedule-page__appointments-item">
                  <div className="schedule-page__appointments-main">
                    <p className="schedule-page__appointments-time">
                      {appt.startTime} - {appt.endTime}
                    </p>

                    <p className="schedule-page__appointments-patient">
                      {appt.patientName || "Bệnh nhân"}
                    </p>

                    {appt.notes && (
                      <p className="schedule-page__appointments-notes">
                        {appt.notes}
                      </p>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
