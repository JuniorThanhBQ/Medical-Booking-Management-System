import SearchCard from "./SearchCard.jsx";

const DashboardHero = ({ onSearch, searching }) => {
  return (
    <section className="dashboard__hero">
      <div className="dashboard__hero-content">
        <h1 className="dashboard__title">
          Khám phá các chuyên khoa của chúng tôi
        </h1>

        <p className="dashboard__subtitle">
          Dễ dàng tra cứu bác sĩ theo chuyên khoa hoặc tên
        </p>

        <p className="dashboard__description">
          Chăm sóc sức khỏe chất lượng, được cá nhân hóa theo nhu cầu của bạn,
          chỉ cách một cú nhấp chuột.
        </p>
      </div>

      <div className="dashboard__hero-search">
        <SearchCard onSearch={onSearch} searching={searching} />
      </div>
    </section>
  );
};

export default DashboardHero;
