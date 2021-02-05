import csv
import shutil
from io import StringIO
from random import randint

from celery import shared_task

from .models import Dataset


@shared_task
def create_csv_2(dataset_pk, rows_amount, column_separator, columns):
    try:
        parsed_cols = []
        split_columns = columns.split(';')
        for c in split_columns:
            c = c.split(':::')
            parsed_cols.append([c[1:]])
        columns = parsed_cols[:-1]

        csv_file = StringIO()
        wr = csv.writer(csv_file, delimiter=column_separator, quoting=csv.QUOTE_MINIMAL)
        wr.writerow([c[0][0] for c in columns])
        for i in range(int(rows_amount)):
            row = []
            for c in columns:
                if len(c[0]) == 1:
                    row.append('qwerty')
                elif len(c[0]) == 3:
                    row.append(randint(int(c[0][1]), int(c[0][2])))
            wr.writerow(row)

        d = Dataset.objects.get(pk=dataset_pk)
        d.status = 'Ready'
        d.csv_file.save('dataset.csv', csv_file)

        with open('C:\\Users\\kn\\Desktop\\file.csv', 'w') as fd:
            csv_file.seek(0)
            shutil.copyfileobj(csv_file, fd)

    except Exception:
        Dataset.objects.get(pk=dataset_pk).delete()