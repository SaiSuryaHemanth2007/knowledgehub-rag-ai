import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";

export default function Home() {
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex flex-1 flex-col">
        {/* Header */}
        <Header />

        {/* Content */}
        <main className="flex flex-1 items-center justify-center bg-gray-50">
          <div className="text-center">
            <h1 className="mb-4 text-5xl font-bold">
              👋 Welcome to KnowledgeHub AI
            </h1>

            <p className="text-lg text-gray-500">
              Ask anything about your uploaded documents.
            </p>
          </div>
        </main>
      </div>
    </div>
  );
}