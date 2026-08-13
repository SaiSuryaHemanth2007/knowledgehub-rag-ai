"use client";

import { useState } from "react";

import {
  Copy,
  Check,
  RotateCcw,
  ThumbsUp,
  ThumbsDown,
} from "lucide-react";

interface Props {
  content: string;
  onRegenerate?: () => void;
}

export default function MessageActions({
  content,
  onRegenerate,
}: Props) {
  const [copied, setCopied] = useState(false);

  async function copyMessage() {
    try {
      await navigator.clipboard.writeText(content);

      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 2000);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div
      className="
        mt-4
        flex
        items-center
        gap-2
        opacity-0
        transition-all
        duration-200
        translate-y-2
        group-hover:opacity-100
        group-hover:translate-y-0
      "
    >
      {/* Copy */}

      <button
        onClick={copyMessage}
        className="
          flex
          items-center
          gap-2
          rounded-lg
          px-3
          py-2
          text-sm
          text-gray-500
          transition
          hover:bg-gray-100
          hover:text-black
        "
      >
        {copied ? (
          <>
            <Check size={16} />
            Copied
          </>
        ) : (
          <>
            <Copy size={16} />
            Copy
          </>
        )}
      </button>

      {/* Regenerate */}

      <button
        className="
          flex
          items-center
          gap-2
          rounded-lg
          px-3
          py-2
          text-sm
          text-gray-500
          transition
          hover:bg-gray-100
          hover:text-black
        "
        onClick={onRegenerate}
      >
        <RotateCcw size={16} />

        Regenerate
      </button>

      {/* Like */}

      <button
        className="
          rounded-lg
          p-2
          text-gray-500
          transition
          hover:bg-gray-100
          hover:text-black
        "
      >
        <ThumbsUp size={16} />
      </button>

      {/* Dislike */}

      <button
        className="
          rounded-lg
          p-2
          text-gray-500
          transition
          hover:bg-gray-100
          hover:text-black
        "
      >
        <ThumbsDown size={16} />
      </button>
    </div>
  );
}