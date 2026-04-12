import { useEffect, useState } from "react";
import "@/assets/css/users/dashboard.css";
import Navbar from "../components/Navbar";
import { getSpecialties } from "@features/shared/services/public-api-service";
import SpecialtyCard from "../components/SpecialtyCard";
import DashboardHero from "../components/DashboardHero";
import { useNavigate } from "react-router-dom";
import { useDashboardSearch } from "../hooks/use-dashboard-search";
import LoadingSpinner from "@features/shared/components/LoadingSpinner"

const Dashboard = () => {
  const navigate = useNavigate();

  const [specialties, setSpecialties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getSpecialties({ limit: 50 })
      .then((items) => {
        setSpecialties(items);
        setError(null);
      })
      .catch(() => setError("Không thể tải dữ liệu chuyên khoa."))
      .finally(() => setLoading(false));
  }, []);


  const { searchResults, lastSearchParams, searchError, searching, handleSearch } =
    useDashboardSearch(specialties);

  if (loading) {
    return (
      <>
        <Navbar />
        <main className="dashboard">
          <LoadingSpinner fullPage label="Đang tải..." />
        </main>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Navbar />
        <main className="dashboard">
          <p style={{ textAlign: "center", padding: "2rem", color: "#c00" }}>
            {error}
          </p>
        </main>
      </>
    );
  }

  return (
    <>
      <Navbar />

      <main className="dashboard">
        <DashboardHero onSearch={handleSearch} searching={searching} />

        {lastSearchParams && (
          <section className="dashboard__specialties-section">
            <div className="dashboard__specialties-inner">
              <div className="dashboard__specialties-header">
                <div>
                  <h2 className="dashboard__specialties-title">
                    Kết quả tìm kiếm
                  </h2>
                  <p className="dashboard__specialties-subtitle">
                    Danh sách chuyên khoa có bác sĩ phù hợp với tìm kiếm của
                    bạn.
                  </p>
                </div>
              </div>

              {searchError ? (
                <p className="dashboard__search-error">{searchError}</p>
              ) : searching ? (
                <LoadingSpinner size="sm" label="Đang tìm kiếm..." />
              ) : searchResults && searchResults.length > 0 ? (
                <div className="dashboard__specialties-grid">
                  {searchResults.map((specialty) => (
                    <SpecialtyCard
                      key={specialty.id}
                      specialty={specialty}
                      onClick={() => navigate(`/specialties/${specialty.id}`)}
                    />
                  ))}
                </div>
              ) : (
                <p className="dashboard__search-empty">
                  Không tìm thấy kết quả.
                </p>
              )}
            </div>
          </section>
        )}

        <section className="dashboard__specialties-section">
          <div className="dashboard__specialties-inner">
            <div className="dashboard__specialties-header">
              <div>
                <h2 className="dashboard__specialties-title">
                  Dịch vụ theo khoa
                </h2>
                <p className="dashboard__specialties-subtitle">
                  Chọn một chuyên khoa để xem các bác sĩ được đánh giá cao
                  trong lĩnh vực đó.
                </p>
              </div>
            </div>

            <div className="dashboard__specialties-grid">
              {specialties.map((specialty) => (
                <SpecialtyCard
                  key={specialty.id}
                  specialty={specialty}
                  onClick={() => navigate(`/specialties/${specialty.id}`)}
                />
              ))}
            </div>
          </div>
        </section>
      </main>
    </>
  );
};

export default Dashboard;
