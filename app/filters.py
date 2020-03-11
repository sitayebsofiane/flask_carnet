from datetime import datetime
from app import app


def make_datetime_obj_from_str(dt):
    date, time = str(dt).split(' ')
    yyyy, mm, dd = list(map(lambda x: int(x), date.split('-')))
    h, m, s = list(map(lambda x: int(x), time.split(':')))
    return datetime(yyyy, mm, dd, h, m, s)


# Timesince in jinja template: flask
@app.template_filter()
def timesince(dt, default="just now"):

    """
        Returns string representing "time since" e.g.
        3 days ago, 5 hours ago etc.
        Usage in template.
            example: {{ time|timesince }}
    """
    dt = make_datetime_obj_from_str(dt)
    now = datetime.utcnow()
    diff = now - dt
    
    periods = (
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:

        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default