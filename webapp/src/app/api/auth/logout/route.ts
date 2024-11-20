// app/logout/api/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  const response = NextResponse.json({
    message: "Logout effettuato con successo",
  });
  response.cookies.set({
    name: "authenticated",
    value: "",
    expires: new Date(0),
    path: "/",
  });
  return response;
}
