"use client";

import { useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  Search,
  Star,
  Download,
  Play,
  GitBranch,
  Code,
  Database,
  BarChart3,
  Cpu,
  Layers,
  Shield,
  Eye,
  Heart,
  Filter,
  SlidersHorizontal,
  Globe,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AspectRatio } from "@/components/ui/aspect-ratio";

// Mock data for marketplace templates
const templates = [
  {
    id: "tmpl_1",
    name: "SaaS Starter",
    description: "Complete SaaS with auth, billing, and dashboard.",
    category: "saas",
    tech_stack: ["FastAPI", "Next.js", "Stripe"],
    preview_url: "https://demo.prodsynth.com/saas-starter",
    price: 0,
    rating: 4.8,
    downloads: 1234,
    isFavorite: false,
  },
  {
    id: "tmpl_2",
    name: "API Service",
    description: "RESTful API with documentation and rate limiting.",
    category: "api",
    tech_stack: ["FastAPI", "PostgreSQL", "Redis"],
    preview_url: "https://demo.prodsynth.com/api-service",
    price: 0,
    rating: 4.5,
    downloads: 856,
    isFavorite: true,
  },
  {
    id: "tmpl_3",
    name: "Dashboard & Analytics",
    description: "Real-time dashboard with charts and metrics.",
    category: "dashboard",
    tech_stack: ["Next.js", "Tailwind", "Recharts"],
    preview_url: "https://demo.prodsynth.com/dashboard",
    price: 49,
    rating: 4.9,
    downloads: 567,
    isFavorite: false,
  },
  {
    id: "tmpl_4",
    name: "E-commerce Platform",
    description: "Full-featured online store with cart and checkout.",
    category: "saas",
    tech_stack: ["Next.js", "Stripe", "PostgreSQL"],
    preview_url: "https://demo.prodsynth.com/ecommerce",
    price: 99,
    rating: 4.7,
    downloads: 432,
    isFavorite: false,
  },
  {
    id: "tmpl_5",
    name: "Data Pipeline",
    description: "ETL pipeline with scheduling and monitoring.",
    category: "api",
    tech_stack: ["Python", "Apache Airflow", "PostgreSQL"],
    preview_url: "https://demo.prodsynth.com/data-pipeline",
    price: 0,
    rating: 4.6,
    downloads: 321,
    isFavorite: false,
  },
];

