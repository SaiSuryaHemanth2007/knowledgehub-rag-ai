"""add conversations and messages

Revision ID: 2e29046b8440
Revises: de87e912b79d
Create Date: 2026-08-15 09:04:22.387784

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2e29046b8440"
down_revision: Union[str, Sequence[str], None] = "de87e912b79d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # =====================================================
    # Conversations
    # =====================================================

    op.create_table(
        "conversations",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "title",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_conversations_id"),
        "conversations",
        ["id"],
        unique=False,
    )


    # =====================================================
    # Messages
    # =====================================================

    op.create_table(
        "messages",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "conversation_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "role",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversations.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_messages_conversation_id"),
        "messages",
        ["conversation_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_messages_created_at"),
        "messages",
        ["created_at"],
        unique=False,
    )

    op.create_index(
        op.f("ix_messages_id"),
        "messages",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    # =====================================================
    # Messages
    # =====================================================

    op.drop_index(
        op.f("ix_messages_id"),
        table_name="messages",
    )

    op.drop_index(
        op.f("ix_messages_created_at"),
        table_name="messages",
    )

    op.drop_index(
        op.f("ix_messages_conversation_id"),
        table_name="messages",
    )

    op.drop_table("messages")


    # =====================================================
    # Conversations
    # =====================================================

    op.drop_index(
        op.f("ix_conversations_id"),
        table_name="conversations",
    )

    op.drop_table("conversations")