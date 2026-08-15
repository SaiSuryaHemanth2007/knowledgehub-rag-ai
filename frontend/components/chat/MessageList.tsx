import ChatBubble from "./ChatBubble";
import LoadingBubble from "./LoadingBubble";

import { Message } from "@/types/message";

interface MessageListProps {
  messages: Message[];
  loading?: boolean;
  onRegenerate?: (
    messageId: string
  ) => void;
}

export default function MessageList({
  messages,
  loading = false,
  onRegenerate,
}: MessageListProps) {
  return (
    <div className="flex flex-col gap-6">

      {messages.map((message) => (
        <ChatBubble
          key={message.id}
          message={message}
          onRegenerate={onRegenerate}
        />
      ))}

      {loading && <LoadingBubble />}

    </div>
  );
}