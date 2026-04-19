import CtaBanner from "../components/CtaBanner";
import FeatureHighlightBand from "../components/FeatureHighlightBand";
import FeatureSections from "../components/FeatureSections";
import HeroSection from "../components/HeroSection";
import Navbar from "../components/Navbar";
import ServicesSection from "../components/ServicesSection";
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
