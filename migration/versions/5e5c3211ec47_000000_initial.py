"""000000_initial

Revision ID: 5e5c3211ec47
Revises: 
Create Date: 2024-11-19 23:28:39.963494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e5c3211ec47'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('addresses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('city', sa.String(length=32), nullable=False),
    sa.Column('region', sa.String(length=32), nullable=False),
    sa.Column('appartament', sa.String(length=32), nullable=False),
    sa.Column('street', sa.String(length=32), nullable=False),
    sa.Column('house', sa.String(length=8), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('championships',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('passports',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('serial', sa.String(length=4), nullable=False),
    sa.Column('number', sa.String(length=6), nullable=False),
    sa.Column('birthday_city', sa.String(length=32), nullable=False),
    sa.Column('issued_by', sa.String(length=128), nullable=False),
    sa.Column('issued_code', sa.String(length=6), nullable=False),
    sa.Column('issued_date', sa.Date(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('directions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('championship_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('is_juniors', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['championship_id'], ['championships.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('persons',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('address_id', sa.BigInteger(), nullable=False),
    sa.Column('passport_id', sa.BigInteger(), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=False),
    sa.Column('middle_name', sa.String(length=32), nullable=False),
    sa.Column('last_name', sa.String(length=32), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=False),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='gender'), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('phone', sa.String(length=10), nullable=False),
    sa.Column('snils', sa.String(length=11), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['address_id'], ['addresses.id'], ),
    sa.ForeignKeyConstraint(['passport_id'], ['passports.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('delivery',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('direction_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('count', sa.BigInteger(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'DELIVERED', 'CANCELLED', name='deliverystatus'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['direction_id'], ['directions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('direction_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('max_score', sa.Float(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['direction_id'], ['directions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('person_id', sa.BigInteger(), nullable=True),
    sa.Column('role', sa.Enum('OWNER', 'ADMIN', 'USER', name='systemroles'), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('password_salt', sa.String(length=16), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('evaluations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('direction_id', sa.BigInteger(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('task_id', sa.BigInteger(), nullable=False),
    sa.Column('score', sa.Float(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['direction_id'], ['directions.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participants',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('role', sa.Enum('CHIEF_EXPERT', 'TECHNICAL_ADMINISTRATOR', 'INDUSTRIAL_EXPERT', 'EXPERT', 'PARTICIPANT', name='directionroles'), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('direction_id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['direction_id'], ['directions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('protocols',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('direction_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('status', sa.Enum('PUBLISHED', 'ASSIGNED', 'ACCEPTED', 'CANCELLED', name='protocolstatus'), nullable=False),
    sa.Column('assigned_by', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['assigned_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['direction_id'], ['directions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('protocols')
    op.drop_table('participants')
    op.drop_table('evaluations')
    op.drop_table('users')
    op.drop_table('tasks')
    op.drop_table('delivery')
    op.drop_table('persons')
    op.drop_table('directions')
    op.drop_table('passports')
    op.drop_table('championships')
    op.drop_table('addresses')
    # ### end Alembic commands ###