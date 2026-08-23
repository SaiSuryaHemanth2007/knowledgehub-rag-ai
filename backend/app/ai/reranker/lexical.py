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
        - Application/use-case relevance
        - Comparison relevance
        - Query-intent-aware boosting

    Base Score:

        Hybrid relevance       -> 50%
        Term coverage          -> 10%
        Phrase relevance       -> 5%
        Concept matching       -> 10%
        Definition evidence    -> 5%
        Application relevance  -> 10%
        Comparison relevance   -> 10%

    Intent Boosts:

        Application intent    -> +20% of application score
        Definition intent     -> +10% of definition score
        Comparison intent     -> +20% of comparison score
    """

    HYBRID_WEIGHT = 0.50
    TERM_COVERAGE_WEIGHT = 0.10
    PHRASE_WEIGHT = 0.05
    CONCEPT_WEIGHT = 0.10
    DEFINITION_WEIGHT = 0.05
    APPLICATION_WEIGHT = 0.10
    COMPARISON_WEIGHT = 0.10

    APPLICATION_INTENT_BOOST = 0.20
    DEFINITION_INTENT_BOOST = 0.10
    COMPARISON_INTENT_BOOST = 0.20

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
        lexical relevance, concept matching,
        definition evidence, application relevance,
        comparison relevance, and query intent.
        """

        if not candidates:
            return []

        query_terms = self._tokenize(query)

        if not query_terms:
            return candidates[:limit]

        application_intent = (
            self._is_application_query(query)
        )

        definition_intent = (
            self._is_definition_query(query)
        )

        comparison_intent = (
            self._is_comparison_query(query)
        )

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

            application_score = self._application_score(
                query,
                content_lower,
            )

            comparison_score = self._comparison_score(
                query,
                content_lower,
            )

            # ------------------------------------------------
            # Base reranking score
            # ------------------------------------------------

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
            ) + (
                application_score
                * self.APPLICATION_WEIGHT
            ) + (
                comparison_score
                * self.COMPARISON_WEIGHT
            )

            # ------------------------------------------------
            # Query-intent-aware adjustment
            # ------------------------------------------------

            if application_intent:
                rerank_score += (
                    application_score
                    * self.APPLICATION_INTENT_BOOST
                )

            if definition_intent:
                rerank_score += (
                    definition_score
                    * self.DEFINITION_INTENT_BOOST
                )

            if comparison_intent:
                rerank_score += (
                    comparison_score
                    * self.COMPARISON_INTENT_BOOST
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

            result["application_score"] = round(
                application_score,
                4,
            )

            result["comparison_score"] = round(
                comparison_score,
                4,
            )

            result["application_intent"] = (
                application_intent
            )

            result["definition_intent"] = (
                definition_intent
            )

            result["comparison_intent"] = (
                comparison_intent
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
            if re.search(
                pattern,
                content_lower,
            ):
                score = max(score, 1.0)

        # ------------------------------------------------
        # GenAI near meaningful concepts
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
        definition or answer to a definition question.
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

    # ==================================================
    # Application / Use-Case Relevance
    # ==================================================

    def _application_score(
        self,
        query: str,
        content: str,
    ) -> float:
        """
        Detect whether a query is asking about
        applications, use cases, examples, or
        business functions.
        """

        query_lower = query.lower()
        content_lower = content.lower()

        application_query_patterns = [
            r"\bapplication(?:s)?\b",
            r"\buse\s+case(?:s)?\b",
            r"\bexamples?\b",
            r"\bused\s+for\b",
            r"\buses?\b",
            r"\busage\b",
            r"\bwhere\s+(?:is|are)\b",
            r"\bbusiness\s+function(?:s)?\b",
            r"\bpractical\s+example(?:s)?\b",
            r"\breal[-\s]?world\b",
        ]

        is_application_query = any(
            re.search(
                pattern,
                query_lower,
            )
            for pattern in application_query_patterns
        )

        if not is_application_query:
            return 0.0

        application_patterns = [
            r"\bcustomer\s+support\b",
            r"\bcustomer\s+service\b",
            r"\bsupport\s+automation\b",
            r"\bsales\b",
            r"\bmarketing\b",
            r"\bdata\s+analysis\b",
            r"\bdata\s+analytics\b",
            r"\breporting\b",
            r"\blead\s+qualification\b",
            r"\bpersonalized\s+communications?\b",
            r"\bcampaign\s+(?:generation|optimization)\b",
            r"\bcode\s+generation\b",
            r"\bautomate\s+(?:tasks?|workflows?)\b",
            r"\bautomation\b",
            r"\bbusiness\s+functions?\b",
            r"\breal[-\s]?world\s+(?:scenarios?|examples?)\b",
            r"\bpractical\s+(?:examples?|applications?)\b",
            r"\buse\s+cases?\b",
            r"\bapplied\s+(?:to|across)\b",
            r"\bapplied\s+across\b",
            r"\bapplications?\s+(?:include|such\s+as)\b",
        ]

        matched_patterns = sum(
            1
            for pattern in application_patterns
            if re.search(
                pattern,
                content_lower,
            )
        )

        if matched_patterns == 0:
            return 0.0

        return min(
            matched_patterns / 3.0,
            1.0,
        )

    # ==================================================
    # Comparison Relevance
    # ==================================================

    def _comparison_score(
        self,
        query: str,
        content: str,
    ) -> float:
        """
        Detect whether a chunk contains useful evidence
        for a comparison/difference question.

        Strong comparison evidence includes:

            - Generative AI vs traditional AI
            - classification
            - prediction
            - creating new content
            - traditional AI
            - model type differences
            - probabilistic behavior
            - deterministic behavior
        """

        if not self._is_comparison_query(query):
            return 0.0

        content_lower = content.lower()

        score = 0.0

        # ------------------------------------------------
        # Direct comparison language
        # ------------------------------------------------

        direct_comparison_patterns = [
            r"\btraditional\s+ai\b",
            r"\bgenerative\s+ai\b",
            r"\bgenai\b",
            r"\bcompared\s+to\b",
            r"\bin\s+contrast\b",
            r"\bunlike\s+traditional\s+ai\b",
            r"\bdifference\s+between\b",
            r"\bwhereas\b",
            r"\bwhile\s+traditional\s+ai\b",
        ]

        direct_matches = sum(
            1
            for pattern in direct_comparison_patterns
            if re.search(
                pattern,
                content_lower,
            )
        )

        if direct_matches >= 2:
            score = max(score, 0.75)

        elif direct_matches == 1:
            score = max(score, 0.25)

        # ------------------------------------------------
        # Traditional AI behavior
        # ------------------------------------------------

        traditional_ai_patterns = [
            r"\bclassif(?:y|ies|ication)\b",
            r"\bpredict(?:s|ion)?\b",
            r"\bspam\b",
            r"\bforecast(?:s|ing)?\b",
            r"\btraditional\s+ai\b",
        ]

        traditional_matches = sum(
            1
            for pattern in traditional_ai_patterns
            if re.search(
                pattern,
                content_lower,
            )
        )

        # ------------------------------------------------
        # Generative AI behavior
        # ------------------------------------------------

        generative_patterns = [
            r"\bcreate(?:s|d)?\s+new\s+content\b",
            r"\bgenerat(?:e|es|ed|ing)\b",
            r"\btext\b",
            r"\bimages?\b",
            r"\bcode\b",
            r"\bsynthetic\s+data\b",
            r"\bllms?\b",
            r"\bfoundation\s+models?\b",
        ]

        generative_matches = sum(
            1
            for pattern in generative_patterns
            if re.search(
                pattern,
                content_lower,
            )
        )

        # ------------------------------------------------
        # Strong comparison evidence
        # ------------------------------------------------

        if (
            traditional_matches >= 2
            and generative_matches >= 2
        ):
            score = max(score, 1.0)

        elif (
            traditional_matches >= 1
            and generative_matches >= 1
        ):
            score = max(score, 0.75)

        # ------------------------------------------------
        # Output behavior comparison
        # ------------------------------------------------

        behavior_patterns = [
            r"\bclassification\b.{0,150}\bprediction\b",
            r"\bprediction\b.{0,150}\bclassification\b",
            r"\bclassif(?:y|ies|ication)\b.{0,150}"
            r"\bgenerat(?:e|es|ed|ing)\b",
            r"\bgenerat(?:e|es|ed|ing)\b.{0,150}"
            r"\bclassif(?:y|ies|ication)\b",
            r"\bdeterministic\b",
            r"\bprobabilistic\b",
        ]

        if any(
            re.search(
                pattern,
                content_lower,
                flags=re.DOTALL,
            )
            for pattern in behavior_patterns
        ):
            score = max(score, 0.75)

        return min(score, 1.0)

    # ==================================================
    # Application Query Intent
    # ==================================================

    def _is_application_query(
        self,
        query: str,
    ) -> bool:
        """
        Detect questions asking about applications,
        use cases, examples, or practical usage.
        """

        query_lower = query.lower()

        patterns = [
            r"\bapplication(?:s)?\b",
            r"\buse\s+case(?:s)?\b",
            r"\bexamples?\b",
            r"\bused\s+for\b",
            r"\bhow\s+is\b.*\bused\b",
            r"\bhow\s+are\b.*\bused\b",
            r"\bwhere\s+(?:is|are)\b",
            r"\bbusiness\s+function(?:s)?\b",
            r"\bpractical\s+(?:example|application)s?\b",
            r"\breal[-\s]?world\b",
        ]

        return any(
            re.search(
                pattern,
                query_lower,
            )
            for pattern in patterns
        )

    # ==================================================
    # Definition Query Intent
    # ==================================================

    def _is_definition_query(
        self,
        query: str,
    ) -> bool:
        """
        Detect questions asking for a definition,
        explanation, or meaning.
        """

        query_lower = query.lower()

        patterns = [
            r"^\s*what\s+is\s+(?:generative\s+ai|genai|gen\s+ai)\b",
            r"^\s*what\s+does\s+(?:generative\s+ai|genai|gen\s+ai)\s+mean\b",
            r"\bdefine\s+(?:generative\s+ai|genai|gen\s+ai)\b",
            r"\bmeaning\s+of\s+(?:generative\s+ai|genai|gen\s+ai)\b",
        ]

        return any(
            re.search(
                pattern,
                query_lower,
            )
            for pattern in patterns
        )

    # ==================================================
    # Comparison Query Intent
    # ==================================================

    def _is_comparison_query(
        self,
        query: str,
    ) -> bool:
        """
        Detect questions asking for differences,
        comparisons, contrasts, or versus-style analysis.
        """

        query_lower = query.lower()

        patterns = [
            r"\bdifference\s+between\b",
            r"\bdifferent\s+from\b",
            r"\bcompare\b",
            r"\bcomparison\b",
            r"\bversus\b",
            r"\bvs\.?\b",
            r"\bcontrast\b",
            r"\bhow\s+is\b.*\bdifferent\b",
            r"\bhow\s+are\b.*\bdifferent\b",
            r"\bwhat\s+makes\b.*\bdifferent\b",
        ]

        return any(
            re.search(
                pattern,
                query_lower,
            )
            for pattern in patterns
        )