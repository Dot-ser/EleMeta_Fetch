from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def clean_metadata(obj):
    if isinstance(obj, bytes):
        try:
            return obj.decode('utf-8', errors='ignore')
        except Exception:
            return str(obj)
    elif hasattr(obj, 'numerator') and hasattr(obj, 'denominator'):
        return float(obj)
    elif isinstance(obj, dict):
        return {clean_metadata(k): clean_metadata(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple, set)):
        return [clean_metadata(item) for item in obj]
    else:
        return obj

def get_decimal_from_dms(dms, ref):
    def to_float(x):
        # Handle tuples like (num, denom)
        try:
            if isinstance(x, tuple) and len(x) == 2 and x[1] != 0:
                return float(x[0]) / float(x[1])
        except Exception:
            pass
        # Objects with numerator/denominator
        if hasattr(x, 'numerator') and hasattr(x, 'denominator'):
            try:
                return float(x.numerator) / float(x.denominator)
            except Exception:
                try:
                    return float(x)
                except Exception:
                    return 0.0
        try:
            return float(x)
        except Exception:
            return 0.0

    degrees = to_float(dms[0])
    minutes = to_float(dms[1])
    seconds = to_float(dms[2])
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def extract_gps_info(gps_info):
    gps_data = {}
    if not gps_info:
        return gps_data

    gps = {}
    for key in gps_info.keys():
        decoded = GPSTAGS.get(key, key)
        gps[decoded] = gps_info[key]

    lat = lon = None
    # Helper to normalize components to floats
    def normalize_dms(dms_seq):
        vals = []
        for x in dms_seq:
            try:
                # tuple (num, denom)
                if isinstance(x, tuple) and len(x) == 2 and x[1] != 0:
                    vals.append(float(x[0]) / float(x[1]))
                    continue
            except Exception:
                pass
            if hasattr(x, 'numerator') and hasattr(x, 'denominator'):
                try:
                    vals.append(float(x.numerator) / float(x.denominator))
                    continue
                except Exception:
                    pass
            try:
                vals.append(float(x))
            except Exception:
                # Fallback
                vals.append(0.0)
        return vals

    if 'GPSLatitude' in gps and 'GPSLatitudeRef' in gps:
        lat = get_decimal_from_dms(normalize_dms(gps['GPSLatitude']), gps['GPSLatitudeRef'])
    if 'GPSLongitude' in gps and 'GPSLongitudeRef' in gps:
        lon = get_decimal_from_dms(normalize_dms(gps['GPSLongitude']), gps['GPSLongitudeRef'])

    if lat is not None and lon is not None:
        gps_data['latitude'] = lat
        gps_data['longitude'] = lon

    return gps_data

def get_image_metadata(image_path):
    metadata = {}
    try:
        img = Image.open(image_path)
        info = img._getexif()
        if info:
            gps_info = None
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == 'GPSInfo':
                    gps_info = value
                # Ensure top-level keys are strings to avoid mixed-type
                # comparisons when serializing/sorting for JSON.
                metadata[str(decoded)] = clean_metadata(value)

            # If GPS exists, extract nice location
            if gps_info:
                gps_location = extract_gps_info(gps_info)
                if gps_location:
                    metadata['Location'] = gps_location

    except Exception as e:
        metadata['error'] = str(e)
    return metadata
