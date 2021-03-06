#!/usr/bin/python3

import configparser
import warnings
import numpy as np
import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from astropy.utils import iers
from astropy.utils.exceptions import AstropyWarning

warnings.simplefilter('ignore', category=AstropyWarning)
iers.conf.auto_download = False  


parameters = configparser.ConfigParser()
parameters.read('config.ini')
Sp_type = 'cat/'+parameters['settings']['Sp_type']+'.csv'
if Sp_type[4] == 'O' and Sp_type[6] == 'V':
    Sp_type = Sp_type.replace(Sp_type[5],'')
Time_of_observation = parameters['settings']['Time']
M_min = float(parameters['settings']['M_min'])
M_max = float(parameters['settings']['M_max'])
RA_min = parameters['settings']['RA_min']
DEC_min = parameters['settings']['DEC_min']
RA_max = parameters['settings']['RA_max']
DEC_max = parameters['settings']['DEC_max']
Alt_min = float(parameters['settings']['Alt_min'])
Az_min = float(parameters['settings']['Az_min'])
Alt_max = float(parameters['settings']['Alt_max'])
Az_max = float(parameters['settings']['Az_max'])
Sort = parameters['settings']['Sort']

def getAz(t, data):
    KGO = EarthLocation(lat=43.74594*u.deg, lon=42.66832*u.deg, height=2112*u.m)
    utcoffset = 3*u.hour
    time = Time(t) - utcoffset
    CoordAZ = SkyCoord(data['RA_J2000'].values, data['DEC_J2000'].values,
                       unit = (u.hourangle, u.deg)).transform_to(
                        AltAz(obstime=time,location=KGO))
    return CoordAZ.alt, CoordAZ.az



def filter_data(data):
    #data['R'] = 1000/data['Parallax']
    #data['A'] = data['V_MAG']-0.03 + 5*np.log10(data['Parallax']/128.93)
    #data['J'] = data['V_MAG'] - data['A'] + data['A']*0.865/3.08
    del(data['CCDM'])
    del(data['Dist'])
    del(data['M'])
    del(data['Parallax'])
    del(data['PM_RA'])
    del(data['PM_DEC'])
    data['Alt'], data['Az'] = getAz(Time_of_observation, data)
    data['Az'] = data['Az'] - 180.0
    data['Az'][data['Az'] < 0] = data['Az'][data['Az'] < 0] + 360.0
    data = data[data['V_MAG'] < M_max]
    data = data[data['V_MAG'] >= M_min]
    '''data = data[data['RA_J2000'] < RA_max]
    data = data[data['RA_J2000'] >= RA_min]
    data = data[data['DEC_J2000'] < DEC_max]
    data = data[data['DEC_J2000'] >= DEC_min]'''
    data = data[data['Alt'] < Alt_max]
    data = data[data['Alt'] >= Alt_min]
    data = data[data['Az'] < Az_max]
    data = data[data['Az'] >= Az_min]
    data = data.sort_values(Sort)
    
    return data






Data = pd.read_csv(Sp_type, sep='\s+', dtype={'RA_J2000':np.str,'DEC_J2000':np.str})

Data = filter_data(Data)


if Data.empty:
    print("""I'm sorry, there's no suitable stars in our catalogue.
             But you can read a limeric instead:
             
             A russian stargazer Andrey
             Had steped at the dangerous way
             He can't sleep at night
             He catches starlight
             That's why he is sad every day""")
else:
    print(Data)
