#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from astropy.utils.data import download_file
import gcn
import healpy as hp
import lxml.etree
import sys
from ligo.gracedb.rest import GraceDb


# In[2]:


import requests
import json
import datetime
from datetime import date, datetime, timedelta


# In[3]:


from astropy.time import Time


# In[4]:


import ligo.skymap.distance


# In[5]:


import os,glob,subprocess


# In[6]:


import voeventparse


# In[7]:


from lalinference.bayespputils import calculate_redshift
from scipy.special import sph_harm, erfinv
from lal import PC_SI, C_SI


# In[8]:


from decimal import Decimal


# In[9]:


#url = ('https://gracedb.ligo.org/apiweb/superevents/S190421ar/files/S190421ar-2-Initial.xml,0')
#url = ('https://gracedb.ligo.org/apiweb/superevents/S190412m/files/S190412m-1-Preliminary.xml,0')
#url = ('https://gracedb.ligo.org/apiweb/superevents/S190408an/files/S190408an-1-Preliminary.xml,0')
#url = ('https://gracedb.ligo.org/apiweb/superevents/S190425z/files/S190425z-1-Initial.xml,0')
#url = ('https://gracedb.ligo.org/apiweb/superevents/S190425z/files/S190425z-2-Update.xml')
#url = ('https://gracedb.ligo.org/apiweb/superevents/S190426c/files/S190426c-2-Initial.xml,0')
url = ('https://gracedb.ligo.org/apiweb/superevents/S190426c/files/S190426c-5-Update.xml,0')
#url = 'https://gracedb.ligo.org/apiweb/superevents/S190426c/files/S190426c-3-Update.xml,0'
#url = ('https://gracedb.ligo.org/apiweb/superevents/S190503bf/files/S190503bf-2-Initial.xml,0')
#url = ('https://gracedb.ligo.org/apiweb/superevents/S190510g/files/S190510g-2-Initial.xml,0')
#url = ('https://gracedb.ligo.org/apiweb/superevents/S190510g/files/S190510g-3-Update.xml,0')
#url = 'https://gracedb.ligo.org/apiweb/superevents/S190513bm/files/S190513bm-2-Initial.xml,0'
#url = 'https://gracedb.ligo.org/apiweb/superevents/S190512at/files/S190512at-2-Initial.xml,0'
#url = 'https://gracedb.ligo.org/apiweb/superevents/S190517h/files/S190517h-1-Preliminary.xml,0'
#url = 'https://gracedb.ligo.org/apiweb/superevents/S190518bb/files/S190518bb-1-Preliminary.xml,0'
#url = 'https://gracedb.ligo.org/apiweb/superevents/S190519bj/files/S190519bj-2-Initial.xml,0'
#url = 'https://gracedb.ligo.org/apiweb/superevents/S190521g/files/S190521g-2-Initial.xml,0'
#url = 'https://gracedb.ligo.org/apiweb/superevents/S190521r/files/S190521r-2-Initial.xml,0'
#url = 'https://gracedb.ligo.org/apiweb/superevents/S190521g/files/S190521g-3-Update.xml,0'
#url = 'https://gracedb.ligo.org/apiweb/superevents/S190602aq/files/S190602aq-2-Initial.xml,0'

filename = download_file( url , cache = True )

payload = open(filename, 'rb').read()
root = lxml.etree.fromstring(payload)

params = {elem.attrib['name']:
              elem.attrib['value']
              for elem in root.iterfind('.//Param')}
#process_gcn(payload, root)

#Extractinf skymap
if 'skymap_fits' in params:
     # Read the HEALPix sky map and the FITS header.
    skymap, header = hp.read_map(params['skymap_fits'],h=True, verbose=False)
    prob , distmu , distsigma , distnorm = hp.read_map(params['skymap_fits'] , field = [ 0 , 1 , 2 , 3 ])
else:
    sys.exit('No skymap available')
    
