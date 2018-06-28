STAR SEARCH
-----------

This is the program for quick finding and sorting stars from 
Spectroscopic (Telluric) Standards of Gemini Observatory 
(http://www.gemini.edu/sciops/instruments/nearir-resources/spectroscopic-standards)

The program uses libraries:
astropy (2.0.2)
configparser (3.5.0)
numpy (1.13.1)
pandas (0.20.3)

All you need to do is to set parameters in config.ini file and then to run
star_search.py program.


ADD JHK
-------

There are only V-band magnitudes in the given catalogue. So, if you want
to add J, H and K magnitudes - activate this utility:
./add_JHK.py <filename>
Where <filename> is the name of file with catalogue (in 'cat' folder)

(c) Vsevolod Lander 2017