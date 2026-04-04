import { INITIAL_DAYS, DAY_LABELS } from "@/configs/const";

export default function WeeklyScheduleCard({
  workDate,
  startTime,
  endTime,
  timeOptions,
  toggleWorking,
  setTime,
  onSave,
  isSaving,
}) {
  return (
    <div className="schedule-page__card">
      <div className="schedule-page__card-header">
        <h2 className="schedule-page__card-title">Giờ làm việc theo tuần</h2>
        <p className="schedule-page__card-description">
          Cài đặt khung giờ khám mặc định cho từng ngày trong tuần. Bệnh nhân chỉ có thể đặt lịch
          trong các khung giờ này.
        </p>
      </div>

      <div className="schedule-page__table-wrapper">
        <table className="schedule-page__table">
          <thead>
            <tr>
              <th>Ngày</th>
              <th className="schedule-page__table-col-wide" />
              <th />
            </tr>
          </thead>
          <tbody>
            {INITIAL_DAYS.map((day) => {
              const isWorking = workDate.includes(day);
              return (
                <tr key={day}>
                  <td>
                    <div className="schedule-page__day-cell">
                      <label className="schedule-page__day-label">
                        <input
                          type="checkbox"
                          checked={isWorking}
                          onChange={() => toggleWorking(day)}
                        />
                        <span>{DAY_LABELS[day]}</span>
                      </label>
                      {!isWorking && (
                        <span className="schedule-page__day-off">Nghỉ</span>
                      )}
                    </div>
                  </td>
                  <td />
                  <td />
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="schedule-page__time-row">
        <div className="schedule-page__time-field">
          <span className="schedule-page__time-label">Giờ bắt đầu</span>
          <select
            className="schedule-page__select"
            value={startTime}
            onChange={(e) => setTime("startTime", e.target.value)}
          >
            {timeOptions.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>
        <span className="schedule-page__time-arrow">→</span>
        <div className="schedule-page__time-field">
          <span className="schedule-page__time-label">Giờ kết thúc</span>
          <select
            className="schedule-page__select"
            value={endTime}
            onChange={(e) => setTime("endTime", e.target.value)}
          >
            {timeOptions.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="schedule-page__card-footer">
        <button
          className="schedule-page__primary-button"
          onClick={onSave}
          disabled={isSaving}
        >
          {isSaving ? "Đang lưu..." : "Lưu lịch làm việc"}
        </button>
      </div>
    </div>
  );
}
