"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { RotateCcw } from "lucide-react";

export default function RefreshButton({ className }: { className?: string }) {
  const router = useRouter();

  const handleRefresh = () => {
    window.location.reload();
  };

  return (
    <Button onClick={handleRefresh} variant={"outline"} className={className}>
      <span className="sr-only">Refresh</span> <RotateCcw size={24} />
    </Button>
  );
}
