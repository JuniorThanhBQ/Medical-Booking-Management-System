import apis, { endpoints } from "@/configs/apis";

export async function verifyEmailStatus(email) {
  try {
    const res = await apis.post(endpoints["auth_email_validator"], { email });
    return { data: res.data.is_valid };
  } catch (err) {
    if (err.response?.status === 400) return { exists: true };

    throw new Error(err?.response?.data?.message);
  }
}

export const verifyEmailToken = async (token) => {
  const response = await apis.post(endpoints["auth_email_verification"], {
    token,
  });
  return response.data;
};
