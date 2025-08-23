import heroVideo from "@/assets/Animate_hopesecure.mp4";
import { Button } from "@/components/ui/button";
import { ArrowRight, Shield } from "lucide-react";
import { useNavigate } from "react-router-dom";

const HeroSection = () => {
  const navigate = useNavigate();

  return (
    <>
      {/* Video Section with overlay text */}
      <section className="relative min-h-screen bg-gradient-hero flex items-center overflow-hidden">
        {/* Animated Video Background */}
        <div className="absolute inset-0 w-full h-full">
          <video
            autoPlay
            loop
            muted
            playsInline
            className="absolute inset-0 w-full h-full object-cover"
          >
            <source src={heroVideo} type="video/mp4" />
          </video>
          {/* Light Blur Overlay - keeping the blur effect as requested */}
          <div className="absolute inset-0 backdrop-blur-sm bg-black/30"></div>
        </div>

        {/* Hero Text Overlay - positioned in the empty space */}
        <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-8 text-center text-white">
          <div className="mt-20">
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
              Advanced Cybersecurity Awareness Platform
            </h2>
            
            <p className="text-xl md:text-2xl text-gray-200 mb-6 max-w-4xl mx-auto">
              Protect your organization with realistic phishing simulations and comprehensive employee training
            </p>

            <p className="text-lg md:text-xl text-green-300 font-semibold mb-8">
              Transform your team into your strongest security defense
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button 
                size="lg" 
                className="bg-green-600 hover:bg-green-700 text-white px-8 py-4 text-lg font-semibold"
                onClick={() => navigate('/signin')}
              >
                Start Your Security Journey
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              
              <Button 
                variant="outline" 
                size="lg" 
                className="border-2 border-white text-white hover:bg-white hover:text-gray-900 px-8 py-4 text-lg font-semibold"
                onClick={() => document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })}
              >
                Explore Features
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Content Section Below Video */}
      <section className="py-16 bg-gradient-to-br from-slate-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 text-center">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <div className="text-blue-600 text-3xl mb-4">📊</div>
              <h3 className="font-bold text-xl mb-3 text-gray-900">Real-Time Monitoring</h3>
              <p className="text-gray-600">Track campaign progress instantly with live analytics and detailed reporting</p>
            </div>
            
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <div className="text-green-600 text-3xl mb-4">🎨</div>
              <h3 className="font-bold text-xl mb-3 text-gray-900">Custom Templates</h3>
              <p className="text-gray-600">Create authentic phishing emails that mimic your company's branding and style</p>
            </div>
            
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <div className="text-purple-600 text-3xl mb-4">📈</div>
              <h3 className="font-bold text-xl mb-3 text-gray-900">Detailed Analytics</h3>
              <p className="text-gray-600">Comprehensive vulnerability reports with actionable security insights</p>
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default HeroSection;