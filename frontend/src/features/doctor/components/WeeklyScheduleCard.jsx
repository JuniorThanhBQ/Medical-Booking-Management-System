import { DAY_LABELS } from "@/configs/const";

export default function WeeklyScheduleCard({
  weeklySchedule,
  timeOptions,
  toggleWorking,
  changeRange,
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
              <th className="schedule-page__table-col-wide">Khung giờ làm việc</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {weeklySchedule.map((entry) => (
              <tr key={entry.day}>
                <td>
                  <div className="schedule-page__day-cell">
                    <label className="schedule-page__day-label">
                      <input
                        type="checkbox"
                        checked={entry.isWorking}
                        onChange={() => toggleWorking(entry.day)}
                      />
                      <span>{DAY_LABELS[entry.day]}</span>
                    </label>
                    {!entry.isWorking && (
                      <span className="schedule-page__day-off">Nghỉ</span>
                    )}
                  </div>
                </td>
                <td>
                  {entry.isWorking && (
                    <div className="schedule-page__ranges">
                      {entry.ranges.map((range) => (
                        <div key={range.id} className="schedule-page__range-row">
                          <select
                            className="schedule-page__select"
                            value={range.start}
                            onChange={(event) =>
                              changeRange({
                                day: entry.day,
                                rangeId: range.id,
                                field: "start",
                                value: event.target.value,
                              })
                            }
                          >
                            {timeOptions.map((time) => (
                              <option key={time} value={time}>
                                {time}
                              </option>
                            ))}
                          </select>
                          <span className="schedule-page__range-separator">-</span>
                          <select
                            className="schedule-page__select"
                            value={range.end}
                            onChange={(event) =>
                              changeRange({
                                day: entry.day,
                                rangeId: range.id,
                                field: "end",
                                value: event.target.value,
                              })
                            }
                          >
                            {timeOptions.map((time) => (
                              <option key={time} value={time}>
                                {time}
                              </option>
                            ))}
                          </select>

                        </div>
                      ))}
                    </div>
                  )}
                </td>
                <td />
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

