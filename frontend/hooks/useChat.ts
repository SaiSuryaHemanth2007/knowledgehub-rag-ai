"use client";

import { useState } from "react";

import {
  askQuestion,
  streamQuestion,
} from "@/services/chat";

import { ChatResponse } from "@/types/chat";

export function useChat() {

  const [loading, setLoading] =
    useState(false);

  const [response, setResponse] =
    useState<ChatResponse | null>(null);

  const [streamResponse, setStreamResponse] =
    useState("");

  const [error, setError] =
    useState<string | null>(null);


  // =====================================================
  // Normal Chat
  // =====================================================

  async function sendMessage(
    question: string
  ) {

    try {

      setLoading(true);
      setError(null);
      setResponse(null);

      const result =
        await askQuestion(question);

      setResponse(result);

    } catch {

      setError(
        "Failed to contact server."
      );

    } finally {

      setLoading(false);

    }
  }


  // =====================================================
  // Streaming Chat
  // =====================================================

  async function streamMessage(
    question: string
  ) {

    try {

      setLoading(true);
      setError(null);

      setStreamResponse("");

      await streamQuestion(
        question,
        (chunk: string) => {

          setStreamResponse(
            (prev) =>
              prev + chunk
          );

        }
      );

    } catch {

      setError(
        "Failed to contact server."
      );

    } finally {

      setLoading(false);

    }
  }


  return {
    loading,
    response,
    streamResponse,
    error,
    sendMessage,
    streamMessage,
  };
}