import { BriefcaseIcon } from "@/assets/icons";

const UpcomingActivityCard = ({ onSearchVenues }) => {
  return (
    <div className="profile-activity__upcoming">
      <div className="profile-activity__empty">
        <div className="profile-activity__empty-icon">
          <BriefcaseIcon size={22} />
        </div>

        <p className="profile-activity__empty-title">Không có lịch hẹn sắp tới</p>
        <p className="profile-activity__empty-desc">
          Lịch hẹn sắp tới sẽ hiển thị tại đây khi bạn đặt lịch
        </p>

      </div>
    </div>
  );
};

export default UpcomingActivityCard;

