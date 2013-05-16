import re
import time
import datetime
import cjson
import pytz


#--- JSON reading ----------------------------------------------
def read(data):
    if data:
        data = data.replace(r'\/', '/')
    d = cjson.decode(data)
    return d


#--- JSON writing ----------------------------------------------
def write(obj, js_date=False, in_local_timezone=False):
    result = write_cjson_our(obj, js_date, in_local_timezone)

    #Remove unicode extra space, breaks JS
    result = result.replace(u"\u2028", '\\n')

    return result.replace('/', '\\/')


#--- CJSON related ----------------------------------------------
RE_DATE = re.compile('"DATE\[\[(.+?)\]\]"')
def write_cjson_our(obj, js_date, in_local_timezone=False):
    try:
        result = cjson.encode(obj)
    except:
        raise

    def _convert_date(match, *k):
        only_date = match.group(1).split(".")[0]
        only_date = re.sub('\+\d\d:\d\d', '', only_date)

        try:
            date_obj = time.strptime(only_date, "%Y-%m-%d %H:%M:%S")
            with_time = True
        except ValueError:
            date_obj = time.strptime(only_date, "%Y-%m-%d")
            with_time = False

        # Format as local time if it's an all day event
        if with_time:
            if in_local_timezone or date_obj.tm_hour == 23 and date_obj.tm_min == 59 and date_obj.tm_sec == 59:
                format = '%a %d %b %Y %H:%M:%S'
            else:
                format = '%a %d %b %Y %H:%M:%S +0000'
        else:
            format = '%a %d %b %Y'

        try:
            res = time.strftime(format, date_obj)
        except ValueError:
            return 'null'

        if js_date:
            return 'new Date("%s")' % res
        else:
            return '"%s"' % res

    return RE_DATE.sub(_convert_date, result)

def parse_date(str_date):
    """
    If `str_date` is a string then it's is formated with datetime.strptime (using the format that jsonist.write uses).
    It will throw a ValueError if the date can't be parsed using datetime.strptime.
    """
    result = None

    if not hasattr(str_date, 'strftime'):
        try:
            result = datetime.datetime.strptime(str_date, "%a %d %b %Y %H:%M:%S +0000")
        except ValueError:
            result = datetime.datetime.strptime(str_date, "%a %d %b %Y %H:%M:%S")

    if result:
        return result.replace(tzinfo=pytz.UTC)
    else:
        raise ValueError()
