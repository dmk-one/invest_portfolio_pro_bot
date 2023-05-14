"""first user, portfolio and log

Revision ID: af69ef71b71f
Revises: 
Create Date: 2023-05-01 15:09:11.334584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af69ef71b71f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('phone_number', sa.BigInteger(), nullable=True),
    sa.Column('language_code', sa.String(length=255), nullable=False),
    sa.Column('added_to_attachment_menu', sa.Boolean(), nullable=True),
    sa.Column('can_join_groups', sa.Boolean(), nullable=True),
    sa.Column('can_read_all_group_messages', sa.Boolean(), nullable=True),
    sa.Column('supports_inline_queries', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('last_activity', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'uuid'),
    sa.UniqueConstraint('first_name'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('last_name'),
    sa.UniqueConstraint('tg_id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('portfolio',
    sa.Column('tg_id', sa.BigInteger(), nullable=True),
    sa.Column('crypto', sa.String(), nullable=False),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['tg_id'], ['user.tg_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'uuid'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('portfolio_log',
    sa.Column('portfolio_id', sa.BigInteger(), nullable=True),
    sa.Column('action_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('action_type', sa.SmallInteger(), nullable=False),
    sa.Column('by_price', sa.Float(), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['portfolio_id'], ['portfolio.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'uuid'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('portfolio_log')
    op.drop_table('portfolio')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###