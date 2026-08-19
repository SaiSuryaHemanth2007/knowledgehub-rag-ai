interface SourceCardProps {
  documentTitle: string;
  filename: string;
  chunkIndex: number;
  score: number;
  preview: string;
}

export default function SourceCard({
  documentTitle,
  filename,
  chunkIndex,
  score,
  preview,
}: SourceCardProps) {
  return (
    <div className="mt-4 rounded-xl border bg-gray-50 p-4">

      {/* =================================================
          Source Header
          ================================================= */}

      <div className="flex items-start justify-between gap-4">

        <div className="min-w-0">

          <p
            className="truncate font-semibold text-gray-900"
            title={filename}
          >
            📄 {filename}
          </p>

          <p
            className="mt-1 truncate text-sm text-gray-500"
            title={documentTitle}
          >
            {documentTitle}
          </p>

        </div>


        {/* Similarity Score */}

        <div className="shrink-0 rounded-lg bg-green-100 px-3 py-1 text-sm font-semibold text-green-700">
          {(score * 100).toFixed(1)}%
        </div>

      </div>


      {/* =================================================
          Source Metadata
          ================================================= */}

      <div className="mt-3 flex items-center gap-2 text-xs text-gray-500">

        <span className="rounded-md bg-white px-2 py-1">
          Chunk {chunkIndex}
        </span>

        <span>
          Semantic similarity
        </span>

      </div>


      {/* =================================================
          Preview
          ================================================= */}

      <p className="mt-3 text-sm leading-6 text-gray-600">
        {preview}
      </p>

    </div>
  );
}