import "@css/doctor/schedule.css";

import { useSchedulePage } from "@features/doctor/hooks/use-schedule-page";
import LoadingSpinner from "@features/shared/components/LoadingSpinner";
import Navbar from "@features/users/components/Navbar";

import SchedulePageHeader from "../components/SchedulePageHeader";
import WeeklyScheduleCard from "../components/WeeklyScheduleCard";

export default function SchedulePage() {
  const {
    workDate,
    startTime,
    endTime,
    timeOptions,
    toggleWorking,
    setTime,
    isLoading,
    scheduleError,
    saveSuccess,
    clearScheduleError,
    handleSave,
    hasSchedule,
    upcomingAppointmentsCount,
    workingDaysText,
    hasUpcoming,
  } = useSchedulePage();

  return (
    <>
      <Navbar />
      <main className="schedule-page">
        <SchedulePageHeader />

        {scheduleError && (
          <div className="schedule-page__alert schedule-page__alert--error">
            <span>{scheduleError}</span>
            <button onClick={clearScheduleError}>&#10005;</button>
          </div>
        )}
        {saveSuccess && (
          <div className="schedule-page__alert schedule-page__alert--success">
            Lưu lịch làm việc thành công!
          </div>
        )}

        {isLoading && (!workDate || workDate.length === 0) ? (
          <LoadingSpinner fullPage label="Đang tải lịch làm việc..." />
        ) : (
          <section className="schedule-page__content">
            <div
              className="schedule-summary-cards"
              style={{ display: "flex", gap: "20px", marginBottom: "24px" }}
            >
              <div
                className="summary-card"
                style={{
                  flex: 1,
                  padding: "20px",
                  backgroundColor: "#f8fafc",
                  borderRadius: "12px",
                  border: "1px solid #e2e8f0",
                }}
              >
                <h3
                  style={{
                    margin: "0 0 12px 0",
                    fontSize: "16px",
                    color: "#64748b",
                  }}
                >
                  Thông tin lịch hiện tại
                </h3>
                <div style={{ fontSize: "15px", color: "#0f172a" }}>
                  {hasSchedule ? (
                    <>
                      <p style={{ margin: "0 0 8px 0" }}>
                        <strong>Khung giờ:</strong> {startTime} - {endTime}
                      </p>
                      <p style={{ margin: 0 }}>
                        <strong>Ngày làm việc:</strong> {workingDaysText}
                      </p>
                    </>
                  ) : (
                    <p
                      style={{
                        margin: 0,
                        color: "#94a3b8",
                        fontStyle: "italic",
                      }}
                    >
                      Bạn chưa thiết lập lịch làm việc hàng tuần. Vui lòng sử
                      dụng form bên dưới để tạo lịch hoặc liên hệ admin để được
                      hỗ trợ.
                    </p>
                  )}
                </div>
              </div>

              <div
                className="summary-card"
                style={{
                  flex: 1,
                  padding: "20px",
                  backgroundColor: hasUpcoming ? "#fef2f2" : "#f0fdf4",
                  borderRadius: "12px",
                  border: `1px solid ${hasUpcoming ? "#fecaca" : "#bbf7d0"}`,
                }}
              >
                <h3
                  style={{
                    margin: "0 0 12px 0",
                    fontSize: "16px",
                    color: hasUpcoming ? "#991b1b" : "#166534",
                  }}
                >
                  Lịch hẹn trong 30 ngày tới
                </h3>
                <div
                  style={{
                    display: "flex",
                    alignItems: "baseline",
                    gap: "8px",
                  }}
                >
                  <span
                    style={{
                      fontSize: "32px",
                      fontWeight: "bold",
                      color: hasUpcoming ? "#b91c1c" : "#15803d",
                    }}
                  >
                    {upcomingAppointmentsCount}
                  </span>
                  <span style={{ color: hasUpcoming ? "#991b1b" : "#166534" }}>
                    bệnh nhân
                  </span>
                </div>
              </div>
            </div>

            <WeeklyScheduleCard
              workDate={workDate}
              startTime={startTime}
              endTime={endTime}
              timeOptions={timeOptions}
              toggleWorking={toggleWorking}
              setTime={setTime}
              onSave={handleSave}
              isSaving={isLoading}
            />
          </section>
        )}
      </main>
    </>
  );
}
