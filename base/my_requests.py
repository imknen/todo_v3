from anytree import Node, RenderTree
from .orm_models import User, Remainder, Task, Note


def get_user_info(id):
    query = User.select().where(User.id_user==id)
    return query[0].f_nick


def add_user(data):
    new_user_id = (User.insert(fname=data[name],
                        ffemale=data[female],
                        fpatronymic=data[patronymic],
                        f_nick=data[nick]).execute())
    return new_user_id


def list_users():
    query = User.select()
    print('List users:')
    for user in query:
        print(f'Nick: {user.f_nick}\n'
              f'Name: {user.fname} {user.ffemale} {user.fpatronymic}')


def add_task(data, id_task=None):
    new_task_id = (Task.insert(ftitle=data[0],
                               fdescription=data[1],
                               fover_date=data[2],
                               fparent_id=id_task).execute())
    return new_task_id


def add_remainder(data):
    id_new_rem = Remainder.insert(fdate_remainder=data[0],
                                  ftitle=data[1],
                                  fmessage=data[2]).execute()
    return id_new_rem


def remainder_link_to_task(id_remainder, id_task):
    Remainder.update(fparent_id=id_task).where(Remainder.id_remainder == id_remainder).execute()


def add_note(data):
    id_new_note = Note.insert(data).execute()
    return id_new_note


def note_link_to_task(id_note, id_task):
    Note.update(fparent_id=id_task).where(Note.id_note == id_note).execute()


def get_task(id_t):
    query = Task.select().where(id_t==Task.id_task)
    return [query[0].ftitle,
            query[0].fdescription,
            query[0].fstart_date,
            query[0].fover_date]


def get_tasks():
    query = Task.select()
    ret = {}
    for counter, item in enumerate(query.namedtuples()):
        ret[counter] = item
    return ret


def get_remainders():
    query = Remainder.select()
    return  query


def get_notes(id_task=None):
    query = (Note
             .select(Note.fvolume)
             .join_from(Note, Task)
             .where(Task.id_task == id_task))
    ret = list(item for item in query.namedtuples())
    return ret

