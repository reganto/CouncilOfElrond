"""
create table user
date created: 2021-11-03 09:58:16.080180
"""


def upgrade(migrator):
    with migrator.create_table('user') as table:
        table.primary_key('id')
        table.char('username', index=True, max_length=255)


def downgrade(migrator):
    migrator.drop_table('user')
