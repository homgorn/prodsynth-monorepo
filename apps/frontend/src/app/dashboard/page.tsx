"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  Cpu,
  GitBranch,
  Code,
  TestTube,
  Rocket,
  BarChart3,
  DollarSign,
  Shield,
  Bell,
  CheckCircle,
  AlertTriangle,
  Clock,
  Users,
  Settings,
  Download,
  Upload,
  Play,
  Square,
  Layers,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AspectRatio } from "@/components/ui/aspect-ratio";

// Mock data for dashboard
const agentStatus = [
  { name: "ResearchAgent", status: "completed", progress: 100, cost: 0.05 },
  { name: "ArchitectAgent", status: "completed", progress: 100, cost: 0.15 },
  { name: "CodeAgent", status: "running", progress: 65, cost: 0.20 },
  { name: "TestAgent", status: "pending", progress: 0, cost: 0.0 },
  { name: "DeployAgent", status: "pending", progress: 0, cost: 0.0 },
];

const projects = [
  {
    id: "proj_123",
    name: "SaaS Dashboard",
    status: "running",
    target: "render",
    progress: 65,
    created: "2026-04-25",
  },
  {
    id: "proj_456",
    name: "API Service",
    status: "completed",
    target: "docker",
    progress: 100,
    created: "2026-04-20",
  },
  {
    id: "proj_789",
    name: "Data Pipeline",
    status: "failed",
    target: "fly",
    progress: 30,
    created: "2026-04-22",
  },
];

