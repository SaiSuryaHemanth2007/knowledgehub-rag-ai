"use client";

import { useEffect, useRef, useState } from "react";

import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";

import ChatInput from "@/components/chat/ChatInput";
import SuggestionCards from "@/components/chat/SuggestionCards";
import MessageList from "@/components/chat/MessageList";

import { useChat } from "@/hooks/useChat";
import { Message } from "@/types/message";

export default function Home() {
  const {
    loading,
    response,
    error,
    sendMessage,
  } = useChat();

  const [messages, setMessages] = useState<Message[]>([]);

  // Auto scroll target
  const bottomRef = useRef<HTMLDivElement>(null);

  async function handleSend(question: string) {
    // Add user message immediately
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    // Send to backend
    await sendMessage(question);
  }

  // Add assistant response
  useEffect(() => {
    if (!response) return;

    setMessages((prev) => {
      const last = prev[prev.length - 1];

      if (last?.role === "assistant") {
        return prev;
      }

      return [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: response.answer,
          response,
        },
      ];
    });
  }, [response]);

  // Auto-scroll whenever messages or loading changes
  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <div className="flex h-screen bg-gray-100">

      {/* Sidebar */}
      <Sidebar />

      {/* Main */}
      <div className="flex flex-1 flex-col">

        {/* Header */}
        <Header />

        {/* Chat Area */}
        <main className="flex flex-1 flex-col bg-gray-50">

          {/* Welcome */}
          <div className="px-8 pt-10 text-center">

            <h1 className="text-5xl font-bold">
              🤖 KnowledgeHub AI
            </h1>

            <p className="mt-3 text-lg text-gray-500">
              Ask anything about your uploaded documents.
            </p>

          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-8 py-8">

            {messages.length === 0 ? (

              <SuggestionCards />

            ) : (

              <div className="mx-auto max-w-5xl">

                <MessageList
                  messages={messages}
                  loading={loading}
                />

                {/* Auto Scroll Target */}
                <div ref={bottomRef} />

              </div>

            )}

            {error && (
              <div className="mt-8 text-center text-red-500">
                {error}
              </div>
            )}

          </div>

          {/* Chat Input */}
          <div className="border-t bg-white p-6">

            <div className="mx-auto max-w-5xl">

              <ChatInput
                onSend={handleSend}
                loading={loading}
              />

            </div>

          </div>

        </main>

      </div>

    </div>
  );
}