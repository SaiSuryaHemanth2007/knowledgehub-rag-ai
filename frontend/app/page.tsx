"use client";

import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import ChatInput from "@/components/chat/ChatInput";
import SuggestionCards from "@/components/chat/SuggestionCards";
import { useChat } from "@/hooks/useChat";

export default function Home() {
  const {
    loading,
    response,
    error,
    sendMessage,
  } = useChat();

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />

      <div className="flex flex-1 flex-col">
        <Header />

        <main className="flex flex-1 items-center justify-center bg-gray-50">
          <div className="w-full max-w-5xl px-8 text-center">
            <h1 className="text-6xl font-bold">
              🤖 KnowledgeHub AI
            </h1>

            <p className="mt-4 text-xl text-gray-500">
              Ask anything about your uploaded documents.
            </p>

            <ChatInput
              onSend={sendMessage}
              loading={loading}
            />

            <SuggestionCards />

            {loading && (
              <p className="mt-8 text-gray-500">
                Thinking...
              </p>
            )}

            {error && (
              <p className="mt-8 text-red-500">
                {error}
              </p>
            )}

            {response && (
              <div className="mt-10 rounded-xl bg-white p-8 text-left shadow">
                <h2 className="mb-4 text-xl font-bold">
                  Answer
                </h2>

                <p className="leading-8">
                  {response.answer}
                </p>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}