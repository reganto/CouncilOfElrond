from faker import Faker

from models import User, Thread, Reply, Channel
import peewee


class BaseFactory:
    def __init__(self, model: peewee.Model, instances: int = 1):
        self.model = model
        self.instances = instances

    def create(self):
        pass

    def make(self):
        pass

    def row(self):
        pass


class UserFactory:
    def __init__(self, instances: int = 1):
        self.model = User
        self.instances = instances
        self._fake = Faker()
        self._users = []

    def _create_user_instance(self):
        if self.instances > 1:
            for _ in range(0, self.instances):
                user = User.create(
                    username=self._fake.user_name(),
                    password=self._fake.password(),
                    email=self._fake.email(),
                    )
                self._users.append(user)
            return self._users
        user = User.create(
                    username=self._fake.user_name(),
                    password=self._fake.password(),
                    email=self._fake.email(),
                    )
        self._users.append(user)
        return user

    def _make_user_instance(self):
        user = dict(
            username=self._fake.user_name(),
            password=self._fake.password(),
            email=self._fake.email(),
            )
        return user

    def create(self):
        return self._create_user_instance()

    def make(self):
        return self._make_user_instance()

    def row(self):
        self._users.append(self.make())
        return self._users

    def rollback(self):
        self.model.delete().execute()


class ThreadFactory(BaseFactory):
    def __init__(self, instances: int = 1):
        self.model = Thread
        self.instances = instances
        self._fake = Faker()
        self._threads = []

    def _create_thread_instance(self):
        if self.instances > 1:
            for _ in range(0, self.instances):
                thread = Thread.create(
                    title=self._fake.sentence(),
                    body=self._fake.text()*4,
                    user=UserFactory().create(),
                    channel=ChannelFactory().create(),
                    )
                self._threads.append(thread)
            return self._threads
        thread = Thread.create(
                    title=self._fake.sentence(),
                    body=self._fake.text()*4,
                    user=UserFactory().create(),
                    channel=ChannelFactory().create(),
                    )
        self._threads.append(thread)
        return thread

    def _make_thread_instance(self):
        thread = dict(
            title=self._fake.sentence(),
            body=self._fake.text()*4,
            user=UserFactory().create(),
            channel=ChannelFactory().create(),
            )
        return thread

    def create(self):
        return self._create_thread_instance()

    def make(self):
        return self._make_thread_instance()

    def row(self):
        self._threads.append(self.make())
        return self._threads

    def rollback(self):
        self.model.delete().execute()


class ReplyFactory(BaseFactory):
    def __init__(self, instances: int = 1):
        self.model = Reply
        self.instances = instances
        self._fake = Faker()
        self._replies = []

    def _create_reply_instance(self):
        if self.instances > 1:
            for _ in range(0, self.instances):
                reply = Reply.create(
                    body=self._fake.text(),
                    user=UserFactory().create(),
                    thread=ThreadFactory().create(),
                    )
                self._replies.append(reply)
            return self._replies
        reply = Reply.create(
                body=self._fake.text(),
                user=UserFactory().create(),
                thread=ThreadFactory().create(),
                )
        self._replies.append(reply)
        return reply

    def _make_reply_instance(self):
        reply = dict(
            body=self._fake.text(),
            user=UserFactory().create(),
            thread=ThreadFactory().create(),
            )
        return reply

    def create(self):
        return self._create_reply_instance()

    def make(self):
        return self._make_reply_instance()

    def row(self):
        self._replies.append(self.make())
        return self._replies

    def rollback(self):
        self.model.delete().execute()


class ChannelFactory(BaseFactory):
    def __init__(self, instances: int = 1):
        self.model = Channel
        self.instances = instances
        self._fake = Faker()
        self._channels = []

    def _create_channel_instance(self):
        if self.instances > 1:
            for _ in range(0, self.instances):
                name = self._fake.word()
                slug = self._fake.slug(name)
                channel = Channel.create(
                    name=name,
                    slug=slug,
                    )
                self._channels.append(channel)
            return self._channels
        name = self._fake.word()
        slug = self._fake.slug(name)
        channel = Channel.create(
            name=name,
            slug=slug,
            )
        self._channels.append(channel)
        return channel

    def _make_channel_instance(self):
        name = self._fake.name()
        slug = self._fake.slug(name)
        channel = dict(
            name=name,
            slug=slug,
            )
        return channel

    def create(self):
        return self._create_channel_instance()

    def make(self):
        return self._make_channel_instance()

    def row(self):
        self._channels.append(self.make())
        return self._channels

    def rollback(self):
        self.model.delete().execute()


class Factory(BaseFactory):
    def __init__(self, model: peewee.Model, instances: int = 1):
        super().__init__(model, instances)

    def create(self) -> peewee.Model:
        '''
        Create a single instance of specific model
        and save it in database then return instance
        :param self:
        :return: A instance of self.model
        '''
        if self.model is User:
            return UserFactory(self.instances).create()
        elif self.model is Thread:
            return ThreadFactory(self.instances).create()
        elif self.model is Reply:
            return ReplyFactory(self.instances).create()
        elif self.model is Channel:
            return ChannelFactory(self.instances).create()
        else:
            raise TypeError(f'Unknown Model {self.model.__name__}')

    def make(self):
        '''
        Make a single instance of specific model
        and return instance without saving that
        in database
        :param self:
        '''
        if self.model is User:
            return UserFactory(self.instances).make()
        elif self.model is Thread:
            return ThreadFactory(self.instances).make()
        elif self.model is Reply:
            return ReplyFactory(self.instances).make()
        elif self.model is Channel:
            return ChannelFactory(self.instances).make()
        else:
            raise TypeError(f'Unknown Model {self.model.__name__}')

    def row(self) -> list:
        '''
        Create a single instance of specific model
        then save that instance to database and append
        instance to instances list and return it.
        :param self:
        '''
        if self.model is User:
            return UserFactory(self.instances).row()
        elif self.model is Thread:
            return ThreadFactory(self.instances).row()
        elif self.model is Reply:
            return ReplyFactory(self.instances).row()
        elif self.model is Channel:
            return ChannelFactory(self.instances).row()
        else:
            raise TypeError(f'Unknown Model {self.model.__name__}')

    def rollback(self):
        '''
        Rollback all changes
        :param self:
        '''
        if self.model is User:
            UserFactory().rollback()
        elif self.model is Thread:
            ThreadFactory().rollback()
        elif self.model is Reply:
            ReplyFactory().rollback()
        elif self.model is Channel:
            ChannelFactory().rollback()
        else:
            raise TypeError(f'Unknown Model {self.model.__name__}')
