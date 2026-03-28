import { useState } from "react";

export function useCtaEmailForm(options = {}) {
  const { onSubmit } = options;

  const [email, setEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);

  function handleSubmit(event) {
    event.preventDefault();
    if (!email) return;

    setSubmitting(true);

    if (typeof onSubmit === "function") {
      onSubmit(email);
    }

    setTimeout(() => {
      setSubmitting(false);
    }, 1500);
  }

  return {
    email,
    setEmail,
    submitting,
    handleSubmit,
  };
}
