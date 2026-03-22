import Navbar from "../components/Navbar";
import HeroSection from "../components/HeroSection";
import FeatureSections from "../components/FeatureSections";
import FeatureHighlightBand from "../components/FeatureHighlightBand";
import ServicesSection from "../components/ServicesSection";
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
