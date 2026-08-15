class PromptBuilder:
    """
    Builds prompts for the language model.

    The prompt contains:
        1. Conversation history
        2. Retrieved document context
        3. Current question
    """

    SYSTEM_PROMPT = """
You are KnowledgeHub AI, an AI assistant that answers questions using uploaded documents and the conversation history.

Rules:

- Answer using the provided document context.
- Use conversation history to understand references such as "it", "they", "this", "that", "the device", or similar follow-up references.
- The retrieved document context is the primary source of truth.
- Do NOT invent facts.
- If the answer is not present in the document context, respond:
  "I don't have enough information in the uploaded document."
- If the context is incomplete, say so.
- Keep answers clear, concise, and accurate.
- Use bullet points when appropriate.
""".strip()

    def build(
        self,
        context: str,
        question: str,
        history: list | None = None,
    ) -> tuple[str, str]:
        """
        Build system and user prompts.
        """

        history_text = ""

        if history:

            history_lines = []

            for message in history:

                role = getattr(
                    message,
                    "role",
                    "unknown",
                )

                content = getattr(
                    message,
                    "content",
                    "",
                )

                if not content:
                    continue

                history_lines.append(
                    f"{role.capitalize()}: {content}"
                )

            if history_lines:
                history_text = "\n".join(
                    history_lines
                )
            else:
                history_text = (
                    "No previous conversation."
                )

        else:

            history_text = (
                "No previous conversation."
            )

        user_prompt = f"""
Conversation History:

{history_text}


Retrieved Document Context:

{context}


Current Question:

{question}
""".strip()

        return (
            self.SYSTEM_PROMPT,
            user_prompt,
        )