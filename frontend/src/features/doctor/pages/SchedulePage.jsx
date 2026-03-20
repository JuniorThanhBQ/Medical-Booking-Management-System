import "@/assets/css/users/schedule.css";
import Navbar from "../../users/components/Navbar";
import { useScheduleStore } from "../hooks/use-schedule-store";
import SchedulePageHeader from "../components/SchedulePageHeader";
import WeeklyScheduleCard from "../components/WeeklyScheduleCard";
import LeaveRequestsCard from "../components/LeaveRequestsCard";

export default function SchedulePage() {
  const {
    weeklySchedule,
    leaveRequests,
    newRequest,
    timeOptions,
    toggleWorking,
    changeRange,
    updateNewRequest,
    addLeaveRequest,
  } = useScheduleStore((state) => state);

  function handleAddRequest(event) {
    event.preventDefault();
    addLeaveRequest();
  }

  return (
    <>
      <Navbar />

      <main className="schedule-page">
        <SchedulePageHeader />

        <section className="schedule-page__content">
          <div className="schedule-page__grid">
            <WeeklyScheduleCard
              weeklySchedule={weeklySchedule}
              timeOptions={timeOptions}
              toggleWorking={toggleWorking}
              changeRange={changeRange}
            />

            <div className="schedule-page__side-column">
              <LeaveRequestsCard
                newRequest={newRequest}
                updateNewRequest={updateNewRequest}
                leaveRequests={leaveRequests}
                onSubmit={handleAddRequest}
              />
            </div>
          </div>
        </section>
      </main>
    </>
  );
}
