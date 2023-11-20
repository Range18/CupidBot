from peewee import SqliteDatabase, Model, IntegerField, BooleanField

db = SqliteDatabase('users.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    tg_id = IntegerField(default=0)
    is_mute = BooleanField(default=False)


class Messages(BaseModel):
    message_id = IntegerField(default=0)
    tg_id = IntegerField(default=0)


db.connect()
db.create_tables([User, Messages])