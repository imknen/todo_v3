from base.tool import createDB, updateDB, clearDB
from base.orm_models import Version_DB
from datetime import datetime
from base.my_requests import add_task, get_task


clearDB()
print()
createDB()
print()

updateDB()
print()

history = Version_DB.select()
print('History:')
for line in history:
    print(f'version:{line.fversion}\n'
          f'date:{line.fdate}\n'
          f'{line.fdescription}')

