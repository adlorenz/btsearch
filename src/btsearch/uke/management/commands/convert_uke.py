from decimal import Decimal, getcontext
getcontext().prec = 8  # Used to calculate decimal geographical coordinates

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from btsearch import services
from btsearch.uke import models


class Command(BaseCommand):
    args = ''
    help = 'Converts RawRecord to Location+Permission models'

    def handle(self, *args, **options):
        self.stdout.write('Processing raw UKE data to models...')

        ctr = 0
        ctr_locations = 0
        ctr_permissions = 0

        rawrecords = models.RawRecord.objects.all()  # [:10]
        self.stdout.write('Number of records to process: %s' %
                          rawrecords.count())

        for rawrecord in rawrecords:
            lat, lng = self.get_decimal_coordinates(rawrecord.latitude, rawrecord.longitude)
            location_hash = services.LocationHasherService(lat, lng).get()
            try:
                location = models.Location.objects.get(location_hash=location_hash)
            except ObjectDoesNotExist:
                location_dict = {
                    'latitude': lat,
                    'longitude': lng,
                    'latitude_uke': rawrecord.latitude,
                    'longitude_uke': rawrecord.longitude,
                    'location_hash': location_hash,
                }
                location = models.Location(**location_dict)
                location.save()
                ctr_locations += 1

            try:
                permission = models.Permission.objects.get(case_number=rawrecord.case_number)
                # TODO: Compare existing permission record with raw data and save as appropriate
            except ObjectDoesNotExist:
                operator = self.fetch_operator(rawrecord.operator_name)
                standard, band = self.get_standard_band(rawrecord.case_number)
                if operator:
                    permission_dict = {
                        'location': location,
                        'operator': operator,
                        'network': operator.network,
                        'station_id': rawrecord.station_id,
                        'standard': standard,
                        'band': band,
                        'town': rawrecord.town,
                        'address': rawrecord.address,
                        'case_number': rawrecord.case_number,
                        'case_type': rawrecord.case_type,
                        'expiry_date': rawrecord.expiry_date,
                    }
                    permission = models.Permission(**permission_dict)
                    permission.save()
                    ctr_permissions += 1

            ctr += 1
            if ctr % 1000 == 0:
                self.stdout.write('- records processed: %s; added locations: %s; added permissions: %s' % (ctr, ctr_locations, ctr_permissions))

        self.stdout.write('Total records: %s; locations: %s; permissions: %s' % (ctr, ctr_locations, ctr_permissions))
        self.stdout.write('Job done')

    def get_decimal_coordinates(self, lat, lng):
        # Convert geographical coordinates to decimal values
        coords = []
        for coord in [lat, lng]:
            degrees = Decimal(coord[0:2])
            minutes = Decimal(coord[3:5])
            seconds = Decimal(coord[5:7])
            coords.append(Decimal(degrees + (minutes + seconds / 60) / 60))
        return coords

    def get_standard_band(self, case_number):
        # Example case_number = UMTS2100/4/0015/4/13
        # => standard=UMTS, band=2100
        standard = []
        band = []
        try:
            for c in case_number.split('/')[0]:
                if c.isalpha():
                    standard.append(c)
                else:
                    band.append(c)
        except:
            self.stderr.write('Could not extract standard/band from case_number="{0}"'.format(case_number))
        return ''.join(standard), ''.join(band)

    def fetch_operator(self, operator_name):
        try:
            operator = models.Operator.objects.get(operator_name=operator_name)
        except ObjectDoesNotExist:
            operator = None
            self.stderr.write('Could not find network matching operator_name="{0}"'.format(operator_name))
            # raise CommandError(
            #     'Could not find network matching operator_name="{0}"'.format(operator_name))
        return operator
