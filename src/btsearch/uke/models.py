from django.db import models


class UkePermission(models.Model):
    id = models.AutoField(
        primary_key=True,
        db_column="UkePermissionId"
    )
    uke_location = models.ForeignKey(
        'UkeLocation',
        db_column='UkeLocationId'
    )
    network = models.ForeignKey(
        'bts.Network',
        db_column="NetworkCode"
    )
    station_id = models.CharField(
        max_length=16,
        db_column='StationId'
    )
    standard = models.CharField(
        max_length=16,
        db_column="Standard"
    )
    band = models.CharField(
        max_length=16,
        db_column="Band"
    )
    town = models.CharField(
        max_length=255,
        db_column='Location'
    )
    address = models.CharField(
        max_length=255,
        db_column='LocationDetails'
    )
    case_number = models.CharField(
        max_length=64,
        db_column='CaseNumber'
    )
    case_type = models.CharField(
        max_length=1,
        db_column='CaseType'
    )
    expiry_date = models.CharField(
        max_length=10,
        db_column='ExpiryDate'
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        db_column="DateAdded"
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=True,
        db_column="DateUpdated"
    )

    class Meta:
        db_table = 'Uke__Permissions'

    def __unicode__(self):
        return '{0}, {1}'.format(self.network.code, self.case_number)


class UkeLocation(models.Model):
    id = models.AutoField(
        primary_key=True,
        db_column="UkeLocationId"
    )
    latitude = models.CharField(
        max_length=16,
        db_column="Latitude"
    )
    longitude = models.CharField(
        max_length=16,
        db_column="Longitude"
    )
    latlng_hash = models.CharField(
        max_length=32,
        unique=True,
        db_column="LatLngHash",
        verbose_name="GPS hash"
    )
    location = models.ForeignKey(
        'bts.Location',
        blank=True,
        null=True,
        db_column='LocationId'
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        db_column="DateAdded"
    )

    class Meta:
        db_table = 'Uke__Locations'

    def __unicode__(self):
       # try:
       #     return self.location.town
       # except:
       #     permissions = self.get_permissions()
       #     raw_record = permissions[0].record
       #     return '[UKE] %s %s' % (raw_record.town, raw_record.address)

        # Returns nothing for performance reasons
        # TODO: Refactor it.
        return ''

    def get_permissions(self, **kwargs):
        qs = UkePermission.objects.distinct()
        if 'standard' in kwargs and 'band' in kwargs:
            return qs.filter(
                uke_location=self,
                standard__in=kwargs.get('standard'),
                band__in=kwargs.get('band')
            )
        elif 'standard' in kwargs:
            return qs.filter(
                uke_location=self,
                standard__in=kwargs.get('standard')
            )
        elif 'band' in kwargs:
            return qs.filter(
                uke_location=self,
                band__in=kwargs.get('band')
            )
        return UkePermission.objects.filter(uke_location=self)

    def get_supported_standards_and_bands_by_network(self, network):
        permissions = self.get_permissions().filter(network=network)
        return permissions.distinct().values('standard', 'band').exclude(standard='?', band='?')

    def get_supported_standards_by_network(self, network):
        permissions = self.get_permissions().filter(network=network)
        return permissions.distinct().values('standard').exclude(standard='?')


class UkeRawRecord(models.Model):
    operator_name = models.CharField(
        max_length=64,
        db_column='Operator'
    )
    case_number = models.CharField(
        primary_key=True,
        max_length=64,
        db_column='CaseNumber'
    )
    case_type = models.CharField(
        max_length=1,
        db_column='CaseType'
    )
    expiry_date = models.CharField(
        max_length=10,
        db_column='ExpiryDate'
    )
    longitude = models.CharField(
        max_length=16,
        db_column='Longitude'
    )
    latitude = models.CharField(
        max_length=16,
        db_column='Latitude'
    )
    town = models.CharField(
        max_length=255,
        db_column='Location'
    )
    address = models.CharField(
        max_length=255,
        db_column='LocationDetails'
    )
    station_id = models.CharField(
        max_length=8,
        db_column='StationId'
    )

    class Meta:
        db_table = 'Uke__RawRecords'

    def __unicode__(self):
        return self.case_number