#Getting FAR
if 'FAR' in params:
    GW_FAR = float(params['FAR'])
else:
    sys.exit('FAR not available from the LVC')


# In[10]:


with open(filename, 'rb') as fread: # see doc at https://buildmedia.readthedocs.org/media/pdf/voevent-parse/latest/voevent-parse.pdf
    v = voeventparse.load(fread)
    
GWauthors = v.Who.Author.contactName # Name of the collaboration from the GW side

if v.What.Group.attrib['type'] == 'GW_SKYMAP':
    GWskymapname = v.What.Group.attrib['name']
GWskymapname = GWskymapname.upper() # Name of the skymap used (e.g. BAYESTAR or LALINFERENCE)


# In[11]:


# Return correct name despite numbering of various bayestar or lalinference skymaps (e.g. 'LALINFERENCE1' -> 'LALIFERENCE')
if 'LALINFERENCE' in GWskymapname:
    GWskymapname = 'LALINFERENCE'
elif 'BAYESTAR' in GWskymapname:
    GWskymapname = 'BAYESTAR'


# In[12]:


# Check GW is from a CBC (can deal with CBC only at the moment)
if params['Group'] != 'CBC':
    sys.exit('GW not from a CBC -> cannot be dealt with in current version')


# In[13]:


# Get additional information on gracedb that is not in VOEvent (e.g. time of the event)

#url_supevent = 'https://gracedb.ligo.org/api/superevents'
#payload = {'format':'json', 'query':params['GraceID']}
#r = requests.get(url_supevent, params=payload)
#jsoninfo = json.loads(r.content)
#print(jsoninfo)
client = GraceDb('https://gracedb.ligo.org/api/')
Event = client.superevent('S190426c').json()
#print(Event)
#Event = jsoninfo['superevents']


# Time of the event in various formats
t0_GPS = Event['t_0'] # Get GPS time of the event
url_voevents = Event['links']['voevents'] # Get urls for voevents
    
t0_UTC = Time(t0_GPS, format='gps', scale='utc')
t0_UTC.format = 'iso' # Conversion from gps format to iso

# Definition of YY-MM-DD and HH:MM:SS
t0_yymmdd = t0_UTC.value[0:10]
t0_hhmmss = t0_UTC.value[11:19]

# To keep (might be useful later on)

url_voevents
payload_voe = {'format':'json'}
r_voe = requests.get(url_voevents, params=payload_voe)
jsoninfo_voe = json.loads(r_voe.content)
Event_voe = jsoninfo_voe
# In[14]:


# rank types depending on their proba

proba = np.array([[params['BBH'], 'BBH'], [params['BNS'], 'BNS'],[params['NSBH'], 'NSBH'],[params['Terrestrial'], 'Terrestrial'] ])

proba = np.flip(proba[proba[:,0].astype(float).argsort()], axis = 0)

proba_num = proba[:,0].astype(float)


# In[15]:


# Print in file
f = open('macro_GW_GRB.tex', 'w')


# In[16]:


# Misc

print('%Template of maccros related to a given association of GW and GRB event\n', file = f)
print('%(Automatically generated)\n', file = f)


# In[17]:


# url VOEvent
print('\\newcommand{\\urlVOEvent}{%s}\n' % (url), file = f)


# In[18]:


# Collaborations

print('\\newcommand{\\GWcolla}{%s}\n' % (GWauthors), file = f)


# In[19]:


# Skymaps name and url

print('\\newcommand{\\GWskyn}{%s}\n' % (GWskymapname), file = f)
print('\\newcommand{\\GWskyurl}{%s}\n' % (params['skymap_fits']), file = f)


# In[20]:


# Detectors

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
    
else: # We will have to see whether or not we consider single ITF events or not
    print('\\newcommand{\\detectors}{\\issue{Detectors}}\n', file = f)
    print('\\newcommand{\\detectorsabvr}{\\issue{Detectors}}\n', file = f)


