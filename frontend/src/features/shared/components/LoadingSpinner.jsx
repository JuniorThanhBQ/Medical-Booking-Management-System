export default function LoadingSpinner({
  fullPage = true,
  size = "lg",
  className = "",
  label = "",
}) {
  const loaderClass = [
    "app-loader",
    fullPage && "app-loader--full-page",
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div className={loaderClass}>
      <div className={`app-spinner app-spinner--${size}`} role="status" />
      <p className="app-loader__label">{label}</p>
    </div>
  );
}
