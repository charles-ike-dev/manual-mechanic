import LogoutButton from "@/components/logoutBtn";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <div className="flex w-full flex-row justify-end py-4 px-4">
        <LogoutButton />
      </div>
      {children}
    </div>
  );
}