export default function MarketplacePage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [favorites, setFavorites] = useState(
    templates.filter((t) => t.isFavorite).map((t) => t.id)
  );

  const filteredTemplates = templates.filter((template) => {
    if (
      searchQuery &&
      !template.name.toLowerCase().includes(searchQuery.toLowerCase()) &&
      !template.description.toLowerCase().includes(searchQuery.toLowerCase())
    ) {
      return false;
    }
    return true;
  });

  const toggleFavorite = (id: string) => {
    if (favorites.includes(id)) {
      setFavorites(favorites.filter((favId) => favId !== id));
    } else {
      setFavorites([...favorites, id]);
    }
  };

  return (
    <main className="min-h-screen bg-background">
      {/* ─── Marketplace Header ─────────────────────────────────── */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" asChild>
              <Link href="/dashboard">
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back to Dashboard
              </Link>
            </Button>
            <div className="h-6 w-px bg-border mx-2" />
            <h1 className="text-xl font-bold">Marketplace</h1>
            <Badge variant="outline" className="ml-2">
              <Layers className="mr-1 h-3 w-3" />
              {templates.length} Templates
            </Badge>
          </div>

          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" asChild>
              <Link href="/pricing">
                <SlidersHorizontal className="mr-2 h-4 w-4" />
                Filters
              </Link>
            </Button>
          </div>
        </div>
      </header>

      <div className="container py-8">
        {/* ─── Search & Stats ─────────────────────────────────── */}
        <div className="mb-8 space-y-4">
          <div className="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
            <div>
              <h2 className="text-3xl font-bold">Product Templates</h2>
              <p className="text-muted-foreground">
                Start with a proven template and customize to your needs.
              </p>
            </div>

            <div className="relative w-full md:w-auto">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search templates..."
                className="pl-10 w-full md:w-[300px]"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-2">
                  <Layers className="h-5 w-5 text-primary" />
                  <div>
                    <div className="text-2xl font-bold">{templates.length}</div>
                    <div className="text-xs text-muted-foreground">Total Templates</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-2">
                  <Download className="h-5 w-5 text-primary" />
                  <div>
                    <div className="text-2xl font-bold">
                      {templates.reduce((sum, t) => sum + t.downloads, 0).toLocaleString()}
                    </div>
                    <div className="text-xs text-muted-foreground">Downloads</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-2">
                  <Heart className="h-5 w-5 text-primary" />
                  <div>
                    <div className="text-2xl font-bold">{favorites.length}</div>
                    <div className="text-xs text-muted-foreground">Favorites</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-2">
                  <Star className="h-5 w-5 text-primary" />
                  <div>
                    <div className="text-2xl font-bold">
                      {(
                        templates.reduce((sum, t) => sum + t.rating, 0) / templates.length
                      ).toFixed(1)}
                    </div>
                    <div className="text-xs text-muted-foreground">Avg Rating</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* ─── Template Grid ─────────────────────────────────── */}
        <Tabs defaultValue="all" className="space-y-4">
          <TabsList>
            <TabsTrigger value="all">All Templates</TabsTrigger>
            <TabsTrigger value="saas">SaaS</TabsTrigger>
            <TabsTrigger value="api">API</TabsTrigger>
            <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
            <TabsTrigger value="favorites">Favorites</TabsTrigger>
          </TabsList>

          <TabsContent value="all" className="space-y-4">
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {filteredTemplates.map((template) => (
                <Card key={template.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-2">
                        {template.category === "saas" && (
                          <Globe className="h-5 w-5 text-primary" />
                        )}
                        {template.category === "api" && (
                          <Code className="h-5 w-5 text-primary" />
                        )}
                        {template.category === "dashboard" && (
                          <BarChart3 className="h-5 w-5 text-primary" />
                        )}
                        <CardTitle className="text-xl">{template.name}</CardTitle>
                      </div>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => toggleFavorite(template.id)}
                      >
                        <Heart
                          className={`h-4 w-4 ${
                            favorites.includes(template.id) ? "fill-red-500 text-red-500" : ""
                          }`}
                        />
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <AspectRatio ratio={16 / 9} className="bg-muted rounded-lg flex items-center justify-center">
                      <Play className="h-8 w-8 text-muted-foreground/50" />
                    </AspectRatio>

                    <p className="text-sm text-muted-foreground">
                      {template.description}
                    </p>

                    <div className="flex flex-wrap gap-2">
                      {template.tech_stack.map((tech, i) => (
                        <Badge key={i} variant="secondary">
                          {tech}
                        </Badge>
                      ))}
                    </div>

                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-1">
                        <Star className="h-4 w-4 text-yellow-500" />
                        <span className="font-medium">{template.rating}</span>
                        <span className="text-muted-foreground">
                          ({template.downloads} downloads)
                        </span>
                      </div>
                      {template.price > 0 ? (
                        <span className="font-bold">${template.price}</span>
                      ) : (
                        <Badge variant="outline">Free</Badge>
                      )}
                    </div>
                  </CardContent>
                  <CardFooter className="flex gap-2">
                    <Button className="flex-1" asChild>
                      <Link href={`/marketplace/${template.id}`}>
                        <Eye className="mr-2 h-4 w-4" />
                        Preview
                      </Link>
                    </Button>
                    <Button className="flex-1" variant="outline" asChild>
                      <Link href={`/dashboard?template=${template.id}`}>
                        <Download className="mr-2 h-4 w-4" />
                        Use Template
                      </Link>
                    </Button>
                  </CardFooter>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Other tabs would filter similarly */}
          <TabsContent value="saas">
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {filteredTemplates
                .filter((t) => t.category === "saas")
                .map((template) => (
                  <Card key={template.id} className="hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-2">
                          <Globe className="h-5 w-5 text-primary" />
                          <CardTitle className="text-xl">{template.name}</CardTitle>
                        </div>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => toggleFavorite(template.id)}
                        >
                          <Heart
                            className={`h-4 w-4 ${
                              favorites.includes(template.id) ? "fill-red-500 text-red-500" : ""
                            }`}
                          />
                        </Button>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <AspectRatio ratio={16 / 9} className="bg-muted rounded-lg flex items-center justify-center">
                        <Play className="h-8 w-8 text-muted-foreground/50" />
                      </AspectRatio>
                      <p className="text-sm text-muted-foreground">{template.description}</p>
                      <div className="flex flex-wrap gap-2">
                        {template.tech_stack.map((tech, i) => (
                          <Badge key={i} variant="secondary">{tech}</Badge>
                        ))}
                      </div>
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-1">
                          <Star className="h-4 w-4 text-yellow-500" />
                          <span className="font-medium">{template.rating}</span>
                          <span className="text-muted-foreground">({template.downloads} downloads)</span>
                        </div>
                        {template.price > 0 ? (
                          <span className="font-bold">${template.price}</span>
                        ) : (
                          <Badge variant="outline">Free</Badge>
                        )}
                      </div>
                    </CardContent>
                    <CardFooter className="flex gap-2">
                      <Button className="flex-1" asChild>
                        <Link href={`/marketplace/${template.id}`}>
                          <Eye className="mr-2 h-4 w-4" />Preview
                        </Link>
                      </Button>
                      <Button className="flex-1" variant="outline" asChild>
                        <Link href={`/dashboard?template=${template.id}`}>
                          <Download className="mr-2 h-4 w-4" />Use Template
                        </Link>
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
            </div>
          </TabsContent>

          <TabsContent value="api">
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {filteredTemplates
                .filter((t) => t.category === "api")
                .map((template) => (
                  <Card key={template.id} className="hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-2">
                          <Code className="h-5 w-5 text-primary" />
                          <CardTitle className="text-xl">{template.name}</CardTitle>
                        </div>
                        <Button variant="ghost" size="icon" onClick={() => toggleFavorite(template.id)}>
                          <Heart className={`h-4 w-4 ${favorites.includes(template.id) ? "fill-red-500 text-red-500" : ""}`} />
                        </Button>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <AspectRatio ratio={16 / 9} className="bg-muted rounded-lg flex items-center justify-center">
                        <Play className="h-8 w-8 text-muted-foreground/50" />
                      </AspectRatio>
                      <p className="text-sm text-muted-foreground">{template.description}</p>
                      <div className="flex flex-wrap gap-2">
                        {template.tech_stack.map((tech, i) => (
                          <Badge key={i} variant="secondary">{tech}</Badge>
                        ))}
                      </div>
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-1">
                          <Star className="h-4 w-4 text-yellow-500" />
                          <span className="font-medium">{template.rating}</span>
                          <span className="text-muted-foreground">({template.downloads} downloads)</span>
                        </div>
                        {template.price > 0 ? (
                          <span className="font-bold">${template.price}</span>
                        ) : (
                          <Badge variant="outline">Free</Badge>
                        )}
                      </div>
                    </CardContent>
                    <CardFooter className="flex gap-2">
                      <Button className="flex-1" asChild>
                        <Link href={`/marketplace/${template.id}`}>
                          <Eye className="mr-2 h-4 w-4" />Preview
                        </Link>
                      </Button>
                      <Button className="flex-1" variant="outline" asChild>
                        <Link href={`/dashboard?template=${template.id}`}>
                          <Download className="mr-2 h-4 w-4" />Use Template
                        </Link>
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
            </div>
          </TabsContent>

          <TabsContent value="dashboard">
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {filteredTemplates
                .filter((t) => t.category === "dashboard")
                .map((template) => (
                  <Card key={template.id} className="hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-2">
                          <BarChart3 className="h-5 w-5 text-primary" />
                          <CardTitle className="text-xl">{template.name}</CardTitle>
                        </div>
                        <Button variant="ghost" size="icon" onClick={() => toggleFavorite(template.id)}>
                          <Heart className={`h-4 w-4 ${favorites.includes(template.id) ? "fill-red-500 text-red-500" : ""}`} />
                        </Button>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <AspectRatio ratio={16 / 9} className="bg-muted rounded-lg flex items-center justify-center">
                        <Play className="h-8 w-8 text-muted-foreground/50" />
                      </AspectRatio>
                      <p className="text-sm text-muted-foreground">{template.description}</p>
                      <div className="flex flex-wrap gap-2">
                        {template.tech_stack.map((tech, i) => (
                          <Badge key={i} variant="secondary">{tech}</Badge>
                        ))}
                      </div>
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-1">
                          <Star className="h-4 w-4 text-yellow-500" />
                          <span className="font-medium">{template.rating}</span>
                          <span className="text-muted-foreground">({template.downloads} downloads)</span>
                        </div>
                        {template.price > 0 ? (
                          <span className="font-bold">${template.price}</span>
                        ) : (
                          <Badge variant="outline">Free</Badge>
                        )}
                      </div>
                    </CardContent>
                    <CardFooter className="flex gap-2">
                      <Button className="flex-1" asChild>
                        <Link href={`/marketplace/${template.id}`}>
                          <Eye className="mr-2 h-4 w-4" />Preview
                        </Link>
                      </Button>
                      <Button className="flex-1" variant="outline" asChild>
                        <Link href={`/dashboard?template=${template.id}`}>
                          <Download className="mr-2 h-4 w-4" />Use Template
                        </Link>
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
            </div>
          </TabsContent>

          <TabsContent value="favorites">
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {filteredTemplates
                .filter((t) => favorites.includes(t.id))
                .map((template) => (
                  <Card key={template.id} className="hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <CardTitle className="text-xl">{template.name}</CardTitle>
                        <Button variant="ghost" size="icon" onClick={() => toggleFavorite(template.id)}>
                          <Heart className={`h-4 w-4 fill-red-500 text-red-500`} />
                        </Button>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <AspectRatio ratio={16 / 9} className="bg-muted rounded-lg flex items-center justify-center">
                        <Play className="h-8 w-8 text-muted-foreground/50" />
                      </AspectRatio>
                      <p className="text-sm text-muted-foreground">{template.description}</p>
                      <div className="flex flex-wrap gap-2">
                        {template.tech_stack.map((tech, i) => (
                          <Badge key={i} variant="secondary">{tech}</Badge>
                        ))}
                      </div>
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-1">
                          <Star className="h-4 w-4 text-yellow-500" />
                          <span className="font-medium">{template.rating}</span>
                          <span className="text-muted-foreground">({template.downloads} downloads)</span>
                        </div>
                        {template.price > 0 ? (
                          <span className="font-bold">${template.price}</span>
                        ) : (
                          <Badge variant="outline">Free</Badge>
                        )}
                      </div>
                    </CardContent>
                    <CardFooter className="flex gap-2">
                      <Button className="flex-1" asChild>
                        <Link href={`/marketplace/${template.id}`}>
                          <Eye className="mr-2 h-4 w-4" />Preview
                        </Link>
                      </Button>
                      <Button className="flex-1" variant="outline" asChild>
                        <Link href={`/dashboard?template=${template.id}`}>
                          <Download className="mr-2 h-4 w-4" />Use Template
                        </Link>
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </main>
  );
}
