"use client";

import { useEffect, useRef, useState } from "react";

import ChatInput from "./ChatInput";
import MessageList from "./MessageList";
import SuggestionCards from "./SuggestionCards";

import { useChat } from "@/hooks/useChat";
import { Message } from "@/types/message";
import { ChatResponse } from "@/types/chat";

export default function ChatContainer() {

  const {
    loading,
    error,
    streamMessage,
  } = useChat();


  // =====================================================
  // Chat messages
  // =====================================================

  const [messages, setMessages] =
    useState<Message[]>([]);


  const bottomRef =
    useRef<HTMLDivElement>(null);


  const hasMessages =
    messages.length > 0;


  // =====================================================
  // Start Streaming
  // =====================================================

  async function startStreaming(
    question: string,
    existingMessageId?: string
  ) {

    await streamMessage(

      question,


      // -------------------------------------------------
      // First assistant token
      // -------------------------------------------------

      (assistantMessage: Message) => {

        setMessages((prev) => {

          const exists =
            prev.some(
              (message) =>
                message.id ===
                assistantMessage.id
            );


          if (exists) {
            return prev;
          }


          return [
            ...prev,
            assistantMessage,
          ];

        });

      },


      // -------------------------------------------------
      // Update assistant message
      // -------------------------------------------------

      (
        messageId: string,
        content: string,
        response?: ChatResponse
      ) => {

        setMessages((prev) =>
          prev.map((message) => {

            if (
              message.id === messageId
            ) {

              return {
                ...message,
                content,

                ...(response
                  ? { response }
                  : {}),
              };

            }


            return message;

          })
        );

      },


      // -------------------------------------------------
      // Existing assistant message ID
      // Used during regeneration
      // -------------------------------------------------

      existingMessageId

    );

  }


  // =====================================================
  // Send New Message
  // =====================================================

  async function handleSend(
    question: string
  ) {

    if (loading) {
      return;
    }


    // ---------------------------------------------------
    // Add user message immediately
    // ---------------------------------------------------

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
    };


    setMessages((prev) => [
      ...prev,
      userMessage,
    ]);


    // ---------------------------------------------------
    // Start streaming
    // ---------------------------------------------------

    await startStreaming(
      question
    );

  }


  // =====================================================
  // Regenerate Answer
  // =====================================================

  async function handleRegenerate(
    assistantMessageId: string
  ) {

    if (loading) {
      return;
    }


    // ---------------------------------------------------
    // Find assistant message
    // ---------------------------------------------------

    const assistantIndex =
      messages.findIndex(
        (message) =>
          message.id ===
          assistantMessageId
      );


    if (assistantIndex === -1) {
      return;
    }


    // ---------------------------------------------------
    // Find corresponding user message
    // ---------------------------------------------------

    const userMessage =
      messages[assistantIndex - 1];


    if (
      !userMessage ||
      userMessage.role !== "user"
    ) {
      return;
    }


    const question =
      userMessage.content;


    // ---------------------------------------------------
    // Clear old answer
    // Keep same message ID and position
    // ---------------------------------------------------

    setMessages((prev) =>
      prev.map((message) => {

        if (
          message.id ===
          assistantMessageId
        ) {

          return {
            ...message,
            content: "",
            response: undefined,
          };

        }


        return message;

      })
    );


    // ---------------------------------------------------
    // Generate again
    //
    // useChat automatically keeps the
    // current conversation ID.
    // ---------------------------------------------------

    await startStreaming(
      question,
      assistantMessageId
    );

  }


  // =====================================================
  // Auto Scroll
  // =====================================================

  useEffect(() => {

    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages, loading]);


  // =====================================================
  // Render
  // =====================================================

  return (
    <main className="flex flex-1 flex-col bg-gray-50 transition-all duration-500">


      {/* =================================================
          Welcome
          ================================================= */}

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


      {/* =================================================
          Messages
          ================================================= */}

      <div className="flex-1 overflow-y-auto px-8 py-8">

        {!hasMessages ? (

          <SuggestionCards />

        ) : (

          <div className="mx-auto max-w-5xl">

            <MessageList
              messages={messages}
              loading={loading}
              onRegenerate={
                handleRegenerate
              }
            />

            <div ref={bottomRef} />

          </div>

        )}


        {/* =================================================
            Error
            ================================================= */}

        {error && (

          <div className="mt-8 text-center text-red-500">
            {error}
          </div>

        )}

      </div>


      {/* =================================================
          Input
          ================================================= */}

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