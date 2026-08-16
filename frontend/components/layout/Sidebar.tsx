"use client";

import {
  MessageSquare,
  Upload,
  Files,
  Settings,
  Plus,
} from "lucide-react";

import {
  useCallback,
  useEffect,
  useState,
} from "react";

import api from "@/services/api";

interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
}

interface ConversationListResponse {
  conversations: Conversation[];
}

interface SidebarProps {
  conversationId?: number;

  onSelectConversation?: (
    conversationId: number
  ) => void;

  onNewChat?: () => void;

  refreshKey?: number;
}

const menuItems = [
  {
    title: "Chat",
    icon: MessageSquare,
  },
  {
    title: "Upload",
    icon: Upload,
  },
  {
    title: "Documents",
    icon: Files,
  },
  {
    title: "Settings",
    icon: Settings,
  },
];

export default function Sidebar({
  conversationId,
  onSelectConversation,
  onNewChat,
  refreshKey,
}: SidebarProps) {
  const [conversations, setConversations] =
    useState<Conversation[]>([]);

  const [loading, setLoading] =
    useState(false);

  // =====================================================
  // Load Conversations
  // =====================================================

  const loadConversations =
    useCallback(async () => {
      try {
        setLoading(true);

        const response =
          await api.get<ConversationListResponse>(
            "/conversations"
          );

        setConversations(
          response.data.conversations
        );
      } catch (error) {
        console.error(
          "Failed to load conversations:",
          error
        );
      } finally {
        setLoading(false);
      }
    }, []);

  // =====================================================
  // Initial Load
  // =====================================================

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void loadConversations();
    }, 0);

    return () => {
      window.clearTimeout(timer);
    };
  }, [loadConversations, refreshKey]);

  // =====================================================
  // Render
  // =====================================================

  return (
    <aside className="flex h-screen w-72 flex-col border-r bg-white shadow-sm">

      {/* =================================================
          Header
          ================================================= */}

      <div className="border-b p-6">
        <h1 className="text-2xl font-bold">
          KnowledgeHub
        </h1>
      </div>


      {/* =================================================
          Main Navigation
          ================================================= */}

      <nav className="border-b p-4">

        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.title}
              className="mb-2 flex w-full items-center gap-3 rounded-lg p-3 transition hover:bg-gray-100"
            >
              <Icon size={20} />

              <span>
                {item.title}
              </span>
            </button>
          );
        })}

      </nav>


      {/* =================================================
          Conversations
          ================================================= */}

      <div className="flex min-h-0 flex-1 flex-col">

        {/* Conversation Header */}

        <div className="flex items-center justify-between border-b px-4 py-3">

          <h2 className="text-sm font-semibold text-gray-700">
            Conversations
          </h2>

          <button
            onClick={onNewChat}
            className="rounded-lg p-2 transition hover:bg-gray-100"
            title="New Chat"
          >
            <Plus size={18} />
          </button>

        </div>


        {/* Conversation List */}

        <div className="flex-1 overflow-y-auto p-3">

          {loading && (
            <p className="px-2 py-3 text-sm text-gray-400">
              Loading conversations...
            </p>
          )}


          {!loading &&
            conversations.length === 0 && (
              <p className="px-2 py-3 text-sm text-gray-400">
                No conversations yet.
              </p>
            )}


          {!loading &&
            conversations.map(
              (conversation) => {

                const isActive =
                  conversation.id ===
                  conversationId;

                return (
                  <button
                    key={conversation.id}
                    onClick={() =>
                      onSelectConversation?.(
                        conversation.id
                      )
                    }
                    className={`mb-1 w-full rounded-lg px-3 py-2 text-left text-sm transition ${
                      isActive
                        ? "bg-gray-100 font-medium text-gray-900"
                        : "text-gray-600 hover:bg-gray-50"
                    }`}
                  >
                    <div className="truncate">
                      {conversation.title}
                    </div>
                  </button>
                );
              }
            )}

        </div>

      </div>

    </aside>
  );
}