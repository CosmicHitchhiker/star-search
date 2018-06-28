#!/usr/bin/python3

import sys
import numpy as np
from astropy.io import ascii
from astroquery.simbad import Simbad

# Configure necessary parameters of Simbad query
Simbad.add_votable_fields('flux(J)')
Simbad.add_votable_fields('flux(H)')
Simbad.add_votable_fields('flux(K)')
Simbad.remove_votable_fields('coordinates')
Simbad.remove_votable_fields('main_id')

# Make column with full names of stars to send it to Simbad
main_file = ascii.read(sys.argv[1])
main_file['HIP_ID_STR'] = np.array(list(map(lambda x: 'hip' + x, main_file['HIP_ID'].astype('str'))))

# Query and conjunction
new_columns = Simbad.query_objects(main_file['HIP_ID_STR'])
main_file.add_columns(new_columns.columns.values())

main_file.write(sys.argv[1], format = 'ascii.basic')

sys.exit(0)
