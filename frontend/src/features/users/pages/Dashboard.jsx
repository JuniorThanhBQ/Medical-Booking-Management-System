import "@css/users/dashboard.css";

import LoadingSpinner from "@features/shared/components/LoadingSpinner";
import {
  getDoctors,
  getSpecialties,
} from "@features/shared/services/public-api-service";
import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { normalizeQuery } from "@/utils/Utils.js";

import DashboardHero from "../components/DashboardHero";
import Navbar from "../components/Navbar";
import SpecialtyCard from "../components/SpecialtyCard";

const Dashboard = () => {
  const navigate = useNavigate();

  const [keyword, setKeyword] = useState("");
  const [activeSearchType, setActiveSearchType] = useState("all");

  const [specialtiesData, setSpecialtiesData] = useState({
    items: [],
    meta: null,
  });
  const [specialtyPage, setSpecialtyPage] = useState(1);
  const [specialtiesLoading, setSpecialtiesLoading] = useState(false);

  const [doctorsData, setDoctorsData] = useState({ items: [], meta: null });
  const [doctorPage, setDoctorPage] = useState(1);
  const [doctorsLoading, setDoctorsLoading] = useState(false);

  const [workDate, setWorkDate] = useState("");

  const [globalError, setGlobalError] = useState(null);

  const fetchSpecialties = useCallback(async (page, searchKeyword, type) => {
    if (type === "doctor") {
      setSpecialtiesData({ items: [], meta: null });
      return;
    }

    setSpecialtiesLoading(true);
    try {
      const data = await getSpecialties({
        page,
        keywords: searchKeyword,
        limit: 4,
      });
      setSpecialtiesData({ items: data.items || [], meta: data.meta });
    } catch {
      setGlobalError("Không thể tải dữ liệu chuyên khoa.");
    } finally {
      setSpecialtiesLoading(false);
    }
  }, []);

  const fetchDoctors = useCallback(
    async (page, searchKeyword, selectedDate, type) => {
      if (type === "specialty") {
        setDoctorsData({ items: [], meta: null });
        return;
      }

      setDoctorsLoading(true);
      try {
        const params = { page, keywords: searchKeyword, limit: 4 };
        if (selectedDate) params.workDates = selectedDate;

        const data = await getDoctors(params);
        setDoctorsData({ items: data.items || [], meta: data.meta });
      } catch {
        setGlobalError("Không thể tải dữ liệu bác sĩ.");
      } finally {
        setDoctorsLoading(false);
      }
    },
    [],
  );

  useEffect(() => {
    fetchSpecialties(specialtyPage, keyword, activeSearchType);
  }, [specialtyPage, keyword, activeSearchType, fetchSpecialties]);

  useEffect(() => {
    fetchDoctors(doctorPage, keyword, workDate, activeSearchType);
  }, [doctorPage, keyword, workDate, activeSearchType, fetchDoctors]);

  const handleSearch = ({ query, type }) => {
    const normalizedQuery = normalizeQuery(query || "");
    setKeyword(normalizedQuery);
    setActiveSearchType(type);
    setSpecialtyPage(1);
    setDoctorPage(1);
  };

  const getInitials = (lastName = "", firstName = "") => {
    const l = lastName.charAt(0).toUpperCase();
    const f = firstName.charAt(0).toUpperCase();
    return `${l}${f}`;
  };

  if (globalError) {
    return (
      <>
        <Navbar />
        <main className="dashboard">
          <p style={{ textAlign: "center", padding: "2rem", color: "#c00" }}>
            {globalError}
          </p>
        </main>
      </>
    );
  }

  const showSpecialties =
    activeSearchType === "all" || activeSearchType === "specialty";
  const showDoctors =
    activeSearchType === "all" || activeSearchType === "doctor";

  return (
    <>
      <Navbar />
      <main className="dashboard">
        <DashboardHero
          onSearch={handleSearch}
          searching={specialtiesLoading || doctorsLoading}
        />

        {showSpecialties && (
          <section className="dashboard__specialties-section">
            <div className="dashboard__specialties-inner">
              <div className="dashboard__specialties-header">
                <div>
                  <h2 className="dashboard__specialties-title">
                    Dịch vụ theo khoa
                  </h2>
                  <p className="dashboard__specialties-subtitle">
                    {keyword
                      ? `Kết quả tìm kiếm chuyên khoa cho "${keyword}"`
                      : "Chọn một chuyên khoa để xem các bác sĩ trong lĩnh vực đó."}
                  </p>
                </div>
              </div>

              {specialtiesLoading ? (
                <LoadingSpinner size="sm" label="Đang tải chuyên khoa..." />
              ) : specialtiesData.items.length > 0 ? (
                <>
                  <div className="dashboard__specialties-grid">
                    {specialtiesData.items.map((specialty) => (
                      <SpecialtyCard
                        key={specialty.id}
                        specialty={specialty}
                        onClick={() => navigate(`/specialties/${specialty.id}`)}
                      />
                    ))}
                  </div>

                  {specialtiesData.meta && specialtiesData.meta.pages > 1 && (
                    <div className="pagination-controls">
                      <button
                        onClick={() => setSpecialtyPage((prev) => prev - 1)}
                        disabled={!specialtiesData.meta.hasPrev}
                      >
                        Trang trước
                      </button>
                      <span>
                        Trang {specialtiesData.meta.currentPage} /{" "}
                        {specialtiesData.meta.pages}
                      </span>
                      <button
                        onClick={() => setSpecialtyPage((prev) => prev + 1)}
                        disabled={!specialtiesData.meta.hasNext}
                      >
                        Trang sau
                      </button>
                    </div>
                  )}
                </>
              ) : (
                <p className="dashboard__search-empty">
                  Không tìm thấy chuyên khoa nào.
                </p>
              )}
            </div>
          </section>
        )}

        {showDoctors && (
          <section
            className="dashboard__specialties-section"
            style={{ backgroundColor: "#f9fafb" }}
          >
            <div className="dashboard__specialties-inner">
              <div
                className="dashboard__specialties-header"
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  flexWrap: "wrap",
                  gap: "1rem",
                }}
              >
                <div>
                  <h2 className="dashboard__specialties-title">
                    Danh sách bác sĩ
                  </h2>
                  <p className="dashboard__specialties-subtitle">
                    {keyword
                      ? `Kết quả tìm kiếm bác sĩ cho "${keyword}"`
                      : "Đội ngũ bác sĩ chuyên môn cao, giàu kinh nghiệm."}
                  </p>
                </div>

                <div>
                  <select
                    value={workDate}
                    onChange={(e) => {
                      setWorkDate(e.target.value);
                      setDoctorPage(1);
                    }}
                    style={{
                      padding: "0.6rem 1rem",
                      borderRadius: "8px",
                      border: "1px solid #d1d5db",
                      backgroundColor: "#fff",
                      cursor: "pointer",
                      outline: "none",
                      fontSize: "0.95rem",
                    }}
                  >
                    <option value="">Tất cả ngày làm việc</option>
                    <option value="MONDAY">Thứ Hai</option>
                    <option value="TUESDAY">Thứ Ba</option>
                    <option value="WEDNESDAY">Thứ Tư</option>
                    <option value="THURSDAY">Thứ Năm</option>
                    <option value="FRIDAY">Thứ Sáu</option>
                    <option value="SATURDAY">Thứ Bảy</option>
                    <option value="SUNDAY">Chủ Nhật</option>
                  </select>
                </div>
              </div>

              {doctorsLoading ? (
                <LoadingSpinner size="sm" label="Đang tải bác sĩ..." />
              ) : doctorsData.items.length > 0 ? (
                <>
                  <div className="dashboard__specialties-grid">
                    {doctorsData.items.map((doctor) => (
                      <div
                        key={doctor.id}
                        className="doctor-card"
                        style={{
                          padding: "1.2rem",
                          border: "1px solid #ddd",
                          borderRadius: "12px",
                          cursor: "pointer",
                          backgroundColor: "#fff",
                          display: "flex",
                          alignItems: "center",
                          gap: "1rem",
                          transition: "box-shadow 0.2s",
                        }}
                        onClick={() => navigate(`/doctors/${doctor.id}`)}
                        onMouseEnter={(e) =>
                          (e.currentTarget.style.boxShadow =
                            "0 4px 12px rgba(0,0,0,0.05)")
                        }
                        onMouseLeave={(e) =>
                          (e.currentTarget.style.boxShadow = "none")
                        }
                      >
                        <div
                          style={{
                            width: "64px",
                            height: "64px",
                            borderRadius: "50%",
                            backgroundColor: "#e5e7eb",
                            color: "#374151",
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            fontSize: "1.25rem",
                            fontWeight: "bold",
                            flexShrink: 0,
                            overflow: "hidden",
                          }}
                        >
                          {doctor.avatar ? (
                            <img
                              src={doctor.avatar}
                              alt={`BS ${doctor.lastName} ${doctor.firstName}`}
                              style={{
                                width: "100%",
                                height: "100%",
                                objectFit: "cover",
                              }}
                            />
                          ) : (
                            <span>
                              {getInitials(doctor.lastName, doctor.firstName)}
                            </span>
                          )}
                        </div>

                        <div>
                          <h3
                            style={{
                              margin: "0 0 0.25rem 0",
                              fontSize: "1.1rem",
                              color: "#111827",
                            }}
                          >
                            {doctor.title} {doctor.lastName} {doctor.firstName}
                          </h3>
                          <p
                            style={{
                              color: "#6b7280",
                              fontSize: "0.9rem",
                              margin: 0,
                              display: "-webkit-box",
                              WebkitLineClamp: 2,
                              WebkitBoxOrient: "vertical",
                              overflow: "hidden",
                            }}
                          >
                            {doctor.bio || "Chưa có thông tin giới thiệu."}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>

                  {doctorsData.meta && doctorsData.meta.pages > 1 && (
                    <div className="pagination-controls">
                      <button
                        onClick={() => setDoctorPage((prev) => prev - 1)}
                        disabled={!doctorsData.meta.hasPrev}
                      >
                        Trang trước
                      </button>
                      <span>
                        Trang {doctorsData.meta.currentPage} /{" "}
                        {doctorsData.meta.pages}
                      </span>
                      <button
                        onClick={() => setDoctorPage((prev) => prev + 1)}
                        disabled={!doctorsData.meta.hasNext}
                      >
                        Trang sau
                      </button>
                    </div>
                  )}
                </>
              ) : (
                <p className="dashboard__search-empty">
                  Không tìm thấy bác sĩ nào phù hợp.
                </p>
              )}
            </div>
          </section>
        )}
      </main>
    </>
  );
};

export default Dashboard;
