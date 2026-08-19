"use client";

import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  FileText,
  Trash2,
  RefreshCw,
  Upload,
} from "lucide-react";

import {
  useRouter,
} from "next/navigation";

import {
  deleteDocument,
  getDocuments,
  Document,
} from "@/services/documents";


export default function DocumentsPage() {

  const router = useRouter();

  // =====================================================
  // Documents
  // =====================================================

  const [
    documents,
    setDocuments,
  ] = useState<Document[]>([]);


  // =====================================================
  // Loading
  // =====================================================

  const [
    loading,
    setLoading,
  ] = useState(true);


  // =====================================================
  // Error
  // =====================================================

  const [
    error,
    setError,
  ] = useState<string | null>(null);


  // =====================================================
  // Deleting
  // =====================================================

  const [
    deletingId,
    setDeletingId,
  ] = useState<number | null>(null);


  // =====================================================
  // Load Documents
  // =====================================================

  const loadDocuments =
    useCallback(async () => {

      try {

        setLoading(true);
        setError(null);

        const result =
          await getDocuments();

        setDocuments(result);

      } catch (error) {

        console.error(
          "Failed to load documents:",
          error
        );

        setError(
          error instanceof Error
            ? error.message
            : "Failed to load documents."
        );

      } finally {

        setLoading(false);

      }

    }, []);


  // =====================================================
  // Initial Load
  // =====================================================

  useEffect(() => {

    const timer =
      window.setTimeout(() => {
        void loadDocuments();
      }, 0);

    return () => {
      window.clearTimeout(timer);
    };

  }, [loadDocuments]);


  // =====================================================
  // Delete Document
  // =====================================================

  async function handleDelete(
    documentId: number,
    title: string
  ) {

    const confirmed =
      window.confirm(
        `Are you sure you want to delete "${title}"? This will also remove its stored chunks and embeddings.`
      );

    if (!confirmed) {
      return;
    }

    try {

      setDeletingId(documentId);
      setError(null);

      await deleteDocument(
        documentId
      );

      setDocuments(
        (currentDocuments) =>
          currentDocuments.filter(
            (document) =>
              document.id !== documentId
          )
      );

    } catch (error) {

      console.error(
        "Failed to delete document:",
        error
      );

      setError(
        error instanceof Error
          ? error.message
          : "Failed to delete document."
      );

    } finally {

      setDeletingId(null);

    }

  }


  // =====================================================
  // Format File Size
  // =====================================================

  function formatFileSize(
    bytes: number
  ): string {

    if (bytes < 1024) {
      return `${bytes} B`;
    }

    if (bytes < 1024 * 1024) {
      return `${(
        bytes / 1024
      ).toFixed(1)} KB`;
    }

    return `${(
      bytes /
      (1024 * 1024)
    ).toFixed(1)} MB`;

  }


  // =====================================================
  // Format Date
  // =====================================================

  function formatDate(
    date: string
  ): string {

    return new Date(
      date
    ).toLocaleDateString(
      undefined,
      {
        year: "numeric",
        month: "short",
        day: "numeric",
      }
    );

  }


  // =====================================================
  // Render
  // =====================================================

  return (
    <main className="min-h-screen bg-gray-100">

      {/* =================================================
          Header
          ================================================= */}

      <div className="border-b bg-white px-8 py-6">

        <div className="flex items-center justify-between">

          <div>

            <h1 className="text-2xl font-bold text-gray-900">
              Documents
            </h1>

            <p className="mt-1 text-sm text-gray-500">
              Manage your uploaded knowledge documents.
            </p>

          </div>


          <div className="flex items-center gap-3">

            {/* Refresh */}

            <button
              onClick={() =>
                void loadDocuments()
              }
              disabled={loading}
              className="flex items-center gap-2 rounded-lg border bg-white px-4 py-2 text-sm font-medium transition hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
            >

              <RefreshCw
                size={16}
                className={
                  loading
                    ? "animate-spin"
                    : ""
                }
              />

              Refresh

            </button>


            {/* Upload */}

            <button
              onClick={() =>
                router.push("/upload")
              }
              className="flex items-center gap-2 rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-gray-800"
            >

              <Upload
                size={16}
              />

              Upload Document

            </button>

          </div>

        </div>

      </div>


      {/* =================================================
          Content
          ================================================= */}

      <div className="p-8">

        {/* Document Count */}

        {!loading &&
          documents.length > 0 && (

            <div className="mb-4 text-sm text-gray-500">
              {documents.length}{" "}
              {documents.length === 1
                ? "document"
                : "documents"}
            </div>

          )}


        {/* Error */}

        {error && (

          <div className="mb-6 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>

        )}


        {/* Loading */}

        {loading && (

          <div className="rounded-xl border bg-white p-8 text-center text-sm text-gray-500">
            Loading documents...
          </div>

        )}


        {/* Empty State */}

        {!loading &&
          documents.length === 0 && (

            <div className="rounded-xl border bg-white p-12 text-center">

              <FileText
                size={40}
                className="mx-auto text-gray-400"
              />

              <h2 className="mt-4 text-lg font-semibold text-gray-900">
                No documents yet
              </h2>

              <p className="mt-2 text-sm text-gray-500">
                Upload a document to start building your knowledge base.
              </p>

              <button
                onClick={() =>
                  router.push("/upload")
                }
                className="mx-auto mt-6 flex items-center gap-2 rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-gray-800"
              >

                <Upload
                  size={16}
                />

                Upload Document

              </button>

            </div>

          )}


        {/* Document List */}

        {!loading &&
          documents.length > 0 && (

            <div className="overflow-hidden rounded-xl border bg-white">

              {/* Table Header */}

              <div className="grid grid-cols-[2fr_1.5fr_1fr_1fr_1fr_auto] gap-4 border-b bg-gray-50 px-6 py-3 text-xs font-semibold uppercase tracking-wide text-gray-500">

                <span>
                  Document
                </span>

                <span>
                  Filename
                </span>

                <span>
                  Type
                </span>

                <span>
                  Size
                </span>

                <span>
                  Uploaded
                </span>

                <span>
                  Action
                </span>

              </div>


              {/* Documents */}

              {documents.map(
                (document) => {

                  const isDeleting =
                    deletingId ===
                    document.id;

                  return (

                    <div
                      key={document.id}
                      className="grid grid-cols-[2fr_1.5fr_1fr_1fr_1fr_auto] items-center gap-4 border-b px-6 py-4 last:border-b-0"
                    >

                      {/* Document */}

                      <div className="flex min-w-0 items-center gap-3">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-gray-100">

                          <FileText
                            size={20}
                            className="text-gray-600"
                          />

                        </div>

                        <div className="min-w-0">

                          <p className="truncate text-sm font-medium text-gray-900">
                            {document.title}
                          </p>

                          <p className="text-xs text-gray-500">
                            ID: {document.id}
                          </p>

                        </div>

                      </div>


                      {/* Filename */}

                      <p
                        className="truncate text-sm text-gray-600"
                        title={
                          document.original_filename
                        }
                      >
                        {document.original_filename}
                      </p>


                      {/* Type */}

                      <p
                        className="truncate text-sm text-gray-600"
                        title={
                          document.file_type
                        }
                      >
                        {document.file_type}
                      </p>


                      {/* Size */}

                      <p className="text-sm text-gray-600">
                        {formatFileSize(
                          document.file_size
                        )}
                      </p>


                      {/* Uploaded */}

                      <p className="text-sm text-gray-600">
                        {formatDate(
                          document.created_at
                        )}
                      </p>


                      {/* Delete */}

                      <button
                        onClick={() =>
                          void handleDelete(
                            document.id,
                            document.title
                          )
                        }
                        disabled={isDeleting}
                        className="rounded-lg p-2 text-gray-500 transition hover:bg-red-50 hover:text-red-600 disabled:cursor-not-allowed disabled:opacity-50"
                        title="Delete document"
                      >

                        <Trash2
                          size={18}
                        />

                      </button>

                    </div>

                  );

                }
              )}

            </div>

          )}

      </div>

    </main>
  );
}