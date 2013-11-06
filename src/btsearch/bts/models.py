from django.db import models


class Location(models.Model):
    id = models.AutoField(
        primary_key=True,
        db_column="LocationId",
    )
    region = models.ForeignKey(
        'Region',
        db_column="RegionId",
        related_name='locations',
    )
    town = models.CharField(
        max_length=128,
        db_column="Town",
    )
    address = models.CharField(
        max_length=512,
        db_column="Address",
    )
    latitude = models.CharField(
        max_length=16,
        blank=True,
        db_column="Latitude",
        db_index=True,
    )
    longitude = models.CharField(
        max_length=16,
        blank=True,
        db_column="Longitude",
        db_index=True,
    )
    latlng_hash = models.CharField(
        max_length=32,
        db_column="LatLngHash",
        verbose_name="GPS hash",
        db_index=True,
    )
    notes = models.CharField(
        max_length=255,
        db_column="LocationNotes",
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        db_column="DateAdded",
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=True,
        db_column="DateUpdated",
    )

    class Meta:
        db_table = 'Bts__Locations'
        ordering = ['town']

    def __unicode__(self):
        return u"{0}, {1}, {2}".format(self.region.name, self.town, self.address)

    def has_latlng_hash(self):
        return self.latlng_hash != ''

    has_latlng_hash.boolean = True
    has_latlng_hash.short_description = 'GPS?'

    def get_base_stations(self, **kwargs):
        if 'standard' in kwargs and 'band' in kwargs:
            return BaseStation.objects.distinct().filter(
                location=self,
                cell__standard__in=kwargs.get('standard'),
                cell__band__in=kwargs.get('band')
            )
        elif 'standard' in kwargs:
            return BaseStation.objects.distinct().filter(
                location=self,
                cell__standard__in=kwargs.get('standard')
            )
        elif 'band' in kwargs:
            return BaseStation.objects.distinct().filter(
                location=self,
                cell__band__in=kwargs.get('band')
            )
        return BaseStation.objects.filter(location=self)


