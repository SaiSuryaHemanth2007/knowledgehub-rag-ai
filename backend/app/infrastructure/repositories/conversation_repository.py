from sqlalchemy.orm import Session

from app.infrastructure.database.models.conversation import (
    ConversationModel,
)


class ConversationRepository:
    """
    Repository responsible for storing and retrieving
    chat conversations.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # Create Conversation
    # =====================================================

    def create(
        self,
        title: str = "New Chat",
    ) -> ConversationModel:
        """
        Create and persist a new conversation.
        """

        conversation = ConversationModel(
            title=title,
        )

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    # =====================================================
    # Get Conversation
    # =====================================================

    def get_by_id(
        self,
        conversation_id: int,
    ) -> ConversationModel | None:
        """
        Retrieve a conversation by ID.
        """

        return (
            self.db.query(ConversationModel)
            .filter(
                ConversationModel.id
                == conversation_id
            )
            .first()
        )

    # =====================================================
    # Get All Conversations
    # =====================================================

    def get_all(
        self,
    ) -> list[ConversationModel]:
        """
        Retrieve all conversations.

        Most recently updated conversations
        are returned first.
        """

        return (
            self.db.query(ConversationModel)
            .order_by(
                ConversationModel.updated_at.desc()
            )
            .all()
        )

    # =====================================================
    # Update Conversation
    # =====================================================

    def update(
        self,
        conversation: ConversationModel,
    ) -> ConversationModel:
        """
        Commit changes made to a conversation.
        """

        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    # =====================================================
    # Delete Conversation
    # =====================================================

    def delete(
        self,
        conversation_id: int,
    ) -> None:
        """
        Delete a conversation by ID.

        Messages are automatically deleted because
        the database foreign key uses ON DELETE CASCADE.
        """

        (
            self.db.query(ConversationModel)
            .filter(
                ConversationModel.id
                == conversation_id
            )
            .delete()
        )

        self.db.commit()