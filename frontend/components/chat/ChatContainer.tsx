"use client";

import {
  useEffect,
  useRef,
  useState,
} from "react";

import ChatInput from "./ChatInput";
import MessageList from "./MessageList";
import SuggestionCards from "./SuggestionCards";

import { useChat } from "@/hooks/useChat";
import { Message } from "@/types/message";
import { ChatResponse } from "@/types/chat";


// =======================================================
// Props
// =======================================================

interface ChatContainerProps {
  conversationId?: number;

  initialMessages: Message[];

  loadingConversation: boolean;

  onConversationCreated: (
    conversationId: number
  ) => void;
}


// =======================================================
// Component
// =======================================================

export default function ChatContainer({
  conversationId,
  initialMessages,
  loadingConversation,
  onConversationCreated,
}: ChatContainerProps) {

  const {
    loading,
    error,
    streamMessage,
  } = useChat();


  // =====================================================
  // Local Conversation State
  // =====================================================

  const [
    localConversationId,
    setLocalConversationId,
  ] = useState<number | undefined>(
    conversationId
  );


  // =====================================================
  // Local Messages
  // =====================================================

  const [
    localMessages,
    setLocalMessages,
  ] = useState<Message[]>(
    initialMessages
  );


  // =====================================================
  // Determine Messages To Display
  // =====================================================
  //
  // If the parent selected another conversation,
  // initialMessages contains that conversation's
  // messages.
  //
  // We intentionally avoid setState inside useEffect
  // so ESLint remains clean.
  // =====================================================

  const messages =
    localConversationId === conversationId
      ? localMessages
      : initialMessages;


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

      (
        assistantMessage: Message
      ) => {

        setLocalMessages((prev) => {

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

        setLocalMessages((prev) =>
          prev.map((message) => {

            if (
              message.id === messageId
            ) {

              return {
                ...message,
                content,

                ...(response
                  ? {
                      response,
                    }
                  : {}),
              };

            }


            return message;

          })
        );

      },


      // -------------------------------------------------
      // Existing assistant message ID
      //
      // Used during regeneration.
      // -------------------------------------------------

      existingMessageId,


      // -------------------------------------------------
      // IMPORTANT:
      // Always use the conversation currently selected
      // in the Sidebar.
      // -------------------------------------------------

      conversationId,


      // -------------------------------------------------
      // Conversation created / returned
      // -------------------------------------------------

      (
        newConversationId: number
      ) => {

        setLocalConversationId(
          newConversationId
        );


        onConversationCreated(
          newConversationId
        );

      }

    );

  }


  // =====================================================
  // Send New Message
  // =====================================================

  async function handleSend(
    question: string
  ) {

    if (
      loading ||
      loadingConversation
    ) {
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


    // ---------------------------------------------------
    // Keep local conversation synchronized
    // ---------------------------------------------------

    setLocalConversationId(
      conversationId
    );


    // ---------------------------------------------------
    // Add message
    // ---------------------------------------------------

    setLocalMessages((prev) => {

      // If a different conversation was selected,
      // start with the messages loaded for that
      // conversation.
      if (
        localConversationId !==
        conversationId
      ) {

        return [
          ...initialMessages,
          userMessage,
        ];

      }


      return [
        ...prev,
        userMessage,
      ];

    });


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

    if (
      loading ||
      loadingConversation
    ) {
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


    if (
      assistantIndex === -1
    ) {
      return;
    }


    // ---------------------------------------------------
    // Find corresponding user message
    // ---------------------------------------------------

    const userMessage =
      messages[
        assistantIndex - 1
      ];


    if (
      !userMessage ||
      userMessage.role !== "user"
    ) {
      return;
    }


    const question =
      userMessage.content;


    // ---------------------------------------------------
    // Make sure local state represents the
    // currently selected conversation.
    // ---------------------------------------------------

    if (
      localConversationId !==
      conversationId
    ) {

      setLocalConversationId(
        conversationId
      );


      setLocalMessages(
        messages
      );

    }


    // ---------------------------------------------------
    // Clear old answer
    //
    // Keep the same assistant message ID
    // and same position.
    // ---------------------------------------------------

    setLocalMessages((prev) =>
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
    // Generate again using the SAME conversation
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

  }, [
    messages,
    loading,
    loadingConversation,
  ]);


  // =====================================================
  // Render
  // =====================================================

  return (
    <main className="flex flex-1 flex-col bg-gray-50 transition-all duration-500">


      {/* =================================================
          Welcome
          ================================================= */}

      {!hasMessages &&
        !loadingConversation && (

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
          Loading Conversation
          ================================================= */}

      {loadingConversation && (

        <div className="flex flex-1 items-center justify-center">

          <div className="text-gray-500">
            Loading conversation...
          </div>

        </div>

      )}


      {/* =================================================
          Messages
          ================================================= */}

      {!loadingConversation && (

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


          {/* =============================================
              Error
              ============================================= */}

          {error && (

            <div className="mt-8 text-center text-red-500">
              {error}
            </div>

          )}

        </div>

      )}


      {/* =================================================
          Input
          ================================================= */}

      <div className="border-t bg-white p-6">

        <div className="mx-auto max-w-5xl">

          <ChatInput
            onSend={handleSend}
            loading={
              loading ||
              loadingConversation
            }
          />

        </div>

      </div>

    </main>
  );
}