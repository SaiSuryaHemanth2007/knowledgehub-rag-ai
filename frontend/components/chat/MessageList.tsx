import ChatBubble from "./ChatBubble";
import LoadingBubble from "./LoadingBubble";

import { Message } from "@/types/message";

interface MessageListProps {
  messages: Message[];
  loading?: boolean;
}

export default function MessageList({
  messages,
  loading = false,
}: MessageListProps) {
  return (
    <div className="flex flex-col gap-6">

      {messages.map((message) => (
        <ChatBubble
            key={message.id}
            message={message}
        />
      ))}

      {loading && <LoadingBubble />}

    </div>
  );
}