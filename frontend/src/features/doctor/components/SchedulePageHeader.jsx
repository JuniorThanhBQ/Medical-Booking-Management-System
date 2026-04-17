export default function SchedulePageHeader() {
  return (
    <section className="schedule-page__header">
      <div className="schedule-page__header-inner">
        <div>
          <p className="schedule-page__eyebrow">Quản lý lịch làm việc</p>
          <h1 className="schedule-page__title">Lịch làm việc của bạn</h1>
          <p className="schedule-page__subtitle">
            Thiết lập giờ làm việc trong tuần, quản lý lịch hẹn của bạn. Lưu ý,
            chỉ được phép đổi lịch làm việc khi 30 ngày tới không có bệnh nhân.
            Nếu có, vui lòng liên hệ lễ tân để được hỗ trợ.
          </p>
        </div>
      </div>
    </section>
  );
}
