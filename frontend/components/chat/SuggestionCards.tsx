const suggestions = [
  "Summarize this PDF",
  "Explain this document",
  "Generate study notes",
  "Find important topics",
];

export default function SuggestionCards() {
  return (
    <div className="mt-8 flex flex-wrap justify-center gap-4">
      {suggestions.map((item) => (
        <button
          key={item}
          className="rounded-xl border bg-white px-5 py-3 shadow-sm transition hover:bg-gray-100"
        >
          {item}
        </button>
      ))}
    </div>
  );
}