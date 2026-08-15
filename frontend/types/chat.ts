// =======================================================
// Source Response
// =======================================================

export interface SourceResponse {
  document_id: number;

  document_title: string;

  original_filename: string;

  chunk_index: number;

  score: number;

  preview: string;
}


// =======================================================
// Chat Request
// =======================================================

export interface ChatRequest {
  question: string;

  conversation_id?: number;
}


// =======================================================
// Chat Response
// =======================================================

export interface ChatResponse {
  answer: string;

  sources: SourceResponse[];

  conversation_id?: number;
}