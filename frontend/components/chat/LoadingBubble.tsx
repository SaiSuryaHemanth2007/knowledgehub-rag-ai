import { Bot } from "lucide-react";

export default function LoadingBubble() {
  return (
    <div className="flex justify-start">
      <div className="flex max-w-3xl gap-3">

        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-zinc-800 text-white">
          <Bot size={20} />
        </div>

        <div className="rounded-2xl border bg-white px-5 py-4 shadow-sm">
          <div className="flex gap-2">

            <div className="h-2 w-2 animate-bounce rounded-full bg-gray-500"></div>

            <div
              className="h-2 w-2 animate-bounce rounded-full bg-gray-500"
              style={{ animationDelay: "150ms" }}
            ></div>

            <div
              className="h-2 w-2 animate-bounce rounded-full bg-gray-500"
              style={{ animationDelay: "300ms" }}
            ></div>

          </div>
        </div>

      </div>
    </div>
  );
}