"""
create table thread
date created: 2021-11-03 08:24:38.672495
"""


def upgrade(migrator):
    with migrator.create_table('thread') as table:
        table.primary_key('id')
        table.char('title', index=True, max_length=255)
        table.text('body')
        table.datetime('created_at')
        table.foreign_key('AUTO', 'user_id', on_delete='CASCADE',
                          on_update='CASCADE', references='user.id')
        table.foreign_key('AUTO', 'channel_id', on_delete='CASCADE',
                          on_update='CASCADE', references='channel.id')


def downgrade(migrator):
    migrator.drop_table('thread')
