from django.db import models


class UkeLocation(models.Model):
    latitude = models.CharField(
        max_length=16,
        db_index=True,
    )
    longitude = models.CharField(
        max_length=16,
        db_index=True,
    )
    latlng_hash = models.CharField(
        max_length=32,
        unique=True,
        verbose_name="GPS hash",
        db_index=True,
    )
    location = models.ForeignKey(
        'bts.Location',
        blank=True,
        null=True,
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
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


class UkePermission(models.Model):
    uke_location = models.ForeignKey(
        'UkeLocation',
        related_name='permissions',
    )
    network = models.ForeignKey(
        'bts.Network',
        related_name='permissions',
    )
    station_id = models.CharField(
        max_length=16,
        db_index=True,
    )
    standard = models.CharField(
        max_length=16,
        db_index=True,
    )
    band = models.CharField(
        max_length=16,
        db_index=True,
    )
    town = models.CharField(
        max_length=255,
    )
    address = models.CharField(
        max_length=255,
    )
    case_number = models.CharField(
        max_length=64,
        db_index=True,
    )
    case_type = models.CharField(
        max_length=16,
    )
    expiry_date = models.CharField(
        max_length=10,
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=True,
    )

    class Meta:
        db_table = 'Uke__Permissions'

    def __unicode__(self):
        return '{0}, {1}'.format(self.network.code, self.case_number)


class UkeRawRecord(models.Model):
    operator_name = models.CharField(
        max_length=200,
    )
    case_number = models.CharField(
        primary_key=True,
        max_length=64,
    )
    case_type = models.CharField(
        max_length=16,
    )
    expiry_date = models.CharField(
        max_length=10,
    )
    longitude = models.CharField(
        max_length=16,
    )
    latitude = models.CharField(
        max_length=16,
    )
    town = models.CharField(
        max_length=255,
    )
    address = models.CharField(
        max_length=255,
    )
    station_id = models.CharField(
        max_length=8,
    )

    class Meta:
        db_table = 'Uke__RawRecords'

    def __unicode__(self):
        return self.case_number


class UkeOperator(models.Model):
    operator_name = models.CharField(
        max_length=64,
        unique=True,
    )
    network = models.ForeignKey(
        'bts.Network'
    )

    class Meta:
        db_table = 'Uke__OperatorMappings'

    def __unicode__(self):
        return u'{0} ({1})'.format(self.operator_name, self.network.name)
