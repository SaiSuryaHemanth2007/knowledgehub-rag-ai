"use client";

import {
  useEffect,
  useMemo,
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

  // =====================================================
  // Chat Hook
  // =====================================================

  const {
    loading,
    error,
    streamMessage,
  } = useChat(
    conversationId
  );


  // =====================================================
  // Local streamed messages
  //
  // These are messages generated after the conversation
  // was loaded.
  // =====================================================

  const [
    localMessages,
    setLocalMessages,
  ] = useState<Message[]>([]);


  // =====================================================
  // Conversation ID for local streamed state
  //
  // This state is ONLY changed when the backend creates
  // a new conversation.
  // =====================================================

  const [
    streamedConversationId,
    setStreamedConversationId,
  ] = useState<number | undefined>(
    conversationId
  );


  // =====================================================
  // Messages to display
  //
  // When viewing an existing conversation, the parent
  // provides initialMessages.
  //
  // When streaming inside that conversation, localMessages
  // are appended.
  //
  // useMemo keeps the array stable for the scroll effect.
  // =====================================================

  const messages = useMemo(() => {

    // ---------------------------------------------------
    // If the selected conversation changed, discard the
    // local streamed messages from the previous chat.
    // ---------------------------------------------------

    if (
      streamedConversationId !==
      conversationId
    ) {

      return initialMessages;

    }


    return [
      ...initialMessages,
      ...localMessages,
    ];

  }, [
    conversationId,
    initialMessages,
    localMessages,
    streamedConversationId,
  ]);


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
      // -------------------------------------------------

      existingMessageId,


      // -------------------------------------------------
      // Current conversation
      // -------------------------------------------------

      conversationId,


      // -------------------------------------------------
      // Backend-created conversation
      // -------------------------------------------------

      (
        newConversationId: number
      ) => {

        setStreamedConversationId(
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
    // If this is a selected existing conversation,
    // make sure local streamed messages belong to it.
    // ---------------------------------------------------

    if (
      streamedConversationId !==
      conversationId
    ) {

      setStreamedConversationId(
        conversationId
      );

      setLocalMessages([]);

    }


    // ---------------------------------------------------
    // Add user message immediately
    // ---------------------------------------------------

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
    };


    setLocalMessages((prev) => [

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
    // Clear the existing answer.
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
    // Regenerate using the selected conversation.
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

    const bottomElement =
      document.getElementById(
        "chat-bottom"
      );

    bottomElement?.scrollIntoView({
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

              <div id="chat-bottom" />

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