import api from "./api";


// =======================================================
// Document Type
// =======================================================

export interface Document {
  id: number;
  title: string;
  original_filename: string;
  stored_filename: string;
  file_type: string;
  file_size: number;
  status: string;
  created_at: string;
  updated_at: string;
}


// =======================================================
// Get All Documents
// =======================================================

export async function getDocuments(): Promise<
  Document[]
> {
  const response =
    await api.get<Document[]>(
      "/documents"
    );

  return response.data;
}


// =======================================================
// Get Document
// =======================================================

export async function getDocument(
  documentId: number
): Promise<Document> {
  const response =
    await api.get<Document>(
      `/documents/${documentId}`
    );

  return response.data;
}


// =======================================================
// Delete Document
// =======================================================

export async function deleteDocument(
  documentId: number
): Promise<void> {
  await api.delete(
    `/documents/${documentId}`
  );
}


// =======================================================
// Upload Document
// =======================================================

export async function uploadDocument(
  title: string,
  file: File
): Promise<Document> {

  const formData =
    new FormData();

  formData.append(
    "title",
    title
  );

  formData.append(
    "file",
    file
  );

  const response =
    await api.post<Document>(
      "/documents/upload",
      formData
    );

  return response.data;
}