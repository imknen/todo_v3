from base.my_requests import add_task, add_remainder, add_note
from datetime import datetime


id_t = add_task(['title', 'description', datetime.now()])

data = [datetime.now(), 'title', 'messasge', ]
data1 = 'data'

for i in range(5):
    add_remainder(data, id_t)
    add_note(data1, id_t)

for i in range(3):
    add_remainder(data)
    add_note(data1)
