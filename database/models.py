from datetime import datetime

from peewee_moves import DatabaseManager
import peewee

from filters.thread_filter import ThreadFilter
from utils.humanize_datetime import humanize

db = peewee.PostgresqlDatabase(
   'testdb',
   user='testuser',
   password='testuser',
   host='localhost',
)
# db = peewee.SqliteDatabase(':memory:')
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


class Channel(BaseModel):
    name = peewee.CharField(
        index=True,
        max_length=255,
    )
    slug = peewee.CharField()

    def __str__(self):
        return self.name


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

    @staticmethod
    def filter(upcoming_filters):
        return ThreadFilter(upcoming_filters).done()

    @humanize
    def diff_for_humans(self):
        return self.created_at


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

    def add_favorite(self, favorite: dict):
        return Favorite.create(
            reply=self.id,
            user=favorite.get('user'),
            favorite_type=favorite.get('favorite_type'),
        )

    def is_favorited(self, user_id):
        if user_id is not None and isinstance(user_id, bytes):
            user_id = int(user_id.decode())
        return self.favorites.where(Favorite.user_id==user_id).exists()


class Favorite(BaseModel):
    favorite_type = peewee.CharField(max_length=50)
    created_at = peewee.DateTimeField(
        default=datetime.now,
    )
    reply = peewee.ForeignKeyField(
        Reply,
        backref='favorites',
        on_delete='CASCADE',
        on_update='CASCADE',
    )
    user = peewee.ForeignKeyField(
        User,
        backref='favorited',
        on_delete='CASCADE',
        on_update='CASCADE',
    )

    class Meta:
        indexes = (
            (('favorite_type', 'reply', 'user'), True),
        )

    def __str__(self):
        return f'{self.favorite_type}<->{self.user}<->{self.reply}'

# db.create_tables(
#     [
#         User,
#         Thread,
#         Reply,
#         Channel,
#         Favorite,
#     ], safe=True)
