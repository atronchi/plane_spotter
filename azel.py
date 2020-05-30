import dateutil.parser
from math import acos, asin, cos, pi, sin, sqrt
import pandas as pd

lle_332 = (37.495583, -122.239246, 15.0)  # 332 E St backyard
lle_ksql = (37.51, -122.25, 6.0)
lle_ksfo = (37.62, -122.38, 13.0)
lle_target = (37.50572, -122.30717, 8925.0)

def get_targets():
    import sqlite3
    con = sqlite3.connect('adsb_messages.db')
    df = pd.DataFrame.from_dict([
        dict(lat=lat, lon=lon, elev_ft=el, code=code, ts=ts)
        for code,ts,lon,lat,el in 
        con.execute("SELECT * FROM locations").fetchall()
        ])

    ae = [azel((row.lat, row.lon, row.elev_ft), verbose=False) for i,row in df.iterrows()]
    df['az'] = [a[0] for a in ae]
    df['el'] = [a[1] for a in ae]
    df['ts'] = df.ts.apply(dateutil.parser.parse)
    df = df.sort_values('ts')

    dt = []
    dazdt = []
    deldt = []
    for g,d in df.groupby('code'):
        d_t = d.ts.diff().apply(lambda x: x.total_seconds())
        dt.append(d_t)

        d_az = d.az.diff().apply(lambda x: x if x < 180 else x - 360)
        dazdt.append(d_az / d_t)

        d_el = d.el.diff().apply(lambda x: x if x < 180 else x - 360)
        deldt.append(d_el / d_t)
    df['dt'] = pd.concat(dt).sort_index()
    df['dazdt'] = pd.concat(dazdt).sort_index()
    df['deldt'] = pd.concat(deldt).sort_index()
    df['adazdt'] = df.dazdt.abs()
    df['adeldt'] = df.deldt.abs()

    return df

def diff_ae(d, ae='az', agg='max'):
    #for g,d in df.groupby('code'):
        d_t = d.ts.diff().apply(lambda x: x.total_seconds())

        if ae == 'az':
            d_az = d.az.diff().apply(lambda x: x if x < 180 else x - 360)
            dazdt = d_az / dt
            return dazdt.abs().agg(agg)
        else:
            d_el = d.el.diff().apply(lambda x: x if x < 180 else x - 360)
            deldt = d_el / dt
            return deldt.abs().agg(agg)

    

# https://www.google.com/maps/place/37%C2%B029'44.1%22N+122%C2%B014'21.3%22W/@37.4955844,-122.2397972,19z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d37.4955831!4d-122.2392459
def azel(lle_target, lle_station=None, verbose=True):
    if lle_station is None:
        lle_station = lle_332
    lat1, lon1, el1 = lle_station
    lat2, lon2, el2 = lle_target

    # http://tchester.org/sgm/analysis/peaks/how_to_get_view_params.html
    # https://www.edwilliams.org/avform.htm

    lat1, lon1, lat2, lon2 = (l * pi/180.0 for l in (lat1, lon1, lat2, lon2))

    # distances
    # https://www.edwilliams.org/avform.htm#Dist
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    #c = 2 * asin(min(1., sqrt(a)))
    d = 2 * asin(sqrt(a))

    R = 20.902e6 # ft, radius of Earth
    d_ft = R * d

    ft_per_nm = 6076.12
    d_nm = d_ft / ft_per_nm

    # azimuth
    # https://www.edwilliams.org/avform.htm#Crs
    x = acos( (sin(lat2) - sin(lat1)*cos(d) ) / (sin(d)*cos(lat1)) ) * 180/pi
    phi = x if sin(lon2-lon1) > 0 else 360 - x

    # elevation

    #lamda = (180/pi) * (asin((el2 - el1) / d) - asin(d / (2*R)))
    lamda = (180/pi) * ( (el2 - el1) / d_ft - d_ft / (2*R) )

    if verbose:
        print(f'''
        lle_station = {lle_station}
        lle_target = {lle_target}

        dlon = {dlon:1.6f}, dlat = {dlat:1.6f}
        distances: a = {a:3.2e}, d[rad] = {d:1.6f}, d[ft] = {d_ft:5.2f}, d[nm] = {d_nm:3.1f}
        azimuths: x = {x:3.2f}, phi[deg] = {phi:3.2f}
        elevation: lamda[deg] = {lamda:3.2f}

        {phi:3.2f}, {lamda:3.2f}
        ''')

    return phi, lamda, d_nm


#azel(lle_target)
azel(lle_ksfo, lle_ksql)