# In[21]:


# Times

print('\\newcommand{\\GWtime}{%s %s UTC (GPS time: %.0f)}\n' % (t0_yymmdd,t0_hhmmss,t0_GPS), file = f)


# In[22]:


# CBC types

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


# In[23]:


# Print macro defining name of the events

#print('%Define the names of the events', file = f)
print('\\newcommand{\\GWevent}{\\textsc{%s}}\n' % (params['GraceID']), file = f)
#print('\\newcommand{\\GRBevent}{\\issue{no GRB ID at the moment}}\n', file = f)


# In[24]:


# Distances

moments = ligo.skymap.distance.parameters_to_marginal_moments(prob,distmu, distsigma)
dist_mean = moments[0]

min_distance_CL90 = ligo.skymap.distance.marginal_ppf([0.1],prob,distmu, distsigma, distnorm)[0]
max_distance_CL90 = ligo.skymap.distance.marginal_ppf([0.9],prob,distmu, distsigma, distnorm)[0]


delta_min = min_distance_CL90 - dist_mean
delta_max = max_distance_CL90 - dist_mean

dL = min_distance_CL90


# In[25]:


print('skymap = %s: mean = %.0f, std_dev = %.0f' % (GWskymapname,moments[0],moments[1]))


# In[26]:


print('\\newcommand{\\distance}{$%.0f$ Mpc}\n' % (dL), file = f )
print('\\newcommand{\\distmean}{{%.0f}}\n' % (dist_mean), file = f )
print('\\newcommand{\\distdeltamin}{{%.0f}}\n' % (delta_min), file = f )
print('\\newcommand{\\distdeltamax}{{+%.0f}}\n' % (delta_max), file = f )


# In[27]:


# Prefered pipeline

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


# ## Box below: all placeholders before we have raven in place

# In[28]:


from ligo.gracedb.rest import GraceDb, HTTPError #GraceDbBasic, HTTPError


# In[29]:


gracedb_api = GraceDb("https://gracedb.ligo.org/api/")

#Warning, for test purpose, one cannot use the actual superevent, since it usually does not have an associated EM event
#superevents = gracedb_api.superevents(params['GraceID']) # Uncomment in final version
superevents = gracedb_api.superevents('S190611j') # Comment in final version


for superevent in superevents:
    t0_GPS = superevent['t_0']
    url_voevent = superevent['links']['voevents']
    emevent_id = superevent['em_events']
    FAR_GW = superevent['far']
    
em = GraceDb(service_url='https://gracedb.ligo.org/api/')
response = em.event(emevent_id[0])
data = response.json()
em_GPS_time = data['gpstime'] 
EM_observer = data['extra_attributes']['GRB']['how_description']
GRBevent = data['graceid']
dto = em_GPS_time - t0_GPS


# In[30]:


print('\\newcommand{\\partners}{\\raven{%s}}' % (EM_observer), file = f) # Name of who made the GRB detection

response = gracedb_api.files('S190611j', 'coincidence_far.json')
data = response.json()
#print(data)
P_temp = data['temporal_coinc_far']
P_ST = data['spatiotemporal_coinc_far']

if P_ST:
    Proba = P_ST
else:
    Proba = P_temp
# In[31]:


response = gracedb_api.files('S190611j', 'coincidence_far.json')
data = response.json()
#print(data)
FAR_temp = data['temporal_coinc_far']
FAR_ST = data['spatiotemporal_coinc_far']

if FAR_ST:
    Proba = FAR_ST / FAR_GW
else:
    Proba = FAR_temp / FAR_GW


# $$ P( X \leq c) = \frac{1}{\sqrt{2 \pi}} \int_{- \infty}^c e^{-x^2/2} dx = \frac{1}{2} \left[1 + \textrm{erf} \left(\frac{c}{\sqrt{2}} \right) \right] $$
# 
# such that
# 
# $$c = \sqrt{2} ~\textrm{erf}^{-1} \left( 2 P - 1\right).$$

