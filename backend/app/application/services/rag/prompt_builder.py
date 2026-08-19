class PromptBuilder:
    """
    Builds prompts for the language model.

    The prompt contains:
        1. Conversation history
        2. Retrieved document context
        3. Current question
    """

    SYSTEM_PROMPT = """
You are KnowledgeHub AI, an AI assistant that answers questions using uploaded documents and conversation history.

Rules:

- Answer using the provided document context.
- The retrieved document context is the primary source of truth.
- Use conversation history only to understand references such as "it", "they", "this", "that", "the device", or similar follow-up references.
- Do NOT invent facts.
- Do NOT use information that is not supported by the retrieved document context.
- If the answer is not present in the document context, respond:
  "I don't have enough information in the uploaded document."
- If the context is incomplete, clearly say so.
- Keep answers clear, concise, and accurate.
- Use bullet points when appropriate.

Citation rules:

- Retrieved context contains labels such as [Chunk 7], [Chunk 1], and [Chunk 20].
- If you mention where information came from, use ONLY the exact chunk numbers provided in the retrieved context.
- NEVER invent a chunk number.
- NEVER refer to a chunk that does not appear in the retrieved context.
- Do not create your own source numbering.
- Do not assume that the order of the retrieved chunks represents their original document order.
- The application separately displays the retrieved source metadata.
- Do not fabricate document names, filenames, page numbers, chunk numbers, or similarity scores.
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

        # ---------------------------------------------------
        # Conversation History
        # ---------------------------------------------------

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

        # ---------------------------------------------------
        # User Prompt
        # ---------------------------------------------------

        user_prompt = f"""
Conversation History:

{history_text}


Retrieved Document Context:

The following chunks were retrieved from the uploaded documents.

The chunk numbers shown below are the actual chunk identifiers.
Use only these chunks as evidence for your answer.

{context}


Current Question:

{question}
""".strip()

        return (
            self.SYSTEM_PROMPT,
            user_prompt,
        )