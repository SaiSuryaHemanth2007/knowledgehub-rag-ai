"use client";

import { useState } from "react";

import {
  askQuestion,
  streamQuestion,
} from "@/services/chat";

import { ChatResponse } from "@/types/chat";
import { Message } from "@/types/message";


// =======================================================
// Hook
// =======================================================

export function useChat(
  initialConversationId?: number
) {

  // =====================================================
  // Loading
  // =====================================================

  const [loading, setLoading] =
    useState(false);


  // =====================================================
  // Response
  // =====================================================

  const [response, setResponse] =
    useState<ChatResponse | null>(null);


  // =====================================================
  // Streaming Response
  // =====================================================

  const [streamResponse, setStreamResponse] =
    useState("");


  // =====================================================
  // Error
  // =====================================================

  const [error, setError] =
    useState<string | null>(null);


  // =====================================================
  // Current Conversation ID
  // =====================================================

  const [conversationId, setConversationId] =
    useState<number | undefined>(
      initialConversationId
    );


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


      setResponse(
        result
      );

    } catch (error) {

      console.error(
        "Chat error:",
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

    existingMessageId?: string,

    currentConversationId?: number,

    onConversationCreated?: (
      conversationId: number
    ) => void
  ) {

    try {

      setLoading(true);
      setError(null);
      setResponse(null);
      setStreamResponse("");


      // -------------------------------------------------
      // Existing assistant ID during regeneration
      // or create a new temporary frontend ID.
      // -------------------------------------------------

      const assistantMessageId =
        existingMessageId ??
        crypto.randomUUID();


      let accumulatedAnswer = "";


      // -------------------------------------------------
      // IMPORTANT:
      //
      // Use the conversation ID supplied by
      // ChatContainer when one is available.
      //
      // This prevents an old conversation ID from
      // being reused after selecting another chat.
      // -------------------------------------------------

      const activeConversationId =
        currentConversationId ??
        conversationId;


      // =================================================
      // Start Streaming
      // =================================================

      await streamQuestion(

        question,

        activeConversationId,


        // =================================================
        // Token received
        // =================================================

        (chunk: string) => {

          accumulatedAnswer +=
            chunk;


          setStreamResponse(
            accumulatedAnswer
          );


          // ------------------------------------------------
          // First token
          // ------------------------------------------------

          if (
            accumulatedAnswer ===
            chunk
          ) {

            const assistantMessage: Message = {
              id:
                assistantMessageId,

              role:
                "assistant",

              content:
                accumulatedAnswer,
            };


            onMessage?.(
              assistantMessage
            );

          }


          // ------------------------------------------------
          // Subsequent tokens
          // ------------------------------------------------

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
            answer:
              accumulatedAnswer,

            sources,
          };


          // ------------------------------------------------
          // Backend returned a conversation ID
          // ------------------------------------------------

          if (
            returnedConversationId !==
            undefined
          ) {

            // Save inside the hook.
            setConversationId(
              returnedConversationId
            );


            // Tell ChatContainer.
            onConversationCreated?.(
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