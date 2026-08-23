import re

from app.ai.reranker.base import BaseReranker


class LexicalReranker(BaseReranker):
    """
    Lightweight dependency-free reranker.

    Combines:

        - Hybrid semantic/keyword relevance
        - Query term coverage
        - Phrase relevance
        - Concept matching
        - Definition/question-answer evidence

    Score:

        Hybrid relevance    -> 60%
        Term coverage       -> 15%
        Phrase relevance    -> 10%
        Concept matching    -> 10%
        Definition evidence -> 5%

    The hybrid score remains the primary signal.
    """

    HYBRID_WEIGHT = 0.60
    TERM_COVERAGE_WEIGHT = 0.15
    PHRASE_WEIGHT = 0.10
    CONCEPT_WEIGHT = 0.10
    DEFINITION_WEIGHT = 0.05

    # ==================================================
    # Public API
    # ==================================================

    def rerank(
        self,
        query: str,
        candidates: list[dict],
        limit: int = 5,
    ) -> list[dict]:
        """
        Rerank candidates using hybrid relevance,
        lexical relevance, concept matching, and
        definition evidence.
        """

        if not candidates:
            return []

        query_terms = self._tokenize(query)

        if not query_terms:
            return candidates[:limit]

        reranked = []

        for candidate in candidates:

            chunk = candidate["chunk"]

            content = (
                getattr(chunk, "content", "")
                or ""
            )

            content_lower = content.lower()

            hybrid_score = float(
                candidate.get("score", 0.0)
            )

            term_coverage = self._term_coverage(
                query_terms,
                content_lower,
            )

            phrase_score = self._phrase_score(
                query,
                content_lower,
            )

            concept_score = self._concept_score(
                query,
                content_lower,
            )

            definition_score = self._definition_score(
                query,
                content_lower,
            )

            rerank_score = (
                hybrid_score
                * self.HYBRID_WEIGHT
            ) + (
                term_coverage
                * self.TERM_COVERAGE_WEIGHT
            ) + (
                phrase_score
                * self.PHRASE_WEIGHT
            ) + (
                concept_score
                * self.CONCEPT_WEIGHT
            ) + (
                definition_score
                * self.DEFINITION_WEIGHT
            )

            result = dict(candidate)

            result["rerank_score"] = round(
                rerank_score,
                4,
            )

            result["term_coverage"] = round(
                term_coverage,
                4,
            )

            result["phrase_score"] = round(
                phrase_score,
                4,
            )

            result["concept_score"] = round(
                concept_score,
                4,
            )

            result["definition_score"] = round(
                definition_score,
                4,
            )

            reranked.append(result)

        reranked.sort(
            key=lambda result: result["rerank_score"],
            reverse=True,
        )

        return reranked[:limit]

    # ==================================================
    # Tokenization
    # ==================================================

    def _tokenize(
        self,
        text: str,
    ) -> list[str]:
        """
        Convert text into meaningful lowercase tokens.
        """

        tokens = re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text.lower(),
        )

        stop_words = {
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "by",
            "for",
            "from",
            "how",
            "in",
            "is",
            "it",
            "of",
            "on",
            "or",
            "the",
            "this",
            "to",
            "was",
            "what",
            "when",
            "where",
            "which",
            "who",
            "why",
            "with",
        }

        return [
            token
            for token in tokens
            if token not in stop_words
        ]

    # ==================================================
    # Term Coverage
    # ==================================================

    def _term_coverage(
        self,
        query_terms: list[str],
        content: str,
    ) -> float:
        """
        Calculate the percentage of meaningful query
        terms appearing in the chunk.
        """

        if not query_terms:
            return 0.0

        content = content.lower()

        matched = sum(
            1
            for term in query_terms
            if re.search(
                rf"\b{re.escape(term)}\b",
                content,
            )
        )

        return matched / len(query_terms)

    # ==================================================
    # Phrase Relevance
    # ==================================================

    def _phrase_score(
        self,
        query: str,
        content: str,
    ) -> float:
        """
        Reward meaningful consecutive query terms.
        """

        query_terms = self._tokenize(query)

        if len(query_terms) < 2:
            return 0.0

        content = content.lower()

        phrases = [
            " ".join(
                query_terms[i:i + 2]
            )
            for i in range(
                len(query_terms) - 1
            )
        ]

        matched_phrases = sum(
            1
            for phrase in phrases
            if phrase in content
        )

        return (
            matched_phrases
            / len(phrases)
        )

    # ==================================================
    # Concept Matching
    # ==================================================

    def _concept_score(
        self,
        query: str,
        content: str,
    ) -> float:
        """
        Detect meaningful contextual matches for
        Generative AI / GenAI.

        A document title such as:

            The Big Book of Generative AI

        should NOT receive full concept credit.

        Strong contextual matches include:

            What is GenAI?
            GenAI focuses on...
            GenAI creates...
            Generative AI is...
        """

        query_lower = query.lower()
        content_lower = content.lower()

        generative_ai_query = bool(
            re.search(
                r"\bgenerative\s+ai\b"
                r"|\bgenai\b"
                r"|\bgen\s+ai\b",
                query_lower,
            )
        )

        if not generative_ai_query:
            return 0.0

        score = 0.0

        # ------------------------------------------------
        # Direct question/reference
        # ------------------------------------------------

        if re.search(
            r"\bwhat\s+is\s+"
            r"(?:genai|gen\s*ai|generative\s+ai)\b",
            content_lower,
        ):
            score = max(score, 1.0)

        # ------------------------------------------------
        # Strong definition/context patterns
        # ------------------------------------------------

        contextual_patterns = [
            r"\bgenai\s+(?:is|focuses|creates|refers)\b",
            r"\bgen\s*ai\s+(?:is|focuses|creates|refers)\b",
            r"\bgenerative\s+ai\s+(?:is|focuses|creates|refers)\b",
            r"\bgenerative\s+artificial\s+intelligence\s+"
            r"(?:is|focuses|creates|refers)\b",
        ]

        for pattern in contextual_patterns:
            if re.search(pattern, content_lower):
                score = max(score, 1.0)

        # ------------------------------------------------
        # "GenAI" appearing near meaningful concepts
        # ------------------------------------------------

        meaningful_context_patterns = [
            r"\bgenai\b.{0,120}"
            r"\b(?:models?|content|text|images?|code|"
            r"synthetic\s+data|traditional\s+ai)\b",

            r"\b(?:models?|content|text|images?|code|"
            r"synthetic\s+data|traditional\s+ai)\b.{0,120}"
            r"\bgenai\b",
        ]

        if any(
            re.search(
                pattern,
                content_lower,
                flags=re.DOTALL,
            )
            for pattern in meaningful_context_patterns
        ):
            score = max(score, 0.75)

        # ------------------------------------------------
        # Generic occurrence only
        #
        # This prevents document titles from getting
        # full concept credit.
        # ------------------------------------------------

        if score == 0.0:

            generic_occurrence = bool(
                re.search(
                    r"\bgenai\b"
                    r"|\bgen\s+ai\b"
                    r"|\bgenerative\s+ai\b",
                    content_lower,
                )
            )

            if generic_occurrence:
                score = 0.20

        return score

    # ==================================================
    # Definition Evidence
    # ==================================================

    def _definition_score(
        self,
        query: str,
        content: str,
    ) -> float:
        """
        Detect whether the chunk contains a direct
        definition or answer to a "What is..." question.
        """

        query_lower = query.lower()
        content_lower = content.lower()

        definition_question = bool(
            re.search(
                r"\bwhat\s+is\b"
                r"|\bwhat\s+are\b"
                r"|\bdefine\b",
                query_lower,
            )
        )

        if not definition_question:
            return 0.0

        score = 0.0

        # ------------------------------------------------
        # Direct question in the document
        # ------------------------------------------------

        if re.search(
            r"\bwhat\s+is\s+"
            r"(?:genai|gen\s*ai|generative\s+ai)\b",
            content_lower,
        ):
            score += 0.50

        # ------------------------------------------------
        # Definition-style statements
        # ------------------------------------------------

        definition_patterns = [
            r"\bgenai\s+(?:is|focuses|creates|refers)\b",
            r"\bgen\s*ai\s+(?:is|focuses|creates|refers)\b",
            r"\bgenerative\s+ai\s+(?:is|focuses|creates|refers)\b",
            r"\bgenerative\s+artificial\s+intelligence\s+"
            r"(?:is|focuses|creates|refers)\b",
        ]

        if any(
            re.search(
                pattern,
                content_lower,
            )
            for pattern in definition_patterns
        ):
            score += 0.50

        return min(score, 1.0)