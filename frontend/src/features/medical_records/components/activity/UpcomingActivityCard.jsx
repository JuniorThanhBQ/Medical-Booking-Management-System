import { BriefcaseIcon } from "@/assets/icons";
import { getStatusLabel } from "@/configs/const";
import { getStatusClassName } from "../../../users/utils/profile-utils.js";

const UpcomingActivityCard = ({ items = [] }) => {
  if (items.length === 0) {
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
  }

  return (
    <div className="profile-activity__upcoming">
      {items.map((item) => {
        const statusModifier = item.status === "confirmed" ? "--confirmed" : "--pending";
        return (
          <div
            key={item.id}
            className={`profile-activity__upcoming-card profile-activity__upcoming-card${statusModifier}`}
          >
            <div className="profile-activity__upcoming-header">
              <span className="profile-activity__upcoming-title">{item.title}</span>
              <span className={`profile-activity__pill ${getStatusClassName(item.status)}`}>
                {getStatusLabel(item.status)}
              </span>
            </div>
            <p className="profile-activity__upcoming-meta">{item.meta}</p>
          </div>
        );
      })}
    </div>
  );
};

export default UpcomingActivityCard;
