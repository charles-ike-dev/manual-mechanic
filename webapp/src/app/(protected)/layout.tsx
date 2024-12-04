import LogoutButton from "@/components/logoutBtn";
import RefreshButton from "@/components/refreshBtn";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <div className="flex w-full flex-row gap-x-2 justify-end py-4 px-4">
        <RefreshButton />
        <LogoutButton />
      </div>
      {children}
    </div>
  );
}
