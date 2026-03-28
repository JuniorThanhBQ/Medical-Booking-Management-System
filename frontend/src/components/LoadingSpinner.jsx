export default function LoadingSpinner({ fullPage = false, size, label }) {
  const loaderClass = `app-loader${fullPage ? " app-loader--full-page" : ""}`;
  const spinnerClass = `app-spinner${size === "sm" ? " app-spinner--sm" : ""}`;

  return (
    <div className={loaderClass}>
      <div className={spinnerClass} />
    </div>
  );
}