# In[32]:


# Translate in terms of Gaussian statistics

Ssigma = erfinv(2. * (1 - Proba) - 1) * np.sqrt(2)  # To be checked


# In[33]:


Proba_exp = np.floor(np.log10(np.abs(Proba))).astype(int)
#Proba_string = str(Proba)
Proba_string = '%.2e' % Decimal(Proba)
Proba_base_string = Proba_string.split("e")
Proba_base = float(Proba_base_string[0])

#check if space-time proba or only time proba

#IS_STortemp = 0 # 1 -> is space-time probability


#if P_ST:
#    IS_STortemp = 1
#    
#if IS_STortemp:
    
# In[34]:


#dto = 2. # (s) placeholder for observed time delay (s) between GW and gamma signal
R_earth = 6.371e6 # (m) 
apogee_Fermi = 5.436e5 # (m)


dt_error_Fermi_pos = (R_earth + apogee_Fermi) / C_SI # (s) Error due to light travel between Fermi and LVC, worst case scenario

dt_error_LVC_pipelines = 0.07 # (s) Max error in timing in low latency pipelines

dt_error_Fermi = 0.05 # (s)

dterror = dt_error_Fermi_pos + dt_error_LVC_pipelines + dt_error_Fermi # (s) cumulative error


# In[35]:


# range of possible emission delay assumed

tee = 0. # (s)  earliest assumed emission time (s) for photons, normally 0s
tel = 10. # (s)  latest assumed emission time (s) for photons, normally 10s


# In[36]:


z=calculate_redshift(dL)[0][0]
dvmax = C_SI*(1+z)*(dto+dterror-(1+z)*tee)/(dL*1e6*PC_SI)
dvmin = C_SI*(1+z)*(dto-dterror-(1+z)*tel)/(dL*1e6*PC_SI)


# In[37]:


dvmin_exp = np.floor(np.log10(np.abs(dvmin))).astype(int)
dvmin_string = str(dvmin)
dvmin_base_string = dvmin_string.split("e")
dvmin_base = float(dvmin_base_string[0])


dvmax_exp = np.floor(np.log10(np.abs(dvmax))).astype(int)
dvmax_string = str(dvmax)
dvmax_base_string = dvmax_string.split("e")
dvmax_base = float(dvmax_base_string[0])


# In[38]:


nbbmax=dvmax/(.5*np.real(sph_harm(0,0,0,0)))

nbbmin=dvmin/(.5*np.real(sph_harm(0,0,0,0)))


# In[39]:


nbbmax_exp = np.floor(np.log10(np.abs(nbbmax))).astype(int)
nbbmax_string = str(nbbmax)
nbbmax_base_string = nbbmax_string.split("e")
nbbmax_base = float(nbbmax_base_string[0])

nbbmin_exp = np.floor(np.log10(np.abs(nbbmin))).astype(int)
nbbmin_string = str(nbbmin)
nbbmin_base_string = nbbmin_string.split("e")
nbbmin_base = float(nbbmin_base_string[0])


# In[40]:


print('%In what follows: placeholders not automatized yet\n', file = f)

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


# In[41]:


f.close()


# In[42]:


commandLine = subprocess.Popen(['pdflatex', 'SoG_LIV_arxiv_aps.tex'])
commandLine.communicate()

commandLine = subprocess.Popen(['bibtex', 'SoG_LIV_arxiv_aps.aux'])
commandLine.communicate()

commandLine = subprocess.Popen(['pdflatex', 'SoG_LIV_arxiv_aps.tex'])
commandLine.communicate()

commandLine = subprocess.Popen(['pdflatex', 'SoG_LIV_arxiv_aps.tex'])
commandLine.communicate()


# In[43]:


os.rename('SoG_LIV_arxiv_aps.pdf','SoG_LIV_arxiv_aps_%s.pdf' % (params['GraceID']))

