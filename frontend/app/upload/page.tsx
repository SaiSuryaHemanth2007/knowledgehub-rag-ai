"use client";

import {
  ChangeEvent,
  useState,
} from "react";

import {
  FileText,
  Upload,
  CheckCircle2,
  AlertCircle,
} from "lucide-react";

import {
  uploadDocument,
} from "@/services/documents";


export default function UploadPage() {

  // =====================================================
  // Form State
  // =====================================================

  const [
    title,
    setTitle,
  ] = useState("");

  const [
    file,
    setFile,
  ] = useState<File | null>(null);


  // =====================================================
  // Upload State
  // =====================================================

  const [
    uploading,
    setUploading,
  ] = useState(false);


  // =====================================================
  // Result State
  // =====================================================

  const [
    success,
    setSuccess,
  ] = useState<string | null>(null);

  const [
    error,
    setError,
  ] = useState<string | null>(null);


  // =====================================================
  // File Selection
  // =====================================================

  function handleFileChange(
    event: ChangeEvent<HTMLInputElement>
  ) {
    const selectedFile =
      event.target.files?.[0] ?? null;

    setFile(selectedFile);

    setSuccess(null);
    setError(null);

    // Automatically use the filename as the title
    // when the title field is empty.

    if (
      selectedFile &&
      !title.trim()
    ) {
      const filename =
        selectedFile.name;

      const lastDot =
        filename.lastIndexOf(".");

      const filenameWithoutExtension =
        lastDot > 0
          ? filename.substring(
              0,
              lastDot
            )
          : filename;

      setTitle(
        filenameWithoutExtension
      );
    }
  }


  // =====================================================
  // Upload
  // =====================================================

  async function handleUpload() {

    setSuccess(null);
    setError(null);

    // ---------------------------------------------------
    // Validate title
    // ---------------------------------------------------

    if (!title.trim()) {
      setError(
        "Please enter a document title."
      );

      return;
    }

    // ---------------------------------------------------
    // Validate file
    // ---------------------------------------------------

    if (!file) {
      setError(
        "Please select a document to upload."
      );

      return;
    }

    try {
      setUploading(true);

      const uploadedDocument =
        await uploadDocument(
          title.trim(),
          file
        );

      setSuccess(
        `"${uploadedDocument.title}" uploaded successfully.`
      );

      // -------------------------------------------------
      // Clear form after successful upload
      // -------------------------------------------------

      setTitle("");
      setFile(null);

      // -------------------------------------------------
      // Reset file input
      // -------------------------------------------------

      const fileInput =
        document.getElementById(
          "document-file"
        ) as HTMLInputElement | null;

      if (fileInput) {
        fileInput.value = "";
      }

    } catch (error) {

      console.error(
        "Document upload failed:",
        error
      );

      setError(
        error instanceof Error
          ? error.message
          : "Failed to upload document."
      );

    } finally {
      setUploading(false);
    }
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

        <h1 className="text-2xl font-bold text-gray-900">
          Upload Document
        </h1>

        <p className="mt-1 text-sm text-gray-500">
          Add a document to your KnowledgeHub
          knowledge base.
        </p>

      </div>


      {/* =================================================
          Content
          ================================================= */}

      <div className="p-8">

        <div className="mx-auto max-w-2xl">

          <div className="rounded-xl border bg-white p-8 shadow-sm">

            {/* =================================================
                Document Title
                ================================================= */}

            <div>

              <label
                htmlFor="document-title"
                className="mb-2 block text-sm font-medium text-gray-700"
              >
                Document Title
              </label>

              <input
                id="document-title"
                type="text"
                value={title}
                onChange={(event) =>
                  setTitle(
                    event.target.value
                  )
                }
                placeholder="Enter document title"
                disabled={uploading}
                className="w-full rounded-lg border px-4 py-3 text-sm outline-none transition focus:border-gray-400 focus:ring-2 focus:ring-gray-200 disabled:bg-gray-100"
              />

            </div>


            {/* =================================================
                File Selection
                ================================================= */}

            <div className="mt-6">

              <label
                htmlFor="document-file"
                className="mb-2 block text-sm font-medium text-gray-700"
              >
                Document File
              </label>

              <label
                htmlFor="document-file"
                className="flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-gray-300 px-6 py-10 transition hover:border-gray-400 hover:bg-gray-50"
              >

                <Upload
                  size={32}
                  className="text-gray-400"
                />

                <p className="mt-3 text-sm font-medium text-gray-700">
                  Choose a document
                </p>

                <p className="mt-1 text-xs text-gray-500">
                  Click here to select a file
                </p>

                <input
                  id="document-file"
                  type="file"
                  onChange={
                    handleFileChange
                  }
                  disabled={uploading}
                  className="hidden"
                />

              </label>


              {/* =================================================
                  Selected File
                  ================================================= */}

              {file && (

                <div className="mt-4 flex items-center gap-3 rounded-lg bg-gray-50 px-4 py-3">

                  <FileText
                    size={20}
                    className="shrink-0 text-gray-500"
                  />

                  <div className="min-w-0">

                    <p className="truncate text-sm font-medium text-gray-800">
                      {file.name}
                    </p>

                    <p className="text-xs text-gray-500">
                      {(
                        file.size /
                        (1024 * 1024)
                      ).toFixed(2)}{" "}
                      MB
                    </p>

                  </div>

                </div>

              )}

            </div>


            {/* =================================================
                Success Message
                ================================================= */}

            {success && (

              <div className="mt-6 flex items-start gap-3 rounded-lg border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">

                <CheckCircle2
                  size={20}
                  className="mt-0.5 shrink-0"
                />

                <p>
                  {success}
                </p>

              </div>

            )}


            {/* =================================================
                Error Message
                ================================================= */}

            {error && (

              <div className="mt-6 flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">

                <AlertCircle
                  size={20}
                  className="mt-0.5 shrink-0"
                />

                <p>
                  {error}
                </p>

              </div>

            )}


            {/* =================================================
                Upload Button
                ================================================= */}

            <button
              type="button"
              onClick={() =>
                void handleUpload()
              }
              disabled={uploading}
              className="mt-6 flex w-full items-center justify-center gap-2 rounded-lg bg-gray-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
            >

              <Upload
                size={18}
              />

              {uploading
                ? "Uploading..."
                : "Upload Document"}

            </button>

          </div>

        </div>

      </div>

    </main>
  );
}