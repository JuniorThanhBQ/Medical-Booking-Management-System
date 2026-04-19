import apis, { endpoints } from "@configs/apis";
import { useEffect, useRef, useState } from "react";
import { toast } from "sonner";

export const useDoctorRegistration = () => {
  const [formData, setFormData] = useState({
    fullName: "",
    dob: "",
    gender: "MALE",
    address: "",
    email: "",
    phone: "",
    reason: "",
  });
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const hasShownToast = useRef(false);

  useEffect(() => {
    if (!hasShownToast.current) {
      toast.info("Khuyến khích gửi hồ sơ trực tiếp qua mail.");
      hasShownToast.current = true;
    }
  }, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type !== "application/pdf") {
        setError("Chỉ chấp nhận file định dạng PDF.");
        setFile(null);
        e.target.value = null;
        return;
      }
      if (selectedFile.size > 5 * 1024 * 1024) {
        setError("Kích thước file không được vượt quá 5MB.");
        setFile(null);
        e.target.value = null;
        return;
      }
      setError("");
      setFile(selectedFile);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Vui lòng đính kèm CV (PDF).");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const submitData = new FormData();
      submitData.append("fullName", formData.fullName);
      submitData.append("dateOfBirth", formData.dob);
      submitData.append("gender", formData.gender);
      submitData.append("address", formData.address);
      submitData.append("email", formData.email);
      submitData.append("phone", formData.phone);
      submitData.append("reason", formData.reason);
      submitData.append("CV", file);

      await apis.post(endpoints["doctor_registration"], submitData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setSuccess(true);
    } catch {
      setError("Có lỗi xảy ra khi gửi thông tin. Vui lòng thử lại sau.");
    } finally {
      setLoading(false);
    }
  };

  return {
    formData,
    error,
    loading,
    success,
    handleChange,
    handleFileChange,
    handleSubmit,
  };
};
