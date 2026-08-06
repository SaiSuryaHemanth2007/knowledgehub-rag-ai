import { User, Bot } from "lucide-react";

import { Message } from "@/types/message";
import MarkdownRenderer from "./MarkdownRenderer";
import SourceCard from "./SourceCard";
import MessageActions from "./MessageActions";

interface ChatBubbleProps {
  message: Message;
}

export default function ChatBubble({
  message,
}: ChatBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`flex max-w-4xl gap-3 ${
          isUser ? "flex-row-reverse" : ""
        }`}
      >
        {/* Avatar */}
        <div
          className={`flex h-10 w-10 items-center justify-center rounded-full ${
            isUser
              ? "bg-blue-600 text-white"
              : "bg-zinc-800 text-white"
          }`}
        >
          {isUser ? (
            <User size={18} />
          ) : (
            <Bot size={18} />
          )}
        </div>

        {/* Message Bubble */}
        <div
            className={`group rounded-2xl px-5 py-4 shadow-sm ${
                isUser
                    ? "bg-blue-600 text-white"
                    : "border border-gray-200 bg-white"
                }`}
        >
          {/* Message Content */}
          {isUser ? (
            <p className="whitespace-pre-wrap leading-7">
              {message.content}
            </p>
          ) : (
            <>
              <MarkdownRenderer
                content={message.content}
              />

              {/* Message Actions */}
              <MessageActions
                content={message.content}
                onRegenerate={() =>
                    console.log("Regenerate")
                }
              />

              {/* Source Citations */}
              {message.response?.sources.map(
                (source, index) => (
                  <SourceCard
                    key={index}
                    documentTitle={
                      source.document_title
                    }
                    filename={
                      source.original_filename
                    }
                    score={source.score}
                    preview={source.preview}
                  />
                )
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}