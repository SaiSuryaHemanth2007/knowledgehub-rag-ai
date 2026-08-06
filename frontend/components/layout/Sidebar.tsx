export default function Sidebar() {
  return (
    <aside className="h-screen w-72 border-r bg-white p-6 shadow-sm">

      <h2 className="mb-8 text-2xl font-bold">
        KnowledgeHub
      </h2>

      <nav className="space-y-4">

        <button className="block w-full rounded-lg p-3 text-left hover:bg-gray-100">
          💬 Chat
        </button>

        <button className="block w-full rounded-lg p-3 text-left hover:bg-gray-100">
          📄 Upload
        </button>

        <button className="block w-full rounded-lg p-3 text-left hover:bg-gray-100">
          📚 Documents
        </button>

        <button className="block w-full rounded-lg p-3 text-left hover:bg-gray-100">
          ⚙ Settings
        </button>

      </nav>

    </aside>
  );
}