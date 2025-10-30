import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Zap, 
  Target, 
  Clock, 
  TrendingUp, 
  CheckCircle, 
  Star,
  ArrowRight,
  Play,
  Brain,
  Shield,
  Award
} from 'lucide-react';
import { featuresData, testimonials } from '@/data/mockData';

const LandingPage = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative pt-20 pb-16 lg:pt-32 lg:pb-24 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-secondary/5 to-background" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            
            <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-blue-600/10 to-indigo-600/10 text-blue-700 ring-1 ring-blue-600/20 mb-4">
            Trusted by hiring teams and top candidates
          </div>
            
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight mb-6">
              Land Your Dream Job with{' '}
              <span className="hero-text">AI-Optimized</span>{' '}
              Resumes
            </h1>
            
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-8 leading-relaxed">
              OptiResume uses advanced AI to analyze your resume against job requirements, 
              providing instant skill matching, personalized recommendations, and professional insights 
              that increase your interview success rate by 300%.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
              <Link to="/upload">
                <Button variant="gradient" size="lg" className="w-full sm:w-auto">
                  <Target className="h-5 w-5 mr-2" />
                  Optimize My Resume
                  <ArrowRight className="h-5 w-5 ml-2" />
                </Button>
              </Link>
            </div>

            {/* Demo Video */}
            <div className="max-w-4xl mx-auto mb-12">
              <div className="relative rounded-2xl overflow-hidden shadow-2xl card-elevated">
                <div className="aspect-video bg-black">
                  <video 
                    controls
                    className="w-full h-full object-cover"
                  >
                    <source src="https://res.cloudinary.com/dpuqctqfl/video/upload/v1757694690/2025-09-12_21-49-04_ivhd6c.mkv" type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-muted/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              { value: '50K+', label: 'Resumes Optimized', icon: Target },
              { value: '95%', label: 'Match Accuracy', icon: CheckCircle },
              { value: '2.5x', label: 'Interview Rate Increase', icon: TrendingUp },
              { value: '3 hrs', label: 'Average Time Saved', icon: Clock },
            ].map((stat, index) => (
              <div key={index} className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-primary/10 rounded-full mb-4">
                  <stat.icon className="h-6 w-6 text-primary" />
                </div>
                <div className="text-3xl font-bold text-foreground mb-2">{stat.value}</div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Scrolling bar */}
      <section className="py-6">
        <div className="marquee bg-white/80 backdrop-blur border-y border-border select-none">
          <div className="marquee__track">
            {[
              "Precision Matching","ATS Friendly","Recruiter-Ready","Executive Reports","LLM-Powered","Actionable Insights","Privacy First"
            ].map((label, i) => (
              <div key={`m1-${i}`} className="flex items-center px-8 py-3">
                <span className="text-slate-700 text-sm font-semibold uppercase tracking-wider whitespace-nowrap">{label}</span>
                <span className="mx-8 h-1 w-1 rounded-full bg-slate-300 inline-block" />
              </div>
            ))}
            {[
              "Precision Matching","ATS Friendly","Recruiter-Ready","Executive Reports","LLM-Powered","Actionable Insights","Privacy First"
            ].map((label, i) => (
              <div key={`m2-${i}`} className="flex items-center px-8 py-3">
                <span className="text-slate-700 text-sm font-semibold uppercase tracking-wider whitespace-nowrap">{label}</span>
                <span className="mx-8 h-1 w-1 rounded-full bg-slate-300 inline-block" />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-4">
              Why Choose OptiResume?
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Our AI-powered platform combines cutting-edge technology with career expertise 
              to give you the competitive edge you need.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {featuresData.map((feature, index) => (
              <Card key={index} className="card-elevated border-0 group cursor-pointer">
                <CardHeader className="text-center pb-4">
                  <div className="text-4xl mb-4">{feature.icon}</div>
                  <CardTitle className="text-xl mb-2">{feature.title}</CardTitle>
                  <CardDescription className="text-muted-foreground">
                    {feature.description}
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-0">
                  <ul className="space-y-2">
                    {feature.benefits.map((benefit, i) => (
                      <li key={i} className="flex items-center text-sm text-muted-foreground">
                        <CheckCircle className="h-4 w-4 text-success mr-2 flex-shrink-0" />
                        {benefit}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-24 bg-muted/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-4">
              How OptiResume Works
            </h2>
            <p className="text-xl text-muted-foreground">
              Get optimized in three simple steps
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: '01',
                title: 'Upload & Input',
                description: 'Upload your resume and enter your target job role. Paste the job description or let us fetch one.',
                icon: Target,
              },
              {
                step: '02',
                title: 'AI Analysis',
                description: 'Our advanced AI analyzes your resume against job requirements with 95% accuracy in seconds.',
                icon: Brain,
              },
              {
                step: '03',
                title: 'Get Results',
                description: 'Receive detailed insights, skill gaps, and personalized recommendations to land your dream job.',
                icon: Award,
              },
            ].map((item, index) => (
              <div key={index} className="text-center relative">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-full mb-6 relative">
                  <item.icon className="h-8 w-8 text-primary-foreground" />
                  <div className="absolute -top-2 -right-2 w-8 h-8 bg-secondary text-secondary-foreground rounded-full flex items-center justify-center text-xs font-bold">
                    {item.step}
                  </div>
                </div>
                <h3 className="text-xl font-semibold mb-4">{item.title}</h3>
                <p className="text-muted-foreground">{item.description}</p>
                {index < 2 && (
                  <ArrowRight className="hidden md:block absolute top-8 -right-4 h-6 w-6 text-muted-foreground" />
                )}
              </div>
            ))}
          </div>
        </div>
      </section>


      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-r from-primary/10 via-secondary/10 to-primary/10">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl lg:text-4xl font-bold mb-6">
            Ready to Land Your Dream Job?
          </h2>
          <p className="text-xl text-muted-foreground mb-8">
            Join 50,000+ professionals who've transformed their careers with AI-powered resume optimization.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/upload">
              <Button variant="gradient" size="lg" className="w-full sm:w-auto">
                <Zap className="h-5 w-5 mr-2" />
                Start Optimizing Now
              </Button>
            </Link>
            <Button variant="outline" size="lg" className="w-full sm:w-auto">
              <Shield className="h-5 w-5 mr-2" />
              Learn More
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;