"use client";

import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import ChatContainer from "@/components/chat/ChatContainer";

export default function Home() {
  return (
    <div className="flex h-screen bg-gray-100">

      <Sidebar />

      <div className="flex flex-1 flex-col">

        <Header />

        <ChatContainer />

      </div>

    </div>
  );
}