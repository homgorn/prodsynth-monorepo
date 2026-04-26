import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { locales, defaultLocale } from "@/i18n/dictionaries";

const PUBLIC_FILE = /\.(.*)$/;

export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname;

  if (
    pathname.startsWith("/_next") ||
    pathname.startsWith("/api") ||
    pathname.startsWith("/static") ||
    PUBLIC_FILE.test(pathname)
  ) {
    return NextResponse.next();
  }

  const locale =
    request.cookies.get("NEXT_LOCALE")?.value ||
    request.headers.get("Accept-Language")?.split(",")[0]?.split("-")[0] ||
    defaultLocale;

  const validLocale = locales.includes(locale as any)
    ? locale
    : defaultLocale;

  const response = NextResponse.next();
  if (validLocale !== defaultLocale) {
    response.cookies.set("NEXT_LOCALE", validLocale, { path: "/" });
  }

  return response;
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};