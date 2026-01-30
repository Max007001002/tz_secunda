"""Создание таблиц.

Revision ID: 0001_create_tables
Revises: 
Create Date: 2026-01-30
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_create_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
    )

    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("parent_id", sa.Integer(), sa.ForeignKey("activities.id"), nullable=True),
    )
    op.create_index("ix_activities_parent_id", "activities", ["parent_id"])

    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("building_id", sa.Integer(), sa.ForeignKey("buildings.id"), nullable=False),
    )
    op.create_index("ix_organizations_building_id", "organizations", ["building_id"])

    op.create_table(
        "organization_phones",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
    )

    op.create_table(
        "organization_activity",
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), primary_key=True),
        sa.Column("activity_id", sa.Integer(), sa.ForeignKey("activities.id"), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table("organization_activity")
    op.drop_table("organization_phones")
    op.drop_index("ix_organizations_building_id", table_name="organizations")
    op.drop_table("organizations")
    op.drop_index("ix_activities_parent_id", table_name="activities")
    op.drop_table("activities")
    op.drop_table("buildings")
