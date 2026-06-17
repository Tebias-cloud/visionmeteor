from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import sys

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image.getexif()

def get_geotagging(exif):
    if not exif:
        return None

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                return None
            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

exif = get_exif('backend/data/ejemplos_demostracion/1_huracan_vis.jpg')
geo = get_geotagging(exif)
print("EXIF Huracan:", exif.keys() if exif else "None")
print("GEO Huracan:", geo)

exif2 = get_exif('backend/data/ejemplos_demostracion/6_tarapaca_camanchaca_vis.jpg')
geo2 = get_geotagging(exif2)
print("EXIF Tarapaca:", exif2.keys() if exif2 else "None")
print("GEO Tarapaca:", geo2)
