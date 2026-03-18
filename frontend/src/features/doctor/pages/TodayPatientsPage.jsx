import "@/assets/css/users/today-patients.css";
import Navbar from "@/features/users/components/Navbar";
import { getRoleMenuItems } from "@/utils/utils";
import { DEFAULT_NAV_LINKS } from "@/configs/const";
import { getStatusLabel } from "@/configs/const";
import { APPOINTMENT_STATUS } from "@/configs/const";
import { mockTodayAppointments } from "../data";

export default function TodayPatientsPage() {
  
  const hasAppointments = mockTodayAppointments.length > 0;

  return (
    <>
      <Navbar menuItems={getRoleMenuItems()} navLinks={DEFAULT_NAV_LINKS} />

      <main className="today-patients">
        <section className="today-patients__header">
          <div className="today-patients__header-inner">
            <div>
              <p className="today-patients__eyebrow">Lịch hẹn hôm nay</p>
              <h1 className="today-patients__title">Bệnh nhân hôm nay</h1>
              <p className="today-patients__subtitle">
                Xem nhanh danh sách bệnh nhân và khung giờ khám trong ngày hôm nay.
              </p>
            </div>
          </div>
        </section>

        <section className="today-patients__section">
          <div className="today-patients__section-inner">
            {!hasAppointments ? (
              <div className="today-patients__empty">
                <h2 className="today-patients__empty-title">
                  Hôm nay bạn chưa có lịch hẹn nào
                </h2>
                <p className="today-patients__empty-subtitle">
                  Khi bệnh nhân đặt lịch khám, lịch hẹn trong ngày sẽ hiển thị tại đây.
                </p>
              </div>
            ) : (
              <div className="today-patients__list">
                {mockTodayAppointments.map((appointment, index) => {
                  const isNext = index === 0 || appointment.status === APPOINTMENT_STATUS.IN_PROGRESS;

                  return (
                    <article
                      key={appointment.id}
                      className={`today-patients__item${
                        isNext ? " today-patients__item--next" : ""
                      }`}
                    >
                      <div className="today-patients__item-main">
                        <div>
                          <h2 className="today-patients__patient-name">
                            {appointment.patientName}
                          </h2>
                          {appointment.notes && (
                            <p className="today-patients__notes">
                              {appointment.notes}
                            </p>
                          )}
                        </div>
                        <div className="today-patients__meta">
                          <span className="today-patients__time">
                            {appointment.startTime} - {appointment.endTime}
                          </span>
                          <span
                            className={`today-patients__status today-patients__status--${appointment.status}`}
                          >
                            {getStatusLabel(appointment.status)}
                          </span>
                        </div>
                      </div>

                      {isNext && (
                        <p className="today-patients__hint">
                          Đây là bệnh nhân tiếp theo mà bạn sẽ khám.
                        </p>
                      )}
                    </article>
                  );
                })}
              </div>
            )}
          </div>
        </section>
      </main>
    </>
  );
}
