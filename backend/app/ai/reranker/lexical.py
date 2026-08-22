import re

from app.ai.reranker.base import BaseReranker


class LexicalReranker(BaseReranker):
    """
    Lightweight dependency-free reranker.

    The hybrid retrieval score remains the primary signal.
    Lexical signals provide additional evidence rather than
    dominating semantic retrieval.

    Score:

        Hybrid score       -> 70%
        Term coverage      -> 20%
        Phrase relevance   -> 10%
    """

    HYBRID_WEIGHT = 0.70
    TERM_COVERAGE_WEIGHT = 0.20
    PHRASE_WEIGHT = 0.10

    def rerank(
        self,
        query: str,
        candidates: list[dict],
        limit: int = 5,
    ) -> list[dict]:
        """
        Rerank candidates using hybrid relevance plus
        lightweight lexical relevance.
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

            rerank_score = (
                hybrid_score
                * self.HYBRID_WEIGHT
            ) + (
                term_coverage
                * self.TERM_COVERAGE_WEIGHT
            ) + (
                phrase_score
                * self.PHRASE_WEIGHT
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

        Matching is case-insensitive.
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

        Matching is case-insensitive.
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