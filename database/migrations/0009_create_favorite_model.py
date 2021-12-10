"""
create favorite model
date created: 2021-12-09 18:11:12.347528
"""


def upgrade(migrator):
    with migrator.create_table('favorite') as table:
        table.primary_key('id')
        table.char('favorite_type', max_length=50)
        table.datetime('created_at')
        table.foreign_key('AUTO', 'user_id', on_delete='CASCADE',
                          on_update='CASCADE', references='user.id')
        table.foreign_key('AUTO', 'reply_id', on_delete='CASCADE',
                          on_update='CASCADE', references='reply.id')
        table.add_index(('favorite_type', 'user_id', 'reply_id'), unique=True)


def downgrade(migrator):
    migrator.drop_table('favorite')


# Migrator API

# with migrator.create_table(name, safe=False) as table:
#     table.primary_key('colname', **kwargs)
#     table.bare('colname', **kwargs)
#     table.biginteger('colname', **kwargs)
#     table.binary('colname', **kwargs)
#     table.blob('colname', **kwargs)
#     table.bool('colname', **kwargs)
#     table.date('colname', **kwargs)
#     table.datetime('colname', **kwargs)
#     table.decimal('colname', **kwargs)
#     table.double('colname', **kwargs)
#     table.fixed('colname', **kwargs)
#     table.float('colname', **kwargs)
#     table.integer('colname', **kwargs)
#     table.char('colname', **kwargs)
#     table.text('colname', **kwargs)
#     table.time('colname', **kwargs)
#     table.uuid('colname', **kwargs)
#     table.foreign_key('coltype', 'colname', references='othertable.col')
#     table.add_index(('col1', 'col2'), unique=True)
#     table.add_constraint('constraint string')

# migrator.drop_table('name', safe=False, cascade=False)
# migrator.add_column('table', 'name', 'type', **kwargs)
# migrator.drop_column('table', 'name', 'field', cascade=True)
# migrator.rename_column('table', 'old_name', 'new_name')
# migrator.rename('table', 'old_name', 'new_name')
# migrator.add_not_null('table', 'column')
# migrator.drop_not_null('table', 'column')
# migrator.add_index('table', 'columns', unique=False)
# migrator.drop_index('table', 'index_name')
# cursor = migrator.execute_sql(sql, params=None)
