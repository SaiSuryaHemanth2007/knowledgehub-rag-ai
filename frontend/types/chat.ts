export interface ChatRequest {
  question: string;
}

export interface Source {
  document_id: number;
  document_title: string;
  original_filename: string;
  chunk_index: number;
  score: number;
  preview: string;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
}