import { ChatWindow } from "@/components/ChatWindow";

export default function AgentsPage() {
  const InfoCard = (
    <div className="p-4 md:p-8 rounded bg-gray-100 w-full max-h-[85%] overflow-hidden">
      This is a Star 7 demo
    </div>
  );
  return (
    <ChatWindow
      endpoint="api/chat/retrieval"
      emptyStateComponent={InfoCard}
      showIngestForm={true}
      placeholder={
        "Ask me anything! I can help you find documents, answer questions, and more."
      }
      emoji="7️⃣"
      titleText="Smart7 Assistant"
    ></ChatWindow>
  );
}
