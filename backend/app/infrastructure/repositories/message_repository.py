from sqlalchemy.orm import Session

from app.infrastructure.database.models.message import (
    MessageModel,
)


class MessageRepository:
    """
    Repository responsible for storing and retrieving
    conversation messages.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # Create Message
    # =====================================================

    def create(
        self,
        conversation_id: int,
        role: str,
        content: str,
    ) -> MessageModel:
        """
        Create and persist a message.
        """

        message = MessageModel(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    # =====================================================
    # Get Message
    # =====================================================

    def get_by_id(
        self,
        message_id: int,
    ) -> MessageModel | None:
        """
        Retrieve a message by ID.
        """

        return (
            self.db.query(MessageModel)
            .filter(
                MessageModel.id == message_id
            )
            .first()
        )

    # =====================================================
    # Get Conversation Messages
    # =====================================================

    def get_by_conversation(
        self,
        conversation_id: int,
        limit: int = 50,
    ) -> list[MessageModel]:
        """
        Retrieve messages belonging to a conversation.

        Messages are returned in chronological order.
        """

        messages = (
            self.db.query(MessageModel)
            .filter(
                MessageModel.conversation_id
                == conversation_id
            )
            .order_by(
                MessageModel.created_at.desc()
            )
            .limit(limit)
            .all()
        )

        return list(reversed(messages))

    # =====================================================
    # Delete Message
    # =====================================================

    def delete(
        self,
        message_id: int,
    ) -> bool:
        """
        Delete a message.

        Returns:
            True if deleted.
            False if message does not exist.
        """

        message = self.get_by_id(message_id)

        if message is None:
            return False

        self.db.delete(message)
        self.db.commit()

        return True