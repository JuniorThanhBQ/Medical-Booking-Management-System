import { useMemo, useState } from "react";
import "@/assets/css/users/dashboard.css";
import Navbar from "../components/Navbar";
import { SPECIALTIES } from "@/data/mocks/specialties";
import { DOCTORS } from "@/data/mocks/doctors";
import SpecialtyCard from "../components/SpecialtyCard";
import DashboardHero from "../components/DashboardHero";
import { useNavigate } from "react-router-dom";
import { validateAppointmentDate } from "../utils/dashboard-util";
import { normalizeQuery } from "@/utils/utils";
const Dashboard = () => {
  const navigate = useNavigate();

  const [searchResults, setSearchResults] = useState(null);
  const [lastSearchParams, setLastSearchParams] = useState(null);
  const [searchError, setSearchError] = useState(null);

  const specialtyById = useMemo(() => {
    const map = {};
    SPECIALTIES.forEach((specialty) => {
      map[specialty.id] = specialty;
    });
    return map;
  }, []);

  const handleSearch = ({ query, date }) => {
    const normalizedQuery = normalizeQuery(query || "");
    let error = null;

    console.log(query, date, normalizedQuery);

    const { isValid, error: dateError } = validateAppointmentDate(date);
    if (!isValid) {
      error = dateError;
    }

    if (!isValid) {
      setSearchResults([]);
      setLastSearchParams({ query, date });
      setSearchError(error);
      return;
    }

    // should be replaced with api call
    const matchingDoctors = DOCTORS.filter((doctor) => {
      if (!normalizedQuery) {
        return true;
      }

      const nameMatch = doctor.name.toLowerCase().includes(normalizedQuery);
      const titleMatch = doctor.title.toLowerCase().includes(normalizedQuery);
      const specialtyName =
        specialtyById[doctor.specialtyId]?.name?.toLowerCase() || "";
      const specialtyMatch = specialtyName.includes(normalizedQuery);

      return nameMatch || titleMatch || specialtyMatch;
    });

    const specialtyIds = new Set(
      matchingDoctors.map((doctor) => doctor.specialtyId),
    );

    const results = SPECIALTIES.filter((specialty) =>
      specialtyIds.has(specialty.id),
    );

    setSearchResults(results);
    setLastSearchParams({ query, date });
    setSearchError(null);
  };

  return (
    <>
      <Navbar />

      <main className="dashboard">
        <DashboardHero onSearch={handleSearch} />

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
                  Chọn một chuyên khoa để xem các bác sĩ được đánh giá cao trong
                  lĩnh vực đó.
                </p>
              </div>
            </div>

            <div className="dashboard__specialties-grid">
              {SPECIALTIES.map((specialty) => (
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
