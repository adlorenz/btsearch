# coding=utf-8
from django.db import models


class Location(models.Model):
    region = models.ForeignKey(
        'Region',
        related_name='locations',
        on_delete=models.CASCADE
    )
    town = models.CharField(
        max_length=128,
    )
    address = models.CharField(
        max_length=512,
    )
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
    location_hash = models.CharField(
        max_length=32,
        db_index=True,
    )
    notes = models.CharField(
        blank=True,
        max_length=500,
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
    )
    date_updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['town']

    def __str__(self):
        return u"{0}, {1}, {2}".format(self.region.name, self.town, self.address)

    def has_location_hash(self):
        return self.location_hash != ''

    has_location_hash.boolean = True
    has_location_hash.short_description = 'GPS?'

    def get_associated_objects(self, **filters):
        # Returns base stations belonging to this location
        qs = BaseStation.objects.distinct().filter(location=self)
        return qs.filter(**filters)


class BaseStation(models.Model):
    ON_AIR, OFFLINE, UNDER_CONSTRUCTION, PLANNED, DISMANTLED = (
        'OnAir',
        'Offline',
        'UnderConstruction',
        'Planned',
        'Dismantled'
    )
    PUBLISHED, APPROVED, QUEUED, REJECTED = (
        'Published',
        'Approved',
        'Queued',
        'Rejected'
    )

    STATION_STATUS_CHOICES = (
        (ON_AIR, ON_AIR),
        (OFFLINE, OFFLINE),
        (UNDER_CONSTRUCTION, UNDER_CONSTRUCTION),
        (PLANNED, PLANNED),
        (DISMANTLED, DISMANTLED)
    )

    EDIT_STATUS_CHOICES = (
        (PUBLISHED, PUBLISHED),
        (APPROVED, APPROVED),
        (QUEUED, QUEUED),
        (REJECTED, REJECTED)
    )

    network = models.ForeignKey(
        'Network',
        related_name='base_stations',
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        'Location',
        related_name='base_stations',
        on_delete=models.CASCADE
    )
    location_details = models.CharField(
        max_length=255,
        blank=True
    )
    station_id = models.CharField(
        verbose_name="StationId",
        max_length=16,
        blank=True,
        db_index=True,
        help_text='Wewnętrzny identyfikator stacji operatora'
    )
    rnc = models.PositiveSmallIntegerField(
        verbose_name="RNC",
        default=0,
        help_text='Radio Network Controller (dla stacji UMTS)'
    )
    enbi = models.PositiveIntegerField(
        verbose_name='eNBID',
        default=0,
        help_text='eNodeB ID (dla stacji LTE)'
    )

    # Are these 5 fields below *really* necessary??
    is_common_bcch = models.BooleanField(default=False)
    is_gsm = models.BooleanField(default=False)
    is_umts = models.BooleanField(default=False)
    is_cdma = models.BooleanField(default=False)
    is_lte = models.BooleanField(default=False)
    # ^^ Really necessary? ^^

    is_networks = models.BooleanField(
        'Is NetWorks!',
        default=False,
        db_index=True
    )
    notes = models.CharField(
        max_length=500,
        blank=True,
    )
    station_status = models.CharField(
        max_length=32,
        choices=STATION_STATUS_CHOICES,
    )
    edit_status = models.CharField(
        max_length=32,
        choices=EDIT_STATUS_CHOICES,
    )
    # permissions = models.ManyToManyField(
    #     'uke.Permission',
    #     verbose_name=u'UKE permissions',
    #     through='BaseStationPermission',
    #     related_name='base_stations',
    # )
    date_added = models.DateTimeField(
        auto_now_add=True,
    )
    date_updated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return u"{0} / {1} / {2}, {3}".format(
            self.network.name,
            self.location.region.name,
            self.location.town,
            self.location.address
        )

    def region_name(self):
        return self.location.region.name

    region_name.short_description = 'Region'
    region_name.admin_order_field = 'location__region__name'

    def town_name(self):
        return self.location.town

    town_name.short_description = 'Town'
    town_name.admin_order_field = 'location__town'

    def address_name(self):
        return self.location.address

    address_name.short_description = 'Address'
    address_name.admin_order_field = 'location__address'

    def location_coords(self):
        return u"{coords.latitude},{coords.longitude}".format(coords=self.location)

    def get_cells(self):
        qs = Cell.objects.filter(base_station=self)
        return qs.order_by('standard', 'band', 'ua_freq', 'cid')

    def get_supported_standards_and_bands(self):
        cells = self.get_cells().distinct()
        return cells.values('standard', 'band').exclude(standard='?').order_by('standard')

    def get_supported_standards(self):
        cells = self.get_cells().distinct()
        return cells.values('standard').exclude(standard='?').order_by('standard')

    def get_cells_by_standard_and_band(self):
        cells = []
        for support in self.get_supported_standards_and_bands():
            cells.append({
                'standard': support['standard'],
                'band': support['band'],
                'cells': self.get_cells().filter(standard=support.get('standard'), band=support.get('band'))
            })
        return cells

    def get_cells_by_standard(self):
        cells = []
        for support in self.get_supported_standards():
            cells.append({
                'standard': support['standard'],
                'cells': self.get_cells().filter(standard=support.get('standard'))
            })
        return cells


