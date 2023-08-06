import datetime
from decimal import Decimal
import glob
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

from astropy import units as u
from astropy import constants
from astropy.cosmology import Planck15 as cosmo
from astropy.cosmology import z_at_value
from astropy.time import Time
from astropy.utils.data import download_file
from datetime import date, datetime, timedelta
import gcn
from gracedb_sdk import Client
import healpy as hp
from ligo.gracedb.rest import GraceDb
import ligo.skymap.distance
import lxml.etree
import numpy as np
from scipy.special import sph_harm, erfinv


#  Get path to working directory
path = os.path.dirname(os.path.abspath(__file__)) + '/files/'

def generate_macrofile(superevent_id, gracedb_url='https://gracedb.ligo.org/api/'):
    """Create macrofile that contains relevant data from superevent
       and preferred external event, to be potentially used to generate
       the pdf of the manuscript.
    
    Parameters
    ----------
    superevent_id: str
        GraceDB ID of the superevent
    gracedb_url: str
        URL of the GraceDB server's API e.g. https://gracedb.ligo.org/api/
    """

    #  Set up APIs for both the REST and sdk clients
    gracedb_api = GraceDb(gracedb_url)
    gracedb_sdk = Client(gracedb_url)
    superevent = gracedb_api.superevent(superevent_id).json()

    #  Grab latest voevent   
    voevent_url = gracedb_sdk.superevents[superevent_id].voevents.get()[-1]['links']['file']
    voevent_payload = gracedb_sdk.superevents[superevent_id].files[voevent_url.split('/')[-1]].get()
    root = lxml.etree.fromstring(voevent_payload.read())

    params = {elem.attrib['name']:
                elem.attrib['value']
                for elem in root.iterfind('.//Param')}

    #  Extract skymap
    if 'skymap_fits' in params:
        # Read the HEALPix sky map and the FITS header.
        kwargs = {'mode': 'w+b'}
        with tempfile.NamedTemporaryFile(**kwargs) as skymapfile:
            skymap_raw = gracedb_sdk.events[superevent_id].files[params['skymap_fits'].split('/')[-1]].get()
            skymapfile.write(skymap_raw.read())
            skymap, header = hp.read_map(skymapfile.name ,h=True)
            prob, distmu, distsigma, distnorm = hp.read_map(skymapfile.name, field = [ 0 , 1 , 2 , 3 ])
    else:
        sys.exit('No skymap available')
        
    #  Get FAR
    if 'FAR' in params:
        GW_FAR = float(params['FAR'])
    else:
        sys.exit('FAR not available from the LVC')

    # Name of the collaboration from the GW side
    GWauthors = [elem.text for elem in root.iterfind('.//contactName')][0]

    print(params)
    GWskymapname = params['skymap_fits']
    GWskymapname = GWskymapname.upper() # Name of the skymap used (e.g. BAYESTAR or LALINFERENCE)

    #  Return correct name despite numbering of various bayestar or lalinference skymaps (e.g. 'LALINFERENCE1' -> 'LALIFERENCE')
    if 'LALINFERENCE' in GWskymapname:
        GWskymapname = 'LALINFERENCE'
    elif 'BAYESTAR' in GWskymapname:
        GWskymapname = 'BAYESTAR'


    #  Check GW is from a CBC (can deal with CBC only at the moment)
    if params['Group'] != 'CBC':
        sys.exit('GW not from a CBC -> cannot be dealt with in current version')

    #  Time of the event in various formats
    t0_GPS = superevent['t_0'] # Get GPS time of the event
    url_vosuperevents = superevent['links']['voevents'] # Get urls for voevents
        
    t0_UTC = Time(t0_GPS, format='gps', scale='utc')
    t0_UTC.format = 'iso' # Conversion from gps format to iso

    #  Definition of YY-MM-DD and HH:MM:SS
    t0_yymmdd = t0_UTC.value[0:10]
    t0_hhmmss = t0_UTC.value[11:19]

    #  Rank types depending on their probability
    proba = np.array([[params['BBH'], 'BBH'], [params['BNS'], 'BNS'],[params['NSBH'], 'NSBH'],[params['Terrestrial'], 'Terrestrial'] ])
    proba = np.flip(proba[proba[:,0].astype(float).argsort()], axis = 0)
    proba_num = proba[:,0].astype(float)

    #  Create macrofile with loaded parameters
    #  Print in file
    f = open(path+'macro_GW_GRB.tex', 'w')

    print('%Template of maccros related to a given association of GW and GRB event\n', file = f)
    print('%(Automatically generated)\n', file = f)

    #  url VOEvent
    print('\\newcommand{\\urlVOEvent}{%s}\n' % (voevent_url), file = f)

    #  Collaborations
    print('\\newcommand{\\GWcolla}{%s}\n' % (GWauthors), file = f)

    #  Skymaps name and url
    print('\\newcommand{\\GWskyn}{%s}\n' % (GWskymapname), file = f)
    print('\\newcommand{\\GWskyurl}{%s}\n' % (params['skymap_fits']), file = f)

    #  Detectors
    print('\\newcommand{\\Hanford}{LIGO Hanford Observatory (H1)}\n', file = f)
    print('\\newcommand{\\Ha}{H1}\n', file = f)

    print('\\newcommand{\\Livingston}{LIGO Livingston Observatory (L1)}\n', file = f)
    print('\\newcommand{\\Li}{L1}\n', file = f)

    print('\\newcommand{\\Virgo}{Virgo Observatory (V1)}\n', file = f)
    print('\\newcommand{\\Vi}{V1}\n', file = f)

    if params['Instruments'] == 'H1,L1,V1':
        print('\\newcommand{\\detectors}{\\Hanford, \\Livingston~and \\Virgo}\n', file = f)
        print('\\newcommand{\\detectorsabvr}{\\Ha, \\Li, \\Vi}\n', file = f)

    elif params['Instruments'] == 'H1,L1':
        print('\\newcommand{\\detectors}{\\Hanford~and \\Livingston}\n', file = f)
        print('\\newcommand{\\detectorsabvr}{\\Ha, \\Li}\n', file = f)
        
    elif params['Instruments'] == 'H1,V1':
        print('\\newcommand{\\detectors}{\\Hanford~and \\Virgo}\n', file = f)
        print('\\newcommand{\\detectorsabvr}{\\Ha, \\Vi}\n', file = f)
        
    elif params['Instruments'] == 'L1,V1':
        print('\\newcommand{\\detectors}{\\Livingston~and \\Virgo}\n', file = f)
        print('\\newcommand{\\detectorsabvr}{\\Li, \\Vi}\n', file = f)
        
    else: #  We will have to see whether or not we consider single ITF events or not
        print('\\newcommand{\\detectors}{\\issue{Detectors}}\n', file = f)
        print('\\newcommand{\\detectorsabvr}{\\issue{Detectors}}\n', file = f)

    #  Times
    print('\\newcommand{\\GWtime}{%s %s UTC (GPS time: %.0f)}\n' % (t0_yymmdd,t0_hhmmss,t0_GPS), file = f)

    #  CBC types
    print('\\newcommand{\\Pevents}{%s (%.2f \%%), %s (%.2f \%%), %s (%.2f \%%) or %s (%.2f \%%)} \n' % (proba[0,1],proba_num[0]*100.,proba[1,1],proba_num[1]*100.,proba[2,1],proba_num[2]*100.,proba[3,1],proba_num[3]*100.), file = f)

    if  proba[0,1] == 'BNS':
        print("\\newcommand{\\etype}{binary neutron star (BNS) merger}\n", file = f)
        print("\\newcommand{\\ety}{BNS}\n", file = f)
    elif proba[0,1] == 'BBH':
        print('\\newcommand{\\etype}{binary black hole (BBH) merger}\n', file = f)
        print("\\newcommand{\\ety}{BBH}\n", file = f)
    elif proba[0,1] == 'NSBH':
        print("\\newcommand{\\etype}{neutron star -- black hole merger (NSBH)}\n", file = f)
        print("\\newcommand{\\ety}{NSBH}\n", file = f)
    elif proba[0,1] == 'Terrestrial':
        print("\\newcommand{\\etype}{\\issue{Terrestrial}}\n", file = f)
        print("\\newcommand{\\ety}{\\issue{Terrestrial}}\n", file = f)
    else:
        print("\\newcommand{\\etype}{\\issue{Problem in CBC type}}\n", file = f)
        print("\\newcommand{\\ety}{\\issue{Problem}}\n", file = f)

    #  Print macro defining name of the events
    print('\\newcommand{\\GWevent}{\\textsc{%s}}\n' % (params['GraceID']), file = f)

    # Distances
    moments = ligo.skymap.distance.parameters_to_marginal_moments(prob, distmu, distsigma)
    dist_mean = moments[0]

    min_distance_CL90 = ligo.skymap.distance.marginal_ppf([0.1],prob,distmu, distsigma, distnorm)[0]
    max_distance_CL90 = ligo.skymap.distance.marginal_ppf([0.9],prob,distmu, distsigma, distnorm)[0]

    delta_min = min_distance_CL90 - dist_mean
    delta_max = max_distance_CL90 - dist_mean

    dL = min_distance_CL90

    print('skymap = %s: mean = %.0f, std_dev = %.0f' % (GWskymapname,moments[0],moments[1]))

    print('\\newcommand{\\distance}{$%.0f$ Mpc}\n' % (dL), file = f )
    print('\\newcommand{\\distmean}{{%.0f}}\n' % (dist_mean), file = f )
    print('\\newcommand{\\distdeltamin}{{%.0f}}\n' % (delta_min), file = f )
    print('\\newcommand{\\distdeltamax}{{+%.0f}}\n' % (delta_max), file = f )

    #  Prefered pipeline
    if params['Pipeline'] == 'gstlal':
        print('\\newcommand{\\pipesup}{GSTLAL \\cite{messik:2017pr,sachdev:2019ax}}\n', file = f)
        
    elif params['Pipeline'] == 'pycbc':
        print('\\newcommand{\\pipesup}{PyCBC Live \\cite{nitz:2017ap,dalcanton:2017ar}}\n', file = f)
        
    elif params['Pipeline'] == 'spiir':
        print('\\newcommand{\\pipesup}{SPIIR \\cite{hooper:2012pr,chu:2017th}}\n', file = f)
        
    elif params['Pipeline'] == 'MBTAOnline':
        print('\\newcommand{\\pipesup}{MBTA \\cite{adams:2016cq}}\n', file = f)
        
    else:
        print('\\newcommand{\\pipesup}{\\issue{Pipeline}}\n', file = f)


    #  Grab external event
    emevent_id = superevent['em_type']
    FAR_GW = superevent['far']
        
    external_event = gracedb_api.event(emevent_id).json()
    em_GPS_time = external_event['gpstime'] 
    EM_observer = external_event['extra_attributes']['GRB']['how_description']
    GRBevent = external_event['graceid']
    dto = em_GPS_time - t0_GPS

    print('\\newcommand{\\partners}{\\raven{%s}}' % (EM_observer), file = f) # Name of who made the GRB detection

    FAR_temp = superevent['time_coinc_far']
    FAR_ST = superevent['space_coinc_far']

    #  TODO: Replace using superevent/external sky map rotation comparison method 
    if FAR_ST:
        Proba = FAR_ST / FAR_GW
    else:
        Proba = FAR_temp / FAR_GW

    #  Translate in terms of Gaussian statistics
    Ssigma = erfinv(2. * (1 - Proba) - 1) * np.sqrt(2)  # To be checked

    Proba_exp = np.floor(np.log10(np.abs(Proba))).astype(int)
    Proba_string = '%.2e' % Decimal(Proba)
    Proba_base_string = Proba_string.split("e")
    Proba_base = float(Proba_base_string[0])
    
    #  Define constants used
    z = z_at_value(cosmo.luminosity_distance, dL * u.Mpc)
    c = constants.c.value

    R_earth = 6.371e6 # (m)
    #  TODO: change this for other experiments, i.e. Swift, INTEGRAL, AGILE-MCAL
    apogee_Fermi = 5.436e5 # (m)

    dt_error_Fermi_pos = (R_earth + apogee_Fermi) / c # (s) Error due to light travel between Fermi and LVC, worst case scenario
    dt_error_LVC_pipelines = 0.07 # (s) Max error in timing in low latency pipelines
    dt_error_Fermi = 0.05 # (s)
    dterror = dt_error_Fermi_pos + dt_error_LVC_pipelines + dt_error_Fermi # (s) cumulative error

    #  Range of possible emission delay assumed
    tee = 0. # (s)  earliest assumed emission time (s) for photons, normally 0s
    tel = 10. # (s)  latest assumed emission time (s) for photons, normally 10s

    #  Get distances using error bars in timing
    dvmax = c*(1+z)*(dto+dterror-(1+z)*tee)/(dL*u.Mpc.to(u.m))
    dvmin = c*(1+z)*(dto-dterror-(1+z)*tel)/(dL*u.Mpc.to(u.m))

    dvmax_exp = np.floor(np.log10(np.abs(dvmax))).astype(int)
    dvmax_string = str(dvmax)
    dvmax_base_string = dvmax_string.split("e")
    dvmax_base = float(dvmax_base_string[0])

    nbbmax=dvmax/(.5*np.real(sph_harm(0,0,0,0)))
    nbbmin=dvmin/(.5*np.real(sph_harm(0,0,0,0)))

    nbbmin_exp = np.floor(np.log10(np.abs(nbbmin))).astype(int)
    nbbmin_string = str(nbbmin)
    nbbmin_base_string = nbbmin_string.split("e")
    nbbmin_base = float(nbbmin_base_string[0])


    #  Add remaining value to macrofile
    print('\\newcommand{\\Pvalues}{$P = 1- \\raven{%0.2f \\times 10^{%.0i}}$}' % (Proba_base,Proba_exp), file = f)
    print('\\newcommand{\\Ssigma}{\\raven{%0.1f }$\\sigma$}' % (Ssigma), file = f)
    print('\\newcommand{\\GRBtime}{\\issue{YYYY-MM-DD HH:MM:SS.mmm UTC (GPS time: X)}}', file = f)
    print('\\newcommand{\\tdelay}{$\\Delta t_{\\text{SGRB--GW}} = \\raven{%0.2f} \pm \\issue{%0.2f} $ s}' % (dto,dterror), file = f)
    print('\\newcommand{\\dtErrorPos}{\\issue{%.2f}}' % (dt_error_Fermi_pos), file = f)
    print('\\newcommand{\\dtErrorLVCpipe}{\\issue{%.2f}}' % (dt_error_LVC_pipelines), file = f)
    print('\\newcommand{\\dtErrorFermipipe}{\\issue{%.2f}}' % (dt_error_Fermi), file = f)
    print('\\newcommand{\\vu}{\\raven{+%.2f \\times 10^{%.0i} }}' % (dvmax_base, dvmax_exp), file = f)
    print('\\newcommand{\\vl}{\\raven{%.2f \\times 10^{%.0i} }}' % (dvmin_base, dvmin_exp), file = f)
    print('\\newcommand{\\FSDratioU}{\\raven{xx~}}', file = f)
    print('\\newcommand{\\FSDratioL}{\\raven{xx~}}', file = f)
    print('\\newcommand{\\GRBevent}{\\raven{\\textsc{%s}}}' % (GRBevent), file = f)
    print('\\newcommand{\\GRBeventTitle}{\\textsc{%s}}' % (GRBevent), file = f) # use just to prevent color issue in a title when using \issue in a section title
    print('\\newcommand{\\saau}{\\raven{+%.0f \\times 10^{%.0i} }}' % (nbbmax_base,nbbmax_exp), file = f)
    print('\\newcommand{\\saal}{\\raven{%.0f \\times 10^{%.0i} }}' % (nbbmin_base,nbbmin_exp), file = f)
    print('\\newcommand{\\mTdelay}{\\raven{%.2f}}' % (dto), file = f)
    print('\\newcommand{\\deltaTdelay}{\\issue{%.2f}}' % (dterror), file = f)

    f.close()

