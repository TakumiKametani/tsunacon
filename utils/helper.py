import datetime

def get_upload_to(instance, filename):
    now = datetime.datetime.now()
    return f'contracts/{now.year}/{now.month}/{filename}'
