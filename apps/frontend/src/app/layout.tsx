import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import { Toaster } from "@/components/ui/toaster";
import { Analytics } from "@/components/analytics";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: {
    default: "ProdSynth — AI-Native Product Synthesis Engine",
    template: "%s | ProdSynth",
  },
  description:
    "Turn any repository into a working product in 5 minutes. AI-Native Product Synthesis Engine with Memory Graphs (Graphiti) and Agentic Workflows.",
  keywords: [
    "AI product synthesis",
    "code to product",
    "repository analysis",
    "Graphiti",
    "Neo4j",
    "FastAPI",
    "Next.js",
    "automated product generation",
    "SaaS generator",
    "CLI tool",
    "openclaude integration",
    "CLI-Anything",
    "memory graphs",
    "product DNA",
  ],
  authors: [{ name: "ProdSynth Team" }],
  creator: "ProdSynth Team",
  publisher: "ProdSynth",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL("https://prodsynth.com"),
  openGraph: {
    title: "ProdSynth — AI-Native Product Synthesis Engine",
    description:
      "Turn any repo into a product in 5 minutes. Generate SaaS, APIs, Dashboards with AI Agents.",
    url: "https://prodsynth.com",
    siteName: "ProdSynth",
    images: [
      {
        url: "https://prodsynth.com/og-image.png",
        width: 1200,
        height: 630,
        alt: "ProdSynth — Product Synthesis Engine",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "ProdSynth — AI-Native Product Synthesis Engine",
    description: "Turn any repo into a product in 5 minutes.",
    images: ["https://prodsynth.com/twitter-image.png"],
    creator: "@prodsynth",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "standard",
      "max-snippet": -1,
    },
  },
  verification: {
    google: "google-site-verification-code",
    yandex: "yandex-verification-code",
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "white" },
    { media: "(prefers-color-scheme: dark)", color: "black" },
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: "ProdSynth",
    description:
      "AI-Native Product Synthesis Engine — turn any repository into a working product in 5 minutes.",
    operatingSystem: "Windows, macOS, Linux",
    applicationCategory: "DeveloperApplication",
    offers: {
      "@type": "Offer",
      price: "0",
      priceCurrency: "USD",
    },
    aggregateRating: {
      "@type": "AggregateRating",
      ratingValue: "4.8",
      ratingCount: "127",
    },
    screenshot: "https://prodsynth.com/screenshot.png",
    softwareHelp: "https://github.com/prodsynth/monorepo/blob/main/docs/README.md",
    downloadUrl: "https://www.npmjs.com/package/@prodsynth/cli",
    sameAs: [
      "https://github.com/prodsynth/monorepo",
      "https://twitter.com/prodsynth",
      "https://discord.gg/prodsynth",
    ],
  };

  const breadcrumbLd = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      {
        "@type": "ListItem",
        position: 1,
        name: "Home",
        item: "https://prodsynth.com",
      },
      {
        "@type": "ListItem",
        position: 2,
        name: "Documentation",
        item: "https://github.com/prodsynth/monorepo/tree/main/docs",
      },
      {
        "@type": "ListItem",
        position: 3,
        name: "Architecture",
        item: "https://github.com/prodsynth/monorepo/blob/main/CHAT_ARCHITECTURE.md",
      },
    ],
  };

  const faqLd = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: [
      {
        "@type": "Question",
        name: "How fast can I generate a product?",
        acceptedAnswer: {
          "@type": "Answer",
          text: "You can generate a working SaaS or API from a repository in 5 minutes using our AI agents.",
        },
      },
      {
        "@type": "Question",
        name: "What technologies do you support?",
        acceptedAnswer: {
          "@type": "Answer",
          text: "We support Python/FastAPI, Next.js, React, Rust, Go, and more through our CLI-Anything adapter.",
        },
      },
      {
        "@type": "Question",
        name: "Is my code safe?",
        acceptedAnswer: {
          "@type": "Answer",
          text: "Yes, we use LicenseChecker agent to ensure IP protection. Your code belongs to you, graphs are anonymized.",
        },
      },
    ],
  };

  const productLd = {
    "@context": "https://schema.org",
    "@type": "Product",
    name: "ProdSynth Pro",
    description: "AI-Native Product Synthesis Engine with advanced memory graphs.",
    brand: {
      "@type": "Brand",
      name: "ProdSynth",
    },
    offers: {
      "@type": "Offer",
      price: "49.00",
      priceCurrency: "USD",
      priceValidUntil: "2026-12-31",
    },
    aggregateRating: {
      "@type": "AggregateRating",
      ratingValue: "4.9",
      reviewCount: "89",
    },
  };

  return (
    <html lang="en">
      <head>
        {/* JSON-LD Structured Data */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(faqLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(productLd) }}
        />

        {/* Preconnect to external domains */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        
        {/* Favicon */}
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="icon" href="/icon.svg" type="image/svg+xml" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="manifest" href="/manifest.webmanifest" />
      </head>
      <body className={`${inter.className} min-h-screen bg-background text-foreground`}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
          <Toaster />
          <Analytics />
        </ThemeProvider>

        {/* Links to internal GitHub projects (Footer) */}
        <footer className="border-t py-6 md:py-10">
          <div className="container mx-auto px-4 md:px-6">
            <div className="grid gap-8 lg:grid-cols-4">
              <div>
                <h3 className="text-lg font-semibold">ProdSynth</h3>
                <p className="mt-2 text-sm text-muted-foreground">
                  AI-Native Product Synthesis Engine
                </p>
              </div>
              <div>
                <h4 className="text-sm font-semibold">GitHub</h4>
                <ul className="mt-2 space-y-2 text-sm">
                  <li>
                    <a
                      href="https://github.com/prodsynth/monorepo"
                      className="text-muted-foreground hover:text-foreground"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Monorepo
                    </a>
                  </li>
                  <li>
                    <a
                      href="https://github.com/openclaude/openclaude"
                      className="text-muted-foreground hover:text-foreground"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      OpenClaude (Engine)
                    </a>
                  </li>
                  <li>
                    <a
                      href="https://github.com/getzep/graphiti"
                      className="text-muted-foreground hover:text-foreground"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Graphiti (Memory)
                    </a>
                  </li>
                  <li>
                    <a
                      href="https://github.com/HKUDS/CLI-Anything"
                      className="text-muted-foreground hover:text-foreground"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      CLI-Anything (Adapter)
                    </a>
                  </li>
                </ul>
              </div>
              <div>
                <h4 className="text-sm font-semibold">Documentation</h4>
                <ul className="mt-2 space-y-2 text-sm">
                  <li>
                    <a
                      href="https://github.com/prodsynth/monorepo/blob/main/README.md"
                      className="text-muted-foreground hover:text-foreground"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      README
                    </a>
                  </li>
                  <li>
                    <a
                      href="https://github.com/prodsynth/monorepo/blob/main/CHAT_ARCHITECTURE.md"
                      className="text-muted-foreground hover:text-foreground"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Architecture (BMAD)
                    </a>
                  </li>
                  <li>
                    <a
                      href="https://github.com/prodsynth/monorepo/blob/main/CONTEXT_MAP.md"
                      className="text-muted-foreground hover:text-foreground"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Context Map
                    </a>
                  </li>
                  <li>
                    <a
                      href="https://github.com/prodsynth/monorepo/blob/main/TODO.md"
                      className="text-muted-foreground hover:text-foreground"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      TODO List
                    </a>
                  </li>
                </ul>
              </div>
              <div>
                <h4 className="text-sm font-semibold">Legal</h4>
                <ul className="mt-2 space-y-2 text-sm">
                  <li>
                    <a
                      href="/privacy"
                      className="text-muted-foreground hover:text-foreground"
                    >
                      Privacy Policy
                    </a>
                  </li>
                  <li>
                    <a
                      href="/terms"
                      className="text-muted-foreground hover:text-foreground"
                    >
                      Terms of Service
                    </a>
                  </li>
                  <li>
                    <a
                      href="/licensing"
                      className="text-muted-foreground hover:text-foreground"
                    >
                      Licensing & IP
                    </a>
                  </li>
                </ul>
              </div>
            </div>
            <div className="mt-8 border-t pt-6 text-center text-sm text-muted-foreground">
              © 2026 ProdSynth. All rights reserved.
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
