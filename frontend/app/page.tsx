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
        <main className="flex flex-1 items-center justify-center">
          <h1 className="text-4xl font-bold text-gray-800">
            Welcome to KnowledgeHub AI 🚀
          </h1>
        </main>

      </div>

    </div>
  );
}