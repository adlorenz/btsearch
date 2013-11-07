from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from ... import models


class Command(BaseCommand):
    args = ''
    help = 'Converts UkeRawRecord to UkeLocation+UkePermission'

    def handle(self, *args, **options):
        uke_records = models.UkeRawRecord.objects.all()[:10]
        for uke_record in uke_records:
            self.stdout.write(uke_record.operator_name)
            self.stdout.write(uke_record.case_number)
            try:
                operator = models.UkeOperator.objects.get(operator_name=uke_record.operator_name)
                self.stdout.write('Matching network: {operator.network.name}'.format(operator=operator))
            except ObjectDoesNotExist:
                self.stderr.write('Could not find network matching operator_name="{0}"'.format(uke_record.operator_name))
