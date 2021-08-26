from peewee import *
from .data_db_login import NAME, PASSWD, BASE
from playhouse.pool import PooledPostgresqlDatabase
from datetime import datetime


db = PooledPostgresqlDatabase(BASE,
                              max_connections=5,
                              stale_timeout=300,
                              user=NAME,
                              password=PASSWD,
                              host='localhost',
                              port='5432')


class BaseModel(Model):
    class Meta:
        database = db


class Version_DB(BaseModel):
    id_record = AutoField()
    fversion = CharField()
    fdate = DateTimeField()
    fdescription = CharField()

    class Meta:
        db_table = 'db_version'


class Task(BaseModel):
    id_task = AutoField()
    ftitle = CharField()
    fdescription = CharField()
    fstart_date = DateField(default=datetime.now())
    fover_date = DateField()
    fparent_id = IntegerField(default=None)
    fdate_completed = DateField()

    class Meta:
        db_table = 'tasks'


class Remainder(BaseModel):
    id_remainder = AutoField()
    fparent_id = ForeignKeyField(Task, backref='remainders')
    ftitle = CharField()
    fmessage = CharField()
    fdate_remainder = DateTimeField()

    class Meta:
        db_table = 'remainders'


class User(BaseModel):
    id_user = AutoField()
    fname = CharField()
    ffemale = CharField()
    fpatronymic = CharField()
    f_nick = CharField()

    class Meta:
        db_table = 'users'


class Note(BaseModel):
    id_note = AutoField()
    fvolume = CharField()
    fparent_id = ForeignKeyField(Task, backref='notes')

    class Meta:
        db_table = 'notes'