export default function DashboardPage() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => setIsLoading(false), 1000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <main className="min-h-screen bg-background">
      {/* ─── Dashboard Header ─────────────────────────────────── */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <Rocket className="h-6 w-6 text-primary" />
            <span className="font-bold text-xl">ProdSynth</span>
            <Badge variant="outline" className="ml-2">
              <Square className="mr-1 h-3 w-3" />
              Dashboard
            </Badge>
          </div>

          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" asChild>
              <Link href="/">
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back to Home
              </Link>
            </Button>
            <Button size="sm" variant="outline">
              <Settings className="mr-2 h-4 w-4" />
              Settings
            </Button>
          </div>
        </div>
      </header>

      <div className="container py-8">
        {/* ─── Stats Overview ─────────────────────────────────── */}
        <div className="grid gap-4 md:grid-cols-4 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Projects</CardTitle>
              <Layers className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">3</div>
              <p className="text-xs text-muted-foreground">+2 from last week</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Cost</CardTitle>
              <DollarSign className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">$1.23</div>
              <p className="text-xs text-muted-foreground">This month</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Agent Runs</CardTitle>
              <Cpu className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">42</div>
              <p className="text-xs text-muted-foreground">98% success rate</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Graph Size</CardTitle>
              <BarChart3 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">1.2 GB</div>
              <p className="text-xs text-muted-foreground">Across all projects</p>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="projects" className="space-y-4">
          <TabsList>
            <TabsTrigger value="projects">Projects</TabsTrigger>
            <TabsTrigger value="agents">Agent Status</TabsTrigger>
            <TabsTrigger value="graph">Graph View</TabsTrigger>
            <TabsTrigger value="billing">Billing</TabsTrigger>
          </TabsList>

          {/* ─── Projects Tab ─────────────────────────────────── */}
          <TabsContent value="projects" className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold">Your Projects</h2>
              <Button asChild>
                <Link href="/#demo">
                  <Play className="mr-2 h-4 w-4" />
                  New Project
                </Link>
              </Button>
            </div>

            <div className="grid gap-4">
              {projects.map((project) => (
                <Card key={project.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="pt-6">
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <h3 className="font-semibold text-lg">{project.name}</h3>
                          <Badge
                            variant={
                              project.status === "completed"
                                ? "default"
                                : project.status === "running"
                                ? "secondary"
                                : "destructive"
                            }
                          >
                            {project.status === "completed" && <CheckCircle className="mr-1 h-3 w-3" />}
                            {project.status === "running" && <Clock className="mr-1 h-3 w-3" />}
                            {project.status === "failed" && <AlertTriangle className="mr-1 h-3 w-3" />}
                            {project.status}
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground">
                          ID: {project.id} • Target: {project.target} • Created: {project.created}
                        </p>
                      </div>

                      <div className="flex items-center gap-4">
                        <div className="flex-1 min-w-[200px]">
                          <div className="flex justify-between text-sm mb-1">
                            <span>Progress</span>
                            <span>{project.progress}%</span>
                          </div>
                          <Progress value={project.progress} className="h-2" />
                        </div>
                        <Button variant="outline" size="sm" asChild>
                          <Link href={`/dashboard/projects/${project.id}`}>
                            View
                          </Link>
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* ─── Agent Status Tab ─────────────────────────────────── */}
          <TabsContent value="agents" className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold">Agent Pipeline Status</h2>
              <Badge variant="outline">
                <Cpu className="mr-1 h-3 w-3" />
                Live
              </Badge>
            </div>

            {/* Pipeline Visualization */}
            <Card>
              <CardContent className="pt-6">
                <div className="flex flex-col md:flex-row items-center justify-center gap-4 md:gap-8">
                  {[
                    { icon: <GitBranch className="h-6 w-6" />, name: "Research", status: "completed" },
                    { icon: <GitBranch className="h-6 w-6" />, name: "Architect", status: "completed" },
                    { icon: <Code className="h-6 w-6" />, name: "Code", status: "running" },
                    { icon: <TestTube className="h-6 w-6" />, name: "Test", status: "pending" },
                    { icon: <Rocket className="h-6 w-6" />, name: "Deploy", status: "pending" },
                  ].map((step, i) => (
                    <div key={i} className="flex flex-col items-center gap-2">
                      <div
                        className={`h-16 w-16 rounded-full flex items-center justify-center ${
                          step.status === "completed"
                            ? "bg-green-100 text-green-700"
                            : step.status === "running"
                            ? "bg-blue-100 text-blue-700 animate-pulse"
                            : "bg-muted text-muted-foreground"
                        }`}
                      >
                        {step.icon}
                      </div>
                      <span className="text-sm font-medium">{step.name}</span>
                      {i < 4 && (
                        <div className="hidden md:block text-muted-foreground">→</div>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Agent Details */}
            <div className="grid gap-4">
              {agentStatus.map((agent, i) => (
                <Card key={i}>
                  <CardContent className="pt-6">
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                      <div className="flex items-center gap-4">
                        <div
                          className={`h-10 w-10 rounded-full flex items-center justify-center ${
                            agent.status === "completed"
                              ? "bg-green-100 text-green-700"
                              : agent.status === "running"
                              ? "bg-blue-100 text-blue-700"
                              : "bg-muted text-muted-foreground"
                          }`}
                        >
                          <Cpu className="h-5 w-5" />
                        </div>
                        <div>
                          <h3 className="font-semibold">{agent.name}</h3>
                          <p className="text-sm text-muted-foreground">
                            Cost: ${agent.cost.toFixed(2)}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center gap-4">
                        <div className="flex-1 min-w-[150px]">
                          <Progress value={agent.progress} className="h-2" />
                        </div>
                        <Badge
                          variant={
                            agent.status === "completed"
                              ? "default"
                              : agent.status === "running"
                              ? "secondary"
                              : "outline"
                          }
                        >
                          {agent.status}
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* ─── Graph View Tab ─────────────────────────────────── */}
          <TabsContent value="graph" className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold">Product DNA Graph</h2>
              <Button variant="outline" size="sm">
                <Download className="mr-2 h-4 w-4" />
                Export Graph
              </Button>
            </div>

            <Card>
              <CardContent className="pt-6">
                <AspectRatio ratio={16 / 9} className="bg-muted rounded-lg flex items-center justify-center">
                  <div className="text-center space-y-2">
                    <BarChart3 className="h-12 w-12 text-muted-foreground mx-auto" />
                    <p className="text-muted-foreground">
                      Graph visualization will appear here
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Connected to Neo4j (Graphiti)
                    </p>
                  </div>
                </AspectRatio>
              </CardContent>
            </Card>

            <div className="grid gap-4 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Graph Stats</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 text-sm">
                    <li className="flex justify-between">
                      <span className="text-muted-foreground">Nodes</span>
                      <span className="font-medium">1,234</span>
                    </li>
                    <li className="flex justify-between">
                      <span className="text-muted-foreground">Edges</span>
                      <span className="font-medium">3,456</span>
                    </li>
                    <li className="flex justify-between">
                      <span className="text-muted-foreground">Last Updated</span>
                      <span className="font-medium">2 min ago</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Recent Activity</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 text-sm">
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      <span>Node added: Function `main`</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      <span>Edge added: Class → Method</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Clock className="h-4 w-4 text-blue-500" />
                      <span>Query running...</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* ─── Billing Tab ─────────────────────────────────── */}
          <TabsContent value="billing" className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold">Billing & Quotas</h2>
              <Button asChild>
                <Link href="/#pricing">
                  Upgrade Plan
                </Link>
              </Button>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>Current Plan: Pro</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between">
                    <span>Price</span>
                    <span className="font-bold">$49/month</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Renewal Date</span>
                    <span>May 26, 2026</span>
                  </div>
                  <Button className="w-full" variant="outline">
                    Manage Subscription
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Usage Quotas</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Token Budget</span>
                      <span>$0.50 used / $10.00</span>
                    </div>
                    <Progress value={5} className="h-2" />
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Graph Storage</span>
                      <span>1.2 GB / 100 GB</span>
                    </div>
                    <Progress value={1.2} className="h-2" />
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>API Calls</span>
                      <span>42 / 1,000</span>
                    </div>
                    <Progress value={4.2} className="h-2" />
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </main>
  );
}
