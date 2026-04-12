import { useState, useEffect } from "react";
import Apis, { endpoints } from "@configs/Apis";

export default function useMedicalServices(perPage = 5) {
  const [services, setServices] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [isTransitioning, setIsTransitioning] = useState(false);

  useEffect(() => {
    const loadServices = async () => {
      setIsTransitioning(true);
      try {
        const response = await Apis.get(endpoints.public_medical_services, {
          params: {
            page: currentPage,
            perPage: perPage,
          },
        });

        const items = response?.data?.data?.items || response?.data?.items || [];
        const pages = response?.data?.data?.meta?.pages || response?.data?.meta?.pages || 1;

        setServices(items);
        setTotalPages(pages);
      } catch (error) {
        console.error("Lỗi khi tải dịch vụ:", error);
      } finally {
        setTimeout(() => {
          setIsTransitioning(false);
        }, 300);
      }
    };

    loadServices();
  }, [currentPage, perPage]);

  const handlePrev = () => {
    if (currentPage > 1 && !isTransitioning) {
      setCurrentPage((prev) => prev - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < totalPages && !isTransitioning) {
      setCurrentPage((prev) => prev + 1);
    }
  };

  return {
    services,
    currentPage,
    totalPages,
    isTransitioning,
    handlePrev,
    handleNext,
  };
}