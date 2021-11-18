"""
add password field to user model
date created: 2021-11-03 10:00:50.631135
"""


def upgrade(migrator):
    migrator.add_column(
        'user',
        'password',
        'char',
        index=True,
        max_length=255,
        null=True,
    )


def downgrade(migrator):
    migrator.drop_column(
        'user',
        'password',
        'char',
    )
