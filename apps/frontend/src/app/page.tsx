"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import {
  ArrowRight,
  Github,
  Twitter,
  Check,
  Zap,
  Code,
  Database,
  Globe,
  Cpu,
  Layers,
  GitBranch,
  Terminal,
  Play,
  Rocket,
  Shield,
  Users,
  BarChart3,
  Clock,
  DollarSign,
  ChevronRight,
  Star,
  GitCommit,
  FileCode,
  Box,
  Server,
  Cloud,
  Lock,
  Menu,
  X,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AspectRatio } from "@/components/ui/aspect-ratio";

export default function HomePage() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <main className="min-h-screen bg-background">
      {/* ─── Navigation ─────────────────────────────────────────── */}
      <nav className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <Rocket className="h-6 w-6 text-primary" />
            <span className="font-bold text-xl">ProdSynth</span>
          </div>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-6">
            <a href="#how-it-works" className="text-sm font-medium text-muted-foreground hover:text-foreground">
              How it Works
            </a>
            <a href="#demo" className="text-sm font-medium text-muted-foreground hover:text-foreground">
              Demo
            </a>
            <a href="#pricing" className="text-sm font-medium text-muted-foreground hover:text-foreground">
              Pricing
            </a>
            <a href="#marketplace" className="text-sm font-medium text-muted-foreground hover:text-foreground">
              Marketplace
            </a>
            <a href="https://github.com/prodsynth/monorepo/blob/main/docs/README.md" className="text-sm font-medium text-muted-foreground hover:text-foreground" target="_blank" rel="noopener noreferrer">
              Docs
            </a>
          </div>

          <div className="hidden md:flex items-center gap-2">
            <Button variant="ghost" size="sm" asChild>
              <a href="https://github.com/prodsynth/monorepo" target="_blank" rel="noopener noreferrer">
                <Github className="mr-2 h-4 w-4" />
                GitHub
              </a>
            </Button>
            <Button size="sm" asChild>
              <Link href="#pricing">Get Started</Link>
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden border-t p-4 space-y-4">
            <a href="#how-it-works" className="block text-sm font-medium text-muted-foreground hover:text-foreground">
              How it Works
            </a>
            <a href="#demo" className="block text-sm font-medium text-muted-foreground hover:text-foreground">
              Demo
            </a>
            <a href="#pricing" className="block text-sm font-medium text-muted-foreground hover:text-foreground">
              Pricing
            </a>
            <a href="#marketplace" className="block text-sm font-medium text-muted-foreground hover:text-foreground">
              Marketplace
            </a>
            <a href="https://github.com/prodsynth/monorepo/blob/main/docs/README.md" className="block text-sm font-medium text-muted-foreground hover:text-foreground" target="_blank">
              Docs
            </a>
            <div className="flex gap-2 pt-2">
              <Button variant="ghost" size="sm" className="flex-1" asChild>
                <a href="https://github.com/prodsynth/monorepo" target="_blank">
                  <Github className="mr-2 h-4 w-4" />
                  GitHub
                </a>
              </Button>
              <Button size="sm" className="flex-1" asChild>
                <Link href="#pricing">Get Started</Link>
              </Button>
            </div>
          </div>
        )}
      </nav>

      {/* ─── Hero Section ─────────────────────────────────────────── */}
      <section className="relative overflow-hidden py-20 md:py-32">
        {/* Background gradient */}
        <div className="absolute inset-0 -z-10 bg-[linear-gradient(to_right,var(--primary)_0%,transparent_50%)] opacity-10" />
        <div className="container relative z-20">
          <div className="mx-auto max-w-3xl text-center">
            <Badge variant="outline" className="mb-4">
              <Zap className="mr-1 h-3 w-3" />
              Now in Public Beta
            </Badge>

            <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
              Turn Any Repository Into a{" "}
              <span className="text-primary">Working Product</span>{" "}
              in 5 Minutes
            </h1>

            <p className="mt-6 text-lg leading-8 text-muted-foreground sm:text-xl sm:leading-9 max-w-2xl mx-auto">
              AI-Native Product Synthesis Engine. Analyze repositories, generate code, run tests, and deploy — all automatically using our agentic workflow.
            </p>

            <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Button size="lg" className="w-full sm:w-auto" asChild>
                <Link href="#pricing">
                  Get Started for Free
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
              <Button size="lg" variant="outline" className="w-full sm:w-auto" asChild>
                <a href="https://github.com/prodsynth/monorepo" target="_blank" rel="noopener noreferrer">
                  <Github className="mr-2 h-4 w-4" />
                  View on GitHub
                </a>
              </Button>
            </div>

            {/* Social Proof */}
            <div className="mt-16 flex flex-col items-center gap-4">
              <p className="text-sm text-muted-foreground">Trusted by innovators worldwide</p>
              <div className="flex flex-wrap items-center justify-center gap-8 opacity-70">
                {/* Placeholder for company logos */}
                <div className="h-8 w-24 rounded bg-muted flex items-center justify-center text-xs text-muted-foreground">
                  Startup Inc.
                </div>
                <div className="h-8 w-24 rounded bg-muted flex items-center justify-center text-xs text-muted-foreground">
                  Tech Corp
                </div>
                <div className="h-8 w-24 rounded bg-muted flex items-center justify-center text-xs text-muted-foreground">
                  AI Labs
                </div>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-8 mt-8 w-full max-w-lg mx-auto">
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary">1000+</div>
                  <div className="text-sm text-muted-foreground">Signups</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary">50+</div>
                  <div className="text-sm text-muted-foreground">Templates</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary">5 min</div>
                  <div className="text-sm text-muted-foreground">To Product</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ─── How it Works ─────────────────────────────────────────── */}
      <section id="how-it-works" className="py-20 bg-muted/50">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold sm:text-4xl">How It Works</h2>
            <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
              Four simple steps from repository to deployed product, powered by AI agents.
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4 max-w-5xl mx-auto">
            {/* Step 1: Analyze */}
            <Card className="relative">
              <CardHeader>
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 mb-4">
                  <GitBranch className="h-6 w-6 text-primary" />
                </div>
                <CardTitle className="text-xl">
                  <span className="text-primary">01.</span> Analyze
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Research Agent parses your repository, builds AST, and creates a knowledge graph in Graphiti (Neo4j). Understands tech stack, dependencies, and risks.
                </p>
                <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500" />
                    AST parsing
                  </li>
                  <li className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500" />
                    Tech stack detection
                  </li>
                  <li className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500" />
                    License check (GPL/MIT)
                  </li>
                </ul>
              </CardContent>
            </Card>

            {/* Step 2: Synthesize */}
            <Card className="relative">
              <CardHeader>
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 mb-4">
                  <Layers className="h-6 w-6 text-primary" />
                </div>
                <CardTitle className="text-xl">
                  <span className="text-primary">02.</span> Synthesize
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Architect Agent designs C4 models, selects optimal tech stack, and plans the product structure. Uses cascading LLM (cheap → expensive) for cost efficiency.
                </p>
                <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500" />
                    C4 architecture
                  </li>
                  <li className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500" />
                    Token budget ($0.50/run)
                  </li>
                  <li className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500" />
                    Product DNA capture
                  </li>
                </ul>
              </CardContent>
            </Card>

            {/* Step 3: Assemble */}
            <Card className="relative">
              <CardHeader>
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 mb-4">
                  <Code className="h-6 w-6 text-primary" />
                </div>
                <CardTitle className="text-xl">
                  <span className="text-primary">03.</span> Assemble
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Code Agent generates production-ready code using OpenClaude. Test Agent runs pytest + Playwright automatically. SafetyGuard ensures no dangerous commands.
                </p>
                <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500" />
                    FastAPI / Next.js code
                  </li>
                  <li className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500" />
                    Auto-generated tests
                  </li>
                  <li className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500" />
                    Security scanning
                  </li>
                </ul>
              </CardContent>
            </Card>

            {/* Step 4: Deploy */}
            <Card className="relative">
              <CardHeader>
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 mb-4">
                  <Rocket className="h-6 w-6 text-primary" />
                </div>
                <CardTitle className="text-xl">
                  <span className="text-primary">04.</span> Deploy
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Deploy Agent handles deployment to Render, Fly.io, Docker, or Kubernetes. Get live URL in minutes. Webhook notifications via Slack/Telegram.
                </p>
                <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500" />
                    One-click deploy
                  </li>
                  <li className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500" />
                    Live URL instantly
                  </li>
                  <li className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500" />
                    Slack/Telegram alerts
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>

          {/* Interactive Terminal Demo */}
          <div id="demo" className="mt-20 max-w-4xl mx-auto">
            <Card className="overflow-hidden">
              <div className="bg-zinc-900 text-zinc-100 p-4 rounded-t-lg font-mono text-sm">
                <div className="flex items-center gap-2 mb-4">
                  <div className="h-3 w-3 rounded-full bg-red-500" />
                  <div className="h-3 w-3 rounded-full bg-yellow-500" />
                  <div className="h-3 w-3 rounded-full bg-green-500" />
                  <span className="ml-4 text-zinc-400">prodsynth — Product Synthesis</span>
                </div>
                <div className="space-y-2">
                  <div>
                    <span className="text-green-400">$</span>{" "}
                    <span className="text-blue-400">prodsynth</span>{" "}
                    <span className="text-yellow-400">generate</span>{" "}
                    <span className="text-green-300">--from github.com/user/repo</span>{" "}
                    <span className="text-purple-400">--template saas</span>
                  </div>
                  <div className="text-zinc-400">[Research Agent] Analyzing repo... ✅</div>
                  <div className="text-zinc-400">[Architect Agent] Designing C4 model... ✅</div>
                  <div className="text-zinc-400">[Code Agent] Generating Python/FastAPI code... ✅</div>
                  <div className="text-zinc-400">[Test Agent] Running pytest + playwright... ✅</div>
                  <div className="text-zinc-400">[Deploy Agent] Deploying to Render... ✅</div>
                  <div className="text-green-400 mt-2">
                    ✨ Product ready at: https://my-product.onrender.com
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* ─── Pricing ──────────────────────────────────────────── */}
      <section id="pricing" className="py-20">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold sm:text-4xl">Simple, Transparent Pricing</h2>
            <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
              Start free. Upgrade when you need more power.
            </p>
          </div>

          <Tabs defaultValue="monthly" className="max-w-5xl mx-auto">
            <div className="flex justify-center mb-8">
              <TabsList>
                <TabsTrigger value="monthly">Monthly</TabsTrigger>
                <TabsTrigger value="yearly">Yearly (Save 20%)</TabsTrigger>
              </TabsList>
            </div>

            <div className="grid gap-8 md:grid-cols-3">
              {/* Free Tier */}
              <TabsContent value="monthly" className="md:col-span-1">
                <Card>
                  <CardHeader>
                    <CardTitle>Free</CardTitle>
                    <div className="mt-4">
                      <span className="text-4xl font-bold">$0</span>
                      <span className="text-muted-foreground">/month</span>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Perfect for trying out the platform.
                    </p>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <ul className="space-y-2">
                      {[
                        "3 projects",
                        "1GB graph storage",
                        "Local CLI only",
                        "Community support",
                      ].map((feature, i) => (
                        <li key={i} className="flex items-center gap-2">
                          <Check className="h-4 w-4 text-green-500 flex-shrink-0" />
                          <span className="text-sm">{feature}</span>
                        </li>
                      ))}
                    </ul>
                    <Button className="w-full" variant="outline" asChild>
                      <Link href="/signup">Get Started</Link>
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="yearly" className="md:col-span-1">
                <Card>
                  <CardHeader>
                    <CardTitle>Free</CardTitle>
                    <div className="mt-4">
                      <span className="text-4xl font-bold">$0</span>
                      <span className="text-muted-foreground">/year</span>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Perfect for trying out the platform.
                    </p>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <ul className="space-y-2">
                      {[
                        "3 projects",
                        "1GB graph storage",
                        "Local CLI only",
                        "Community support",
                      ].map((feature, i) => (
                        <li key={i} className="flex items-center gap-2">
                          <Check className="h-4 w-4 text-green-500 flex-shrink-0" />
                          <span className="text-sm">{feature}</span>
                        </li>
                      ))}
                    </ul>
                    <Button className="w-full" variant="outline" asChild>
                      <Link href="/signup">Get Started</Link>
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Pro Tier */}
              <TabsContent value="monthly" className="md:col-span-1">
                <Card className="border-primary shadow-lg relative">
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                    <Badge>Most Popular</Badge>
                  </div>
                  <CardHeader>
                    <CardTitle>Pro</CardTitle>
                    <div className="mt-4">
                      <span className="text-4xl font-bold">$49</span>
                      <span className="text-muted-foreground">/month</span>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      For teams building multiple products.
                    </p>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <ul className="space-y-2">
                      {[
                        "Unlimited projects",
                        "100GB graph storage",
                        "Team collaboration",
                        "GPU simulations",
                        "Deploy to 5 targets",
                        "Priority support",
                      ].map((feature, i) => (
                        <li key={i} className="flex items-center gap-2">
                          <Check className="h-4 w-4 text-green-500 flex-shrink-0" />
                          <span className="text-sm">{feature}</span>
                        </li>
                      ))}
                    </ul>
                    <Button className="w-full" asChild>
                      <Link href="/signup?plan=pro">Start Free Trial</Link>
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="yearly" className="md:col-span-1">
                <Card className="border-primary shadow-lg relative">
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                    <Badge>Most Popular</Badge>
                  </div>
                  <CardHeader>
                    <CardTitle>Pro</CardTitle>
                    <div className="mt-4">
                      <span className="text-4xl font-bold">$470</span>
                      <span className="text-muted-foreground">/year</span>
                      <span className="ml-2 text-sm text-green-500">Save $58</span>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      For teams building multiple products.
                    </p>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <ul className="space-y-2">
                      {[
                        "Unlimited projects",
                        "100GB graph storage",
                        "Team collaboration",
                        "GPU simulations",
                        "Deploy to 5 targets",
                        "Priority support",
                      ].map((feature, i) => (
                        <li key={i} className="flex items-center gap-2">
                          <Check className="h-4 w-4 text-green-500 flex-shrink-0" />
                          <span className="text-sm">{feature}</span>
                        </li>
                      ))}
                    </ul>
                    <Button className="w-full" asChild>
                      <Link href="/signup?plan=pro&billing=yearly">Start Free Trial</Link>
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Enterprise Tier */}
              <TabsContent value="monthly" className="md:col-span-1">
                <Card>
                  <CardHeader>
                    <CardTitle>Enterprise</CardTitle>
                    <div className="mt-4">
                      <span className="text-4xl font-bold">$999+</span>
                      <span className="text-muted-foreground">/month</span>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      For large organizations with custom needs.
                    </p>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <ul className="space-y-2">
                      {[
                        "Everything in Pro",
                        "On-premises deployment",
                        "SSO / SAML / OIDC",
                        "SLA 99.9%",
                        "Custom agents",
                        "Dedicated support",
                      ].map((feature, i) => (
                        <li key={i} className="flex items-center gap-2">
                          <Check className="h-4 w-4 text-green-500 flex-shrink-0" />
                          <span className="text-sm">{feature}</span>
                        </li>
                      ))}
                    </ul>
                    <Button className="w-full" variant="outline" asChild>
                      <Link href="/contact">Contact Sales</Link>
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="yearly" className="md:col-span-1">
                <Card>
                  <CardHeader>
                    <CardTitle>Enterprise</CardTitle>
                    <div className="mt-4">
                      <span className="text-4xl font-bold">$9,990+</span>
                      <span className="text-muted-foreground">/year</span>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      For large organizations with custom needs.
                    </p>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <ul className="space-y-2">
                      {[
                        "Everything in Pro",
                        "On-premises deployment",
                        "SSO / SAML / OIDC",
                        "SLA 99.9%",
                        "Custom agents",
                        "Dedicated support",
                      ].map((feature, i) => (
                        <li key={i} className="flex items-center gap-2">
                          <Check className="h-4 w-4 text-green-500 flex-shrink-0" />
                          <span className="text-sm">{feature}</span>
                        </li>
                      ))}
                    </ul>
                    <Button className="w-full" variant="outline" asChild>
                      <Link href="/contact">Contact Sales</Link>
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>
            </div>
          </Tabs>
        </div>
      </section>

      {/* ─── Marketplace Preview ───────────────────────────────────── */}
      <section id="marketplace" className="py-20 bg-muted/50">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold sm:text-4xl">Marketplace Templates</h2>
            <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
              Start with a proven template and customize to your needs.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-3 max-w-5xl mx-auto">
            {[
              {
                title: "SaaS Starter",
                description: "Complete SaaS with auth, billing, and dashboard.",
                icon: <Globe className="h-6 w-6 text-primary" />,
                tags: ["FastAPI", "Next.js", "Stripe"],
              },
              {
                title: "API Service",
                description: "RESTful API with documentation and rate limiting.",
                icon: <Server className="h-6 w-6 text-primary" />,
                tags: ["FastAPI", "PostgreSQL", "Redis"],
              },
              {
                title: "Dashboard & Analytics",
                description: "Real-time dashboard with charts and metrics.",
                icon: <BarChart3 className="h-6 w-6 text-primary" />,
                tags: ["Next.js", "Tailwind", "Recharts"],
              },
            ].map((template, i) => (
              <Card key={i} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center gap-4">
                    {template.icon}
                    <CardTitle className="text-xl">{template.title}</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-4">{template.description}</p>
                  <div className="flex flex-wrap gap-2">
                    {template.tags.map((tag, j) => (
                      <Badge key={j} variant="secondary">{tag}</Badge>
                    ))}
                  </div>
                  <Button className="w-full mt-6" variant="outline" asChild>
                    <Link href="/marketplace">View Template</Link>
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="text-center mt-10">
            <Button size="lg" variant="outline" asChild>
              <Link href="/marketplace">
                Browse All Templates
                <ChevronRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* ─── FAQ ──────────────────────────────────────────────── */}
      <section className="py-20">
        <div className="container max-w-3xl">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold sm:text-4xl">Frequently Asked Questions</h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Can't find the answer you're looking for?{" "}
              <a href="/contact" className="text-primary hover:underline">
                Contact our support team
              </a>
              .
            </p>
          </div>

          <Accordion type="single" collapsible className="w-full">
            {[
              {
                question: "How fast can I generate a product?",
                answer:
                  "You can generate a working SaaS or API from a repository in 5 minutes using our AI agents. The process involves analyzing your repo, designing architecture, generating code, running tests, and deploying — all automatically.",
              },
              {
                question: "What technologies do you support?",
                answer:
                  "We support Python/FastAPI, Next.js, React, Rust, Go, and more through our CLI-Anything adapter. Our platform is designed to be extensible, so we're always adding new tech stacks.",
              },
              {
                question: "Is my code safe and who owns it?",
                answer:
                  "Yes, your code is safe. We use LicenseChecker agent to ensure IP protection. You own the generated code, while graphs are anonymized. Our platform follows GDPR and OWASP security standards.",
              },
              {
                question: "How does the token budget work?",
                answer:
                  "We use cascading LLM (cheap models → expensive models) to optimize costs. Each synthesis run has a $0.50 budget by default. Graphiti acts as a cache to avoid reprocessing the same data.",
              },
              {
                question: "Can I deploy to my own infrastructure?",
                answer:
                  "Yes! We support deployment to Render, Fly.io, Docker, and Kubernetes. Enterprise customers can also use on-premises deployment with full SSO and RBAC support.",
              },
            ].map((faq, i) => (
              <AccordionItem key={i} value={`item-${i}`}>
                <AccordionTrigger className="text-left">
                  <Star className="mr-2 h-4 w-4 text-primary inline" />
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </section>

      {/* ─── CTA Section ────────────────────────────────────────── */}
      <section className="py-20 bg-primary text-primary-foreground">
        <div className="container text-center">
          <h2 className="text-3xl font-bold sm:text-4xl">Ready to Build Your Next Product?</h2>
          <p className="mt-4 text-xl text-primary-foreground/80 max-w-2xl mx-auto">
            Join 1000+ developers who are already using ProdSynth to turn their ideas into working products.
          </p>
          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button size="lg" variant="secondary" className="w-full sm:w-auto" asChild>
              <Link href="/signup">
                Get Started for Free
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="w-full sm:w-auto border-primary-foreground text-primary-foreground hover:bg-primary-foreground hover:text-primary"
              asChild
            >
              <a href="https://github.com/prodsynth/monorepo" target="_blank" rel="noopener noreferrer">
                <Github className="mr-2 h-4 w-4" />
                Star on GitHub
              </a>
            </Button>
          </div>
        </div>
      </section>
    </main>
  );
}