def generate_pdf(superevent_id, gracedb_url='https://gracedb.ligo.org/api/',
                 keep_local_copy=False, compress_files=False,
                 use_latexmk=True, use_test_macrofile=False):
    """Generate pdf of manuscript using macrofile.
    
    Parameters
    ----------
    superevent_id: str
        GraceDB ID of the superevent
    gracedb_url: str
        URL of the GraceDB server's API e.g. https://gracedb.ligo.org/api/
    keep_local_copy: bool
        If True, keeps copy of pdf in local directory
    compress_files: bool
        If True, creates and tarball of all files
    use_latemk: bool
        If True, uses latexmk instead of pdflatex to generate pdf
    use_test_macrofile: bool
        If True, uses local test copy of macro file rather than querying GraceDB
    """

    #  Create macrofile to generate manusrcipt from 
    if not use_test_macrofile:
        #  Query GraceDB to generate macrofile
        generate_macrofile(superevent_id, gracedb_url=gracedb_url)
    else:
        #  Use macrofile from test
        print(path)
        commandLine = subprocess.Popen(['cp', '../../test/files/macro_GW_GRB.tex', '.'], cwd=path)
        commandLine.communicate()

    if use_latexmk:
        #  Create manuscript using latexmk
        commandLine = subprocess.Popen(['latexmk', '--pdf', 'SoG_LIV_arxiv_aps.tex'], cwd=path)
        commandLine.communicate()
    else:
        #  Create manuscript using pdflatex
        commandLine = subprocess.Popen(['pdflatex', 'SoG_LIV_arxiv_aps.tex'], cwd=path)
        commandLine.communicate()

        commandLine = subprocess.Popen(['bibtex', 'SoG_LIV_arxiv_aps.aux'], cwd=path)
        commandLine.communicate()

        commandLine = subprocess.Popen(['pdflatex', 'SoG_LIV_arxiv_aps.tex'], cwd=path)
        commandLine.communicate()

        commandLine = subprocess.Popen(['pdflatex', 'SoG_LIV_arxiv_aps.tex'], cwd=path)
        commandLine.communicate()


    #  Create copy in current directory
    if keep_local_copy:
        commandLine = subprocess.Popen(['cp', path+'SoG_LIV_arxiv_aps.pdf',
                                        'SoG_LIV_arxiv_aps.pdf'])
        commandLine.communicate()

    if compress_files:
        with tarfile.open('SoG_LIV_files.tar.gz', "w:gz") as tar:
            tar.add(path, arcname=os.path.basename(path))

    #  Remove unnecessary generated files
    os.unlink(path + 'macro_GW_GRB.tex')
    os.unlink(path + 'SoG_LIV_arxiv_aps.log')
    os.unlink(path + 'SoG_LIV_arxiv_aps.aux')
    os.unlink(path + 'SoG_LIV_arxiv_aps.out')
    os.unlink(path + 'SoG_LIV_arxiv_aps.bbl')
    os.unlink(path + 'SoG_LIV_arxiv_aps.blg')
    os.unlink(path + 'SoG_LIV_arxiv_apsNotes.bib')
    

