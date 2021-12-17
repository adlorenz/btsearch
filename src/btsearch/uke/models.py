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
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['id']

    def get_associated_objects(self, **filters):
        # Returns permissions belonging to this location
        qs = Permission.objects.filter(location=self)
        return qs.filter(**filters)


class Permission(models.Model):
    location = models.ForeignKey(
        'Location',
        related_name='permissions',
        on_delete=models.CASCADE
    )
    operator = models.ForeignKey(
        'Operator',
        related_name='permissions',
        on_delete=models.CASCADE
    )
    network = models.ForeignKey(
        'bts.Network',
        related_name='permissions',
        null=True,
        on_delete=models.CASCADE
    )  # Field 'network' is added to Permission model to improve database performance
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
    case_number_orig = models.CharField(
        max_length=64,
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
    )

    def __str__(self):
        return '{0}, {1}'.format(self.network.code, self.case_number)

    def case_number_display(self):
        return self.case_number_orig if self.case_number_orig else self.case_number

    # @property
    # def network(self):
        # This method/property is used in MapIconService
        # return self.operator.network


class Operator(models.Model):
    operator_name = models.CharField(
        max_length=64,
        unique=True,
    )
    network = models.ForeignKey(
        'bts.Network',
        related_name='uke_operators',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return u'{0} ({1})'.format(self.operator_name, self.network.name)


class RawRecord(models.Model):
    operator_name = models.CharField(
        max_length=200,
    )
    case_number = models.CharField(
        primary_key=True,
        max_length=64,
    )
    case_number_orig = models.CharField(
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

    def __str__(self):
        return self.case_number
