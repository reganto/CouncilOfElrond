from datetime import datetime

import peewee
from peewee_moves import DatabaseManager

# db = peewee.PostgresqlDatabase(
#    'testdb',
#    user='testuser',
#    password='testuser',
#    host='localhost',
# )
db = peewee.SqliteDatabase(':memory:')
# db = peewee.SqliteDatabase('database/db.sqlite3')


migrator = DatabaseManager(
    db,
    table_name='migration_history',
    directory='database/migrations/'
)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    username = peewee.CharField(
        max_length=255,
        index=True,
        null=True,
    )
    password = peewee.CharField(
        max_length=255,
        null=True,
    )
    email = peewee.CharField(
        max_length=255,
    )

    def __str__(self):
        return self.username

    # class Meta:
    #     table_name = 'users'


class Channel(BaseModel):
    name = peewee.CharField(
        index=True,
        max_length=255,
        )
    slug = peewee.CharField()

    def __str__(self):
        return self.name

    # class Meta:
    #     table_name = 'channels'


class Thread(BaseModel):
    title = peewee.CharField(
        max_length=255,
        index=True,
        null=False,
    )
    body = peewee.TextField(null=False,)
    created_at = peewee.DateTimeField(
        default=datetime.now,
    )
    user = peewee.ForeignKeyField(
        User,
        backref='threads',
        on_delete='CASCADE',
        on_update='CASCADE',
        null=False,
    )
    channel = peewee.ForeignKeyField(
        Channel,
        backref='threads',
        on_delete='CASCADE',
        on_update='CASCADE',
        null=False,
        )

    def __str__(self):
        return self.title

    @property
    def path(self):
        return f'/threads/{self.channel.slug}/{self.id}'

    @property
    def creator(self):
        return self.user.id

    def add_reply(self, reply: dict):
        return Reply.create(
            thread=self.id,
            user=reply.get('user'),
            body=reply.get('body'),
            )

    # class Meta:
    #     table_name = 'threads'


class Reply(BaseModel):
    body = peewee.TextField()
    created_at = peewee.DateTimeField(
        default=datetime.now,
    )
    user = peewee.ForeignKeyField(
        User,
        backref='replies',
        on_delete='CASCADE',
        on_update='CASCADE',
    )
    thread = peewee.ForeignKeyField(
        Thread,
        backref='replies',
        on_delete='CASCADE',
        on_update='CASCADE',
    )

    def __str__(self):
        return self.body[:10]

    @property
    def owner(self):
        return self.user.id

    # class Meta:
    #     table_name = 'replies'


# db.create_tables([User, Thread, Reply, Channel], safe=True)
# db.drop_tables([User, Thread, Reply, Channel, ])
