import {
  getDoctors,
  getSpecialties,
} from "@features/shared/services/public-api-service";
import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { normalizeQuery } from "@/utils/Utils.js";

export const useDashboard = () => {
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
    const loadSpecialties = async () => {
      await fetchSpecialties(specialtyPage, keyword, activeSearchType);
    };
    loadSpecialties();
  }, [specialtyPage, keyword, activeSearchType, fetchSpecialties]);

  useEffect(() => {
    const loadDoctors = async () => {
      await fetchDoctors(doctorPage, keyword, workDate, activeSearchType);
    };
    loadDoctors();
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

  const handleSpecialtyClick = (id) => {
    navigate(`/specialties/${id}`);
  };

  const handleDoctorClick = (id) => {
    navigate(`/doctors/${id}`);
  };

  const handleWorkDateChange = (e) => {
    setWorkDate(e.target.value);
    setDoctorPage(1);
  };

  const showSpecialties =
    activeSearchType === "all" || activeSearchType === "specialty";
  const showDoctors =
    activeSearchType === "all" || activeSearchType === "doctor";

  return {
    keyword,
    activeSearchType,
    specialtiesData,
    specialtyPage,
    setSpecialtyPage,
    specialtiesLoading,
    doctorsData,
    doctorPage,
    setDoctorPage,
    doctorsLoading,
    workDate,
    globalError,
    showSpecialties,
    showDoctors,
    handleSearch,
    getInitials,
    handleSpecialtyClick,
    handleDoctorClick,
    handleWorkDateChange,
  };
};
