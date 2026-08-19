import { User, Bot } from "lucide-react";

import { Message } from "@/types/message";

import MarkdownRenderer from "./MarkdownRenderer";
import SourceCard from "./SourceCard";
import MessageActions from "./MessageActions";


interface ChatBubbleProps {
  message: Message;

  onRegenerate?: (
    messageId: string
  ) => void;
}


export default function ChatBubble({
  message,
  onRegenerate,
}: ChatBubbleProps) {

  const isUser =
    message.role === "user";


  return (
    <div
      className={`flex ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >

      <div
        className={`flex max-w-4xl gap-3 ${
          isUser
            ? "flex-row-reverse"
            : ""
        }`}
      >

        {/* =================================================
            Avatar
            ================================================= */}

        <div
          className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full ${
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


        {/* =================================================
            Message Bubble
            ================================================= */}

        <div
          className={`group rounded-2xl px-5 py-4 shadow-sm ${
            isUser
              ? "bg-blue-600 text-white"
              : "border border-gray-200 bg-white"
          }`}
        >

          {/* =================================================
              User Message
              ================================================= */}

          {isUser ? (

            <p className="whitespace-pre-wrap leading-7">
              {message.content}
            </p>

          ) : (

            <>

              {/* =================================================
                  Assistant Answer
                  ================================================= */}

              <MarkdownRenderer
                content={message.content}
              />


              {/* =================================================
                  Message Actions
                  ================================================= */}

              <MessageActions
                content={message.content}
                onRegenerate={() => {

                  onRegenerate?.(
                    message.id
                  );

                }}
              />


              {/* =================================================
                  Retrieved Sources
                  ================================================= */}

              {message.response?.sources &&
                message.response.sources.length > 0 && (

                  <div className="mt-4">

                    <p className="mb-2 text-sm font-semibold text-gray-700">
                      Sources
                    </p>

                    {message.response.sources.map(
                      (source, index) => (

                        <SourceCard
                          key={`${source.document_id}-${source.chunk_index}-${index}`}
                          documentTitle={
                            source.document_title
                          }
                          filename={
                            source.original_filename
                          }
                          chunkIndex={
                            source.chunk_index
                          }
                          score={
                            source.score
                          }
                          preview={
                            source.preview
                          }
                        />

                      )
                    )}

                  </div>

                )}

            </>

          )}

        </div>

      </div>

    </div>
  );
}