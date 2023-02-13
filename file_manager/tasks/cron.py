from .models import Tasks
from datetime import datetime

def task_expiry_check():
    today = datetime.today().strftime('%m-%d-%Y')
    tasks_obj = Tasks.objects.all()
    for task in tasks_obj:
        exp_date = task.completion_date.strftime('%m-%d-%Y')

        if exp_date < today and task.task_status != 'Completed' :
            task.task_status = 'Overdue'
            task.save()
    print('===============>triggered')
            #add send email notification here!
