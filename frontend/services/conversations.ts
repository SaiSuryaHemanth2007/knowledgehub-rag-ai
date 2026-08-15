import api from "./api";

import {
  Conversation,
  ConversationListResponse,
  MessageListResponse,
} from "@/types/conversation";


// =======================================================
// Get all conversations
// =======================================================

export async function getConversations(): Promise<
  Conversation[]
> {
  const response =
    await api.get<ConversationListResponse>(
      "/conversations"
    );

  return response.data.conversations;
}


// =======================================================
// Create conversation
// =======================================================

export async function createConversation(
  title: string = "New Chat"
): Promise<Conversation> {

  const response =
    await api.post<Conversation>(
      "/conversations",
      {
        title,
      }
    );

  return response.data;
}


// =======================================================
// Get conversation messages
// =======================================================

export async function getConversationMessages(
  conversationId: number
): Promise<MessageListResponse> {

  const response =
    await api.get<MessageListResponse>(
      `/conversations/${conversationId}/messages`
    );

  return response.data;
}


// =======================================================
// Delete conversation
// =======================================================

export async function deleteConversation(
  conversationId: number
): Promise<void> {

  await api.delete(
    `/conversations/${conversationId}`
  );
}