import { toast } from "sonner";

export function AuthFooter() {
  const handleSupportClick = () => {
    toast.info(
      "Hiện tại, bạn vui lòng liên hệ đến quản trị hoặc lễ tân để được hỗ trợ!",
    );
  };


  return (
    <footer className="signin-page__footer">
      <button type="button" className="signin-footer__link" onClick={handleSupportClick}>
        <span className="signin-footer__text">Hướng dẫn và hỗ trợ</span>
        <span className="signin-footer__icon">?</span>
      </button>
    </footer>
  );


}
