export default function Header() {
  return (
    <header className="flex h-16 items-center justify-between border-b bg-white px-6 shadow-sm">

      <h1 className="text-xl font-bold">
        KnowledgeHub AI
      </h1>

      <div className="flex items-center gap-4">
        <button className="text-xl">🌙</button>
        <button className="text-xl">👤</button>
      </div>

    </header>
  );
}