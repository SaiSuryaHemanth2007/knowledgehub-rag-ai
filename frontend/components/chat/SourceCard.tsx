interface SourceCardProps {
  documentTitle: string;
  filename: string;
  score: number;
  preview: string;
}

export default function SourceCard({
  documentTitle,
  filename,
  score,
  preview,
}: SourceCardProps) {
  return (
    <div className="mt-4 rounded-xl border bg-gray-50 p-4">

      <div className="flex items-center justify-between">

        <div>

          <p className="font-semibold">
            📄 {filename}
          </p>

          <p className="text-sm text-gray-500">
            {documentTitle}
          </p>

        </div>

        <div className="rounded-lg bg-green-100 px-3 py-1 text-sm font-semibold text-green-700">
          {(score * 100).toFixed(1)}%
        </div>

      </div>

      <p className="mt-3 text-sm leading-6 text-gray-600">
        {preview}
      </p>

    </div>
  );
}