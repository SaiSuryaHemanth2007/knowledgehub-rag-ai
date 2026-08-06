"use client";

import { useState } from "react";
import { Send } from "lucide-react";

interface ChatInputProps {
  onSend: (question: string) => void;
  loading?: boolean;
}

export default function ChatInput({
  onSend,
  loading = false,
}: ChatInputProps) {
  const [question, setQuestion] = useState("");

  function handleSend() {
    if (!question.trim()) return;

    onSend(question);
    setQuestion("");
  }

  function handleKeyDown(
    e: React.KeyboardEvent<HTMLInputElement>
  ) {
    if (e.key === "Enter") {
      handleSend();
    }
  }

  return (
    <div className="mt-10 flex justify-center">
      <div className="flex w-full max-w-4xl rounded-3xl border bg-white shadow-sm">
        <input
          type="text"
          placeholder="Ask anything about your documents..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          className="flex-1 rounded-l-3xl px-6 py-5 text-lg outline-none"
          disabled={loading}
        />

        <button
          onClick={handleSend}
          disabled={loading}
          className="m-3 rounded-2xl bg-black p-4 text-white transition hover:bg-gray-800 disabled:opacity-50"
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
}