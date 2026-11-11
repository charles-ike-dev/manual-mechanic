import { version } from "@/lib/config";
import { redirect } from "next/navigation";

export default function Page() {
  redirect(`/${version}`);
}
