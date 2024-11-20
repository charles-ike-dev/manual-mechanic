// app/login/api/route.ts
import { NextRequest, NextResponse } from "next/server";
import { allowedEmails, allowedPassword } from "@/lib/allowedUsers";

export async function POST(request: NextRequest) {
  const { email, password } = await request.json();

  // Aggiungi console log per il debug
  console.log("Email:", email);
  console.log("Password:", password);

  if (allowedEmails.includes(email) && password === allowedPassword) {
    // Imposta un cookie di autenticazione
    const response = NextResponse.json({
      message: "Login effettuato con successo",
    });
    response.cookies.set("authenticated", "true", {
      httpOnly: true,
      path: "/",
    });
    return response;
  } else {
    return NextResponse.json(
      { message: "Credenziali non valide" },
      { status: 401 }
    );
  }
}
