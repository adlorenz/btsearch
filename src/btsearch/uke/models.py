from django.db import models


class UkeLocation(models.Model):

    class Meta:
        db_table = 'Uke__Locations'

    id = models.AutoField(primary_key=True, db_column="UkeLocationId")
    location = models.ForeignKey('bts.Location', blank=True, db_column='LocationId')
    latitude = models.CharField(max_length=16, db_column="Latitude")
    longitude = models.CharField(max_length=16, db_column="Longitude")
    latlng_hash = models.CharField(max_length=32, unique=True, db_column="LatLngHash", verbose_name="GPS hash")
    date_added = models.DateTimeField(auto_now_add=True, db_column="DateAdded")

    def __unicode__(self):
#        try:
#            return self.location.town
#        except:
#            permissions = self.get_permissions()
#            raw_record = permissions[0].record
#            return '[UKE] %s %s' % (raw_record.town, raw_record.address)

        # Returns nothing for performance reasons
        return ''

    def get_permissions(self, **kwargs):
        if 'standard' in kwargs and 'band' in kwargs:
            return UkePermission.objects.distinct().filter(uke_location=self, standard__in=kwargs['standard'], band__in=kwargs['band'])
        elif 'standard' in kwargs:
            return UkePermission.objects.distinct().filter(uke_location=self, standard__in=kwargs['standard'])
        elif 'band' in kwargs:
            return UkePermission.objects.distinct().filter(uke_location=self, band__in=kwargs['band'])
        else:
            return UkePermission.objects.filter(uke_location=self)

    def get_supported_standards_and_bands_by_network(self, network):
        permissions = self.get_permissions().filter(network=network)
        return permissions.distinct().values('standard', 'band').exclude(standard='?').exclude(band='?')

    def get_supported_standards_by_network(self, network):
        permissions = self.get_permissions().filter(network=network)
        return permissions.distinct().values('standard').exclude(standard='?')


class UkePermission(models.Model):

    class Meta:
        db_table = 'Uke__Permissions'

    id = models.AutoField(primary_key=True, db_column="UkePermissionId")
    uke_location = models.ForeignKey('UkeLocation', db_column='UkeLocationId')
    network = models.ForeignKey('bts.Network', db_column="NetworkCode")
    station_id = models.CharField(max_length=16, db_column='StationId')
    standard = models.CharField(max_length=16, db_column="Standard")
    band = models.CharField(max_length=16, db_column="Band")
    town = models.CharField(max_length=255, db_column='Location')
    address = models.CharField(max_length=255, db_column='LocationDetails')
    case_number = models.CharField(max_length=64, db_column='CaseNumber')
    case_type = models.CharField(max_length=1, db_column='CaseType')
    expiry_date = models.CharField(max_length=10, db_column='ExpiryDate')
    date_added = models.DateTimeField(auto_now_add=True, db_column="DateAdded")
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=True, db_column="DateUpdated")

    def __unicode__(self):
        return '%s, %s' % (self.network.code, self.case_number)


class UkeRecord(models.Model):

    class Meta:
        db_table = 'Uke__RawRecords'

    operator_name = models.CharField(max_length=64, db_column='Operator')
    case_number = models.CharField(primary_key=True, max_length=64, db_column='CaseNumber')
    case_type = models.CharField(max_length=1, db_column='CaseType')
    expiry_date = models.CharField(max_length=10, db_column='ExpiryDate')
    longitude = models.CharField(max_length=16, db_column='Longitude')
    latitude = models.CharField(max_length=16, db_column='Latitude')
    town = models.CharField(max_length=255, db_column='Location')
    address = models.CharField(max_length=255, db_column='LocationDetails')
    station_id = models.CharField(max_length=8, db_column='StationId')

    def __unicode__(self):
        return self.case_number
