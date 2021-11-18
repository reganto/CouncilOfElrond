"""
add email field to user model
date created: 2021-11-03 11:41:32.466435
"""


def upgrade(migrator):
    migrator.add_column(
        'user',
        'email',
        'char',
        max_length=255,
        null=True
    )


def downgrade(migrator):
    migrator.drop_column(
        'user',
        'email',
        'char',
    )
