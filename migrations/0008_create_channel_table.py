"""
create tag table
date created: 2021-11-12 08:06:34.219545
"""


def upgrade(migrator):
    with migrator.create_table('channel') as table:
        table.primary_key('id')
        table.char('name', index=True, max_length=255)
        table.char('slug', max_length=255)


def downgrade(migrator):
    migrator.drop_table('channel')
