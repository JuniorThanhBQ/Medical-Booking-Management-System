import { formatTimeDisplay, toISODate } from "@utils/booking-utils";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

import { BASE_URL, endpoints } from "@/configs/apis";
import useAuth from "@/contexts/auth/AuthContext";

export function BookingConfirmStep({
  specialtyName,
  serviceName,
  selectedDate,
  selectedTime,
  selectedDoctorName,
  patientNotes,
  onPatientNotesChange,
  onConfirm,
  canConfirm,
  submitting = false,
  submitError = null,
  isReceptionist,
  patientInfo,
  onInfoChange,
  onTimeout,
}) {
  const { api } = useAuth();
  const navigate = useNavigate();
  const [isLocked, setIsLocked] = useState(false);
  const [lockError, setLockError] = useState(null);

  const timerRef = useRef(null);
  const isConfirmedRef = useRef(false);

  const payload = useMemo(
    () => ({
      appointmentDate: selectedTime,
      doctorName: selectedDoctorName,
      serviceName: serviceName,
    }),
    [selectedTime, selectedDoctorName, serviceName],
  );

  const unlockOnUnload = useCallback(() => {
    const token =
      api.defaults?.headers?.Authorization ||
      api.defaults?.headers?.common?.Authorization;
    const headers = { "Content-Type": "application/json" };
    if (token) headers["Authorization"] = token;

    fetch(`${BASE_URL}${endpoints.booking_transaction_unlock}`, {
      method: "POST",
      headers,
      body: JSON.stringify(payload),
      keepalive: true,
    }).catch(() => {});
  }, [api, payload]);

  useEffect(() => {
    if (!api || !selectedDoctorName || !serviceName || !selectedTime) return;

    let isMounted = true;
    let isLockApiCalled = false;

    const lockTransaction = async () => {
      isLockApiCalled = true;
      try {
        const res = await api.post(endpoints.booking_transaction_lock, payload);
        if (res.status === 204 || res.status === 200) {
          if (isMounted) {
            setIsLocked(true);
            timerRef.current = setTimeout(() => {
              toast.error("Phát hiện treo máy, đã huỷ lịch hẹn.");
              if (onTimeout) onTimeout();
              navigate("/dashboard");
            }, 1200000);
          }
        }
      } catch (error) {
        if (isMounted) {
          if (error.response?.status === 409) {
            setLockError("Khung giờ này đang được người khác giữ chỗ.");
            toast.error("Khung giờ đang được người khác đặt.");
            navigate("/dashboard");
          } else {
            setLockError("Chức năng đặt lịch đang có vấn đề thử lại sau.");
            toast.error("Có lỗi xảy ra trong luồng đặt lịch");
            navigate("/dashboard");
          }
        }
      }
    };

    lockTransaction();

    const handleBeforeUnload = () => {
      if (isLockApiCalled && !isConfirmedRef.current) {
        unlockOnUnload();
      }
    };

    window.addEventListener("beforeunload", handleBeforeUnload);

    return () => {
      isMounted = false;
      if (timerRef.current) clearTimeout(timerRef.current);
      window.removeEventListener("beforeunload", handleBeforeUnload);

      if (isLockApiCalled && !isConfirmedRef.current) {
        api.post(endpoints.booking_transaction_unlock, payload).catch(() => {});
      }
    };
  }, [
    api,
    payload,
    onTimeout,
    navigate,
    unlockOnUnload,
    selectedDoctorName,
    serviceName,
    selectedTime,
  ]);

  const handleConfirmClick = async () => {
    isConfirmedRef.current = true;
    try {
      await api.post(endpoints.booking_transaction_unlock, payload);
      onConfirm();
    } catch {
      isConfirmedRef.current = false;
      toast.error("Lỗi khi mở khóa lịch hẹn, vui lòng thử lại.");
    }
  };

  const isButtonDisabled =
    !canConfirm || submitting || !!lockError || !isLocked;

  return (
    <div className="booking__step-panel">
      <h2 className="booking__panel-title">Xác nhận thông tin</h2>
      <p className="booking__panel-subtitle">
        Kiểm tra thông tin trước khi xác nhận.
      </p>
      <div className="booking__confirm">
        <div className="booking__confirm-row">
          <span className="booking__confirm-label">Chuyên khoa</span>
          <span className="booking__confirm-value">{specialtyName}</span>
        </div>
        <div className="booking__confirm-row">
          <span className="booking__confirm-label">Dịch vụ</span>
          <span className="booking__confirm-value">{serviceName || "—"}</span>
        </div>
        <div className="booking__confirm-row">
          <span className="booking__confirm-label">Ngày</span>
          <span className="booking__confirm-value">
            {selectedDate ? toISODate(selectedDate) : "—"}
          </span>
        </div>
        <div className="booking__confirm-row">
          <span className="booking__confirm-label">Thời gian</span>
          <span className="booking__confirm-value">
            {selectedTime ? formatTimeDisplay(selectedTime) : "—"}
          </span>
        </div>
        <div className="booking__confirm-row">
          <span className="booking__confirm-label">Bác sĩ</span>
          <span className="booking__confirm-value">
            {selectedDoctorName || "—"}
          </span>
        </div>
        <div className="booking__notes">
          <label className="booking__notes-label" htmlFor="notes">
            Ghi chú (tùy chọn)
          </label>
          <textarea
            id="notes"
            className="booking__notes-input"
            placeholder="Bất kỳ triệu chứng, sở thích hay câu hỏi nào cho bác sĩ..."
            value={patientNotes}
            onChange={(e) => onPatientNotesChange(e.target.value)}
          />
        </div>
      </div>
      {isReceptionist && (
        <div className="booking__receptionist-form">
          <h3 className="booking__receptionist-title">Thông tin bệnh nhân</h3>

          <div className="booking__input-group">
            <input
              className="booking__notes-input"
              placeholder="Họ"
              value={patientInfo.firstName}
              onChange={(e) => onInfoChange.setFirstName(e.target.value)}
            />
            <input
              className="booking__notes-input"
              placeholder="Tên"
              value={patientInfo.lastName}
              onChange={(e) => onInfoChange.setLastName(e.target.value)}
            />
          </div>

          <input
            className="booking__notes-input"
            placeholder="Số điện thoại"
            value={patientInfo.phone}
            onChange={(e) => onInfoChange.setPhone(e.target.value)}
          />

          <div className="booking__input-group">
            <select
              className="booking__notes-input"
              value={patientInfo.gender}
              onChange={(e) => onInfoChange.setGender(e.target.value)}
            >
              <option value="MALE">Nam</option>
              <option value="FEMALE">Nữ</option>
            </select>
            <input
              type="date"
              className="booking__notes-input"
              value={patientInfo.birthday}
              onChange={(e) => onInfoChange.setBirthday(e.target.value)}
            />
          </div>

          <input
            className="booking__notes-input"
            placeholder="Địa chỉ"
            value={patientInfo.address}
            onChange={(e) => onInfoChange.setAddress(e.target.value)}
          />
        </div>
      )}
      <div className="booking__confirm-actions">
        <button
          type="button"
          className="booking__primary"
          onClick={handleConfirmClick}
          disabled={isButtonDisabled}
        >
          {submitting
            ? "Đang xử lý..."
            : !isLocked && !lockError
              ? "Đang giữ chỗ..."
              : "Xác nhận lịch hẹn"}
        </button>
        {submitError && <p className="booking__error">{submitError}</p>}
        {lockError && <p className="booking__error">{lockError}</p>}
        <p className="booking__hint">
          Bằng việc xác nhận, bạn đồng ý thông tin trên là chính xác.
        </p>
      </div>
    </div>
  );
}
