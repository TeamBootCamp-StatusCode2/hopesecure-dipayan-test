import { Button } from "@/components/ui/button";
import { Shield, Zap, Target, RefreshCw, Play } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useGlobalStats } from "@/hooks/useGlobalStats";
import heroImage from "@/assets/hero-security.jpg";
import heroVideo from "@/assets/Animate_hs_word_202508231645.mp4";

const HeroSection = () => {
  const navigate = useNavigate();
  const { stats, loading, error } = useGlobalStats();
  
  const scrollToVideo = () => {
    const videoElement = document.querySelector('#hero-video');
    if (videoElement) {
      videoElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      // Play the video if it's not already playing
      const video = videoElement.querySelector('video');
      if (video && video.paused) {
        video.play();
      }
    }
  };
  
  return (
    <section className="relative min-h-screen bg-gradient-hero flex items-center overflow-hidden">
      {/* Background Video */}
      <video 
        autoPlay 
        muted 
        loop 
        className="absolute inset-0 w-full h-full object-cover opacity-30 z-0"
        poster={heroImage}
      >
        <source src={heroVideo} type="video/mp4" />
        {/* Fallback background image */}
        <div 
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage: `url(${heroImage})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        />
      </video>
      
      {/* Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-8 py-24">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="text-white">
            <div className="flex items-center gap-3 mb-6">
              <Shield className="h-8 w-8 text-security-green" />
              <span className="text-2xl font-bold">HopeSecure</span>
              <span className="text-security-green text-2xl font-bold">Feeder</span>
            </div>
            
            <h1 className="text-5xl lg:text-6xl font-bold mb-6 leading-tight">
              Test. Measure.{" "}
              <span className="text-security-green">Secure.</span>
            </h1>
            
            <p className="text-xl text-gray-200 mb-8 leading-relaxed max-w-xl">
              Launch realistic cyber awareness simulations to measure your team's readiness against phishing and data breach attempts.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 mb-12">
              <Button 
                variant="hero" 
                size="lg" 
                className="text-lg px-8 py-4 bg-blue-600 hover:bg-blue-700"
                onClick={() => navigate('/dashboard')}
              >
                Start Your Campaign
              </Button>
              <Button 
                variant="outline" 
                size="lg" 
                className="text-lg px-8 py-4 border-white/20 hover:bg-white/10"
                onClick={scrollToVideo}
              >
                <Play className="h-5 w-5 mr-2" />
                Watch Demo
              </Button>
            </div>
            
            <div className="grid grid-cols-3 gap-8 pt-8 border-t border-white/20">
              <div className="text-center group">
                <div className="text-3xl font-bold text-security-green mb-2 flex items-center justify-center gap-2 transition-all duration-300 group-hover:scale-105">
                  {loading ? (
                    <RefreshCw className="h-6 w-6 animate-spin" />
                  ) : (
                    <span className="tabular-nums">{stats?.detectionRate || "98%"}</span>
                  )}
                </div>
                <div className="text-sm text-gray-200">Detection Rate</div>
              </div>
              <div className="text-center group">
                <div className="text-3xl font-bold text-security-green mb-2 flex items-center justify-center gap-2 transition-all duration-300 group-hover:scale-105">
                  {loading ? (
                    <RefreshCw className="h-6 w-6 animate-spin" />
                  ) : (
                    <span className="tabular-nums">{stats?.testsCount || "50K+"}</span>
                  )}
                </div>
                <div className="text-sm text-gray-200">Tests Conducted</div>
              </div>
              <div className="text-center group">
                <div className="text-3xl font-bold text-security-green mb-2 flex items-center justify-center gap-2 transition-all duration-300 group-hover:scale-105">
                  {loading ? (
                    <RefreshCw className="h-6 w-6 animate-spin" />
                  ) : (
                    <span className="tabular-nums">{stats?.clientsCount || "500+"}</span>
                  )}
                </div>
                <div className="text-sm text-gray-200">Enterprise Clients</div>
              </div>
            </div>
            
            {/* Live data indicator */}
            <div className="flex items-center justify-center gap-2 mt-4 text-sm text-gray-300">
              <div className={`w-2 h-2 rounded-full transition-colors duration-300 ${
                loading ? 'bg-yellow-400 animate-pulse' : 'bg-green-400 animate-ping'
              }`}></div>
              <span className="transition-opacity duration-300">
                {loading ? 'Updating live data...' : 'Real-time data • Updates every 30s'}
              </span>
              {error && (
                <span className="text-red-400 ml-2 animate-pulse">({error})</span>
              )}
            </div>
          </div>
          
          <div className="relative" id="hero-video">
            <div className="bg-black/20 backdrop-blur-sm rounded-xl border border-white/10 overflow-hidden">
              <div className="relative">
                <video 
                  controls 
                  className="w-full h-auto"
                  poster={heroImage}
                >
                  <source src={heroVideo} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
              </div>
              <div className="p-6 bg-gradient-to-t from-black/40 to-transparent">
                <h3 className="text-white text-xl font-semibold mb-3">See HopeSecure in Action</h3>
                <p className="text-gray-200 text-sm mb-4 leading-relaxed">
                  Watch how our advanced phishing simulation platform helps organizations test and improve their security awareness.
                </p>
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <Target className="h-5 w-5 text-security-green flex-shrink-0" />
                    <div>
                      <h4 className="text-white font-medium text-sm">Realistic Simulations</h4>
                      <p className="text-gray-300 text-xs">Domain imitation and authentic campaigns</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <Zap className="h-5 w-5 text-security-green flex-shrink-0" />
                    <div>
                      <h4 className="text-white font-medium text-sm">Instant Setup</h4>
                      <p className="text-gray-300 text-xs">Launch campaigns in minutes</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <Shield className="h-5 w-5 text-security-green flex-shrink-0" />
                    <div>
                      <h4 className="text-white font-medium text-sm">Detailed Analytics</h4>
                      <p className="text-gray-300 text-xs">Comprehensive insights</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;