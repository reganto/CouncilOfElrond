"""
update username column in user model
date created: 2021-11-03 10:44:05.976306
"""


def upgrade(migrator):
    migrator.drop_column(
        'user',
        'username',
        'char'
    )
    migrator.add_column(
        'user',
        'username',
        'char',
        max_length=255,
        index=True,
        null=True,
    )


def downgrade(migrator):
    migrator.drop_column(
        'user',
        'username',
        'char',
    )
    migrator.add_column(
        'user',
        'username',
        'char',
        index=True,
        max_length=255
    )