def upload_pdf(superevent_id, gracedb_url='https://gracedb.ligo.org/api/',
               keep_local_copy=False, compress_files=False,  
               use_latexmk=True, use_test_macrofile=False):
    """Generate and upload pdf to superevent.
    
    Parameters
    ----------
    superevent_id: str
        GraceDB ID of the superevent
    gracedb_url: str
        URL of the GraceDB server's API e.g. https://gracedb.ligo.org/api/
    keep_local_copy: bool
        If True, keeps copy of pdf (and tarball of files if compressed) in local directory
    compress_files: bool
        If True, creates and uploads tarball of all files
    use_latemk: bool
        If True, uses latexmk instead of pdflatex to generate pdf
    use_test_macrofile: bool
        If True, uses local test copy of macro file rather than querying GraceDB
    """
    
    #  Create manuscript
    generate_pdf(superevent_id, gracedb_url=gracedb_url,
                 keep_local_copy=keep_local_copy,
                 compress_files=compress_files,
                 use_test_macrofile=use_test_macrofile)

    #  Prepare gracedb client to upload to
    gracedb_sdk = Client(gracedb_url)

    #  Open and upload pdf file to gracedb superevent
    with open(path + 'SoG_LIV_arxiv_aps.pdf', 'rb') as file:
        gracedb_sdk.superevents[superevent_id].logs.create(
            comment="Measurement of speed of gravity manuscript",
            filename="SoG_LIV_arxiv_aps.pdf",
            filecontents=file,
            tags=["ext_coinc"]
        )

    #  Remove local copy in working directory
    os.unlink(path + 'SoG_LIV_arxiv_aps.pdf')

    #  Upload tarball of all files
    if compress_files:
        with open('SoG_LIV_files.tar.gz', 'rb') as file:
            gracedb_sdk.superevents[superevent_id].logs.create(
                comment="Files for speed of gravity manuscript",
                filename="SoG_LIV_files.tar.gz",
                filecontents=file,
                tags=["ext_coinc"]
            )

        #  Remove if not needed
        if not keep_local_copy:
            os.unlink('SoG_LIV_files.tar.gz')