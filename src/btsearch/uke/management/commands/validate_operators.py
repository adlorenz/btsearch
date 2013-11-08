from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from btsearch.uke import models


class Command(BaseCommand):
    args = ''
    help = 'Checks whether any of the operator names in the raw UKE data is missing from Operator model'

    def handle(self, *args, **options):
        self.stdout.write('Validation starts...')
        rawrecords = models.RawRecord.objects.values('operator_name').distinct().order_by('operator_name')
        for rawrecord in rawrecords:
            self.stdout.write(' - %s' % rawrecord['operator_name'])
            try:
                models.Operator.objects.get(operator_name=rawrecord['operator_name'])
            except ObjectDoesNotExist:
                self.stderr.write('- operator %s not matched in Operator model' % rawrecord['operator_name'])

        self.stdout.write('Job done')
