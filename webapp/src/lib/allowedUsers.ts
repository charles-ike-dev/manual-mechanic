// allowedUsers.ts
export const allowedEmails: string[] =
  process.env.ALLOWED_EMAILS?.split(",") || [];
export const allowedPassword: string = process.env.ALLOWED_PASSWORD || "";
