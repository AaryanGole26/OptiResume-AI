import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Zap, 
  Target, 
  Brain,
  FileText,
  TrendingUp,
  Shield,
  Clock,
  CheckCircle,
  Star,
  Crown,
  Users,
  Download,
  BarChart,
  MessageSquare,
  Calendar,
  Sparkles,
  Rocket,
  Award
} from 'lucide-react';
import { Link } from 'react-router-dom';

const FeaturesPage = () => {
  const coreFeatures = [
    {
      icon: Brain,
      title: "AI-Powered Analysis",
      description: "Advanced machine learning algorithms analyze your resume against job requirements with 95% accuracy.",
      features: ["NLP skill extraction", "Contextual matching", "Industry-specific insights"]
    },
    {
      icon: Target,
      title: "Skill Gap Analysis",
      description: "Identify exactly what skills you're missing and get actionable recommendations to fill gaps.",
      features: ["Missing skill detection", "Proficiency scoring", "Learning path suggestions"]
    },
    {
      icon: FileText,
      title: "Resume Optimization",
      description: "Get specific suggestions to improve your resume format, content, and keyword optimization.",
      features: ["ATS optimization", "Keyword suggestions", "Format improvements"]
    },
    {
      icon: TrendingUp,
      title: "Match Scoring",
      description: "See exactly how well your resume matches job requirements with detailed breakdown scores.",
      features: ["Overall match percentage", "Category-specific scores", "Improvement tracking"]
    }
  ];

  const freePlan = [
    "3 resume analyses per month",
    "Basic skill matching",
    "PDF resume upload",
    "Match percentage scoring",
    "Standard report export"
  ];

  const proPlan = [
    "Unlimited resume analyses",
    "Advanced AI recommendations",
    "ATS optimization scores",
    "Progress tracking & history",
    "Priority email support",
    "Custom job description fetch",
    "Interview preparation tips",
    "Salary range insights",
    "Career path recommendations",
    "1-on-1 expert consultation (monthly)"
  ];

  const enterpriseFeatures = [
    {
      icon: Users,
      title: "Team Management",
      description: "Manage multiple team members and track their career development progress.",
      badge: "Enterprise"
    },
    {
      icon: BarChart,
      title: "Analytics Dashboard", 
      description: "Comprehensive analytics on team skills, gaps, and hiring insights.",
      badge: "Enterprise"
    },
    {
      icon: Shield,
      title: "Enterprise Security",
      description: "SOC 2 compliance, SSO integration, and advanced data protection.",
      badge: "Enterprise"
    },
    {
      icon: MessageSquare,
      title: "Dedicated Support",
      description: "24/7 priority support with dedicated account manager.",
      badge: "Enterprise"
    }
  ];

  return (
    <div className="min-h-screen pt-20 pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="text-center mb-20">
          <Badge variant="secondary" className="mb-6">
            <Sparkles className="h-4 w-4 mr-2" />
            Platform Features
          </Badge>
          <h1 className="text-5xl md:text-6xl font-bold mb-8 hero-text">
            Powerful Tools for
            <span className="gradient-text"> Career Success</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-4xl mx-auto leading-relaxed">
            Discover all the features that make OptiResume the most comprehensive 
            AI-powered resume optimization platform for modern job seekers.
          </p>
        </div>

        {/* Core Features */}
        <div className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Core Features</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Essential tools that every job seeker needs to optimize their resume and land interviews
            </p>
          </div>
          <div className="grid md:grid-cols-2 gap-8">
            {coreFeatures.map((feature, index) => (
              <Card key={index} className="card-elevated border-0 h-full">
                <CardHeader>
                  <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mb-4">
                    <feature.icon className="h-8 w-8 text-primary" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {feature.features.map((item, i) => (
                      <li key={i} className="flex items-center text-sm">
                        <CheckCircle className="h-4 w-4 text-success mr-3 flex-shrink-0" />
                        {item}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Pricing Plans */}
        <div className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Choose Your Plan</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Start free and upgrade as your career grows. All plans include our core AI analysis.
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {/* Free Plan */}
            <Card className="card-elevated border-0 relative">
              <CardHeader className="text-center pb-8">
                <Badge variant="outline" className="w-fit mx-auto mb-4">
                  Free Plan
                </Badge>
                <CardTitle className="text-2xl mb-2">Starter</CardTitle>
                <div className="text-4xl font-bold mb-2">$0</div>
                <CardDescription>Perfect for getting started</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <ul className="space-y-3">
                  {freePlan.map((feature, i) => (
                    <li key={i} className="flex items-center text-sm">
                      <CheckCircle className="h-4 w-4 text-success mr-3 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>
                <Link to="/upload">
                  <Button variant="outline" className="w-full">
                    Get Started Free
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Pro Plan */}
            <Card className="card-elevated border-0 relative border-primary">
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <Badge variant="default" className="bg-primary">
                  <Star className="h-3 w-3 mr-1" />
                  Most Popular
                </Badge>
              </div>
              <CardHeader className="text-center pb-8">
                <Badge variant="default" className="w-fit mx-auto mb-4 bg-primary">
                  Pro Plan
                </Badge>
                <CardTitle className="text-2xl mb-2">Professional</CardTitle>
                <div className="text-4xl font-bold mb-2">$29<span className="text-lg text-muted-foreground">/mo</span></div>
                <CardDescription>For serious job seekers</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <ul className="space-y-3">
                  {proPlan.map((feature, i) => (
                    <li key={i} className="flex items-center text-sm">
                      <CheckCircle className="h-4 w-4 text-success mr-3 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>
                <Button variant="gradient" className="w-full">
                  <Crown className="h-4 w-4 mr-2" />
                  Upgrade to Pro
                </Button>
              </CardContent>
            </Card>

            {/* Enterprise Plan */}
            <Card className="card-elevated border-0 relative">
              <CardHeader className="text-center pb-8">
                <Badge variant="outline" className="w-fit mx-auto mb-4">
                  Enterprise
                </Badge>
                <CardTitle className="text-2xl mb-2">Custom</CardTitle>
                <div className="text-4xl font-bold mb-2">Custom</div>
                <CardDescription>For teams and organizations</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <p className="text-sm text-muted-foreground">
                  Everything in Pro, plus:
                </p>
                <ul className="space-y-3">
                  <li className="flex items-center text-sm">
                    <CheckCircle className="h-4 w-4 text-success mr-3 flex-shrink-0" />
                    Unlimited team members
                  </li>
                  <li className="flex items-center text-sm">
                    <CheckCircle className="h-4 w-4 text-success mr-3 flex-shrink-0" />
                    Advanced analytics
                  </li>
                  <li className="flex items-center text-sm">
                    <CheckCircle className="h-4 w-4 text-success mr-3 flex-shrink-0" />
                    Custom integrations
                  </li>
                  <li className="flex items-center text-sm">
                    <CheckCircle className="h-4 w-4 text-success mr-3 flex-shrink-0" />
                    Dedicated support
                  </li>
                </ul>
                <Link to="/contact">
                  <Button variant="outline" className="w-full">
                    Contact Sales
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Enterprise Features */}
        <div className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Enterprise Features</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Advanced capabilities for teams and organizations
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {enterpriseFeatures.map((feature, index) => (
              <Card key={index} className="card-elevated border-0 text-center">
                <CardContent className="p-6">
                  <Badge variant="secondary" className="mb-4">
                    {feature.badge}
                  </Badge>
                  <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mx-auto mb-4">
                    <feature.icon className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="font-semibold mb-2">{feature.title}</h3>
                  <p className="text-sm text-muted-foreground">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Additional Features */}
        <Card className="card-elevated border-0 mb-20">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl mb-2">Additional Features</CardTitle>
            <CardDescription>
              More tools to accelerate your career growth
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center space-y-4">
                <Clock className="h-12 w-12 text-primary mx-auto" />
                <h4 className="font-semibold">Real-time Processing</h4>
                <p className="text-sm text-muted-foreground">
                  Get your resume analysis results in under 60 seconds with our optimized AI pipeline.
                </p>
              </div>
              <div className="text-center space-y-4">
                <Download className="h-12 w-12 text-primary mx-auto" />
                <h4 className="font-semibold">Export Options</h4>
                <p className="text-sm text-muted-foreground">
                  Download detailed PDF reports or share results with recruiters and career coaches.
                </p>
              </div>
              <div className="text-center space-y-4">
                <Calendar className="h-12 w-12 text-primary mx-auto" />
                <h4 className="font-semibold">Progress Tracking</h4>
                <p className="text-sm text-muted-foreground">
                  Monitor your improvement over time and track your career development journey.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* CTA */}
        <Card className="card-elevated border-0 bg-gradient-to-r from-primary/5 to-secondary/5">
          <CardContent className="p-12 text-center">
            <Rocket className="h-16 w-16 text-primary mx-auto mb-6" />
            <h3 className="text-3xl font-bold mb-4">Ready to Optimize Your Resume?</h3>
            <p className="text-muted-foreground mb-8 max-w-2xl mx-auto">
              Join thousands of professionals who have already transformed their careers with OptiResume's 
              AI-powered resume optimization platform.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/upload">
                <Button variant="gradient" size="lg">
                  <Zap className="h-5 w-5 mr-2" />
                  Start Free Analysis
                </Button>
              </Link>
              <Link to="/contact">
                <Button variant="outline" size="lg">
                  <MessageSquare className="h-5 w-5 mr-2" />
                  Talk to Sales
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default FeaturesPage;