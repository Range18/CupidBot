from peewee import SqliteDatabase, Model, TextField, IntegerField, BooleanField

db = SqliteDatabase('users.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    tg_id = IntegerField(default=0)
    all_message = TextField(default="[]")
    is_mute = BooleanField(default=False)


db.connect()
db.create_tables([User])