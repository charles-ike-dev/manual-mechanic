// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { version } from "@/lib/config";

function isPublicFile(pathname: string): boolean {
  // Exclude static files (e.g., images, scripts, styles)
  return /\.(.*)$/.test(pathname);
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const isLoginPage = pathname === "/login" || pathname.startsWith("/login/");
  const isApiRoute = pathname.startsWith("/api/");
  const authenticated = request.cookies.get("authenticated")?.value;
  const isPublic = isPublicFile(pathname);
  if (isApiRoute || isPublic) {
    // Allow API routes and public files to proceed
    return NextResponse.next();
  }

  if (!authenticated && !isLoginPage) {
    // Redirect unauthenticated users to the login page
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (authenticated && (isLoginPage || pathname !== `/${version}`)) {
    // Redirect authenticated users away from the login page
    return NextResponse.redirect(new URL(`/${version}`, request.url));
  }
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
