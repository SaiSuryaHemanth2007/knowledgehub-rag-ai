"use client";

import { useState } from "react";

import {
  askQuestion,
  streamQuestion,
} from "@/services/chat";

import { ChatResponse } from "@/types/chat";
import { Message } from "@/types/message";


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
  // Conversation ID
  // =====================================================

  const [conversationId, setConversationId] =
    useState<number | undefined>(undefined);


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
        await askQuestion(
          question,
          conversationId
        );

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
    question: string,
    onMessage?: (
      message: Message
    ) => void,
    onUpdate?: (
      messageId: string,
      content: string,
      response?: ChatResponse
    ) => void,
    existingMessageId?: string
  ) {

    try {

      setLoading(true);
      setError(null);
      setResponse(null);
      setStreamResponse("");


      // -------------------------------------------------
      // Use existing ID for regeneration
      // or create a new ID for a new question
      // -------------------------------------------------

      const assistantMessageId =
        existingMessageId ??
        crypto.randomUUID();

      let accumulatedAnswer = "";


      // -------------------------------------------------
      // Start streaming
      // -------------------------------------------------

      await streamQuestion(

        question,

        // Current conversation
        conversationId,

        // =================================================
        // Token received
        // =================================================

        (chunk: string) => {

          accumulatedAnswer += chunk;

          setStreamResponse(
            accumulatedAnswer
          );


          // -----------------------------------------------
          // First token
          // -----------------------------------------------

          if (
            accumulatedAnswer === chunk
          ) {

            const assistantMessage: Message = {
              id: assistantMessageId,
              role: "assistant",
              content: accumulatedAnswer,
            };

            onMessage?.(
              assistantMessage
            );

          }


          // -----------------------------------------------
          // Subsequent tokens
          // -----------------------------------------------

          else {

            onUpdate?.(
              assistantMessageId,
              accumulatedAnswer
            );

          }

        },


        // =================================================
        // Stream completed
        // =================================================

        (
          sources,
          returnedConversationId
        ) => {

          const finalResponse: ChatResponse = {
            answer: accumulatedAnswer,
            sources,
          };


          // ------------------------------------------------
          // Save conversation ID returned by backend
          // ------------------------------------------------

          if (
            returnedConversationId !== undefined
          ) {

            setConversationId(
              returnedConversationId
            );

          }


          // ------------------------------------------------
          // Save complete response
          // ------------------------------------------------

          setResponse(
            finalResponse
          );


          // ------------------------------------------------
          // Attach final response + sources
          // ------------------------------------------------

          onUpdate?.(
            assistantMessageId,
            accumulatedAnswer,
            finalResponse
          );

        }

      );

    } catch (error) {

      console.error(
        "Streaming error:",
        error
      );

      setError(
        error instanceof Error
          ? error.message
          : "Failed to contact server."
      );

    } finally {

      setLoading(false);

    }

  }


  // =====================================================
  // Return
  // =====================================================

  return {

    loading,

    response,

    streamResponse,

    error,

    conversationId,

    setConversationId,

    sendMessage,

    streamMessage,

  };

}