import Navbar from "../../medical_records/components/Navbar.jsx";
import HeroSection from "../components/HeroSection";
import FeatureSections from "../../medical_records/components/FeatureSections.jsx";
import FeatureHighlightBand from "../components/FeatureHighlightBand";
import ServicesSection from "../../booking/components/ServicesSection.jsx";
import CtaBanner from "../components/CtaBanner";
import SiteFooter from "../components/SiteFooter";

export default function LandingPage() {
  return (
    <>
      <Navbar />
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
