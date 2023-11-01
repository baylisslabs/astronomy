"""
Sure, here's a Python function that utilizes the Skyfield module to determine the next moonrise time in Perth, WA:
"""
from datetime import datetime, timedelta
from pytz import timezone, utc
from skyfield import api, almanac


def get_next_moonrise():
    # Initialise Perth location and timezone information
    ts = api.load.timescale()
    tz = timezone("Australia/Perth")
    perth = api.wgs84.latlon(-31.9523, 115.8614)

    # Load ephemeris table data file
    eph = api.load("de421.bsp")

    # Get current time and define a search window of 24 hours
    now = datetime.now().astimezone()
    t0 = ts.from_datetime(now)
    t1 = ts.from_datetime(now + timedelta(hours=25))

    # Get a function return true if the Moon is risen or set at a given time, with an adjustment for the radius of the body
    is_up_predicate = almanac.risings_and_settings(
        eph, eph["Moon"], perth, radius_degrees=0.25
    )

    # Find the next rise and set times inside the time window
    ts, ys = almanac.find_discrete(t0, t1, is_up_predicate)

    # Extract the next rise time
    for t, y in zip(ts, ys):
        if y:
            return t.astimezone(tz)


"""
This code defines a function next_moonrise_perth() that calculates the next moonrise time in Perth, WA, using the Skyfield module. It first loads the Perth location and time zone information, loads the ephemeris data tables, then retrieves the current time. It then uses the risings_and_settings() routine to get a function giving the risen or set state for moon from the Perth observation point given a certain time. Then it the finds the first rise time in the next 24 hours. Finally, it converts the UTC time to Perth local time and returns that value.
"""
# test
print(get_next_moonrise())
