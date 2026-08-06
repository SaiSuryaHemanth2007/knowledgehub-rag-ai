"use client";

import { useEffect, useRef, useState } from "react";

import ChatInput from "./ChatInput";
import MessageList from "./MessageList";
import SuggestionCards from "./SuggestionCards";

import { useChat } from "@/hooks/useChat";
import { Message } from "@/types/message";

export default function ChatContainer() {
  const {
    loading,
    response,
    streamResponse,
    error,
    streamMessage,
  } = useChat();

  const [messages, setMessages] = useState<Message[]>([]);

  const bottomRef = useRef<HTMLDivElement>(null);

  const hasMessages = messages.length > 0;

  async function handleSend(question: string) {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    await sendMessage(question);
  }

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

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <main className="flex flex-1 flex-col bg-gray-50 transition-all duration-500">

      {!hasMessages && (
        <div className="px-8 pt-16 text-center">
          <h1 className="text-6xl font-bold">
            🤖 KnowledgeHub AI
          </h1>

          <p className="mt-4 text-xl text-gray-500">
            Ask anything about your uploaded documents.
          </p>
        </div>
      )}

      <div className="flex-1 overflow-y-auto px-8 py-8">

        {!hasMessages ? (
          <SuggestionCards />
        ) : (
          <div className="mx-auto max-w-5xl">
            <MessageList
              messages={messages}
              loading={loading}
            />

            <div ref={bottomRef} />
          </div>
        )}

        {error && (
          <div className="mt-8 text-center text-red-500">
            {error}
          </div>
        )}

      </div>

      <div className="border-t bg-white p-6">
        <div className="mx-auto max-w-5xl">
          <ChatInput
            onSend={handleSend}
            loading={loading}
          />
        </div>
      </div>

    </main>
  );
}