import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import ChatInput from "@/components/chat/ChatInput";
import SuggestionCards from "@/components/chat/SuggestionCards";

export default function Home() {
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex flex-1 flex-col">
        {/* Header */}
        <Header />

        {/* ChatGPT-style Home */}
        <main className="flex flex-1 items-center justify-center bg-gray-50">
          <div className="w-full max-w-5xl px-8 text-center">
            <h1 className="text-6xl font-bold">
              🤖 KnowledgeHub AI
            </h1>

            <p className="mt-4 text-xl text-gray-500">
              Ask anything about your uploaded documents.
            </p>

            {/* Chat Input */}
            <ChatInput />

            {/* Suggested Prompts */}
            <SuggestionCards />
          </div>
        </main>
      </div>
    </div>
  );
}