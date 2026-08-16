from sqlalchemy.orm import Session

from app.infrastructure.repositories.conversation_repository import (
    ConversationRepository,
)


class ConversationService:
    """
    Application service responsible for conversation
    management.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.repository = ConversationRepository(db)

    # =====================================================
    # Create Conversation
    # =====================================================

    def create(
        self,
        title: str = "New Chat",
    ):
        """
        Create a new conversation.
        """

        return self.repository.create(
            title=title,
        )

    # =====================================================
    # Get Conversation
    # =====================================================

    def get(
        self,
        conversation_id: int,
    ):
        """
        Retrieve a conversation by ID.
        """

        return self.repository.get_by_id(
            conversation_id,
        )

    # =====================================================
    # Update Conversation Title
    # =====================================================

    def update_title(
        self,
        conversation,
        title: str,
    ):
        """
        Update the title of an existing conversation.
        """

        conversation.title = title

        return self.repository.update(
            conversation,
        )

    # =====================================================
    # List Conversations
    # =====================================================

    def list_all(self):
        """
        Retrieve all conversations.
        """

        return self.repository.get_all()

    # =====================================================
    # Delete Conversation
    # =====================================================

    def delete(
        self,
        conversation_id: int,
    ) -> bool:
        """
        Delete a conversation.

        Returns:
            True if deleted.
            False if conversation does not exist.
        """

        conversation = self.repository.get_by_id(
            conversation_id,
        )

        if conversation is None:
            return False

        self.repository.delete(
            conversation_id,
        )

        return True