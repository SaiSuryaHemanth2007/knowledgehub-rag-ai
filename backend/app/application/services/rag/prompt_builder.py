class PromptBuilder:
    """
    Builds prompts for the language model.
    Returns separate system and user prompts
    for modern chat-based LLM APIs.
    """

    SYSTEM_PROMPT = """
You are KnowledgeHub AI, an AI assistant that answers questions using uploaded documents.

Rules:
- Answer ONLY using the provided context.
- Do NOT invent facts.
- If the answer is not present in the context, respond:
  "I don't have enough information in the uploaded document."
- If the context is incomplete, say so.
- Keep answers clear, concise, and accurate.
- Use bullet points when appropriate.
""".strip()

    def build(
        self,
        context: str,
        question: str,
    ) -> tuple[str, str]:
        """
        Returns:
            tuple(system_prompt, user_prompt)
        """

        user_prompt = f"""
Context:

{context}

Question:

{question}
""".strip()

        return (
            self.SYSTEM_PROMPT,
            user_prompt,
        )