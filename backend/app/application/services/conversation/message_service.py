from datetime import datetime

from sqlalchemy.orm import Session

from app.infrastructure.database.models.conversation import (
    ConversationModel,
)
from app.infrastructure.database.models.message import (
    MessageModel,
)


class MessageService:
    """
    Service responsible for creating and retrieving
    conversation messages.
    """

    def __init__(self, db: Session):
        self.db = db

    # =======================================================
    # Create Message
    # =======================================================

    def create(
        self,
        conversation_id: int,
        role: str,
        content: str,
    ):
        """
        Create a message and update the parent
        conversation's updated_at timestamp.
        """

        message = MessageModel(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.db.add(message)

        # ---------------------------------------------------
        # Update conversation timestamp
        # ---------------------------------------------------

        conversation = (
            self.db.query(ConversationModel)
            .filter(
                ConversationModel.id
                == conversation_id
            )
            .first()
        )

        if conversation:
            conversation.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(message)

        return message

    # =======================================================
    # Get Conversation History
    # =======================================================

    def get_history(
        self,
        conversation_id: int,
    ) -> list[MessageModel]:
        """
        Retrieve all messages belonging to a conversation
        in chronological order.
        """

        return (
            self.db.query(MessageModel)
            .filter(
                MessageModel.conversation_id
                == conversation_id
            )
            .order_by(
                MessageModel.created_at.asc()
            )
            .all()
        )