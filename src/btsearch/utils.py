import hashlib


def get_location_hash(lat, lng):
    string = "{0}{1}".format(str(lat), str(lng))
    return hashlib.md5(string).hexdigest()
