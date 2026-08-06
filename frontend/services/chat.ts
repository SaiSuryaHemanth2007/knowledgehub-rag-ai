import api from "./api";
import { ChatRequest, ChatResponse } from "@/types/chat";

export async function askQuestion(
  question: string
): Promise<ChatResponse> {
  const payload: ChatRequest = {
    question,
  };

  const response = await api.post<ChatResponse>(
    "/chat",
    payload
  );

  return response.data;
}