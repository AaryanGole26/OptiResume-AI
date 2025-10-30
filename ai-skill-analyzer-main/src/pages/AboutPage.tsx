import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Target, 
  Users, 
  TrendingUp, 
  Heart,
  Shield,
  Zap,
  Globe,
  CheckCircle,
  Star,
  Lightbulb,
  Rocket
} from 'lucide-react';
import { Link } from 'react-router-dom';

const AboutPage = () => {
  const teamMembers = [
    {
      name: "Ayush Mayekar",
      role: "CEO & Co-Founder",
      description: "AI/ML Expert, Bachelor of Engineering from VCET",
      image: "/am.jpg"
    },
    {
      name: "Aaryan Gole",
      role: "CTO & Co-Founder", 
      description: "AI/ML Expert, Bachelor of Engineering from VCET",
      image: "/acg.jpg"
    },
    {
      name: "Dnyanesh Panchal",
      role: "CMO & Co-Founder",
      description: "AI/ML Expert, Bachelor of Engineering from VCET",
      image: "/dp.jpg"
    }    
  ];

  const values = [
    {
      icon: Heart,
      title: "Empowering Careers",
      description: "We believe everyone deserves their dream job and we're here to make it accessible."
    },
    {
      icon: Shield,
      title: "Privacy First",
      description: "Your data is yours. We use enterprise-grade security and never store personal information."
    },
    {
      icon: Zap,
      title: "Innovation",
      description: "Cutting-edge AI technology meets human expertise to deliver the best results."
    },
    {
      icon: Globe,
      title: "Accessibility",
      description: "Quality career tools shouldn't be expensive. We democratize professional growth."
    }
  ];

  return (
    <div className="min-h-screen pt-20 pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="text-center mb-20">
          <Badge variant="secondary" className="mb-6">
            <Rocket className="h-4 w-4 mr-2" />
            About OptiResume.
          </Badge>
          <h1 className="text-5xl md:text-6xl font-bold mb-8 hero-text">
            Transforming Careers with 
            <span className="gradient-text"> AI Innovation</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-4xl mx-auto leading-relaxed">
            Founded in 2023, OptiResume combines cutting-edge artificial intelligence with deep 
            recruiting expertise to help job seekers optimize their resumes and accelerate their careers. 
            We've analyzed over 2 million resumes and helped 50,000+ professionals land their dream jobs.
          </p>
        </div>

        {/* Mission & Vision */}
        <div className="grid lg:grid-cols-2 gap-12 mb-20">
          <Card className="card-elevated border-0 h-full">
            <CardHeader>
              <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mb-4">
                <Target className="h-8 w-8 text-primary" />
              </div>
              <CardTitle className="text-2xl">Our Mission</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground leading-relaxed">
                To democratize career advancement by making professional resume optimization 
                accessible to everyone. We believe that with the right tools and insights, 
                anyone can unlock their career potential and land the job they deserve.
              </p>
            </CardContent>
          </Card>

          <Card className="card-elevated border-0 h-full">
            <CardHeader>
              <div className="w-16 h-16 bg-secondary/10 rounded-2xl flex items-center justify-center mb-4">
                <Lightbulb className="h-8 w-8 text-secondary" />
              </div>
              <CardTitle className="text-2xl">Our Vision</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground leading-relaxed">
                To create a world where career success is determined by potential and passion, 
                not by access to expensive career services. We envision a future where AI-powered 
                tools level the playing field for all job seekers.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Statistics */}
        <Card className="card-elevated border-0 mb-20">
          <CardContent className="p-12">
            <div className="grid md:grid-cols-4 gap-8 text-center">
              <div>
                <div className="text-4xl font-bold text-primary mb-2">50K+</div>
                <p className="text-muted-foreground">Professionals Helped</p>
              </div>
              <div>
                <div className="text-4xl font-bold text-secondary mb-2">2M+</div>
                <p className="text-muted-foreground">Resumes Analyzed</p>
              </div>
              <div>
                <div className="text-4xl font-bold text-success mb-2">95%</div>
                <p className="text-muted-foreground">Success Rate</p>
              </div>
              <div>
                <div className="text-4xl font-bold text-warning mb-2">80%</div>
                <p className="text-muted-foreground">Interview Rate Increase</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Values */}
        <div className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Our Core Values</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              The principles that guide everything we do at OptiResume
            </p>
          </div>
          <div className="grid md:grid-cols-3 lg:grid-cols-3 gap-8">
            {values.map((value, index) => (
              <Card key={index} className="card-elevated border-0 text-center h-full">
                <CardContent className="p-8">
                  <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <value.icon className="h-8 w-8 text-primary" />
                  </div>
                  <h3 className="font-semibold mb-3">{value.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {value.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Team */}
        <div className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Meet Our Team</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Industry experts and AI innovators working together to transform careers
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 items-stretch">
            {teamMembers.map((member, index) => (
              <Card key={index} className="card-elevated border-0 text-center h-full">
                <CardContent className="p-8 flex flex-col items-center h-full">
                  <img
                    src={member.image}
                    alt={member.name}
                    className="w-24 h-24 rounded-full object-cover mx-auto mb-6 ring-2 ring-primary/20 shadow-sm"
                  />
                  <h3 className="font-semibold mb-1">{member.name}</h3>
                  <p className="text-sm text-primary font-medium mb-3">{member.role}</p>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    {member.description}
                  </p>
                  <div className="flex-1" />
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
        
        {/* CTA */}
        <Card className="card-elevated border-0 bg-gradient-to-r from-primary/5 to-secondary/5">
          <CardContent className="p-12 text-center">
            <h3 className="text-3xl font-bold mb-4">Ready to Transform Your Career?</h3>
            <p className="text-muted-foreground mb-8 max-w-2xl mx-auto">
              Join thousands of professionals who have already optimized their resumes 
              and accelerated their career growth with OptiResume.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/upload">
                <Button variant="gradient" size="lg">
                  <Target className="h-5 w-5 mr-2" />
                  Start Your Analysis
                </Button>
              </Link>
              <Link to="/contact">
                <Button variant="outline" size="lg">
                  Contact Our Team
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AboutPage;