class Cell(models.Model):
    STANDARDS = (
        ('GSM', 'GSM'),
        ('UMTS', 'UMTS'),
        ('CDMA', 'CDMA'),
        ('LTE', 'LTE'),
        ('5G', '5G'),
        ('IOT', 'IOT')
        )

    BANDS = (
        ('420', '420'),
        ('450', '450'),
        ('800', '800'),
        ('850', '850'),
        ('900', '900'),
        ('1800', '1800'),
        ('2100', '2100'),
        ('2600', '2600'),
        ('3500', '3500')
    )

    base_station = models.ForeignKey(
        'BaseStation',
        related_name='cells',
        on_delete=models.CASCADE
    )
    standard = models.CharField(
        max_length=8,
        choices=STANDARDS,
        db_index=True,
    )
    band = models.CharField(
        max_length=8,
        choices=BANDS,
        db_index=True,
    )
    ua_freq = models.PositiveSmallIntegerField(
        verbose_name="UaFreq",
        default=0,
        blank=True,
        help_text=u'Częstotliwość nośnej (kanał RF)',
    )
    lac = models.PositiveSmallIntegerField(
        verbose_name="LAC",
        default=0,
        blank=True,
    )
    cid = models.PositiveSmallIntegerField(
        verbose_name="CID/CLID",
        default=0,
        blank=True,
        help_text='CellID / Cell Local ID (uniwersalny)',
    )
    cid_long = models.PositiveIntegerField(
        verbose_name="Long CID/E-CID",
        default=0,
        blank=True,
        help_text='UMTS: RNC*65536+CID; LTE: eNBID*256+CLID',
    )
    azimuth = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )
    is_confirmed = models.BooleanField(
        verbose_name="Confirmed?",
    )
    notes = models.CharField(
        max_length=500,
        blank=True,
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
    )
    date_updated = models.DateTimeField(
        auto_now=True,
    )
    date_ping = models.DateTimeField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return u"ID: {cell.id} / {cell.standard}{cell.band} / {cell.lac} / {cell.cid}".format(cell=self)

    def save(self, *args, **kwargs):
        self._sanitize_blank_values()
        return super(Cell, self).save(*args, **kwargs)

    def network_name(self):
        return self.base_station.network

    def _sanitize_blank_values(self):
        if not self.lac:
            self.lac = 0
        if not self.cid:
            self.cid = 0
        if not self.cid_long:
            self.cid_long = 0

    network_name.short_description = 'Network'
    network_name.admin_order_field = 'base_station__network__name'


class Network(models.Model):
    code = models.CharField(
        primary_key=True,
        max_length=6,
    )
    name = models.CharField(
        max_length=128,
    )
    operator_name = models.CharField(
        max_length=128,
    )
    country_code = models.CharField(
        max_length=2,
    )

    class Meta:
        ordering = ['code']

    def __str__(self):
        return u'{network.name} ({network.code})'.format(network=self)


class Region(models.Model):
    name = models.CharField(
        max_length=64,
    )
    code = models.CharField(
        max_length=3,
    )
    country_code = models.CharField(
        max_length=2,
    )

    def __str__(self):
        return self.name


class BaseStationPermission(models.Model):
    base_station = models.ForeignKey(
        'BaseStation',
        verbose_name=u'Base station',
        related_name='permissions',
        on_delete=models.CASCADE
    )
    permission = models.ForeignKey(
        'uke.Permission',
        verbose_name=u'UKE Permission',
        related_name='base_stations',
        on_delete=models.CASCADE
    )
    station_id = models.CharField(
        max_length=16,
        db_index=True,
        verbose_name="StationId",
    )

    class Meta:
        unique_together = ['base_station', 'permission', 'station_id']
