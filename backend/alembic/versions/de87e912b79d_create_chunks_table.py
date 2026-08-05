"""create chunks table

Revision ID: de87e912b79d
Revises: 700240dfe866
Create Date: 2026-08-04 23:33:45.786361
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = "de87e912b79d"
down_revision: Union[str, Sequence[str], None] = "700240dfe866"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "chunks",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "document_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "chunk_index",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "embedding",
            Vector(dim=3072),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["documents.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
        ),
    )

    op.create_index(
        op.f("ix_chunks_document_id"),
        "chunks",
        ["document_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_chunks_id"),
        "chunks",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_chunks_id"),
        table_name="chunks",
    )

    op.drop_index(
        op.f("ix_chunks_document_id"),
        table_name="chunks",
    )

    op.drop_table(
        "chunks",
    )