class BaseStation(models.Model):
    ON_AIR, OFFLINE, UNDER_CONSTRUCTION, PLANNED, DISMANTLED = ('OnAir', 'Offline', 'UnderConstruction', 'Planned', 'Dismantled')
    PUBLISHED, APPROVED, QUEUED, REJECTED = ('Published', 'Approved', 'Queued', 'Rejected')

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

    id = models.AutoField(
        primary_key=True,
        db_column="BaseStationId",
    )
    network = models.ForeignKey(
        'Network',
        db_column="NetworkCode",
        related_name='base_stations',
    )
    location = models.ForeignKey(
        'Location',
        db_column="LocationId",
        related_name='base_stations',
    )
    location_details = models.CharField(
        max_length=255,
        db_column="LocationDetails",
    )
    station_id = models.CharField(
        max_length=16,
        blank=True,
        db_column="StationId",
        verbose_name="UKE StationId",
    )
    rnc = models.PositiveSmallIntegerField(
        db_column="Rnc",
        verbose_name="RNC",
    )

    # Are these 5 fields below *really* necessary??
    is_common_bcch = models.BooleanField(
        db_column="IsCommonBcch",
    )
    is_gsm = models.BooleanField(
        db_column="IsGsm",
    )
    is_umts = models.BooleanField(
        db_column="IsUmts",
    )
    is_cdma = models.BooleanField(
        db_column="IsCdma",
    )
    is_lte = models.BooleanField(
        db_column="IsLte",
    )
    # ^^ Really necessary? ^^

    notes = models.CharField(
        max_length=255,
        blank=True,
        db_column="BaseStationNotes",
    )
    station_status = models.CharField(
        max_length=32,
        db_column="StationStatus",
        choices=STATION_STATUS_CHOICES,
    )
    edit_status = models.CharField(
        max_length=32,
        db_column="EditStatus",
        choices=EDIT_STATUS_CHOICES,
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        db_column="DateAdded",
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=True,
        db_column="DateUpdated",
    )

    class Meta:
        db_table = 'Bts__BaseStations'

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
        return "{coords.latitude},{coords.longitude}".format(coords=self.location)

    def get_cells(self):
        return Cell.objects.filter(base_station=self)

    def get_supported_standards_and_bands(self):
        cells = self.get_cells()
        return cells.distinct().values('standard', 'band').exclude(standard='?').exclude(band='?').order_by('standard')

    def get_supported_standards(self):
        cells = self.get_cells()
        return cells.distinct().values('standard').exclude(standard='?')

    def get_cells_by_standard_and_band(self):
        cells = []
        for support in self.get_supported_standards_and_bands():
            cells.append({'standard': support['standard'],
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

    id = models.AutoField(
        primary_key=True,
        db_column="CellId",
    )
    base_station = models.ForeignKey(
        'BaseStation',
        db_column="BaseStationId",
        # related_name='cells'
    )
    standard = models.CharField(
        max_length=8,
        db_column="Standard",
        choices=STANDARDS,
    )
    band = models.CharField(
        max_length=8,
        db_column="Band",
        choices=BANDS,
    )
    ua_freq = models.PositiveSmallIntegerField(
        db_column="UaFreq",
        verbose_name="UaFreq",
    )
    lac = models.PositiveSmallIntegerField(
        db_column="Lac",
        verbose_name="LAC",
    )
    cid = models.PositiveSmallIntegerField(
        db_column="Cid",
        verbose_name="CID",
    )
    cid_long = models.PositiveIntegerField(
        db_column="CidLong",
        verbose_name="LongCID",
    )
    azimuth = models.PositiveSmallIntegerField(
        db_column="Azimuth",
        blank=True,
        # null=True
    )
    is_confirmed = models.BooleanField(
        db_column="IsConfirmed",
        verbose_name="Confirmed?",
    )
    notes = models.CharField(
        max_length=255,
        blank=True,
        db_column="CellNotes",
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        db_column="DateAdded",
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=True,
        db_column="DateUpdated",
    )
    date_ping = models.DateTimeField(
        blank=True,
        db_column="DatePing",
    )

    class Meta:
        db_table = 'Bts__Cells'

    def __unicode__(self):
        return u"{cell.standard}{cell.band} / {cell.lac} / {cell.cid}".format(cell=self)

    def network_name(self):
        return self.base_station.network

    network_name.short_description = 'Network'
    network_name.admin_order_field = 'base_station__network__name'


class Network(models.Model):
    code = models.CharField(
        primary_key=True,
        max_length=6,
        db_column="NetworkCode",
    )
    name = models.CharField(
        max_length=128,
        db_column="NetworkName",
    )
    operator = models.CharField(
        max_length=128,
        db_column="OperatorName",
    )
    country_code = models.CharField(
        max_length=2,
        db_column="CountryCodeIso",
    )

    class Meta:
        db_table = 'Bts__Networks'
        ordering = ['code']

    def __unicode__(self):
        return u'{network.name} ({network.code})'.format(network=self)


class Region(models.Model):
    id = models.AutoField(
        primary_key=True,
        db_column="RegionId",
    )
    name = models.CharField(
        max_length=64,
        db_column="RegionName",
    )
    country_code = models.CharField(
        max_length=2,
        db_column="CountryCodeIso",
    )

    class Meta:
        db_table = 'Bts__Regions'

    def __unicode__(self):
        return self.name


'''
--- LEGACY MODELS
--- VERY SOON TO BECOME OBSOLETE AND DEAD
'''


class LegacyBaseStation(models.Model):

    class Meta:
        db_table = 'BtsOld__All'

    id = models.AutoField(primary_key=True)
    network = models.ForeignKey('LegacyNetwork', db_column='siec_id')
    region = models.ForeignKey('LegacyRegion', db_column='wojewodztwo_id')
    town = models.CharField(max_length=255, db_column='miejscowosc')
    location = models.CharField(max_length=255, db_column='lokalizacja')
    standard = models.CharField(max_length=5)
    band = models.CharField(max_length=8, db_column='pasmo')
    lac = models.CharField(max_length=6)
    btsid = models.DecimalField(max_digits=10, decimal_places=0)
    cid1 = models.CharField(max_length=1)
    cid2 = models.CharField(max_length=1)
    cid3 = models.CharField(max_length=1)
    cid4 = models.CharField(max_length=1)
    cid5 = models.CharField(max_length=1)
    cid6 = models.CharField(max_length=1)
    cid7 = models.CharField(max_length=1)
    cid8 = models.CharField(max_length=1)
    cid9 = models.CharField(max_length=1)
    cid0 = models.CharField(max_length=1)
    notes = models.CharField(max_length=255, db_column='uwagi')
    date_updated = models.DateField(db_column='aktualizacja')
    station_id = models.CharField(max_length=20, db_column='StationId')
    rnc = models.CharField(max_length=5, db_column='RNC')
    carrier = models.CharField(max_length=6)
    longitude_uke = models.CharField(max_length=10, db_column='LONGuke')
    latitude_uke = models.CharField(max_length=10, db_column='LATIuke')
    longitude = models.CharField(max_length=10, db_column='LONGp')
    latitude = models.CharField(max_length=10, db_column='LATIp')


class LegacyNetwork(models.Model):

    class Meta:
        db_table = 'BtsOld__Networks'

    id = models.AutoField(primary_key=True)
    network_name = models.CharField(max_length=16, db_column='nazwa')

    def __unicode__(self):
        return self.network_name


class LegacyRegion(models.Model):

    class Meta:
        db_table = 'BtsOld__Regions'

    id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=128, db_column='nazwa')
    region_code = models.CharField(max_length=3, db_column='nazwa_short')

    def __unicode__(self):
        return self.region_name
