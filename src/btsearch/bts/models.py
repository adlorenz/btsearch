from django.db import models


class Location(models.Model):
    region = models.ForeignKey(
        'Region',
        related_name='locations',
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
        max_length=500,
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=True,
    )

    class Meta:
        ordering = ['town']

    def __unicode__(self):
        return u"{0}, {1}, {2}".format(self.region.name, self.town, self.address)

    def save(self, *args, **kwargs):
        # TODO:
        # - calculate / validate location_hash
        return super(Cell, self).save(*args, **kwargs)

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
    )
    location = models.ForeignKey(
        'Location',
        related_name='base_stations',
    )
    location_details = models.CharField(
        max_length=255,
    )
    station_id = models.CharField(
        max_length=16,
        blank=True,
        db_index=True,
        verbose_name="StationId",
    )
    rnc = models.PositiveSmallIntegerField(
        verbose_name="RNC",
    )

    # Are these 5 fields below *really* necessary??
    is_common_bcch = models.BooleanField(default=False)
    is_gsm = models.BooleanField(default=False)
    is_umts = models.BooleanField(default=False)
    is_cdma = models.BooleanField(default=False)
    is_lte = models.BooleanField(default=False)
    is_networks = models.BooleanField('Is NetWorks!', default=False, db_index=True)
    # ^^ Really necessary? ^^

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
    date_added = models.DateTimeField(
        auto_now_add=True,
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=True,
    )

    def __unicode__(self):
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
        cells = self.get_cells()
        return cells.distinct().values('standard', 'band').exclude(standard='?').exclude(band='?').order_by('standard')

    def get_supported_standards(self):
        cells = self.get_cells()
        return cells.distinct().values('standard').exclude(standard='?')

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
            cells.append({'standard': support['standard'],
                          'cells': self.get_cells().filter(standard=support.get('standard'))
                          })
        return cells


class Cell(models.Model):
    STANDARDS = (
        ('GSM', 'GSM'),
        ('UMTS', 'UMTS'),
        ('CDMA', 'CDMA'),
        ('LTE', 'LTE')
    )

    BANDS = (
        ('420', '420'),
        ('450', '450'),
        ('850', '850'),
        ('900', '900'),
        ('1800', '1800'),
        ('2100', '2100'),
        ('2600', '2600')
    )

    base_station = models.ForeignKey(
        'BaseStation',
        related_name='cells'
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
    )
    lac = models.PositiveSmallIntegerField(
        verbose_name="LAC",
    )
    cid = models.PositiveSmallIntegerField(
        verbose_name="CID",
    )
    cid_long = models.PositiveIntegerField(
        verbose_name="LongCID",
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
        auto_now_add=True,
    )
    date_ping = models.DateTimeField(
        blank=True,
    )

    def __unicode__(self):
        return u"ID: {cell.id} / {cell.standard}{cell.band} / {cell.lac} / {cell.cid}".format(cell=self)

    def save(self, *args, **kwargs):
        # TODO:
        # - calculate / validate cid, cid_long, rnc
        return super(Cell, self).save(*args, **kwargs)

    def network_name(self):
        return self.base_station.network

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

    def __unicode__(self):
        return u'{network.name} ({network.code})'.format(network=self)


class Region(models.Model):
    name = models.CharField(
        max_length=64,
    )
    country_code = models.CharField(
        max_length=2,
    )

    def __unicode__(self):
        return self.name


'''
--- LEGACY MODELS
--- VERY SOON TO BECOME OBSOLETE AND DEAD
'''


# class LegacyBaseStation(models.Model):

#     class Meta:
#         db_table = 'BtsOld__All'

#     id = models.AutoField(primary_key=True)
#     network = models.ForeignKey('LegacyNetwork', db_column='siec_id')
#     region = models.ForeignKey('LegacyRegion', db_column='wojewodztwo_id')
#     town = models.CharField(max_length=255, db_column='miejscowosc')
#     location = models.CharField(max_length=255, db_column='lokalizacja')
#     standard = models.CharField(max_length=5)
#     band = models.CharField(max_length=8, db_column='pasmo')
#     lac = models.CharField(max_length=6)
#     btsid = models.DecimalField(max_digits=10, decimal_places=0)
#     cid1 = models.CharField(max_length=1)
#     cid2 = models.CharField(max_length=1)
#     cid3 = models.CharField(max_length=1)
#     cid4 = models.CharField(max_length=1)
#     cid5 = models.CharField(max_length=1)
#     cid6 = models.CharField(max_length=1)
#     cid7 = models.CharField(max_length=1)
#     cid8 = models.CharField(max_length=1)
#     cid9 = models.CharField(max_length=1)
#     cid0 = models.CharField(max_length=1)
#     notes = models.CharField(max_length=255, db_column='uwagi')
#     date_updated = models.DateField(db_column='aktualizacja')
#     station_id = models.CharField(max_length=20, db_column='StationId')
#     rnc = models.CharField(max_length=5, db_column='RNC')
#     carrier = models.CharField(max_length=6)
#     longitude_uke = models.CharField(max_length=10, db_column='LONGuke')
#     latitude_uke = models.CharField(max_length=10, db_column='LATIuke')
#     longitude = models.CharField(max_length=10, db_column='LONGp')
#     latitude = models.CharField(max_length=10, db_column='LATIp')


# class LegacyNetwork(models.Model):

#     class Meta:
#         db_table = 'BtsOld__Networks'

#     id = models.AutoField(primary_key=True)
#     network_name = models.CharField(max_length=16, db_column='nazwa')

#     def __unicode__(self):
#         return self.network_name


# class LegacyRegion(models.Model):

#     class Meta:
#         db_table = 'BtsOld__Regions'

#     id = models.AutoField(primary_key=True)
#     region_name = models.CharField(max_length=128, db_column='nazwa')
#     region_code = models.CharField(max_length=3, db_column='nazwa_short')

#     def __unicode__(self):
#         return self.region_name
