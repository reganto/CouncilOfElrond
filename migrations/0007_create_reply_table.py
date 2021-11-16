"""
create table reply
date created: 2021-11-03 14:04:47.442751
"""


def upgrade(migrator):
    with migrator.create_table('reply') as table:
        table.primary_key('id')
        table.text('body')
        table.datetime('created_at')
        table.foreign_key('AUTO', 'user_id', on_delete='CASCADE',
                          on_update='CASCADE', references='user.id')
        table.foreign_key('AUTO', 'thread_id', on_delete='CASCADE',
                          on_update='CASCADE', references='thread.id')


def downgrade(migrator):
    migrator.drop_table('reply')
