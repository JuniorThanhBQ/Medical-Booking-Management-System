import { useEffect } from "react";
import "@/assets/css/users/schedule.css";
import Navbar from "../../users/components/Navbar";
import { useScheduleStore } from "../hooks/use-schedule-store";
import SchedulePageHeader from "../components/SchedulePageHeader";
import WeeklyScheduleCard from "../components/WeeklyScheduleCard";
import LoadingSpinner from "@/components/LoadingSpinner";

export default function SchedulePage() {
  const {
    workDate, startTime, endTime, timeOptions,
    toggleWorking, setTime,
    isLoading, scheduleError, saveSuccess,
    loadSchedule, saveSchedule, clearScheduleError,
  } = useScheduleStore((state) => state);

  useEffect(() => { loadSchedule(); }, [loadSchedule]);

  useEffect(() => {
    if (!saveSuccess) return;
    const timer = setTimeout(() => clearScheduleError(), 3000);
    return () => clearTimeout(timer);
  }, [saveSuccess, clearScheduleError]);

  return (
    <>
      <Navbar />

      <main className="schedule-page">
        <SchedulePageHeader />

        {scheduleError && (
          <div className="schedule-page__alert schedule-page__alert--error">
            <span>{scheduleError}</span>
            <button onClick={clearScheduleError}>&times;</button>
          </div>
        )}
        {saveSuccess && (
          <div className="schedule-page__alert schedule-page__alert--success">
            Lưu lịch làm việc thành công!
          </div>
        )}

        {isLoading && workDate.length === 0 ? (
          <LoadingSpinner />
        ) : (
          <section className="schedule-page__content">
            <WeeklyScheduleCard
              workDate={workDate}
              startTime={startTime}
              endTime={endTime}
              timeOptions={timeOptions}
              toggleWorking={toggleWorking}
              setTime={setTime}
              onSave={() => saveSchedule()}
              isSaving={isLoading}
            />
          </section>
        )}
      </main>
    </>
  );
}
