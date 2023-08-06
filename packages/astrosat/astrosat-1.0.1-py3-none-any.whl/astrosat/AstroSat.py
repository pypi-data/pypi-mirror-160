# author: James Osborn, james.osborn@durham.ac.uk
# MJT
# license?

import numpy
import ephem
import datetime
import astropy.units as u
import astropy.coordinates
import math
import scipy.interpolate
from urllib.request import urlopen
from astroquery.simbad import Simbad
import os
from tqdm import tqdm

# from .parameters import Parameters

import warnings
warnings.filterwarnings("ignore")


class AstroSat:
    def __init__(self, parameters):

        self.parameters = parameters

        self.sun = ephem.Sun()

        self.stars = self.get_bright_stars()

        self.search_radius = numpy.max([15.,self.parameters.radius])

    def get_TLEs(self,satellite_type='active',forceNew=0):
        '''
        Download TLEs
        check all times take closest one, if time now is closer to obs date download new

        '''
        timeStamp = self.parameters.date.timestamp()
        timeNow = datetime.datetime.now().timestamp()
        timeTempList=[]
        if forceNew == 0:
            fnlist = os.listdir(self.parameters.TLEdir)
            fnlist.sort()
            for fn in fnlist:
                # make a list of archived TLE files
                if '.dat' in fn:
                    timeTemp = int(fn.split('_')[0])
                    typeTemp = fn.split('_')[1][:-4]
                    if typeTemp == satellite_type:
                        timeTempList.append(timeTemp)
            if len(timeTempList)>0:
                if len(timeTempList)==1:
                    # if only one file in archive
                    timeTemp = timeTempList[0]
                    if abs(timeStamp - timeTemp) > abs(timeStamp - timeNow):
                        # if archived file is further in time to now download new TLE
                        forceNew = 1
                elif len(timeTempList)>1:
                    # more files in list, find closest
                    timeTemp = timeTempList[numpy.argmin(abs(timeStamp-numpy.array(timeTempList)))]
                    if abs(timeStamp - timeTemp) > abs(timeStamp - timeNow):
                        # if archived file is further in time to now download new TLE
                        forceNew = 1
                if forceNew == 0:
                # if 1:
                    # read TLE for file
                    fn = '%i_%s.dat' % (timeTemp,satellite_type)
                    if self.parameters.verbose:
                        print('Loading TLE:%s from file: %s'%(satellite_type,fn))
                    satTLEs = []
                    with open(self.parameters.TLEdir+'/'+fn,'r') as f:
                        for line in f:
                            satTLEs.append(line.split(','))
                    f.close()
            elif len(timeTempList)==0:
                # no files in archive - download new ones
                forceNew = 1
                        
        # download and archive new TLEs
        if forceNew == 1:
            if self.parameters.verbose:
                print('Downloading TLE:%s'%satellite_type)

            TLE_URL = 'https://www.celestrak.com/NORAD/elements/%s.txt'%(satellite_type)
            TLEs = urlopen(TLE_URL)
            TLEs = [item.strip() for item in TLEs]
            satTLEs = [(TLEs[i].decode('utf-8'), TLEs[i+1].decode('utf-8'), TLEs[i+2].decode('utf-8')) for i in numpy.arange(0, len(TLEs)-2, 3)]
        
            # write to file
            fn = '%i_%s.dat' %(datetime.datetime.now().timestamp(),satellite_type)
            f = open(self.parameters.TLEdir+'/'+fn,'w')
            for TLE in satTLEs:
                f.write('%s,%s,%s\n' %(TLE[0],TLE[1],TLE[2]))
            f.close()

        return satTLEs

    def get_satellites(self,satTLEs):
        self.sats={}
        for tle in satTLEs:
            self.sats[tle[0]] = ephem.readtle(tle[0], tle[1], tle[2])
        return self.sats


    def process_satellite(self, sat, date, Fmodel=None, satDict={}):
        '''
        Parse sat into satellite orbits and project onto observers RA/DEC
        '''

        date_temp = date
        self.parameters.obs.date = date_temp

        sat.compute(self.parameters.obs)
        sat_name = sat.name
        RA_sat = sat.ra
        DEC_sat = sat.dec

        RA_angle_diff = (self.parameters.RA - RA_sat*180/numpy.pi + 180 + 360) % 360 - 180
        DEC_angle_diff = (self.parameters.DEC - DEC_sat*180/numpy.pi + 180 + 360) % 360 - 180

        if abs(RA_angle_diff) < self.search_radius:
            if abs(DEC_angle_diff) < self.search_radius:

                self.sun.compute(self.parameters.obs)
                
                if Fmodel=='diffuseSpherical':
                    # solar phase angle
                    a = self.sun.earth_distance * 1.496e+11  # distance sun from observer (Km)
                    b = sat.range*1. 
                    if self.parameters.obs.elevation < -1000.:
                        b -= ephem.earth_radius
                    angle_c = ephem.separation((sat.az, sat.alt), (self.sun.az, self.sun.alt))
                    c = math.sqrt(math.pow(a, 2) + math.pow(b, 2) - 2*a*b*math.cos(angle_c))
                    angle_a = math.acos((math.pow(b, 2) + math.pow(c, 2) - math.pow(a, 2)) / (2 * b * c))
                    phase_angle = angle_a 

                    # "Optical Tracking and Spectral Characterization of Cubesats for Operational Missions"
                    # Gasdia, Forrest, (2016). PhD Dissertations and Master's Theses. 212.
                    # https://commons.erau.edu/edt/212
                    F = (2/(3*numpy.pi**2))*(numpy.sin(phase_angle) + (numpy.pi-phase_angle)*numpy.cos(phase_angle))

                elif Fmodel==None:
                    # no solar phase angle dependence
                    F = 1

                # extinction due to airmass
                if self.parameters.obs.elevation < -1000:
                    gamma = 0.
                else:
                    # https://www.aanda.org/articles/aa/full_html/2020/04/aa37501-20/aa37501-20.html
                    # include curvature of Earth in airmass (for low elevation angles)
                    # gamma = 0.12*1./(numpy.sin(sat.alt)+0.15*(sat.alt*180./numpy.pi + 3.885)**(-1.253))

                    # calculate directly from TLE
                    gamma = 0.12 * sat.range/sat.elevation
                    
                # "Optical Tracking and Spectral Characterization of Cubesats for Operational Missions"
                # Gasdia, Forrest, (2016). PhD Dissertations and Master's Theses. 212.
                # https://commons.erau.edu/edt/212
                mag_sat = -26.74 - 2.5*numpy.log10((self.parameters.cross_section*F)/sat.range**2) + gamma

                if sat.eclipsed:
                    # in shadow
                    mag_sat = None
                elif mag_sat<0.:
                    # Too bright - geometry gone wrong (small angles)
                    mag_sat = None
                elif sat.alt<0.:
                    # below horizon
                    if self.parameters.obs.elevation > -1000:
                        # not if centre of Earth observer
                        mag_sat = None

                if sat_name not in satDict.keys():
                    satDict[sat_name] = {}
                    satDict[sat_name]['RA'] = []
                    satDict[sat_name]['DEC'] = []
                    satDict[sat_name]['MAG'] = []
                    satDict[sat_name]['Time'] = []
                    satDict[sat_name]['sunElev'] = []
                    satDict[sat_name]['ALT'] = []
                    satDict[sat_name]['AZ'] = []
                    satDict[sat_name]['RANGE'] = []
                    satDict[sat_name]['ELEV'] = []

                satDict[sat_name]['RA'].append(RA_sat*12./numpy.pi)
                satDict[sat_name]['DEC'].append(DEC_sat*180/numpy.pi)
                satDict[sat_name]['MAG'].append(mag_sat)
                satDict[sat_name]['Time'].append(date_temp)
                satDict[sat_name]['ALT'].append(sat.alt*180./numpy.pi)
                satDict[sat_name]['AZ'].append(sat.az*180./numpy.pi)
                satDict[sat_name]['sunElev'].append(self.sun.alt*180./numpy.pi)
                satDict[sat_name]['RANGE'].append(sat.range)
                satDict[sat_name]['ELEV'].append(sat.elevation)

        return satDict

    def print_satellite_dictionary(self, satellite_dictionary):
        '''
        Calculate and print satellites that intersect with field of view
        '''
        sat_table = []
        RAtemp = numpy.arange(self.parameters.RA-self.parameters.radius, self.parameters.RA+self.parameters.radius, 1./3600.)
        for i_sat in (satellite_dictionary.keys()):
            mag_sat = satellite_dictionary[i_sat]['MAG'][0]
            if mag_sat is not None:
                RA_sat = satellite_dictionary[i_sat]['RA']
                DEC_sat = satellite_dictionary[i_sat]['DEC']
                if len(satellite_dictionary[i_sat]['Time']) > 1:
                    time_sat = []
                    for timeTemp in satellite_dictionary[i_sat]['Time']:
                        time_sat.append(timeTemp.timestamp())

                    # find transit time through FoV
                    f = scipy.interpolate.interp1d(numpy.array(RA_sat)*180/12., DEC_sat, fill_value='extrapolate',kind='slinear')
                    DECextrap = f(RAtemp)

                    RA1 = RAtemp[numpy.argmin(abs(DECextrap-(self.parameters.DEC-self.parameters.radius)))]
                    RA2 = RAtemp[numpy.argmin(abs(DECextrap-(self.parameters.DEC+self.parameters.radius)))]
                    
                    if RA1 < self.parameters.RA-self.parameters.radius:
                        RAmin = self.parameters.RA-self.parameters.radius
                    elif RA1 > self.parameters.RA+self.parameters.radius:
                        RAmin = self.parameters.RA+self.parameters.radius
                    else:
                        RAmin = RA1
                    if RA2 < self.parameters.RA-self.parameters.radius:
                        RAmax = self.parameters.RA-self.parameters.radius
                    elif RA2 > self.parameters.RA+self.parameters.radius:
                        RAmax = self.parameters.RA+self.parameters.radius
                    else:
                        RAmax = RA2

                    DEC1 = f(RAmin)
                    DEC2 = f(RAmax)

                    DECmin = numpy.max([DEC1,self.parameters.DEC-self.parameters.radius])
                    DECmax = numpy.min([DEC2,self.parameters.DEC+self.parameters.radius])

                    if DECmin != DECmax and RAmin != RAmax:
                        f2 = scipy.interpolate.interp1d(numpy.array(RA_sat)*180/12.,time_sat,fill_value='extrapolate')
                        timeRA = f2([RAmin,RAmax])
                        f3 = scipy.interpolate.interp1d(DEC_sat,time_sat,fill_value='extrapolate')
                        timeDEC = f3([DECmin,DECmax])

                        if numpy.array_equal(timeRA.astype(int),timeDEC.astype(int)):
                            # make sure the satellite is where we think it is!
                            try:
                                satDict = self.process_satellite(self.sats[i_sat],datetime.datetime.fromtimestamp(numpy.mean(timeRA)),satDict={})
                                mag_sat=satDict[i_sat]['MAG'][0]

                                time0 = numpy.min(timeRA)
                                if time0 > self.parameters.date.timestamp() and time0 < self.parameters.date.timestamp()+self.parameters.duration:
                                    if satDict[i_sat]['RA'][0]*180/12.<RAmax and satDict[i_sat]['RA'][0]*180./12.>RAmin:
                                        if satDict[i_sat]['DEC'][0]<DECmax and satDict[i_sat]['DEC'][0]>DECmin:
                                        # intercept FOV
                                            if mag_sat != None:
                                                sat_table.append([i_sat, datetime.datetime.strftime(datetime.datetime.fromtimestamp(time0),'%H:%M:%S'), abs(timeRA[1]-timeRA[0]), mag_sat, [RAmin,RAmax],[DECmin,DECmax]])
                            except:
                                # satellite outside range
                                pass 
                # else:
                #     # only one event
                #     if self.parameters.RA+self.parameters.radius > RA_sat[0]*180./12. > self.parameters.RA-self.parameters.radius:
                #         if self.parameters.DEC+self.parameters.radius > DEC_sat[0] > self.parameters.DEC-self.parameters.radius:
                #             sat_table.append([i_sat, datetime.datetime.strftime(satellite_dictionary[i_sat]['Time'][0], '%H:%M:%S'), 0, satellite_dictionary[i_sat]['MAG'][0]])
        if len(sat_table)>0:
            print("{: <30} {: <15} {: <15}{: <10}".format(*['Name', 'Time (UTC)', 'Duration (s)', 'Mag (V)']))
            for row in sat_table:
                print("{: <30} {: <15} {: <15.1f}{: <10.2f}".format(*row[:-2]))
        else:
            print("No satellite intercept predicted")
        return sat_table

    def find_intercept_sats(self,Fmodel):
        '''
        do recursive search - 10 sec steps to find small number potential sats and time window then 1 sec
        '''
        sats = self.sats
        for timeStep in tqdm([10,1]):
            satDict = {}
            for istep in (range(0, int(self.parameters.duration), timeStep)):
                dateTemp = self.parameters.date+datetime.timedelta(seconds=istep)
                for isat in sats.keys():
                    satDict = self.process_satellite(sats[isat], dateTemp, Fmodel, satDict)
            sats = {sat_key:sats[sat_key] for sat_key in satDict.keys()}
        return satDict


    def get_bright_stars(self):
        '''
        Extract bright star catalogue to python list
        '''
        stars=[]
        # find the stars
        if self.parameters.radius < 2.:
            # small FoV - use simbad
            if self.parameters.verbose:
                print('Connecting to Simbad')
            useBSC=0
            try:
                self.parameters.obs.date = self.parameters.date
                star = ephem.FixedBody()
                star._ra = self.parameters.RA*numpy.pi/180.
                star._dec = self.parameters.DEC*numpy.pi/180
                star.compute(self.parameters.obs)
                RA_simbad, DEC_simbad = self.parameters.obs.radec_of(star.az, star.alt)
                custom_simbad = Simbad()
                custom_simbad.add_votable_fields('flux(V)')
                pointing = astropy.coordinates.SkyCoord(ra=RA_simbad*u.rad, dec=DEC_simbad*u.rad)
                starsSimbad = custom_simbad.query_region(pointing, radius=self.parameters.radius*1.5 * u.deg)
                for row in starsSimbad:
                    if len(row[1].split()) == 3:
                        RAstar = (numpy.array(row[1].split()).astype(float)*numpy.array([1, 1./60., 1./3600.])).sum() *360./24.
                    if len(row[1].split()) == 2:
                        RAstar = (numpy.array(row[1].split()).astype(float)*numpy.array([1, 1./60.])).sum()

                    if len(row[2].split()) == 3:
                        DECstar = (numpy.array(row[2].split()).astype(float)*numpy.array([1, 1./60., 1./3600.])).sum()
                    if len(row[2].split()) == 2:
                        DECstar = (numpy.array(row[2].split()).astype(float)*numpy.array([1, 1./60.])).sum()
                    if numpy.isnan(row[11]) == False:
                        magstar = float(row[11])
                        stars.append([row[0].decode('utf-8'),RAstar,DECstar,magstar])

            except:
                if self.parameters.verbose:
                    print('Connection to Simbad failed')
                useBSC=1
                # use BSC

        if self.parameters.radius >= 2. or useBSC ==1:
            # For large fields of view just use bright stars otherwise plots get cluttered     
            # 
            #   
            # 
            #  
            if self.parameters.verbose:
                print('Using Bright Star Catalogue')
            with open("astroSat/data/bsc.dat",'r') as f:     
                for line in f:
                    # Loop through the Yale Bright Star Catalog, line by line
                    # Ignore blank lines and comment lines
                    if (len(line) < 100) or (line[0] == '#'):
                        continue
                    try:
                        # Read the Henry Draper (i.e. HD) number for this star
                        hd = int(line[25:31])
                        # Read the right ascension of this star (J2000)
                        ra_hrs = float(line[75:77])
                        ra_min = float(line[77:79])
                        ra_sec = float(line[79:82])
                        # Read the declination of this star (J2000)
                        dec_neg = (line[83] == '-')
                        dec_deg = float(line[84:86])
                        dec_min = float(line[86:88])
                        dec_sec = float(line[88:90])
                        # Read the V magnitude of this star
                        mag = float(line[102:107])
                    except ValueError:
                        continue
                    # Turn RA and Dec from sexagesimal units into decimal
                    ra = (numpy.array([ra_hrs,ra_min,ra_sec]).astype(float)*numpy.array([1, 1./60., 1./3600.])).sum() *360./24.
                    dec = (numpy.array([dec_deg,dec_min,dec_sec]).astype(float)*numpy.array([1, 1./60., 1./3600.])).sum()
                    if dec_neg:
                        dec = -dec
                    stars.append([hd,ra,dec,mag])
            
        return stars

