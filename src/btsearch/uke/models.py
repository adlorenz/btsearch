from django.db import models


class Location(models.Model):
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        db_index=True,
    )
    longitude = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        db_index=True,
    )
    latitude_uke = models.CharField(
        max_length=16,
    )
    longitude_uke = models.CharField(
        max_length=16,
    )
    location_hash = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        verbose_name="GPS hash",
    )
    # We don't really need that relation right now...
    #
    # location = models.ForeignKey(
    #     'bts.Location',
    #     blank=True,
    #     null=True,
    # )
    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    def __unicode__(self):
        return ''

    def get_permissions(self, **kwargs):
        # TODO: This method is probably redundant.
        qs = Permission.objects.distinct()
        if 'standard' in kwargs and 'band' in kwargs:
            return qs.filter(
                location=self,
                standard__in=kwargs.get('standard'),
                band__in=kwargs.get('band')
            )
        elif 'standard' in kwargs:
            return qs.filter(
                location=self,
                standard__in=kwargs.get('standard')
            )
        elif 'band' in kwargs:
            return qs.filter(
                location=self,
                band__in=kwargs.get('band')
            )
        return Permission.objects.filter(location=self)

    def get_supported_standards_and_bands_by_network(self, network):
        permissions = self.get_permissions().filter(operator__network=network)
        return permissions.distinct().values('standard', 'band').exclude(standard='?', band='?')

    def get_supported_standards_by_network(self, network):
        permissions = self.get_permissions().filter(operator__network=network)
        return permissions.distinct().values('standard').exclude(standard='?')


class Permission(models.Model):
    location = models.ForeignKey(
        'Location',
        related_name='permissions',
    )
    operator = models.ForeignKey(
        'Operator',
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
        unique=True,
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

    def __unicode__(self):
        return '{0}, {1}'.format(self.network.code, self.case_number)

    @property
    def network(self):
        return self.operator.network


class Operator(models.Model):
    operator_name = models.CharField(
        max_length=64,
        unique=True,
    )
    network = models.ForeignKey(
        'bts.Network',
        related_name='uke_operators',
    )

    def __unicode__(self):
        return u'{0} ({1})'.format(self.operator_name, self.network.name)


class RawRecord(models.Model):
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

    def __unicode__(self):
        return self.case_number
