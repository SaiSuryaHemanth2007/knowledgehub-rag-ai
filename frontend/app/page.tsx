"use client";

import { useState } from "react";

import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import ChatContainer from "@/components/chat/ChatContainer";

import {
  getConversationMessages,
  createConversation,
} from "@/services/conversations";

import { Message } from "@/types/message";

export default function Home() {
  // =====================================================
  // Current Conversation
  // =====================================================

  const [
    conversationId,
    setConversationId,
  ] = useState<number | undefined>(undefined);

  // =====================================================
  // Conversation Messages
  // =====================================================

  const [
    conversationMessages,
    setConversationMessages,
  ] = useState<Message[]>([]);

  // =====================================================
  // Loading Conversation
  // =====================================================

  const [
    loadingConversation,
    setLoadingConversation,
  ] = useState(false);

  // =====================================================
  // Chat Session Key
  //
  // Changes when the user selects an existing
  // conversation or creates a new chat.
  // =====================================================

  const [
    chatSessionKey,
    setChatSessionKey,
  ] = useState(0);

  // =====================================================
  // Sidebar Refresh Key
  //
  // Changes whenever a conversation is created.
  // This tells Sidebar to reload the conversations.
  // =====================================================

  const [
    conversationRefreshKey,
    setConversationRefreshKey,
  ] = useState(0);

  // =====================================================
  // Select Existing Conversation
  // =====================================================

  async function handleSelectConversation(
    id: number
  ) {
    if (id === conversationId) {
      return;
    }

    try {
      setLoadingConversation(true);

      const result =
        await getConversationMessages(id);

      const messages: Message[] =
        result.messages.map(
          (message) => ({
            id: String(message.id),
            role: message.role,
            content: message.content,
          })
        );

      // -------------------------------------------------
      // Update selected conversation
      // -------------------------------------------------

      setConversationId(id);

      // -------------------------------------------------
      // Replace conversation messages
      // -------------------------------------------------

      setConversationMessages(messages);

      // -------------------------------------------------
      // Force ChatContainer to start with this
      // conversation's messages.
      // -------------------------------------------------

      setChatSessionKey(
        (previous) => previous + 1
      );

    } catch (error) {
      console.error(
        "Failed to load conversation:",
        error
      );
    } finally {
      setLoadingConversation(false);
    }
  }

  // =====================================================
  // New Chat
  // =====================================================

  async function handleNewChat() {
    try {
      const conversation =
        await createConversation("New Chat");

      // -------------------------------------------------
      // Select newly created conversation
      // -------------------------------------------------

      setConversationId(
        conversation.id
      );

      // -------------------------------------------------
      // New conversation has no messages
      // -------------------------------------------------

      setConversationMessages([]);

      // -------------------------------------------------
      // Start a completely fresh ChatContainer
      // -------------------------------------------------

      setChatSessionKey(
        (previous) => previous + 1
      );

      // -------------------------------------------------
      // Refresh Sidebar
      // -------------------------------------------------

      setConversationRefreshKey(
        (previous) => previous + 1
      );

    } catch (error) {
      console.error(
        "Failed to create conversation:",
        error
      );
    }
  }

  // =====================================================
  // Conversation Created During Chat
  // =====================================================

  function handleConversationCreated(
    id: number
  ) {
    // -------------------------------------------------
    // Keep the current conversation ID
    // -------------------------------------------------

    setConversationId(id);

    // -------------------------------------------------
    // Refresh Sidebar
    //
    // This is important when the conversation is created
    // by the backend during the first streamed message.
    // -------------------------------------------------

    setConversationRefreshKey(
      (previous) => previous + 1
    );
  }

  // =====================================================
  // Render
  // =====================================================

  return (
    <div className="flex h-screen bg-gray-100">

      <Sidebar
        conversationId={conversationId}
        onSelectConversation={
          handleSelectConversation
        }
        onNewChat={
          handleNewChat
        }
        refreshKey={
          conversationRefreshKey
        }
      />

      <div className="flex flex-1 flex-col">

        <Header />

        <ChatContainer
          key={chatSessionKey}
          conversationId={conversationId}
          initialMessages={
            conversationMessages
          }
          loadingConversation={
            loadingConversation
          }
          onConversationCreated={
            handleConversationCreated
          }
        />

      </div>

    </div>
  );
}