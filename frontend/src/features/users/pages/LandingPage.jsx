import Navbar from "../components/Navbar";
import HeroSection from "../components/HeroSection";
import FeatureSections from "../components/FeatureSections";
import FeatureHighlightBand from "../components/FeatureHighlightBand";
import ServicesSection from "../components/ServicesSection";
import CtaBanner from "../components/CtaBanner";
import SiteFooter from "../components/SiteFooter";
import { getRoleMenuItems } from "../../../utils/utils";

export default function LandingPage() {
  return (
    <>
      <Navbar menuItems={getRoleMenuItems()}/>
      <main>
        <HeroSection />
        <FeatureHighlightBand />
        <FeatureSections />
        <ServicesSection />
        <CtaBanner />
      </main>
      <SiteFooter />
    </>
  );
}
