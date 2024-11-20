import { useState } from "react";
import { Copy } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "./ui/button";

export default function CopyBtn({
  text,
  disabled,
  className,
  ...props
}: {
  text: string;
  disabled?: boolean;
  className?: string;
  [key: string]: any;
}) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async (txt: string) => {
    try {
      await navigator.clipboard.writeText(txt);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000); // Reset status after 2 seconds
    } catch (err) {
      console.error("Failed to copy: ", err);
    }
  };

  return (
    <Button
      onClick={() => copyToClipboard(text)}
      type="button"
      variant={"outline"}
      className={cn(className, "flex flex-row items-center gap-x-2")}
      disabled={disabled}
      {...props}
    >
      <Copy className="w-4 h-4" />

      {copied ? " Copied!" : " Copy"}
    </Button>
  );
}
