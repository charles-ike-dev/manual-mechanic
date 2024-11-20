// app/components/LogoutButton.tsx
"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

const LogoutButton: React.FC = () => {
  const router = useRouter();

  const handleLogout = async () => {
    await fetch("/api/auth/logout", {
      method: "POST",
    });
    router.replace("/login");
  };

  return <Button onClick={handleLogout}>Logout</Button>;
};

export default LogoutButton;
