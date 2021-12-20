import json
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Soluciona problemas con los errores de duplicidad en los fichero dumpdata y los uuid'
    
    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        first_user_id = 1
        newData = []
        uniques = []
        with open(options['file']) as fr:
            data = json.load(fr)
        for line in data:
            if line['model'] == 'authtoken.token':
                continue
                # print(line['fields']['user'])
                # if line['fields']['user'] in uniques:
                #     continue
                # uniques.append(line['fields']['user'])
                # line['fields']['user'] = first_user_id
                # first_user_id += 1 
            newData.append(line)
        with open('/tmp/salida.json', 'w') as fw:
            json.dump(newData, fw)