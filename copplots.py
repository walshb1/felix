from pylab import *
import csv
import copy
import prettyplotlib as ppl
import matplotlib.patches as pts
from matplotlib import rc
from matplotlib import colors
from textwrap import wrap
from distutils.util import strtobool
rc('text', usetex=False)

params = {'savefig.bbox': 'tight', #or 'standard'
          #'savefig.pad_inches': 0.1 
          'xtick.labelsize': 8,
          'ytick.labelsize': 8,
          'legend.fontsize': 10,
          'legend.linewidth': 2, 
          'legend.fancybox': True,
          'savefig.facecolor': 'white',   # figure facecolor when saving
          'savefig.edgecolor': 'white'    # figure edgecolor when saving
          }
plt.rcParams.update(params)

import sys
sys.path.insert(0, '/Users/brian/Desktop/Dropbox/python/my_libraries')

import esm_plotting_tools
reload(esm_plotting_tools)
from esm_plotting_tools import *

import tools
reload(tools)
from tools import *

import rcp_informations
reload(rcp_informations)
from rcp_informations import *

sns.set()
sns.set_context("paper")
sns.set_style("white")
#sns.set_style("darkgrid", {"grid.linewidth": .5, "axes.facecolor": ".9"})

#############################################


# Run rcop with oceans
if len(sys.argv) >= 2: 
    plot_rcop = bool(strtobool(sys.argv[1]))
    if plot_rcop == False: print "***Transforming RAF into airborne fraction***"
else: plot_rcop = True

# Conversion Factors
mtoe_to_ej = .041868

# Formatting Controls
plot_errors = False
label_HD = False
dots = 15      # scatter/dot size
yl_sz = 10     # y-axis label size
lf_sz = 7      # label font size
hatch_str ='++++++++++\\\\\\\\\\\\\\\\\\\\\\\////////////'

do_scatter_2100 = False

def insert_panel_label(plt,panel_str,n_subp=2,equiv_yr=1937):
    y_val = 1.0
    trans = plt.gca().get_xaxis_transform() # x in data units, y in axes fraction
    annotate(panel_str,size=21, xy=(equiv_yr,y_val),xycoords=trans,ha='right',va='center',weight='bold',annotation_clip=False)

def do_ENE_range(theEM,plt,ecs_str="3C",start_yr=0):
    be_lo_search = []
    be_hi_search = []
    be3_lo_search = []
    be3_hi_search = []

    if ecs_str == "3C":
        plt.fill_between(aYear[start_yr:],theEM[fbau_lo_00_3C_idx][start_yr:],theEM[fbau_hi_00_3C_idx][start_yr:],facecolor=cop_color("FossilBAU"),edgecolor='none',alpha=0.45)
        plt.fill_between(aYear[start_yr:],theEM[bau_lo_00_3C_idx][start_yr:],theEM[bau_hi_00_3C_idx][start_yr:],facecolor=cop_color("BAU"),edgecolor='none',alpha=0.45)

        plt.fill_between(aYear[start_yr:],theEM[be_lo_00_3C_idx][start_yr:],theEM[be_hi_00_3C_idx][start_yr:],facecolor=cop_color("BioEnergy"),edgecolor='none',alpha=0.5)    
        plt.fill_between(aYear[start_yr:],theEM[be3_lo_00_3C_idx][start_yr:],theEM[be3_hi_00_3C_idx][start_yr:],hatch=hatch_str,facecolor='none',edgecolor=cop_color("BioEnergy"),alpha=1)

        plt.fill_between(aYear[start_yr:],theEM[be_lo_80_3C_idx][start_yr:],theEM[be_hi_80_3C_idx][start_yr:],facecolor=cop_color("BioEnergy CCS80"),edgecolor='none',alpha=0.5)
        plt.fill_between(aYear[start_yr:],theEM[be3_lo_80_3C_idx][start_yr:],theEM[be3_hi_80_3C_idx][start_yr:],hatch=hatch_str,facecolor='none',edgecolor=cop_color("BioEnergy CCS80"),alpha=1)

        for iYear in range(len(aYear[start_yr:])):
            be_lo_search.append(min(theEM[be_lo_40_3C_idx][start_yr+iYear], theEM[be_40_3C_idx][start_yr+iYear], theEM[be_hi_40_3C_idx][start_yr+iYear]))
            be_hi_search.append(max(theEM[be_lo_40_3C_idx][start_yr+iYear], theEM[be_40_3C_idx][start_yr+iYear], theEM[be_hi_40_3C_idx][start_yr+iYear]))
            #
            be3_lo_search.append(min(theEM[be3_lo_40_3C_idx][start_yr+iYear], theEM[be3_40_3C_idx][start_yr+iYear], theEM[be3_hi_40_3C_idx][start_yr+iYear]))
            be3_hi_search.append(max(theEM[be3_lo_40_3C_idx][start_yr+iYear], theEM[be3_40_3C_idx][start_yr+iYear], theEM[be3_hi_40_3C_idx][start_yr+iYear]))

        plt.fill_between(aYear[start_yr:],be_lo_search,be_hi_search,facecolor=cop_color("BioEnergy CCS40"),edgecolor='none',alpha=0.5)
        plt.fill_between(aYear[start_yr:],be3_lo_search,be3_hi_search,hatch=hatch_str,facecolor='none',edgecolor=cop_color("BioEnergy CCS40"),alpha=1)

    else:
        plt.fill_between(aYear[start_yr:],theEM[fbau_lo_00_idx][start_yr:],theEM[fbau_hi_00_idx][start_yr:],facecolor=cop_color("FossilBAU"),edgecolor='none',alpha=0.45)
        plt.fill_between(aYear[start_yr:],theEM[bau_lo_00_idx][start_yr:],theEM[bau_hi_00_idx][start_yr:],facecolor=cop_color("BAU"),edgecolor='none',alpha=0.45)

        plt.fill_between(aYear[start_yr:],theEM[be_lo_00_idx][start_yr:],theEM[be_hi_00_idx][start_yr:],facecolor=cop_color("BioEnergy"),edgecolor='none',alpha=0.5)
        plt.fill_between(aYear[start_yr:],theEM[be_lo_80_25C_idx][start_yr:],theEM[be_hi_80_25C_idx][start_yr:],facecolor=cop_color("BioEnergy CCS80"),edgecolor='none',alpha=0.5)
    
        plt.fill_between(aYear[start_yr:],theEM[be3_lo_00_idx][start_yr:],theEM[be3_hi_00_idx][start_yr:],hatch=hatch_str,facecolor='none',edgecolor=cop_color("BioEnergy"),alpha=1)
        plt.fill_between(aYear[start_yr:],theEM[be3_lo_80_25C_idx][start_yr:],theEM[be3_hi_80_25C_idx][start_yr:],hatch=hatch_str,facecolor='none',edgecolor=cop_color("BioEnergy CCS80"),alpha=1)

        for iYear in range(len(aYear[start_yr:])):
            be_lo_search.append(min(theEM[be_lo_40_25C_idx][start_yr+iYear], theEM[be_40_25C_idx][start_yr+iYear], theEM[be_hi_40_25C_idx][start_yr+iYear]))
            be_hi_search.append(max(theEM[be_lo_40_25C_idx][start_yr+iYear], theEM[be_40_25C_idx][start_yr+iYear], theEM[be_hi_40_25C_idx][start_yr+iYear]))
            #
            be3_lo_search.append(min(theEM[be3_lo_40_25C_idx][start_yr+iYear], theEM[be3_40_25C_idx][start_yr+iYear], theEM[be3_hi_40_25C_idx][start_yr+iYear]))
            be3_hi_search.append(max(theEM[be3_lo_40_25C_idx][start_yr+iYear], theEM[be3_40_25C_idx][start_yr+iYear], theEM[be3_hi_40_25C_idx][start_yr+iYear]))

        plt.fill_between(aYear[start_yr:],be_lo_search,be_hi_search,facecolor=cop_color("BioEnergy CCS40"),edgecolor='none',alpha=0.5)
        plt.fill_between(aYear[start_yr:],be3_lo_search,be3_hi_search,hatch=hatch_str,facecolor='none',edgecolor=cop_color("BioEnergy CCS40"),alpha=1)

        #plt.fill_between(aYear[start_yr:],theEM[be_lo_40_25C_idx][start_yr:],theEM[be_hi_40_25C_idx][start_yr:],facecolor=cop_color("BioEnergy CCS40"),edgecolor='none',alpha=0.5)
        #plt.fill_between(aYear[start_yr:],theEM[be3_lo_40_25C_idx][start_yr:],theEM[be3_hi_40_25C_idx][start_yr:],hatch=hatch_str,facecolor='none',edgecolor=cop_color("BioEnergy CCS40"),alpha=1)

def insta_scen(iScen,ecs_opt="3C"):

    #if ecs_opt == "overlaps":
    #    if "BioEnergy3 CCS25" in nScen[j]: return False
    #    if "BioEnergy3 CCS50" in nScen[j]: return False
    #    return True

    if "RCP" in iScen: return False

    if ecs_opt == "3C":
        if "3C" not in iScen: return False
    elif "3C" in iScen: return False

    if "15C" in iScen or "45C" in iScen: return False

    if "BAU" in iScen and "CCS" in iScen: return False
    if "hi" in iScen: return False
    if "lo" in iScen: return False
    #
    if "BioEnergy1" in iScen: return False
    if "BioEnergy2" in iScen: return False
    #
    if "Historical" in iScen: return False
    if "noUD" in iScen: return False
    #if "FossilBAU" in iScen and "en05" in iScen: return True
    if "Fossil" in iScen and "en" in iScen: return False
    if "char" in iScen or "Char" in iScen: return False

    #Pick set of CCS values to show:
    if "CCS25" in iScen: return False
    if "CCS50" in iScen: return False
    if "CCS75" in iScen: return False
    if "CCS40" in iScen: return True
    if "CCS80" in iScen: return True

    return True

def getZ(iScen):
    if iScen == "HistoricalData": return 99.9
    if iScen == "BAU": return 99.8
    if "BAU" in iScen: return 99.7
    else: return 99.0

#############################################
iRow = 0
iScen = 0
nScen = []
aYear = []
aHyr = [[]]
nBM = 0
BMtypes = []
aBioMass = [[[]]]

def getalfa(iScen):
    if "BAU" in iScen: return 1.0
    elif "RCP" in iScen: return 0.6
    else: return 0.6

def cop_scen_rep(iScen):
    return iScen.replace(" ","+").replace("BioEnergy3","RE-High").replace("BioEnergy2","RE-High").replace("BioEnergy1","RE-Med").replace("BioEnergy","RE-Low").replace("+3C","").replace("p+25C","").replace("FossilBAU","Fossil Fuels").replace("CCS40p",r'$\frac{1}{2}$CCS').replace("CCS80p","CCS")

def cop_style(iScen):
    if "BioEnergy1" in iScen: return ':'
    if "BioEnergy3" in iScen: return '-.'
    else: return '-'

def range_with_capitals(pltA,central_val=0,error=0,n_subplot=1,year=2011,hd_source='IPCC'):
    if hd_source == 'IPCC':
        sel_col = browns[10]#greys[7]
        sel_mark = 'o'
        set_alpha = 0.8
        dot_zorder = 100
    
    elif hd_source == 'CMIP5':
        sel_col = browns[0]
        sel_mark = 'D'
        set_alpha = 0.8
        dot_zorder = 100

    ylo = central_val-error
    yhi = central_val+error

    label_hack = hd_source+" Data"
    if label_hack in pltA.gca().get_legend_handles_labels()[1]: label_hack = ""


    pltA.gca().errorbar(year, central_val, yerr=error,markersize=4,color=sel_col,alpha=set_alpha,zorder=dot_zorder,label=label_hack,fmt=sel_mark)

    #scatter([year,],[central_val,],s=dots-5,marker=sel_mark,color=sel_col,label=label_hack,zorder=dot_zorder,alpha=1.0)
    #pltA.gca().add_patch(Rectangle((year-0.15,ylo),0.30,(yhi-ylo),color=sel_col,zorder=line_zorder,alpha=set_alpha))

    #if n_subplot == 1:
    #    cap_height = (pltA.gca().get_ylim()[1]-pltA.gca().get_ylim()[0])/330
    #else: cap_height = (pltA.gca().get_ylim()[1]-pltA.gca().get_ylim()[0])/110

    #pltA.gca().add_patch(Rectangle((year-1,ylo),2.0,(cap_height),color=sel_col,zorder=line_zorder,alpha=set_alpha))
    #pltA.gca().add_patch(Rectangle((year-1,yhi-cap_height),2.0,(cap_height),color=sel_col,zorder=line_zorder,alpha=set_alpha))    

#############################################
#############################################
# Emissions
#

iRow = 0
iScen = 0
nScen = []
aYear = []
aHyr = [[]]
nEM = 0
EMtypes = []
aEM = [[[]]]

fig = plt.gcf()
size = fig.get_size_inches()
print "\nFigure size =",size,"\n"

with open("tables/emissions_table.csv") as f: 
    reader = csv.reader(f)
    allRows = list(reader)
    nRows = len(allRows)

with open("tables/emissions_table.csv") as f: 
    reader = csv.reader(f)
    
    for row in reader:

##### TIME INFO
        if iRow == 0:
            for i in range(1,len(row)-1):
                aYear.append(int(float(row[i])))
                if int(float(row[i])) == 1995: yr1995idx = len(aYear)-1
                if int(float(row[i])) == 1997: yr1997idx = len(aYear)-1
                if int(float(row[i])) == 2000: yr2000idx = len(aYear)-1
                if int(float(row[i])) == 2010: yr2010idx = len(aYear)-1
                if int(float(row[i])) == 2050: yr2050idx = len(aYear)-1
         
##### SCENARIO INFO
        elif iRow == 1:
            for i in range(1,len(row)):
                if row[i] != "": nScen.append(row[i])
                if row[i] == "BAU": BAUidx = len(nScen)-1
                if (row[i] == "FossilBAU" or row[i] == "Fossil Fuels"): FBAUidx = len(nScen)-1
                if (row[i] == "FossilBAU_3C" or row[i] == "Fossil Fuels_3C"): FBAUidx3C = len(nScen)-1
                if row[i] == "HistoricalData": HDidx = len(nScen)-1

            nEM  = (nRows-2)/len(nScen)
            if nEM%1 != 0: print "Error: Unexpected number of rows!"
                
            for n in range(nEM):
                aEM.append([])
                aHyr.append([])
                for m in range(len(nScen)):
                    aEM[n].append([])
##### SCENARIO DATA
        else:
            if (iRow-2)%len(nScen) == 0:
                #print iRow-2,len(nScen),row[0]
                EMtypes.append(row[0])
                #print EMtypes
                iScen = 0

            for i in range(1,len(row)-1):

                if "--" not in row[i] and row[i] != "":                    
                    if "Historical" in row[0]: 
                        aHyr[len(EMtypes)-1].append(aYear[i-1])

                    if ("Fossil Fuels" in EMtypes[len(EMtypes)-1] 
                        or "Emissions" in EMtypes[len(EMtypes)-1]
                        or "Renewables" in EMtypes[len(EMtypes)-1]
                        or "C in Storage" in EMtypes[len(EMtypes)-1]
                        or "C Emission from Land Use Change" in EMtypes[len(EMtypes)-1]
                        or "C in Atmosphere" in EMtypes[len(EMtypes)-1]
                        or "Cumulative Uptake by Oceans" in EMtypes[len(EMtypes)-1]
                        or "Flux" in EMtypes[len(EMtypes)-1]
                        or "Land Sink" in EMtypes[len(EMtypes)-1]
                        or "Net C Emission from Energy Sector" in EMtypes[len(EMtypes)-1]
                        or "Total C Emission from Energy Sector" in EMtypes[len(EMtypes)-1]
                        or "Afforestation" in EMtypes[len(EMtypes)-1]
                        or "Leeching to Atmosphere" in EMtypes[len(EMtypes)-1]):
                        aEM[len(EMtypes)-1][iScen].append(float(row[i])/1E009)
                    else: 
                        #print iScen,"trying to fit into",len(aEM[len(EMtypes)-1])
                        aEM[len(EMtypes)-1][iScen].append(float(row[i]))
    
            iScen = iScen+1
        iRow = iRow+1

#################################
# Plot Emissions Data
standardize_scenario_names(nScen)

kaya_gdp_idx = -1

for i in range(nEM):

    if EMtypes[i] == "Cumulative Emissions from Fossil Fuels": cum_ff_em = i
    elif EMtypes[i] == "Cumulative LULUC Emissions": cum_luc_em = i
    #elif EMtypes[i] == "Cumulative LUC Emissions": cum_luc_em = i
    elif EMtypes[i] == "C in Storage": cseq_em = i
    elif EMtypes[i] == "Cumulative Uptake by Oceans": cum_ocn_em = i
    elif EMtypes[i] == "Cumulative Atmosphere to Land Sink": cum_lsk_em = i
    elif EMtypes[i] == "Leeching to Atmosphere": leech_em = i
    elif EMtypes[i] == "CCS Improvement Factor": ccs_factor_idx = i
    elif EMtypes[i] == "Total C Emission from Fossil Fuels": ann_ffem_idx = i
    elif EMtypes[i] == "Total C Emission from Renewables": ann_bem_idx = i
    elif EMtypes[i] == "Net C Emission from Energy Sector": ann_esec_idx = i
    ###
    elif "Temperature Anomalies" in EMtypes[i]: temp_anom_idx = i
    elif "Atmospheric Concentration CO2" in EMtypes[i]: atm_ppm_idx = i
    elif "Total Radiative Forcing" == EMtypes[i]: rad_for_idx = i
    ###
    elif "GWP per Capita" == EMtypes[i]: kaya_gdp_idx = i
    elif "Energy Intensity of GDP" == EMtypes[i]: kaya_eig_idx = i
    elif "Carbon Intensity of Energy" == EMtypes[i]: kaya_cie_idx = i
    elif "Population" == EMtypes[i]: kaya_pop_idx = i
    #
    elif "UNDESA WPP Population LowVar" == EMtypes[i]:  pop_lovar_idx = i
    elif "UNDESA WPP Population MedVar" == EMtypes[i]:  pop_mdvar_idx = i
    elif "UNDESA WPP Population HighVar" == EMtypes[i]: pop_hivar_idx = i
    ###
    elif "Cumulative Emissions" == EMtypes[i]: cum_em_idx = i

for j in range(len(nScen)):

    if nScen[j] == "FossilBAU lo": fbau_lo_00_idx = j
    if nScen[j] == "FossilBAU hi": fbau_hi_00_idx = j
    if nScen[j] == "BAU lo": bau_lo_00_idx = j
    if nScen[j] == "BAU hi": bau_hi_00_idx = j
    if nScen[j] == "BioEnergy lo": be_lo_00_idx = j
    if nScen[j] == "BioEnergy hi": be_hi_00_idx = j
    if nScen[j] == "BioEnergy CCS40p 25C": be_40_25C_idx = j
    if nScen[j] == "BioEnergy CCS40p 25C": be_40_25C_idx = j
    if nScen[j] == "BioEnergy CCS80p 25C": be_80_25C_idx = j
    if nScen[j] == "BioEnergy CCS80p 25C": be_80_25C_idx = j
    if nScen[j] == "BioEnergy lo CCS40p 25C": be_lo_40_25C_idx = j
    if nScen[j] == "BioEnergy hi CCS40p 25C": be_hi_40_25C_idx = j
    if nScen[j] == "BioEnergy lo CCS80p 25C": be_lo_80_25C_idx = j
    if nScen[j] == "BioEnergy hi CCS80p 25C": be_hi_80_25C_idx = j
    if nScen[j] == "BioEnergy3 lo": be3_lo_00_idx = j
    if nScen[j] == "BioEnergy3 hi": be3_hi_00_idx = j
    if nScen[j] == "BioEnergy3 CCS40p 25C": be3_40_25C_idx = j
    if nScen[j] == "BioEnergy3 CCS40p 25C": be3_40_25C_idx = j
    if nScen[j] == "BioEnergy3 CCS80p 25C": be3_80_25C_idx = j
    if nScen[j] == "BioEnergy3 CCS80p 25C": be3_80_25C_idx = j
    if nScen[j] == "BioEnergy3 lo CCS40p 25C": be3_lo_40_25C_idx = j
    if nScen[j] == "BioEnergy3 hi CCS40p 25C": be3_hi_40_25C_idx = j
    if nScen[j] == "BioEnergy3 lo CCS80p 25C": be3_lo_80_25C_idx = j
    if nScen[j] == "BioEnergy3 hi CCS80p 25C": be3_hi_80_25C_idx = j
    #
    if nScen[j] == "FossilBAU lo 3C": fbau_lo_00_3C_idx = j
    if nScen[j] == "FossilBAU hi 3C": fbau_hi_00_3C_idx = j
    if nScen[j] == "BAU lo 3C": bau_lo_00_3C_idx = j
    if nScen[j] == "BAU hi 3C": bau_hi_00_3C_idx = j
    if nScen[j] == "BioEnergy lo 3C": be_lo_00_3C_idx = j
    if nScen[j] == "BioEnergy hi 3C": be_hi_00_3C_idx = j
    if nScen[j] == "BioEnergy CCS40p 3C": be_40_3C_idx = j
    if nScen[j] == "BioEnergy CCS40p 3C": be_40_3C_idx = j
    if nScen[j] == "BioEnergy CCS80p 3C": be_80_3C_idx = j
    if nScen[j] == "BioEnergy CCS80p 3C": be_80_3C_idx = j
    if nScen[j] == "BioEnergy lo CCS40p 3C": be_lo_40_3C_idx = j
    if nScen[j] == "BioEnergy hi CCS40p 3C": be_hi_40_3C_idx = j
    if nScen[j] == "BioEnergy lo CCS80p 3C": be_lo_80_3C_idx = j
    if nScen[j] == "BioEnergy hi CCS80p 3C": be_hi_80_3C_idx = j
    if nScen[j] == "BioEnergy3 lo 3C": be3_lo_00_3C_idx = j
    if nScen[j] == "BioEnergy3 hi 3C": be3_hi_00_3C_idx = j
    if nScen[j] == "BioEnergy3 CCS40p 3C": be3_40_3C_idx = j
    if nScen[j] == "BioEnergy3 CCS40p 3C": be3_40_3C_idx = j
    if nScen[j] == "BioEnergy3 CCS80p 3C": be3_80_3C_idx = j
    if nScen[j] == "BioEnergy3 CCS80p 3C": be3_80_3C_idx = j
    if nScen[j] == "BioEnergy3 lo CCS40p 3C": be3_lo_40_3C_idx = j
    if nScen[j] == "BioEnergy3 hi CCS40p 3C": be3_hi_40_3C_idx = j
    if nScen[j] == "BioEnergy3 lo CCS80p 3C": be3_lo_80_3C_idx = j
    if nScen[j] == "BioEnergy3 hi CCS80p 3C": be3_hi_80_3C_idx = j

for i in range(nEM):

    allYval = []
    tempY = 0
    plt.clf()    

    if (i != ann_bem_idx and i != atm_ppm_idx
        and EMtypes[i] != "Flux Atmosphere to Land Sink"
        and EMtypes[i] != "Total C Emission from Fossil Fuels"
        and EMtypes[i] != "Total C Emission from Energy Sector"
        and EMtypes[i] != "C Emission from Land Use Change"
        and EMtypes[i] != "Flux Atmosphere to Ocean"
        and EMtypes[i] != "C in Atmosphere"
        and EMtypes[i] != "Net C Emission from Energy Sector"
        and EMtypes[i] != "Total C Emission from Energy Sector"
        and EMtypes[i] != "COP Ratio"
        and EMtypes[i] != "Net Emissions"
        and EMtypes[i] != "Total Radiative Forcing"
        and EMtypes[i] != "Cumulative Emissions"
        and EMtypes[i] != "CCS Improvement Factor"
        and "Temperature Anomalies" not in EMtypes[i]
        and i != kaya_pop_idx and i != kaya_gdp_idx and i != kaya_eig_idx and i != kaya_cie_idx 
        and i != cum_lsk_em and i != cum_ocn_em): 
        print "*** SKIP:",EMtypes[i]
        continue
    print EMtypes[i]
        
    if (EMtypes[i] != "Total Radiative Forcing" 
        and EMtypes[i] != "Net Emissions"
        and EMtypes[i] != "Cumulative Emissions"
        and "Temperature Anomalies" not in EMtypes[i]
        and "CCS Improvement Factor" not in EMtypes[i]):
        fig = plt.figure(figsize=(6.4,5.0))

    if i == ann_esec_idx:
        fig = plt.figure(figsize=(6.4,7.5))

    if i == cum_lsk_em or i == cum_ocn_em:
        plt.xlim(300,800)
        plt.ylim(0,500)      

        plt.xlabel("Atmospheric Carbon Concentration [ppm]")
        if i == cum_lsk_em:
            plt.ylabel("Cumulative Land Sink Uptake [PgC]")
            annotate("ECS = 3$^{\circ}$C/2xCO$_2$", xy=(0.98,0.03),xycoords='axes fraction',size=8,va="center",ha="right")
            insert_panel_label(plt,"a",1,262)
        elif i == cum_ocn_em:
            plt.ylabel("Cumulative Ocean Uptake [PgC]")
            annotate("ECS = 3$^{\circ}$C/2xCO$_2$", xy=(0.98,0.03),xycoords='axes fraction',size=8,va="center",ha="right")
            insert_panel_label(plt,"b",1,262)

        for j in range(len(nScen)):
            if "Historical" in nScen[j]: continue
                    
            elif insta_scen(nScen[j],"3C") == True:
                plt.plot(aEM[atm_ppm_idx][j],aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
            
                if nScen[j] == "BAU" or nScen[j] == "BAU 3C":
                    plt.scatter(aEM[atm_ppm_idx][j][yr2000idx],aEM[i][j][yr2000idx],15,marker="x",linewidth=2,color=greys[6],zorder=100)
                    annotate("Year 2000",xy=(aEM[atm_ppm_idx][j][yr2000idx],aEM[i][j][yr2000idx]),xycoords='data',
                             xytext=(aEM[atm_ppm_idx][j][yr2000idx]+10,aEM[i][j][yr2000idx]-20), textcoords='data',
                             color=greys[6],va='center',ha='left',size=7,arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=0.4"))
                    annotate("2050",xy=(aEM[atm_ppm_idx][FBAUidx3C][yr2050idx],aEM[i][FBAUidx3C][yr2050idx]),xycoords='data',
                             xytext=(aEM[atm_ppm_idx][FBAUidx3C][yr2050idx]+10,aEM[i][FBAUidx3C][yr2050idx]-20), textcoords='data',
                             color=greys[6],va='center',ha='left',size=7,arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=0.5"))
                    annotate("2100",xy=(aEM[atm_ppm_idx][FBAUidx3C][-1],aEM[i][FBAUidx3C][-1]),xycoords='data',
                             xytext=(aEM[atm_ppm_idx][FBAUidx3C][-1]+05,aEM[i][FBAUidx3C][-1]-25), textcoords='data',
                             color=greys[6],va='center',ha='left',size=7,arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=0.5"))

                plt.scatter(aEM[atm_ppm_idx][j][yr2050idx],aEM[i][j][yr2050idx],10,marker="s",color=cop_color(nScen[j]),zorder=getZ(nScen[j]))
                plt.scatter(aEM[atm_ppm_idx][j][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))
                
        if i == cum_lsk_em:
            handles, labels = plt.gca().get_legend_handles_labels()
            hls,lbs = legend_fliparoo(handles, labels,2)
            leg = plt.legend(hls,lbs,loc='best',ncol=1,fontsize=9,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)

    if EMtypes[i] == "Cumulative Emissions":

        # First, make a CumEm bar plot to keep it interesting
        plt.ylim(0,1600)
        plt.ylabel("Net Anthropogenic Emissions\n(Cum. 2001-2100) [PgC]")
        
        x_ax_labels = [[],[]]
        x_ax_val = 0.3

        plt.bar([x_ax_val],[rcp_cum_em_hist],width=0.8,label=cop_scen_rep("Historical"),facecolor=cop_color(nScen[j]),edgecolor='none',alpha=0.66)
        plt.plot([x_ax_val+0.4-0.5,x_ax_val+0.4+0.5],[felix_cum_em_1900to2000,felix_cum_em_1900to2000],'k-',lw=1.5,color='black',zorder=100)
        plt.plot([x_ax_val+0.4,x_ax_val+0.4],[felix_cum_em_1900to2000-50,felix_cum_em_1900to2000],'k-',lw=1.5,color='black',zorder=100)
        annotate("FeliX",xy=(x_ax_val+0.4,felix_cum_em_1900to2000-75), xycoords='data',ha='center',va='top',size=8,rotation=90,weight='bold')

        x_ax_labels[0].append(x_ax_val+0.4)
        x_ax_labels[1].append(cop_scen_rep("Historical\n(1901-2000)"))
        plt.plot([1.4,1.4],plt.gca().get_ylim(),'k-',lw=1.5,color='black',zorder=1)
        x_ax_val+=1.4

        for j in range(len(nScen)):
            if nScen[j] == "HistoricalData": continue
            
            if insta_scen(nScen[j],"3C") == True:

                if "BioEnergy3" in nScen[j]:
                    plt.bar([cumEM_x_ax_val_dict[nScen[j]]],[(aEM[i][j][-1]-aEM[i][j][yr2000idx])],width=0.8,
                            label=cop_scen_rep(nScen[j]),hatch=hatch_str,facecolor='none',edgecolor=cop_color(nScen[j]),alpha=1.0)
                    x_ax_labels[0].append(cumEM_x_ax_val_dict[nScen[j]]+0.4)
                    x_ax_labels[1].append(cop_scen_rep(nScen[j]))
                    x_ax_val+=1
                elif "BioEnergy" in nScen[j]:
                    plt.bar([cumEM_x_ax_val_dict[nScen[j]]],[(aEM[i][j][-1]-aEM[i][j][yr2000idx])],width=0.8,
                            label=cop_scen_rep(nScen[j]),facecolor=cop_color(nScen[j]),edgecolor='none',alpha=0.66)
                    x_ax_labels[0].append(cumEM_x_ax_val_dict[nScen[j]]+0.4)
                    x_ax_labels[1].append(cop_scen_rep(nScen[j]))
                    x_ax_val+=1
                else:
                    plt.bar([cumEM_x_ax_val_dict[nScen[j]]],[(aEM[i][j][-1]-aEM[i][j][yr2000idx])],width=0.8,
                            color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),label=cop_scen_rep(nScen[j]))
                    x_ax_labels[0].append(cumEM_x_ax_val_dict[nScen[j]]+0.4)
                    x_ax_labels[1].append(cop_scen_rep(nScen[j]))
                    x_ax_val+=1

        plt.plot([1.4,plt.gca().get_xlim()[1]],[cum_em_sub_2C,cum_em_sub_2C],'k-',lw=0.75,color=greys[4],zorder=1)
        annotate("Limit for $\Delta$T<2$^{\circ}$C",xy=(plt.gca().get_xlim()[1]-0.15,rcp_cum_em_26+10),va='bottom',ha='right',color=greys[4],size=7)

        plt.plot([1.4,plt.gca().get_xlim()[1]],[rcp_cum_em_26,rcp_cum_em_26],'k-',lw=0.75,color=greys[6],zorder=1)#marker="s",ms=4)
        annotate("RCP 2.6",xy=(plt.gca().get_xlim()[1]-0.15,rcp_cum_em_26-10),color=greys[6],va='top',ha='right',size=7)

        plt.plot([1.4,plt.gca().get_xlim()[1]],[rcp_cum_em_45,rcp_cum_em_45],'k-',lw=0.75,color=greys[6],zorder=1)#marker=">",ms=4)
        annotate("RCP 4.5",xy=(plt.gca().get_xlim()[1]-0.15,rcp_cum_em_45-10),color=greys[6],va='top',ha='right',size=7)

        plt.plot([1.4,plt.gca().get_xlim()[1]],[rcp_cum_em_60,rcp_cum_em_60],'k-',lw=0.75,color=greys[6],zorder=1)#marker="d",ms=4)
        annotate("RCP 6.0",xy=(plt.gca().get_xlim()[1]-0.15,rcp_cum_em_60-10),color=greys[6],va='top',ha='right',size=7)
        
        plt.gca().set_xticks(x_ax_labels[0])
        plt.gca().set_xticklabels(x_ax_labels[1],rotation=30,ha='right')

        insert_panel_label(plt,"b",1,-1.1)
        plt.draw()
        plt.savefig('figures/biomass_Cumulative_Emissions_barplot.pdf',format='pdf', dpi=1200)
        plt.clf()
        plt.close('all')

        plt.ylim(0,2000)
        plt.ylabel("Cumulative Anthropogenic Emissions [PgC]")

        for j in range(len(nScen)):
            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1:
                    # This HD comes from HadCRUT4
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="HadCRUT4 Data",marker="x",zorder=getZ(nScen[j]))
                    if do_scatter_2100: plt.scatter(aHyr[i][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))
                    
            elif insta_scen(nScen[j],"3C") == True:
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                if do_scatter_2100: scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                annotate(int(round(aEM[i][j][-1],0)),xy=(2102,aEM[i][j][-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=8,weight='bold')

    if i == kaya_pop_idx or i == kaya_gdp_idx or i == kaya_cie_idx or i == kaya_eig_idx:

        fig = plt.gcf()
        fig.set_size_inches(size)
        print "**Figure size set to ",fig.get_size_inches()

        # Kaya Factors: Compare these plots to Fig. 6.1 in ipcc_wg3_ar5_chapter6.pdf (pg 425)
        plt.xlim(1980,2102)
        plt.plot(plt.gca().get_xlim(),[1,1],'k-',ls=':',color=greys[5],zorder=1,lw=1.5)
        
        if i == kaya_pop_idx:
            plt.ylim(0,2.5)
            plt.ylabel("Population (Index: 2010=1)")

            # Plot WPP population projection variants
            BAU_index_value = aEM[kaya_pop_idx][BAUidx][yr2010idx]
            for anIndex, aValue in enumerate(aEM[pop_lovar_idx][HDidx]):
                aEM[pop_lovar_idx][HDidx][anIndex] = float(aValue)*1E9/BAU_index_value
            for anIndex, aValue in enumerate(aEM[pop_mdvar_idx][HDidx]):
                aEM[pop_mdvar_idx][HDidx][anIndex] = float(aValue)*1E9/BAU_index_value
            for anIndex, aValue in enumerate(aEM[pop_hivar_idx][HDidx]):
                aEM[pop_hivar_idx][HDidx][anIndex] = float(aValue)*1E9/BAU_index_value
                      
            plt.plot(aHyr[pop_lovar_idx],aEM[pop_lovar_idx][HDidx],color=greys[7],lw=1.5,ls="--",zorder=1.0)          
            plt.plot(aHyr[pop_mdvar_idx],aEM[pop_mdvar_idx][HDidx],color=greys[7],lw=1.5,ls="--",zorder=1.0)     
            plt.plot(aHyr[pop_hivar_idx],aEM[pop_hivar_idx][HDidx],color=greys[7],lw=1.5,ls="--",zorder=1.0)   

            annotate("WPP Low Var", xy=(aHyr[pop_lovar_idx][-6],aEM[pop_lovar_idx][HDidx][-6]),
                     ha='left',va='top',size=8,xycoords='data',xytext=(+10,+20), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=0.2"))
   
            annotate("WPP Med. Var",xy=(aHyr[pop_mdvar_idx][-6],aEM[pop_mdvar_idx][HDidx][-6]),
                     ha='left',va='top',size=8,xycoords='data',xytext=(-5,+20), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=0.2"))

            annotate("WPP High Var",xy=(aHyr[pop_hivar_idx][-6],aEM[pop_hivar_idx][HDidx][-6]),
                     ha='right',va='top',size=8,xycoords='data',xytext=(-10,+20), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=-0.2"))

        elif i == kaya_gdp_idx:
            plt.ylim(0,5)
            plt.ylabel("GPD per Capita (Index: 2010=1)")

            hist_change_year = [1980+iPower for iPower in xrange(2100-1979)]
            hist_change_rate = [math.pow((1+0.014),iPower-30) for iPower in xrange(2100-1979)]
            plt.plot(hist_change_year,hist_change_rate,color=greys[7],lw=1.5,ls="--",label="Historical Rate of Decline",zorder=1.0)

        elif i == kaya_cie_idx:
            plt.ylim(-0.3,1.1)
            plt.ylabel("Carbon Intensity of Energy (Index: 2010=1)")
            plt.plot(plt.gca().get_xlim(),[0,0],'k-',color=greys[4],zorder=1,lw=1.5)
            plt.fill_between(plt.gca().get_xlim(),[0,0],[-1,-1], facecolor=greys[4], alpha=0.15)
            annotate("Carbon net-negative energy sector",xy=(plt.gca().get_xlim()[0]+2,-0.02),ha='left',va='top',size=7)
            #do_ENE_range(aEM[i],plt,ecs_str="3C")

        elif i == kaya_eig_idx:
            plt.ylim(0.0,2.)
            plt.ylabel("Energy Intensity of GDP (Index: 2010=1)")         

            hist_change_year = [1980+iPower for iPower in xrange(2100-1979)]
            hist_change_rate = [math.pow((1-0.008),iPower-30) for iPower in xrange(2100-1979)]
            plt.plot(hist_change_year,hist_change_rate,color=greys[7],lw=1.5,ls="--",label="Historical Rate of Decline",zorder=1.0)
            
        BAU_index_value = aEM[i][BAUidx][yr2010idx]

        for j in range(len(nScen)):

            for anIndex, aValue in enumerate(aEM[i][j]):
                aEM[i][j][anIndex] = float(aValue)/BAU_index_value

            if "Historical" in nScen[j] and len(aHyr[i]) > 1:
                plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),marker="x",zorder=getZ(nScen[j]))
                if do_scatter_2100: plt.scatter(aHyr[i][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))

            elif insta_scen(nScen[j],"3C") == True:
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                if do_scatter_2100: scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                #annotate(int(round(aEM[i][j][-1],0)),xy=(2102,aEM[i][j][-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=8,weight='bold')

        if i == kaya_pop_idx:
            ax = plt.gca()
            handles, labels = plt.gca().get_legend_handles_labels()
            hls,lbs = legend_fliparoo(handles, labels,2)
            leg = ax.legend(hls,lbs,loc='lower right',labelspacing=0.75,ncol=2,fontsize=9,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)

            annotate("Historical data\nsource: FAO",xy=(aHyr[i][-5],aEM[i][HDidx][-5]),
                     ha='left',va='top',size=8,xycoords='data',xytext=(+5,-15), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=-0.2"))

        elif i == kaya_gdp_idx:
            annotate("Historical data source:\n(Maddison, 2006)",xy=(aHyr[i][-5],aEM[i][HDidx][-5]),
                     ha='left',va='top',size=8,xycoords='data',xytext=(+0,-10), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=-0.2"))

        elif i == kaya_eig_idx:
            annotate("Historical data source:\nIEA & (Maddison, 2006)",xy=(aHyr[i][-10],aEM[i][HDidx][-10]),
                     ha='left',va='top',size=8,xycoords='data',xytext=(+15,+20), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=+0.2"))

        elif i == kaya_cie_idx:
            annotate("Historical data\nsource: CDIAC & IEA",xy=(aHyr[i][-20],aEM[i][HDidx][-20]),
                     ha='left',va='top',size=8,xycoords='data',xytext=(-20,-15), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=-0.2"))            

    if i == ccs_factor_idx:
        plt.xlim(1950,2102)
        plt.ylim(0,100)
        insert_panel_label(plt,"a",1,1940)
        plt.ylabel("Gross Energy Emissions Captured [%]")
        sns.despine()       

        ccs_zeroes_string = "Scenarios without carbon\ncapture & sequestration:\n"

        for j in range(len(nScen)):
            if insta_scen(nScen[j],"3C") == True:
                ccs_values_holder = []

                for aCCSval in aEM[i][j]:
                    ccs_values_holder.append(aCCSval*100.)

                if ccs_values_holder[-1] == 0.:
                    ccs_zeroes_string += "   "+cop_scen_rep(nScen[j])+"\n"
                else:
                    plt.plot(aYear,ccs_values_holder,color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                             label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                    if do_scatter_2100: scatter([2100,],[ccs_values_holder[-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

        annotate(ccs_zeroes_string,xy=(0.03,0.03),xycoords="axes fraction",fontsize=8,ha='left',va='bottom')
        ax = plt.gca()
        leg = ax.legend(loc='best',ncol=1,fontsize=9,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)

    if i == rad_for_idx:
        plt.xlim(1950,2100)
        plt.ylim(0,6.5)
        plt.ylabel("Total Radiative Forcing [W m$^{-2}$]")
        sns.despine()       

        for j in range(len(nScen)):
            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1:
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="HadCRUT4 Data",marker="x",zorder=getZ(nScen[j]))
                    if do_scatter_2100: plt.scatter(aHyr[i][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))

            elif insta_scen(nScen[j],"3C") == True:
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                if do_scatter_2100: scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
        
        plt.plot(rcp_time[1:],rcp_for_tot_26[1:],color=greys[6],ls='-',lw=1,marker="8",ms=4,alpha=getalfa("RCP"),zorder=01)
        annotate("RCP 2.6",xy=(2102,rcp_for_tot_26[-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7,annotation_clip=False)

        plt.plot(rcp_time[1:],rcp_for_tot_45[1:],color=greys[6],ls='-',lw=1,marker="s",ms=4,alpha=getalfa("RCP"),zorder=01)
        annotate("RCP 4.5",xy=(2102,rcp_for_tot_45[-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7,annotation_clip=False)

        plt.plot(rcp_time[1:],rcp_for_tot_60[1:],color=greys[6],ls='-',lw=1,marker=">",ms=4,alpha=getalfa("RCP"),zorder=01)
        annotate("RCP 6.0",xy=(2102,rcp_for_tot_60[-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7,annotation_clip=False)

        plt.plot(rcp_time[1:],rcp_for_tot_85[1:],color=greys[6],ls='-',lw=1,marker="d",ms=4,alpha=getalfa("RCP"),zorder=01)
        annotate("RCP 8.5",xy=(2072,rcp_for_tot_85[-4]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7,annotation_clip=False)

        do_ENE_range(aEM[i],plt,ecs_str="3C")
        annotate("ECS = 3$^{\circ}$C/2xCO$_2$", xy=(0.98,0.03),xycoords='axes fraction',size=8,va="center",ha="right")
        insert_panel_label(plt,"c",1,1941)

    if i == atm_ppm_idx:
        plt.xlim(1950,2100)
        plt.ylim(300,800)
        plt.ylabel("Atmospheric CO$_2$ Concentration [ppm]")
        sns.despine()
        
        annotate("ECS = 3$^{\circ}$C/2xCO$_2$", xy=(0.98,0.03),xycoords='axes fraction',size=8,va="center",ha="right")

        atm_co2_file = open('atmospheric_co2_ppm.csv', 'w')
        atm_co2_file.write("Year,")
        for out_aYear in aYear:
            atm_co2_file.write(str(out_aYear)+",")
        atm_co2_file.write("\n")
        for j in range(len(nScen)):
            atm_co2_file.write(nScen[j]+",")
            for out_aVal in aEM[i][j]:
                atm_co2_file.write(str(out_aVal)+",")
            atm_co2_file.write("\n")
        atm_co2_file.close()
            
        for j in range(len(nScen)):

            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1:
                    # This comes from HadCRUT4
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="CDIAC Data",marker="x",zorder=getZ(nScen[j]))
                    if do_scatter_2100: plt.scatter(aHyr[i][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))

            elif insta_scen(nScen[j],"3C") == True:
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                if do_scatter_2100: scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
        
        plt.plot(rcp_time[2:],rcp_ppm_26[2:],color=greys[6],ls='-',lw=1,marker="8",ms=4,alpha=getalfa("RCP"),zorder=01,clip_on=False)
        annotate("RCP 2.6",xy=(2102,rcp_ppm_26[-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7,annotation_clip=False)

        plt.plot(rcp_time[2:],rcp_ppm_45[2:],color=greys[6],ls='-',lw=1,marker="s",ms=4,alpha=getalfa("RCP"),zorder=01,clip_on=False)
        annotate("RCP 4.5",xy=(2102,rcp_ppm_45[-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7,annotation_clip=False)

        plt.plot(rcp_time[2:],rcp_ppm_60[2:],color=greys[6],ls='-',lw=1,marker=">",ms=4,alpha=getalfa("RCP"),zorder=01,clip_on=False)
        annotate("RCP 6.0",xy=(2102,rcp_ppm_60[-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7,annotation_clip=False)

        plt.plot(rcp_time[2:],rcp_ppm_85[2:],color=greys[6],ls='-',lw=1,marker="d",ms=4,alpha=getalfa("RCP"),zorder=01)
        annotate("RCP 8.5",xy=(2076,rcp_ppm_85[-3]),xycoords='data',xytext=(2,-3), textcoords='offset points',size=7,ha='right')

        do_ENE_range(aEM[i],plt,ecs_str="3C")

        insert_panel_label(plt,"a",1)

    if "Net Emissions" in EMtypes[i]:
        for j in range(len(nScen)):
            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1: 
                    # This comes from HadCRUT4
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="HadCRUT4 Data",marker="x",zorder=getZ(nScen[j]))
                    if do_scatter_2100: plt.scatter(aHyr[i][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))

            elif insta_scen(nScen[j],"3C") == True:
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                if do_scatter_2100: scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                
        # This Historical Data is from the RCP database
        plt.plot(rcp_hist_time, rcp_hist_em,color=get_color('HistoricalData'),linewidth=get_linewidth("HistoricalData"),label='RCP Data',marker="x",zorder=100)
        plt.scatter(rcp_hist_time[-1],rcp_hist_em[-1],10,color=cop_color("HistoricalData"),zorder=getZ("HistoricalData"))
                    
        plt.plot(rcp_time[1:],rcp_em_26[1:],color=greys[6],ls='-',lw=1,marker="8",ms=4,alpha=getalfa("RCP"),zorder=01,clip_on=False)
        annotate("RCP 2.6",xy=(2102,rcp_em_26[-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7,annotation_clip=False)

        plt.plot(rcp_time[1:],rcp_em_45[1:],color=greys[6],ls='-',lw=1,marker="s",ms=4,alpha=getalfa("RCP"),zorder=01,clip_on=False)
        annotate("RCP 4.5",xy=(2102,rcp_em_45[-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7,annotation_clip=False)

        plt.plot(rcp_time[1:],rcp_em_60[1:],color=greys[6],ls='-',lw=1,marker=">",ms=4,alpha=getalfa("RCP"),zorder=01,clip_on=False)
        annotate("RCP 6.0",xy=(2102,rcp_em_60[-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7,annotation_clip=False)

        plt.plot(rcp_time[1:],rcp_em_85[1:],color=greys[6],ls='-',lw=1,marker="d",ms=4,alpha=getalfa("RCP"),zorder=01)
        annotate("RCP 8.5",xy=(2062,rcp_em_85[-5]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7)

        do_ENE_range(aEM[i],plt,ecs_str="3C")

        plt.xlim(1950,2100)
        plt.plot([1950,2100],[0,0],'k-',color=greys[7],zorder=1.2,lw=1.0)
        plt.ylim(-6,25)
        plt.ylabel("Net Anthropogenic Emissions (Ann.) [PgC yr$^{-1}$]")
        insert_panel_label(plt,"a",1,1941)

        range_with_capitals(plt,-10,1,n_subplot=1,year=2000,hd_source='IPCC')
        range_with_capitals(plt,-10,1,n_subplot=1,year=2000,hd_source='CMIP5')

    if "Temperature Anomalies" in EMtypes[i]:

        plt.xlim(1950,2120)
        plt.ylim(0,4.5)
        plt.xticks([1960,1980,2000,2020,2040,2060,2080,2100])

        plt.ylabel("Temperature Anomaly [$^{\circ}$C]")
        annotate("HadCRUT4 Data",xy=(1990,0.4), xycoords='data',xytext=(-17,-20), textcoords='offset points',size=7,ha='left',va='bottom',
                 arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=0.2"))   

        y_off_hack = {"2.6":-0.01, "4.5":-0.05, "6.0":0.06, "8.5":0}
        rcp_dict = {}
    
        for j in range(len(nScen)):
            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1: 
                    # This historical data is from HADCRUT4
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="HadCRUT4 Data",marker="x",zorder=getZ(nScen[j]))
                    if do_scatter_2100: plt.scatter(aHyr[i][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))  

            if "RCP" in nScen[j]:
                idx_key = nScen[j].find("RCP")
                rcp_str = nScen[j][idx_key+3]+"."+nScen[j][idx_key+4]
                rcp_str = rcp_str.replace("2.5","2.6")
                
                rcp_dict[rcp_str] = j
                
                plt.plot(aYear,aEM[i][j],color=get_color(rcp_str),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

                rcp_str2 = "RCP "+rcp_str.replace("4.5","4.5*")                
                annotate(rcp_str2,xy=(2103,aEM[i][j][-1]+y_off_hack[rcp_str]),xycoords='data',color=get_color(rcp_str),size=7,ha='left',va='center')

        annotate("Emissions pathway\nfor non-CO$_2$ gases\n(exogenous)",xy=(2110,4.25),xycoords='data',color=greys[6],size=7,weight='bold',ha='center',va='center')        
        annotate("*RCP 4.5 is exogenously\nassumed to describe non-CO$_2$\nemissions pathways for all\nFeliX scenarios.",
                 xy=(2065,0.5),xycoords='data',color=greys[6],size=7,ha='left',va='center')   
        plt.fill_between(aYear,aEM[i][rcp_dict["2.6"]],aEM[i][rcp_dict["8.5"]],edgecolor='none',facecolor=greys[3],alpha=0.30)
        #annotate("$\Delta$T = "+str(round(aEM[i][rcp_dict["8.5"]][-1]-aEM[i][rcp_dict["2.6"]][-1],1)),
        #         (2119,aEM[i][rcp_dict["2.6"]][-1]+(aEM[i][rcp_dict["8.5"]][-1]-aEM[i][rcp_dict["2.6"]][-1])/2),size=9,va='center',ha='left')
        #plt.fill_between(aYear,aEM[i][rcp_dict["4.5"]],aEM[i][rcp_dict["6.0"]],edgecolor='none',facecolor=cop_color("BAU"),alpha=0.30)

        sns.despine()
        insert_panel_label(plt,"b",1)
        plt.grid(True)
        plt.draw()
        plt.savefig('figures/temp_anomaly_RCPs.pdf',format='pdf')
        plt.clf()
        plt.close('all')        

        ecs_str = ["2.5C",0]
        while ecs_str[1] < 3:
            print " -->",ecs_str
            
            plt.xlim(1950,2135)
            plt.ylabel("Temperature Anomaly [$^{\circ}$C]")
            annotate("HadCRUT4 Data",xy=(1990,0.4), xycoords='data',xytext=(-17,-20), textcoords='offset points',size=7,ha='left',va='bottom',
                     arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=0.2"))

            if ecs_str[1] == 0: insert_panel_label(plt,"b",1940)
            if ecs_str[1] == 1: insert_panel_label(plt,"d",1)

            if ecs_str[1] == 2:
                plt.xlim(1950,2120)
                plt.ylim(0,4.5)
                plt.xticks([1960,1980,2000,2020,2040,2060,2080,2100])

                for j in range(len(nScen)):     
                    if "Historical" in nScen[j]:
                        if len(aHyr[i]) > 1: 
                            # This historical data is from HADCRUT4
                            plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="HadCRUT4 Data",marker="x",zorder=getZ(nScen[j]))
                            if do_scatter_2100: plt.scatter(aHyr[i][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))  

                        # RCP Projections
                        scatter([2104,],[rcp_temp_26[1],],dots,marker="8",color=get_color("2.6"))
                        scatter([2108,],[rcp_temp_45[1],],dots,marker="s",color=get_color("4.5"))
                        scatter([2112,],[rcp_temp_60[1],],dots,marker=">",color=get_color("6.0"))
                        scatter([2116,],[rcp_temp_85[1],],dots,marker="d",color=get_color("8.5"))
                        
                        annotate('RCP 2.6',xy=(2105, rcp_temp_26[1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7)
                        annotate('RCP 4.5',xy=(2109, rcp_temp_45[1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7)
                        annotate('RCP 6.0',xy=(2113, rcp_temp_60[1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7)
                        annotate('RCP 8.5',xy=(2117, rcp_temp_85[0]+0.1), xycoords='data',xytext=(0,-20), 
                                 textcoords='offset points',size=7,arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=0.5"))
                        
                        plt.plot([2104,2104],[rcp_temp_26[0],rcp_temp_26[2]],'k-',color=get_color("2.6"),lw=2.0)
                        plt.plot([2103,2105],[rcp_temp_26[0],rcp_temp_26[0]],'k-',color=get_color("2.6"),lw=2.0)
                        plt.plot([2103,2105],[rcp_temp_26[2],rcp_temp_26[2]],'k-',color=get_color("2.6"),lw=2.0)
                        #
                        plt.plot([2108,2108],[rcp_temp_45[0],rcp_temp_45[2]],'k-',color=get_color("4.5"),lw=2.0)
                        plt.plot([2107,2109],[rcp_temp_45[0],rcp_temp_45[0]],'k-',color=get_color("4.5"),lw=2.0)
                        plt.plot([2107,2109],[rcp_temp_45[2],rcp_temp_45[2]],'k-',color=get_color("4.5"),lw=2.0)
                        #
                        plt.plot([2112,2112],[rcp_temp_60[0],rcp_temp_60[2]],'k-',color=get_color("6.0"),lw=2.0)
                        plt.plot([2111,2113],[rcp_temp_60[0],rcp_temp_60[0]],'k-',color=get_color("6.0"),lw=2.0)
                        plt.plot([2111,2113],[rcp_temp_60[2],rcp_temp_60[2]],'k-',color=get_color("6.0"),lw=2.0)
                        #
                        plt.plot([2116,2116],[rcp_temp_85[0],rcp_temp_85[2]],'k-',color=get_color("8.5"),lw=2.0)
                        plt.plot([2115,2117],[rcp_temp_85[0],rcp_temp_85[0]],'k-',color=get_color("8.5"),lw=2.0)

                    elif nScen[j] == "BAU 15C": bau_15C_idx = j
                    elif nScen[j] == "BAU":     bau_25C_idx = j
                    elif nScen[j] == "BAU 3C":  bau_30C_idx = j
                    elif nScen[j] == "BAU 45C": bau_45C_idx = j

                    elif nScen[j] == "FossilBAU 15C": fbau_15C_idx = j
                    elif nScen[j] == "FossilBAU":     fbau_25C_idx = j
                    elif nScen[j] == "FossilBAU 3C":  fbau_30C_idx = j
                    elif nScen[j] == "FossilBAU 45C": fbau_45C_idx = j

                    elif nScen[j] == "BioEnergy 15C": be_15C_idx = j
                    elif nScen[j] == "BioEnergy":     be_25C_idx = j
                    elif nScen[j] == "BioEnergy 3C":  be_30C_idx = j
                    elif nScen[j] == "BioEnergy 45C": be_45C_idx = j

                    #elif (nScen[j] == "BAU" or nScen[j] == "BAU 3C" or nScen[j] == "FossilBAU" or nScen[j] == "FossilBAU 3C"):
                    #    plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                    #             label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

                plt.fill_between(aYear, aEM[i][bau_15C_idx], aEM[i][bau_45C_idx],edgecolor='none',facecolor=cop_color("BAU"),alpha=0.15)
                plt.fill_between(aYear, aEM[i][bau_25C_idx], aEM[i][bau_30C_idx],edgecolor='none',facecolor=cop_color("BAU"),alpha=0.30)

                annotate('ECS = 4.5$^{\circ}$C/2xCO$_2$',xy=(aYear[-25],aEM[i][bau_45C_idx][-25]),xycoords='data',xytext=(-25,+10),
                         textcoords='offset points',size=8,ha='right',arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=-0.15"))
                annotate('ECS = 3.0',xy=(aYear[-25],aEM[i][bau_30C_idx][-25]),xycoords='data',xytext=(-25,+10),
                         textcoords='offset points',size=8,ha='right',arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=-0.15"))
                annotate('ECS = 2.5',xy=(aYear[-50],aEM[i][bau_25C_idx][-50]),xycoords='data',xytext=(+25,-10),
                         textcoords='offset points',size=8,ha='left',arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=-0.15"))
                annotate('ECS = 1.5',xy=(aYear[-50],aEM[i][bau_15C_idx][-50]),xycoords='data',xytext=(+25,-10),
                         textcoords='offset points',size=8,ha='left',arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=-0.15"))

                #plt.fill_between(aYear,aEM[i][fbau_25C_idx],aEM[i][fbau_30C_idx],edgecolor='none',facecolor=cop_color("FossilBAU"),alpha=0.30)
                #plt.fill_between(aYear,aEM[i][fbau_15C_idx],aEM[i][fbau_45C_idx],edgecolor='none',facecolor=cop_color("FossilBAU"),alpha=0.15)

                #plt.fill_between(aYear, aEM[i][be_25C_idx], aEM[i][be_30C_idx],edgecolor='none',facecolor=cop_color("BioEnergy"),alpha=0.30)
                #plt.fill_between(aYear, aEM[i][be_15C_idx], aEM[i][be_45C_idx],edgecolor='none',facecolor=cop_color("BioEnergy"),alpha=0.15)

                #plt.fill_between(aYear,aEM[i][be3_25C_idx],aEM[i][be3_30C_idx],edgecolor='none',facecolor=cop_color("BioEnergy2 CCS75"),alpha=0.30)
                #plt.fill_between(aYear,aEM[i][be3_15C_idx],aEM[i][be3_45C_idx],edgecolor='none',facecolor=cop_color("BioEnergy2 CCS75"),alpha=0.15)

                sns.despine()
                plt.grid(True)
                insert_panel_label(plt,"a",1)
                plt.draw()
                plt.savefig('figures/biomass_'+EMtypes[i].replace("&","").replace("+","").replace("  ","_").replace(" ","_")+'_comparison.pdf',format='pdf', dpi=1200)
                plt.clf()
                plt.close('all')

                ecs_str[1] += 1
                continue
                
            plt.ylim(0,3.6)
            ylims = plt.gca().get_ylim()
            plt.fill_between([2080,2100],[ylims[0],ylims[0]],[ylims[1],ylims[1]],facecolor=greys[4], alpha=0.15)

            for j in range(len(nScen)):
            
                if "Historical" in nScen[j]:
                    if len(aHyr[i]) > 1: 
                        # This historical data is from HADCRUT4
                        plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="HadCRUT4 Data",marker="x",zorder=getZ(nScen[j]))
                        if do_scatter_2100: plt.scatter(aHyr[i][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))

                    # RCP Projections
                    scatter([2120,],[rcp_temp_26[1],],dots,marker="8",color=get_color("2.6"))
                    scatter([2124,],[rcp_temp_45[1],],dots,marker="s",color=get_color("4.5"))
                    scatter([2128,],[rcp_temp_60[1],],dots,marker=">",color=get_color("6.0"))
                    scatter([2132,],[rcp_temp_85[1],],dots,marker="d",color=get_color("8.5"))
            
                    annotate('RCP 2.6',xy=(2121, rcp_temp_26[1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7)
                    annotate('RCP 4.5',xy=(2125, rcp_temp_45[1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7)
                    annotate('RCP 6.0',xy=(2129, rcp_temp_60[1]), xycoords='data',xytext=(2,-3), textcoords='offset points',size=7)
                    annotate('RCP 8.5',xy=(2131, rcp_temp_85[0]+0.1), xycoords='data',xytext=(0,-20), 
                             textcoords='offset points',size=7,arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=0.5"))

                    plt.plot([2120,2120],[rcp_temp_26[0],rcp_temp_26[2]],'k-',color=get_color("2.6"),lw=2.0)
                    plt.plot([2119,2121],[rcp_temp_26[0],rcp_temp_26[0]],'k-',color=get_color("2.6"),lw=2.0)
                    plt.plot([2119,2121],[rcp_temp_26[2],rcp_temp_26[2]],'k-',color=get_color("2.6"),lw=2.0)
                    #
                    plt.plot([2124,2124],[rcp_temp_45[0],rcp_temp_45[2]],'k-',color=get_color("4.5"),lw=2.0)
                    plt.plot([2123,2125],[rcp_temp_45[0],rcp_temp_45[0]],'k-',color=get_color("4.5"),lw=2.0)
                    plt.plot([2123,2125],[rcp_temp_45[2],rcp_temp_45[2]],'k-',color=get_color("4.5"),lw=2.0)
                    #
                    plt.plot([2128,2128],[rcp_temp_60[0],rcp_temp_60[2]],'k-',color=get_color("6.0"),lw=2.0)
                    plt.plot([2127,2129],[rcp_temp_60[0],rcp_temp_60[0]],'k-',color=get_color("6.0"),lw=2.0)
                    plt.plot([2127,2129],[rcp_temp_60[2],rcp_temp_60[2]],'k-',color=get_color("6.0"),lw=2.0)
                    #
                    plt.plot([2132,2132],[rcp_temp_85[0],rcp_temp_85[2]],'k-',color=get_color("8.5"),lw=2.0)
                    plt.plot([2131,2133],[rcp_temp_85[0],rcp_temp_85[0]],'k-',color=get_color("8.5"),lw=2.0)
                    
                if ecs_str[0] == "3C" and "3C" not in nScen[j]: continue
                elif ecs_str[0] != "3C" and "3C" in nScen[j]: continue
                temp_label_str = nScen[j].replace("3C","")
                
                # Not using char scenarios at all right now
                if "char" in nScen[j]: continue

                if insta_scen(nScen[j],ecs_str[0]) == True:
                    plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                             label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                    #scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

                    # Hack to calculate average anomaly 2081-2100:
                    avgTempAnom = 0
                    avgTempAnom_count = 0
                    for avgYears_idx, avgYears in enumerate(aYear):
                        if avgYears >= 2081 and avgYears <= 2100:
                            avgTempAnom += aEM[i][j][avgYears_idx]
                            avgTempAnom_count += 1

                    assert(avgTempAnom_count == 20)
                    avgTempAnom = avgTempAnom/avgTempAnom_count
                
                    if insta_scen(nScen[j],ecs_str[0]) == True:
                        annotate(str(round(avgTempAnom,1))+"$^{\circ}$C",xy=(2110,aEM[i][j][-1]),xycoords='data',ha='center',va='center',size=7,weight='bold')

            do_ENE_range(aEM[i],plt,ecs_str[0])
         
            annotate("$\Delta$T [2081-2100]",xy=(2117.5,0.55),xycoords='data',ha='center',va='center',size=7) 
            plt.plot([2103,2132],[0.64,0.64],'k-',color='black',lw=1.5)
            plt.plot([2103,2103],[0.64,0.67],'k-',color='black',lw=1.5)
            plt.plot([2132,2132],[0.64,0.67],'k-',color='black',lw=1.5)
        
            annotate("ECS = "+ecs_str[0][:-1]+"$^{\circ}$C/2xCO$_2$", xy=(0.98,0.03),xycoords='axes fraction',size=8,va="center",ha="right")
            
            #if ecs_str[1] <= 1:
            sns.despine()
            plt.grid(True)
            plt.draw()
            plt.savefig('figures/biomass_'+EMtypes[i].replace("&","").replace("+","").replace("  ","_").replace(" ","_")+'_'+ecs_str[0].replace(".","")+'.pdf',format='pdf')
            plt.clf()
            plt.close('all')
            ecs_str = ["3C",ecs_str[1]+1]

    if EMtypes[i] == "COP Ratio":
        plt.xlim(1950,2100)
        plt.ylim(-1.0,3.0)

        for j in range(len(nScen)):
            if "Historical" in nScen[j]: continue
            elif insta_scen(nScen[j],"3C") == True:
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         label=nScen[j],alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

    if EMtypes[i] == "Total C Emission from Energy Sector":
        print "Running COP Ratio Plots"

        # Transient Climate Sensitivity switch
        ecs_str = ["2.5C",0]

        plt.xlim(1950,2100)
        plt.ylim(-1.0,3.0)

        while ecs_str[1] < 2:
                    
            xTM = 2116
            xTMpmA = 1
            xTMpm = 1.5
            xTMtxt =  xTMpmA+5.5

            hack_i = ann_esec_idx

            for j in range(len(nScen)):
            
                if "Historical" in nScen[j]:
                    if len(aHyr[hack_i]) > 1: 
                        plt.plot(aHyr[hack_i],aEM[hack_i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="HadCRUT4 Data",marker="x",zorder=getZ(nScen[j]))
                else:
                    master_numerator = np.array(aEM[hack_i][j])
                    master_denominator = np.array(aEM[hack_i][j])
                    master_denominator -= np.array(aEM[hack_i][j])
                
                    for ij in range(nEM):
                        
                        if EMtypes[ij] == "Afforestation":
                            master_numerator -= np.array(aEM[ij][j])
                        if EMtypes[ij] == "C Emission from Land Use Change":
                            master_numerator += np.array(aEM[ij][j])
                        if EMtypes[ij] == "Leeching to Atmosphere":
                            master_numerator += np.array(aEM[ij][j])
                        if EMtypes[ij] == "Flux Atmosphere to Land Sink":
                            master_denominator += np.array(aEM[ij][j])
                        if EMtypes[ij] == "Flux Atmosphere to Ocean":
                            master_denominator += np.array(aEM[ij][j])

                        if "Temperature Anomalies" in EMtypes[ij]:
                            #temperature_string = "$\Delta$T = "+str(round(aEM[ij][j][-1],1))+"$^{\circ}$C"
                            temperature_string = str(round(aEM[ij][j][-1],1))

                    if plot_rcop == False:
                        airfrac_denom = master_numerator
                        airfrac_numer = master_numerator-master_denominator
                        
                        master_numerator = airfrac_numer
                        master_denominator = airfrac_denom
                        
                    master_quotient = master_numerator/master_denominator
                    
                    if ecs_str[0] == "3C" and "3C" not in nScen[j]: continue
                    elif ecs_str[0] != "3C" and "3C" in nScen[j]: continue
                    temp_label_str = nScen[j].replace("3C","")
                
                    # Not using char scenarios at all right now
                    if "char" in nScen[j]: continue

                    append_str_hack = ""

                    if insta_scen(nScen[j],ecs_str[0]) == True:
                        if "BAU" in nScen[j]:
                            plt.plot(aYear,master_quotient,color=cop_color(nScen[j]),ls=cop_style(nScen[j]),
                                     lw=get_linewidth(nScen[j]),label=temp_label_str,alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                            plt.plot([xTM-xTMpm,xTM+xTMpm],[master_quotient[-1],master_quotient[-1]], 'k-', color=cop_color(nScen[j]),lw=3.0)
                            annotate(temperature_string,xy=(xTM-xTMtxt,master_quotient[-1]),size=lf_sz, va='center',ha='center',weight='bold')

                        else:
                            if "BioEnergy CCS40p" in nScen[j]:     ccs40_bound = master_quotient
                            if "BioEnergy CCS80p" in nScen[j]:     ccs80_bound = master_quotient
                            if "BioEnergy3 CCS40p" in nScen[j]: be3ccs40_bound = master_quotient
                            if "BioEnergy3 CCS80p" in nScen[j]: be3ccs80_bound = master_quotient

                        #HACK - here and below: denominator goes negative (sinks begin outgassing) so ratio flips to positive...
                            if plot_rcop == True and "CCS80" in nScen[j]:
                                print "--> running the fix on RCOP plots to fix scenarios that flip positive"
                                holdRatio = master_quotient[0]
                                for iRatio in range(len(master_quotient)):
                                    if holdRatio < 0 and master_quotient[iRatio] > 0:
                                        master_quotient[iRatio]*=-1
                                    holdRatio = master_quotient[iRatio]
                                if "BioEnergy3 CCS80" in nScen[j]: append_str_hack = "noRange"
                                
                            plt.plot(aYear,master_quotient,color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]+append_str_hack),
                                     label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                            #print " ",nScen[j], master_quotient[-1]
                        if do_scatter_2100: scatter([2100,],[master_quotient[-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

                    elif "FossilBAU lo" in nScen[j]:
                        fbau_lo_bound = master_quotient
                    elif "FossilBAU hi" in nScen[j]:
                        fbau_hi_bound = master_quotient

                    elif "BAU lo" in nScen[j]:
                        bau_lo_bound = master_quotient
                    elif "BAU hi" in nScen[j]:
                        bau_hi_bound = master_quotient   

                    elif "BioEnergy lo CCS40p" in nScen[j]: 
                        ccs40_lo_bound = master_quotient

                    elif "BioEnergy hi CCS40p" in nScen[j]: 
                        ccs40_hi_bound = master_quotient
                        xtmp = xTM + 2*xTMpmA
                        annotate(temperature_string,xy=(xtmp+xTMtxt,master_quotient[-1]),size=lf_sz, va='center',ha='center',weight='bold')
                    
                    elif "BioEnergy lo CCS80p" in nScen[j]: 
                        ccs80_lo_bound = master_quotient

                        # HACK
                        if plot_rcop == True:
                            holdRatio = ccs80_lo_bound[0]
                            for iRatio in range(len(ccs80_lo_bound)):
                                if holdRatio < 0 and ccs80_lo_bound[iRatio] > 0:
                                    ccs80_lo_bound[iRatio]*=-1
                                holdRatio = ccs80_lo_bound[iRatio]
                        #low temp band (high)
                        annotate(temperature_string,xy=(xtmp+xTMtxt,plt.gca().get_ylim()[0]+0.15),size=lf_sz, va='center',ha='center',weight='bold')

                    elif "BioEnergy hi CCS80p" in nScen[j]: 
                        ccs80_hi_bound = master_quotient

                        # HACK
                        if plot_rcop == True:
                            holdRatio = ccs80_hi_bound[0]
                            for iRatio in range(len(ccs80_hi_bound)):
                                if holdRatio < 0 and ccs80_hi_bound[iRatio] > 0:
                                    ccs80_hi_bound[iRatio]*=-1
                                holdRatio = ccs80_hi_bound[iRatio]

                    elif nScen[j] == "BioEnergy lo" or nScen[j] == "BioEnergy lo 3C":
                        ccs00_lo_bound = master_quotient

                    elif  nScen[j] == "BioEnergy hi" or nScen[j] == "BioEnergy hi 3C": 
                        ccs00_hi_bound = master_quotient
                        xtmp = xTM - 2*xTMpmA
                        annotate(temperature_string,xy=(xtmp-xTMtxt,master_quotient[-1]),size=lf_sz, va='center',ha='center',weight='bold')

                    elif "BioEnergy3 lo CCS40p" in nScen[j]: 
                        be3ccs40_lo_bound = master_quotient
                        xtmp = xTM + 2*xTMpmA
                        annotate(temperature_string,xy=(xtmp+xTMtxt,master_quotient[-1]),size=lf_sz, va='center',ha='center',weight='bold')

                    elif "BioEnergy3 hi CCS40p" in nScen[j]: 
                        be3ccs40_hi_bound = master_quotient

                        # HACK
                        if plot_rcop == True:
                            holdRatio = be3ccs40_hi_bound[0]
                            for iRatio in range(len(be3ccs40_hi_bound)):
                                if holdRatio < 0 and be3ccs40_hi_bound[iRatio] > 0:
                                    be3ccs40_hi_bound[iRatio]*=-1
                                holdRatio = be3ccs40_hi_bound[iRatio]

                        #xtmp = xTM + 2*xTMpmA
                        plt.plot([xtmp,xtmp],[ccs40_hi_bound[-1],be3ccs40_lo_bound[-1]], 'k-', color=cop_color("BioEnergy CCS40"),lw=3.0)
                        plt.plot([xtmp-xTMpm,xtmp+xTMpm],[be3ccs40_lo_bound[-1],be3ccs40_lo_bound[-1]], 'k-', color=cop_color("BioEnergy CCS40"),lw=3.0)
                        plt.plot([xtmp-xTMpm,xtmp+xTMpm],[ccs40_hi_bound[-1],ccs40_hi_bound[-1]], 'k-', color=cop_color("BioEnergy CCS40"),lw=3.0)

                    elif "BioEnergy3 lo CCS80" in nScen[j]: 
                        be3ccs80_lo_bound = master_quotient
                     
                        # HACK
                        if plot_rcop == True:
                            holdRatio = be3ccs80_lo_bound[0]
                            for iRatio in range(len(be3ccs80_lo_bound)):
                                if holdRatio < 0 and be3ccs80_lo_bound[iRatio] > 0:
                                    be3ccs80_lo_bound[iRatio]*=-1
                                holdRatio = be3ccs80_lo_bound[iRatio]

                    elif "BioEnergy3 hi CCS80" in nScen[j]: 
                        plt.ylim(-1.,3.)   
                        be3ccs80_hi_bound = master_quotient

                        #HACK
                        if plot_rcop == True:
                            holdRatio = be3ccs80_hi_bound[0]
                            for iRatio in range(len(be3ccs80_hi_bound)):
                                if holdRatio < 0 and be3ccs80_hi_bound[iRatio] > 0:
                                    be3ccs80_hi_bound[iRatio]*=-1
                                holdRatio = be3ccs80_hi_bound[iRatio]

                        xtmp = xTM + 2*xTMpmA
                        #low temp band (low)
                        annotate(temperature_string,xy=(xtmp+xTMtxt,plt.gca().get_ylim()[0]-0.15),size=lf_sz,va='center',ha='center',weight='bold',annotation_clip=False)
              
                        plt.plot([xtmp,xtmp],[plt.gca().get_ylim()[0]-0.15,plt.gca().get_ylim()[0]+0.15], 'k-', color=cop_color("BioEnergy CCS80"),lw=3.0,clip_on=False)
                        plt.plot([xtmp-xTMpm,xtmp+xTMpm],[plt.gca().get_ylim()[0]+0.15,plt.gca().get_ylim()[0]+0.15], 'k-', color=cop_color("BioEnergy CCS80"),lw=3.0,clip_on=False)
                        plt.plot([xtmp-xTMpm,xtmp+xTMpm],[plt.gca().get_ylim()[0]-0.15,plt.gca().get_ylim()[0]-0.15], 'k-', color=cop_color("BioEnergy CCS80"),lw=3.0,clip_on=False)
                        #annotate("",xy=(xtmp+xTMtxt,plt.gca().get_ylim()[0]-0.15),size=lf_sz,va='center',ha='center',weight='bold',annotation_clip=False)
                        annotate("",xy=(2110,plt.gca().get_ylim()[0]-0.30), xycoords='data',xytext=(xtmp-xTMpm,plt.gca().get_ylim()[0]), 
                                    textcoords='data',arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=0.4"),annotation_clip=False)

                        # Arrow Bits
                        #plt.plot([xtmp-xTMpm,xtmp+xTMpm],[plt.gca().get_ylim()[0]+0.08,plt.gca().get_ylim()[0]+0.08], 'k-', color=cop_color("BioEnergy CCS80"),lw=3.0)
                        #plt.plot([xtmp,xtmp-xTMpm],[plt.gca().get_ylim()[0]+0.03,plt.gca().get_ylim()[0]+0.08], 'k-', color=cop_color("BioEnergy CCS80"),lw=3.0)
                        #plt.plot([xtmp,xtmp+xTMpm],[plt.gca().get_ylim()[0]+0.03,plt.gca().get_ylim()[0]+0.08], 'k-', color=cop_color("BioEnergy CCS80"),lw=3.0)

                    elif nScen[j] == "BioEnergy3 lo" or nScen[j] == "BioEnergy3 lo 3C": 
                        be3ccs00_lo_bound = master_quotient
                        xtmp = xTM - 2*xTMpmA
                        annotate(temperature_string,xy=(xtmp-xTMtxt,master_quotient[-1]),size=lf_sz, va='center',ha='center',weight='bold')
                        plt.plot([xtmp,xtmp],[ccs00_hi_bound[-1],be3ccs00_lo_bound[-1]], 'k-', color=cop_color("BioEnergy"),lw=3.0)
                        plt.plot([xtmp-xTMpm,xtmp+xTMpm],[be3ccs00_lo_bound[-1],be3ccs00_lo_bound[-1]], 'k-', color=cop_color("BioEnergy"),lw=3.0)
                        plt.plot([xtmp-xTMpm,xtmp+xTMpm],[ccs00_hi_bound[-1],ccs00_hi_bound[-1]], 'k-', color=cop_color("BioEnergy"),lw=3.0)

                    elif nScen[j] == "BioEnergy3 hi" or nScen[j] == "BioEnergy3 hi 3C": 
                        be3ccs00_hi_bound = master_quotient

            if plot_rcop == True: 
                if ecs_str[0] == "2.5C": ann_TA_yval = 2.6
                else: ann_TA_yval = 2.7
            else: ann_TA_yval = 4.9
            annotate("Temperature\nAnomaly [$^{\circ}$C]\n(2100)$\dagger$",xy=(2116,ann_TA_yval),size=lf_sz, va='bottom',ha='center',clip_on=False,weight='bold')

            plt.fill_between(aYear,fbau_lo_bound,fbau_hi_bound,edgecolor='none',facecolor=cop_color("FossilBAU"),alpha=0.45)
            plt.fill_between(aYear,bau_lo_bound,bau_hi_bound,edgecolor='none',facecolor=cop_color("BAU"),alpha=0.45)

            # This set of commands does each scenario independently          
            plt.fill_between(aYear,ccs00_lo_bound,ccs00_hi_bound,edgecolor='none',facecolor=cop_color("BioEnergy"),alpha=0.5)
            plt.fill_between(aYear,be3ccs00_lo_bound,be3ccs00_hi_bound,facecolor='none',alpha=1.0,hatch=hatch_str,edgecolor=cop_color("BioEnergy"))

            plt.fill_between(aYear,ccs80_lo_bound,ccs80_hi_bound,edgecolor='none',facecolor=cop_color("BioEnergy CCS80"),alpha=0.5)
            plt.fill_between(aYear,be3ccs80_lo_bound,be3ccs80_hi_bound,facecolor='none',alpha=1.0,hatch=hatch_str,edgecolor=cop_color("BioEnergy CCS80"))

            be_ccs40_lo_search = []
            be_ccs40_hi_search = []
            #                  
            be3_ccs40_lo_search = []
            be3_ccs40_hi_search = []

            for iYear in range(len(aYear)):
                be_ccs40_lo_search.append(min(ccs40_lo_bound[iYear],ccs40_hi_bound[iYear],ccs40_bound[iYear]))
                be_ccs40_hi_search.append(max(ccs40_lo_bound[iYear],ccs40_hi_bound[iYear],ccs40_bound[iYear]))
                #                  
                be3_ccs40_lo_search.append(min(be3ccs40_lo_bound[iYear],be3ccs40_hi_bound[iYear],be3ccs40_bound[iYear]))
                be3_ccs40_hi_search.append(max(be3ccs40_lo_bound[iYear],be3ccs40_hi_bound[iYear],be3ccs40_bound[iYear]))

            plt.fill_between(aYear,be_ccs40_lo_search,be_ccs40_hi_search,edgecolor='none',facecolor=cop_color("BioEnergy CCS40"),alpha=0.5)
            plt.fill_between(aYear,be3_ccs40_lo_search,be3_ccs40_hi_search,facecolor='none',alpha=1.0,hatch=hatch_str,edgecolor=cop_color("BioEnergy CCS40"))

            # This set of commands treats energy scenarios (LO->HI) as a continuum
            #plt.fill_between(aYear,ccs00_hi_bound,be3ccs00_lo_bound,edgecolor='none',facecolor=cop_color("BioEnergy"),alpha=0.5)
            ## For below: not using be3ccs40_lo_bound because it crosses the central line
            #plt.fill_between(aYear,ccs40_hi_bound,be3ccs40_bound,edgecolor='none',facecolor=cop_color("BioEnergy CCS40"),alpha=0.5)
            #plt.fill_between(aYear,ccs80_lo_bound,be3ccs80_hi_bound,edgecolor='none',facecolor=cop_color("BioEnergy CCS80"),alpha=0.5)           
            
            # This set of commands treats ccs efficiency (40->80) as a continuum
            #plt.fill_between(aYear,ccs00_lo_bound,ccs00_hi_bound,edgecolor='none',facecolor=cop_color("BioEnergy"),alpha=0.5)
            #plt.fill_between(aYear,be3ccs00_lo_bound,be3ccs00_hi_bound,facecolor='none',alpha=1.0,hatch=hatch_str,edgecolor=cop_color("BioEnergy"))
            #plt.fill_between(aYear,ccs40_bound,ccs80_bound,edgecolor='none',facecolor=cop_color("BioEnergy CCS40"),alpha=0.5)
            #plt.fill_between(aYear,be3ccs40_bound,be3ccs80_bound,edgecolor='none',facecolor=cop_color("BioEnergy CCS80"),alpha=0.5)
         
            # For period 2002-2011:
            # A = 8.3 pm 0.7 (FF & cement)
            # B = 0.9 pm 0.8 (LUC)
            # C = 2.4 pm 0.7 (Oceans)
            # D = 2.5 pm 1.3 (Land Sink)
            # T = 4.3 pm 0.2 (Net Atm Flux)
            # (8.3+0.9)/(2.4+2.5) = 1.878
            # Err = 0.22 (propagated quadratically, use T = A+B-C-D to replace C and D in denominator
            if plot_rcop == True:
                # Smaller error ranges
                #range_with_capitals(plt,1.971,0.273,n_subplot=1,year=1984.5,hd_source='IPCC')
                #range_with_capitals(plt,1.646,0.144,n_subplot=1,year=1994.5,hd_source='IPCC')
                #range_with_capitals(plt,1.878,0.205,n_subplot=1,year=2006.5,hd_source='IPCC')
                # Larger error ranges
                range_with_capitals(plt,1.971,0.626,n_subplot=1,year=1984.5,hd_source='IPCC')
                range_with_capitals(plt,1.646,0.434,n_subplot=1,year=1993,hd_source='IPCC')
                range_with_capitals(plt,1.878,0.507,n_subplot=1,year=2006.5,hd_source='IPCC')
              
            else:
                range_with_capitals(plt,3.68,0.205,n_subplot=1,year=2006.5,hd_source='IPCC')
                
            plt.plot([0,2100],[1,1],'k-',color=greys[6],ls="--",lw=1.0)
            plt.plot([0,2100],[0,0],'k-',color=greys[6],lw=1.25)
            plt.fill_between([2100,2132],[-10,-10],[10,10], facecolor=greys[4], alpha=0.15)
        
            annotate("Net Negative Atmospheric Flux",xy=(1980,0.95),size=lf_sz, va='top',ha='center')
            annotate("Net Positive Atmospheric Flux",xy=(1980,1.05),size=lf_sz, va='bottom',ha='center')
            annotate("Net Negative Anthropogenic\nEmissions (COP target)",xy=(1980,-0.05),size=lf_sz, va='top',ha='center')
            
            plt.xlim(1950,2132)
            plt.ylim(-1.,3.)         
            plt.ylabel("Ratio of Net Anthropogenic Emissions\nto Net Natural Sinks (R$_{AF}$)",size=yl_sz)

            if ecs_str[1] == 0:#RCOP
                sns.despine(bottom=True)
                plt.grid(True)
                insert_panel_label(plt,"a",1940)

                handles, labels = plt.gca().get_legend_handles_labels()
                hls,lbs = legend_fliparoo(handles, labels,2)
                leg = plt.legend(hls,lbs,bbox_to_anchor=(0.92,0.38,0.26,0.5),labelspacing=1,fontsize=9,
                                 bbox_transform=plt.gcf().transFigure,mode="expand",loc=3,ncol=1,borderpad=0.75,fancybox=True,frameon=True)

                annotate("$\dagger$ ECS = "+ecs_str[0].replace("C","")+"$^{\circ}$C/2xCO$_2$", xy=(0.12,0.0), xycoords=leg.get_frame(),size=8,va="center",ha="left")
                plt.draw()
                plt.savefig('figures/biomass_'+EMtypes[i].replace("&","").replace("+","").replace("  ","_").replace(" ","_")+'_25C.pdf',format='pdf', dpi=1200)
                plt.clf()
                plt.close('all')
                ecs_str = ["3C",ecs_str[1]+1]
                plt.ylim(-1.,3.)
            else: 
                ecs_str[1] += 1

    if EMtypes[i] == "Flux Atmosphere to Land Sink":

        fig = plt.gcf()
        fig.set_size_inches([size[0],size[1]*1.5])
        print "**Figure size set to ",fig.get_size_inches()

        for j in range(len(nScen)):
            
            plt.subplot(211)
            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1: 
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="Historical Data",marker="x",zorder=getZ(nScen[j]))
                range_with_capitals(plt,1.5,1.1,n_subplot=2,year=1984,hd_source='IPCC')  
                range_with_capitals(plt,2.6,1.2,n_subplot=2,year=1993.5,hd_source='IPCC')
                #range_with_capitals(plt,2.6,1.2,n_subplot=2,year=2004,hd_source='IPCC')        
                range_with_capitals(plt,2.5,1.3,n_subplot=2,year=2006,hd_source='IPCC')
                range_with_capitals(plt,2.7,0.7,n_subplot=2,year=1995.5,hd_source='CMIP5')
                
            elif insta_scen(nScen[j],"3C") == True:
                plt.subplot(211)
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),alpha=getalfa(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                if do_scatter_2100: scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

                plt.subplot(212)
                plt.plot(aYear,aEM[cum_lsk_em][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         alpha=getalfa(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                if do_scatter_2100: scatter([2100,],[aEM[cum_lsk_em][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

        plt.subplot(211)
        do_ENE_range(aEM[i],plt,ecs_str="3C")

        plt.grid(True)
        plt.xlim(1950,2100)
        plt.ylim(-2,4)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color=greys[7],lw=1.2,zorder=1,clip_on=False)
        plt.ylabel("Land Sink Uptake\n(Ann.) [PgC yr$^{-1}$]",size=yl_sz)

        insert_panel_label(plt,"c",2)

        plt.subplot(212)
        do_ENE_range(aEM[cum_lsk_em],plt,ecs_str="3C")

        plt.grid(True)
        plt.xlim(1950,2100)
        plt.ylim(0,500)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color=greys[7],lw=1.2,zorder=1,clip_on=False)
        range_with_capitals(plt,160,90,n_subplot=2,year=2011,hd_source='IPCC')
        range_with_capitals(plt,139,90,n_subplot=2,year=2005,hd_source='CMIP5')
        plt.ylabel("Land Sink Uptake\n(Cum.) [PgC]",size=yl_sz)
        annotate("ECS = 3$^{\circ}$C/2xCO$_2$", xy=(0.98,0.06),xycoords='axes fraction',size=8,va="center",ha="right")
    
    if EMtypes[i] == "Flux Atmosphere to Ocean":

        fig = plt.gcf()
        fig.set_size_inches([size[0],size[1]*1.5])
        print "**Figure size set to ",fig.get_size_inches()
        
        for j in range(len(nScen)):
            
            plt.subplot(211)
            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1: 
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="Historical Data",marker="x",zorder=getZ(nScen[j]))
                range_with_capitals(plt,2.0,0.7,n_subplot=2,year=1984,hd_source='IPCC')
                range_with_capitals(plt,2.2,0.7,n_subplot=2,year=1993.5,hd_source='IPCC')
                #range_with_capitals(plt,2.3,0.7,n_subplot=2,year=2004,hd_source='IPCC')
                range_with_capitals(plt,2.4,0.7,n_subplot=2,year=2006,hd_source='IPCC')
                range_with_capitals(plt,2.2,0.4,n_subplot=2,year=1995.5,hd_source='CMIP5')
                
            elif insta_scen(nScen[j],"3C") == True:
                plt.subplot(211)
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                         lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                if do_scatter_2100: scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

                plt.subplot(212)
                plt.plot(aYear,aEM[cum_ocn_em][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                         lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                if do_scatter_2100: scatter([2100,],[aEM[cum_ocn_em][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

        plt.subplot(211)
        do_ENE_range(aEM[i],plt,ecs_str="3C")
        insert_panel_label(plt,"b",2)

        plt.grid(True)
        sns.despine(bottom=True)
        plt.xlim(1950,2100)
        plt.ylim(-2,4)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color=greys[7],lw=1.2,zorder=1,clip_on=False)

        plt.ylabel("Net Ocean Uptake\n(Ann.) [PgC yr$^{-1}$]",size=yl_sz)

        plt.subplot(212)
        do_ENE_range(aEM[cum_ocn_em],plt,ecs_str="3C")

        range_with_capitals(plt,155,30,n_subplot=2,year=2011,hd_source='IPCC')
        range_with_capitals(plt,141,27,n_subplot=2,year=2005,hd_source='CMIP5')    
        
        plt.grid(True)
        plt.xlim(1950,2100)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color=greys[7],lw=1.2,zorder=1,clip_on=False)
        plt.ylim(0,500)
        plt.ylabel("Net Ocean Uptake\n (Cum.) [PgC]",size=yl_sz)
        annotate("ECS = 3$^{\circ}$C/2xCO$_2$", xy=(0.98,0.06),xycoords='axes fraction',size=8,va="center",ha="right")

    if i == ann_esec_idx:
        plt.clf()
        # Plotting 
        # 311) Annual Net Emissions from entire energy sector
        net_emissions_enesec = []
        # 312) Cumulative Sequestration (CCU/S)
        # 313) Cumulative Emissions from entire energy sector
        cum_emissions_enesec = []

        #need to subtract "Afforestation"
        for iil in range(nEM):
            if "Afforestation" in EMtypes[iil]:
                for j in range(len(nScen)):
                    if "Historical" not in nScen[j]:
                        net_emissions_enesec.append(np.array(aEM[i][j])-np.array(aEM[iil][j]))

        #need to subtract "Cumulative LULUC Emissions" from "Cumulative Emissions"
        for iil in range(nEM):
            if "Cumulative LULUC Emissions" in EMtypes[iil]:
                for j in range(len(nScen)):
                    if "Historical" not in nScen[j]:
                        cum_emissions_enesec.append(np.array(aEM[cum_em_idx][j])-np.array(aEM[iil][j]))

        for j in range(len(nScen)):

            if "Historical" in nScen[j]:
                if len(aHyr[ann_ffem_idx]) > 1: 
                    plt.subplot(311)
                    plt.plot(aHyr[ann_ffem_idx],aEM[ann_ffem_idx][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="CDIAC Data",marker="x",zorder=100)

                    range_with_capitals(plt,9.5,0.8,n_subplot=3)
                    # Average Concrete (1980-1989): 1.334E8/yr
                    range_with_capitals(plt,5.3666,0.4,n_subplot=3,year=1984)
                    # Average Concrete (1990-1999): 1.882E8/yr
                    range_with_capitals(plt,6.2118,0.5,n_subplot=3,year=1994)
                    # Average Concrete (2000-2009): 3.146E8/yr
                    range_with_capitals(plt,7.4854,0.6,n_subplot=3,year=2004)

                if len(aHyr[ann_ffem_idx]) > 1: 
                    plt.subplot(313)
                    plt.plot(aHyr[cum_ff_em],aEM[cum_ff_em][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="CDIAC Data",marker="x",zorder=100)

                    range_with_capitals(plt,366,30,n_subplot=3)   

                #if len(aHyr[cum_ff_em]) > 1: 
                #    plt.subplot(212)
                #    plt.plot(aHyr[cum_ff_em],aEM[cum_ff_em][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="Historical Data",marker="x",zorder=100)
                # IPCC Range: is there data?             
                        
            
            elif insta_scen(nScen[j],"3C") == True:
                plt.subplot(311)
                plt.plot(aYear,net_emissions_enesec[j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                         lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                if do_scatter_2100: scatter([2100,],[net_emissions_enesec[j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j])) 

                plt.subplot(312)
                plt.plot(aYear,aEM[cseq_em][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                         lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                if do_scatter_2100: scatter([2100,],[aEM[cseq_em][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

                plt.subplot(313)
                plt.plot(aYear,cum_emissions_enesec[j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                         lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                if do_scatter_2100: scatter([2100,],[cum_emissions_enesec[j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

        plt.subplot(311)
        plt.xlim(1950,2100)
        plt.ylim(-7,21)
        plt.grid(True)
        plt.ylabel("Net Energy Sector\nEmissions (Ann.) [PgC yr$^{-1}$]",size=yl_sz)
        do_ENE_range(net_emissions_enesec,plt,ecs_str="3C")
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color=greys[7],lw=1.2,zorder=1,clip_on=False)
        insert_panel_label(plt,"a",3,1926)

        handles, labels = plt.gca().get_legend_handles_labels()
        hls,lbs = legend_fliparoo(handles, labels,2)
        leg = plt.legend(hls,lbs,bbox_to_anchor=(0.92,0.50,0.26,0.5),labelspacing=1,fontsize=10,
                         bbox_transform=plt.gcf().transFigure,mode="expand",loc=3,ncol=1,
                         borderpad=0.75,fancybox=True,frameon=True)

        plt.subplot(312)
        plt.xlim(1950,2100)
        plt.ylim(0,1000)
        plt.grid(True)
        plt.ylabel("Carbon Sequestration\n(Cum.) [PgC]",size=yl_sz)
        do_ENE_range(aEM[cseq_em],plt,ecs_str="3C")
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color=greys[7],lw=1.2,zorder=1,clip_on=False)
        sns.despine(bottom=True)
        insert_panel_label(plt,"b",3,1926)

        plt.subplot(313)
        plt.xlim(1950,2100)
        plt.ylim(0,2000)
        plt.grid(True)
        plt.ylabel("Net Energy Sector\nEmissions (Cum.) [PgC]",size=yl_sz)
        do_ENE_range(cum_emissions_enesec,plt,ecs_str="3C")
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color=greys[7],lw=1.2,zorder=1,clip_on=False)
        insert_panel_label(plt,"c",3,1924)
            
    if i == ann_bem_idx:

        for iil in range(nEM):
            if "Total Additional Emissions" in EMtypes[iil]:
                for iik in range(nEM):
                    if "Afforestation" in EMtypes[iik]:
                        for iij in range(nEM):
                            if "CCS Improvement Factor" in EMtypes[iij]:
                                for j in range(len(nScen)):
                                    aEM[i][j] = np.array(aEM[i][j])*(np.array([1 for iim in range(len(aEM[iij][j]))])-np.array(aEM[iij][j]))+np.array(aEM[iil][j])-np.array(aEM[iik][j])
                              
        for j in range(len(nScen)):

            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1: 
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="Historical Data",marker="x",zorder=getZ(nScen[j]))
                # IPCC Range: is there data?             
                        
            elif insta_scen(nScen[j],"3C") == True:
                plt.subplot(211)
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                         lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                if do_scatter_2100: scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j])) 
                #annotate(round(aEM[i][j][-1],1),xy=(2102,aEM[i][j][-1]),size=lf_sz, va='center',ha='left',weight='bold')

                plt.subplot(212)
                plt.plot(aYear,aEM[cseq_em][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                         lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                if do_scatter_2100: scatter([2100,],[aEM[cseq_em][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

        plt.subplot(211)    
        do_ENE_range(aEM[i],plt,ecs_str="3C")

        plt.ylabel("Net Renewables\Emissions (Ann.) [PgC yr$^{-1}$]",size=yl_sz)
        plt.xlim(1950,2102)
        #plt.ylim(-6,1)
        plt.grid(True)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color=greys[7],zorder=1.2,lw=1.0)

        plt.subplot(212)
        do_ENE_range(aEM[cseq_em],plt,ecs_str="3C")

        plt.xlim(1950,2102)
        plt.ylim(0,1000)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color=greys[7],lw=1.2,zorder=1,clip_on=False)
        plt.ylabel("Carbon\nSequestration (Cum.) [PgC]",size=yl_sz)

    if EMtypes[i] == "C in Atmosphere":

        fig = plt.gcf()
        fig.set_size_inches(size)
        print "**Figure size set to ",fig.get_size_inches()
                
        for j in range(len(nScen)):

            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1: 
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="CDIAC Data",marker="x",zorder=getZ(nScen[j]))
                # IPCC Range: 230-250; C(preind,FeliX) = 606.411
                range_with_capitals(plt,846.411,10,n_subplot=1,hd_source='IPCC')                
            
            elif insta_scen(nScen[j],"3C") == True:
                if do_scatter_2100: scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                         lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))

            elif nScen[j] == "FossilBAU lo": fbau_lo_bound = aEM[i][j]
            elif nScen[j] == "FossilBAU hi": fbau_hi_bound = aEM[i][j]  
            elif nScen[j] == "BAU lo": bau_lo_bound = aEM[i][j]
            elif nScen[j] == "BAU hi": bau_hi_bound = aEM[i][j]          
            elif "BioEnergy lo CCS40p" in nScen[j]: ccs40_lo_bound = aEM[i][j]
            elif "BioEnergy hi CCS40p" in nScen[j]: ccs40_hi_bound = aEM[i][j]
            elif "BioEnergy lo CCS80p" in nScen[j]: ccs80_lo_bound = aEM[i][j]
            elif "BioEnergy hi CCS80p" in nScen[j]: ccs80_hi_bound = aEM[i][j]
            elif nScen[j] == "BioEnergy lo": ccs00_lo_bound = aEM[i][j]
            elif nScen[j] == "BioEnergy hi": ccs00_hi_bound = aEM[i][j]
            elif "BioEnergy2 lo CCS40p" in nScen[j]: be2ccs40_lo_bound = aEM[i][j]
            elif "BioEnergy2 hi CCS40p" in nScen[j]: be2ccs40_hi_bound = aEM[i][j]
            elif "BioEnergy2 lo CCS80p" in nScen[j]: be2ccs80_lo_bound = aEM[i][j]
            elif "BioEnergy2 hi CCS80p" in nScen[j]: be2ccs80_hi_bound = aEM[i][j]
            elif nScen[j] == "BioEnergy2 lo": be2ccs00_lo_bound = aEM[i][j]
            elif nScen[j] == "BioEnergy2 hi": be2ccs00_hi_bound = aEM[i][j]
            elif "BioEnergy3 lo CCS40p" in nScen[j]: be3ccs40_lo_bound = aEM[i][j]
            elif "BioEnergy3 hi CCS40p" in nScen[j]: be3ccs40_hi_bound = aEM[i][j]
            elif "BioEnergy3 lo CCS80p" in nScen[j]: be3ccs80_lo_bound = aEM[i][j]
            elif "BioEnergy3 hi CCS80p" in nScen[j]: be3ccs80_hi_bound = aEM[i][j]
            elif nScen[j] == "BioEnergy3 lo": be3ccs00_lo_bound = aEM[i][j]
            elif nScen[j] == "BioEnergy3 hi": be3ccs00_hi_bound = aEM[i][j]

        plt.fill_between(aYear,ccs00_lo_bound,ccs00_hi_bound,facecolor=cop_color("BioEnergy"),edgecolor='none',alpha=0.5)
        plt.fill_between(aYear,ccs40_lo_bound,ccs40_hi_bound,facecolor=cop_color("BioEnergy CCS40"),edgecolor='none',alpha=0.5)
        plt.fill_between(aYear,ccs80_lo_bound,ccs80_hi_bound,facecolor=cop_color("BioEnergy CCS80"),edgecolor='none',alpha=0.5)
        #
        plt.fill_between(aYear,be3ccs00_lo_bound,be3ccs00_hi_bound,facecolor='none',edgecolor=cop_color("BioEnergy"),hatch=hatch_str,alpha=1.0)
        plt.fill_between(aYear,be3ccs40_lo_bound,be3ccs40_hi_bound,facecolor='none',edgecolor=cop_color("BioEnergy CCS40"),hatch=hatch_str,alpha=1.0)
        plt.fill_between(aYear,be3ccs80_lo_bound,be3ccs80_hi_bound,facecolor='none',edgecolor=cop_color("BioEnergy CCS80"),hatch=hatch_str,alpha=1.0)
        plt.ylabel("Atmospheric Carbon [PgC]",size=yl_sz)

    if EMtypes[i] == "C Emission from Land Use Change":

        fig = plt.gcf()
        fig.set_size_inches([size[0],size[1]*2])
        print "**Figure size set to ",fig.get_size_inches()
        
        for j in range(len(nScen)):

            if "Historical" in nScen[j]: 

                if len(aHyr[i]) > 1: 
                    plt.subplot(211) 

                    rcp_lulucf_low = []
                    rcp_lulucf_high = []
                    for nstep, istep in enumerate(rcp_time):
                        rcp_lulucf_low.append(min([rcp_luc_26[nstep],rcp_luc_45[nstep],rcp_luc_60[nstep],rcp_luc_85[nstep]]))
                        rcp_lulucf_high.append(max([rcp_luc_26[nstep],rcp_luc_45[nstep],rcp_luc_60[nstep],rcp_luc_85[nstep]]))                      
                    plt.fill_between(rcp_time,rcp_lulucf_low,rcp_lulucf_high,facecolor=greys[4],alpha=0.5)

                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="CDIAC Data",marker="x",zorder=getZ(nScen[j]))
                    plt.plot(rcp_h_time_lulucf,rcp_h_ann_lulucf,color=greys[4],ls='-',lw=1,marker="8",ms=4,label='RCP Data',alpha=getalfa("RCP"),zorder=01)

                    range_with_capitals(plt,0.9,0.8,n_subplot=2,year=2011,hd_source='IPCC')
                    range_with_capitals(plt,1.4,0.8,n_subplot=2,year=1984,hd_source='IPCC')
                    range_with_capitals(plt,1.5,0.8,n_subplot=2,year=1993.5,hd_source='IPCC')
                    range_with_capitals(plt,1.1,0.8,n_subplot=2,year=2004,hd_source='IPCC')
                    range_with_capitals(plt,1.1,0.5,n_subplot=2,year=1995.5,hd_source='CMIP5')

                    annotate('Full range of RCP\nprojections',size=7, xy=(2040,-0.25),ha='center',va='center',color=greys[6])
                   
                plt.subplot(212)

                rcp_lulucf_cum_low = []
                rcp_lulucf_cum_high = []                    
                for nstep, istep in enumerate(rcp_time):
                    rcp_lulucf_cum_low.append(min([rcp_luc_cum_26[nstep],rcp_luc_cum_45[nstep],rcp_luc_cum_60[nstep],rcp_luc_cum_85[nstep]]))
                    rcp_lulucf_cum_high.append(max([rcp_luc_cum_26[nstep],rcp_luc_cum_45[nstep],rcp_luc_cum_60[nstep],rcp_luc_cum_85[nstep]]))   
                plt.fill_between(rcp_time,rcp_lulucf_cum_low,rcp_lulucf_cum_high,facecolor=greys[4],alpha=0.5)
                #annotate('RCP\nprojections',size=7, xy=(2080,150),ha='center',va='center',color=greys[6])

                range_with_capitals(plt,180,80,n_subplot=2)
                range_with_capitals(plt,150,101.5,n_subplot=2,year=2005,hd_source='CMIP5')
                
                plt.plot(rcp_h_time_lulucf,rcp_h_cum_lulucf,color=greys[4],ls='-',lw=1,marker="8",ms=4,label='RCP Data',alpha=getalfa("RCP"),zorder=01)

                if len(aHyr[cum_luc_em]) > 1:
                    # HACK:
                    for a_hist_luc_idx, a_hist_luc_val in enumerate(aEM[cum_luc_em][j]):
                        aEM[cum_luc_em][j][a_hist_luc_idx] = a_hist_luc_val*1E6
                        
                    plt.plot(aHyr[cum_luc_em],aEM[cum_luc_em][j],color=cop_color(nScen[j]),
                             lw=get_linewidth(nScen[j]),label=nScen[j],marker="x",zorder=getZ(nScen[j]))

            elif insta_scen(nScen[j],"3C") == True and "CCS" not in nScen[j]:
                plt.subplot(211)
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         alpha=getalfa(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))

                plt.subplot(212)
                plt.plot(aYear,aEM[cum_luc_em][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         alpha=getalfa(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
 
        plt.subplot(211) 
        #plt.fill_between(aYear,aEM[i][be_lo_00_idx],aEM[i][be_hi_00_idx],facecolor=cop_color("BioEnergy"),alpha=0.5)
 
        plt.grid(True)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color=greys[7],zorder=1,lw=1.2)
        plt.xlim(1950,2100) 
        plt.ylabel("Net LULUCF Emissions (Ann.) [PgC yr$^{-1}$]",size=yl_sz)
        insert_panel_label(plt,"a",2)
            
        leg = plt.legend(labelspacing=1,loc='upper right',ncol=2,borderpad=0.75,fontsize=9,fancybox=True,frameon=True)
        annotate("LULUCF emissions in CCS scenarios do not\ndiffer significantly from non-CCS scenarios.", xy=(0.07,0.06), 
                 xycoords=leg.get_frame(),size=7,va="center",ha="left")

        plt.subplot(212)
        #plt.fill_between(aYear,aEM[cum_luc_em][be_lo_00_idx],aEM[cum_luc_em][be_hi_00_idx],facecolor=cop_color("BioEnergy"),alpha=0.5)

        plt.grid(True)
        plt.xlim(1950,2100)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color=greys[7],zorder=1.2,lw=1.0,clip_on=False)
        plt.ylim(0,)
        plt.ylabel("Net LULUCF Emissions (Cum.) [PgC]",size=yl_sz)
        insert_panel_label(plt,"b",2)
        
    if EMtypes[i] == "Total C Emission from Fossil Fuels":

        for ii in range(nEM):
            if (EMtypes[ii] != "Cumulative Emissions from Fossil Fuels" and EMtypes[ii] != "Total C Emission from Fossil Fuels"): continue

            subplot_string = 0
            if EMtypes[ii] == "Total C Emission from Fossil Fuels": subplot_string = 211
            elif ii == cum_ff_em: subplot_string = 212
            plt.subplot(subplot_string)

            for j in range(len(nScen)):

                if "Historical" in nScen[j]:
                    if len(aHyr[ii]) > 1:
                        plt.plot(aHyr[ii],aEM[ii][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="CDIAC Data",marker="x",zorder=getZ(nScen[j]))
                    if EMtypes[ii] == "Total C Emission from Fossil Fuels": 
                        range_with_capitals(plt,9.5,0.8,n_subplot=2)
                        # Average Concrete (1980-1989): 1.334E8/yr
                        range_with_capitals(plt,5.3666,0.4,n_subplot=2,year=1984)
                        # Average Concrete (1990-1999): 1.882E8/yr
                        range_with_capitals(plt,6.2118,0.5,n_subplot=2,year=1994)
                        # Average Concrete (2000-2009): 3.146E8/yr
                        range_with_capitals(plt,7.4854,0.6,n_subplot=2,year=2004)
                        
                    if ii == cum_ff_em: range_with_capitals(plt,366,30,n_subplot=2)   

                elif insta_scen(nScen[j],"3C") == True:

                    if EMtypes[ii] == "Total C Emission from Fossil Fuels": 

                        emissions_with_ccs = np.array(aEM[ii][j])*(1-np.array(aEM[ccs_factor_idx][j]))
                        if do_scatter_2100: scatter([2100,],[emissions_with_ccs[-1],],dots,alpha=getalfa(nScen[j]),color=cop_color(nScen[j]),zorder=getZ(nScen[j]))

                        if "BAU" == nScen[j]:

                            plt.plot(rcp_time[1:],rcp_ff_26[1:],color=greys[6],ls='-',lw=1,marker="8",ms=4,label='RCP 2.6',alpha=getalfa("RCP"),zorder=01)
                            plt.plot(rcp_time[1:],rcp_ff_45[1:],color=greys[6],ls='-',lw=1,marker="s",ms=4,label='RCP 4.5',alpha=getalfa("RCP"),zorder=01)
                            plt.plot(rcp_time[1:],rcp_ff_60[1:],color=greys[6],ls='-',lw=1,marker=">",ms=4,label='RCP 6.0',alpha=getalfa("RCP"),zorder=01)
                            plt.plot(rcp_time[1:],rcp_ff_85[1:],color=greys[6],ls='-',lw=1,marker="d",ms=4,label='RCP 8.5',alpha=getalfa("RCP"),zorder=01)        

                            plt.plot(aYear,emissions_with_ccs,color=cop_color(nScen[j]),ls=cop_style(nScen[j]),
                                     alpha=getalfa(nScen[j]),lw=get_linewidth(nScen[j]),label=nScen[j],zorder=getZ(nScen[j]))

                            em_ccs_lo = np.array(aEM[ii][fbau_lo_00_idx])*(1-np.array(aEM[ccs_factor_idx][fbau_lo_00_idx]))                       
                            em_ccs_hi = np.array(aEM[ii][fbau_hi_00_idx])*(1-np.array(aEM[ccs_factor_idx][fbau_hi_00_idx])) 
                            plt.fill_between(aYear,em_ccs_lo,em_ccs_hi,edgecolor='none',facecolor=cop_color("FossilBAU"),alpha=0.45)

                            em_ccs_lo = np.array(aEM[ii][bau_lo_00_idx])*(1-np.array(aEM[ccs_factor_idx][bau_lo_00_idx]))                       
                            em_ccs_hi = np.array(aEM[ii][bau_hi_00_idx])*(1-np.array(aEM[ccs_factor_idx][bau_hi_00_idx])) 
                            plt.fill_between(aYear,em_ccs_lo,em_ccs_hi,edgecolor='none',facecolor=cop_color("BAU"),alpha=0.45)

                            em_ccs_lo = np.array(aEM[ii][be_lo_00_idx])*(1-np.array(aEM[ccs_factor_idx][be_lo_00_idx]))                       
                            em_ccs_hi = np.array(aEM[ii][be_hi_00_idx])*(1-np.array(aEM[ccs_factor_idx][be_hi_00_idx])) 
                            plt.fill_between(aYear,em_ccs_lo,em_ccs_hi,edgecolor='none',facecolor=cop_color("BioEnergy"),alpha=0.5)

                            em_ccs_lo = np.array(aEM[ii][be3_lo_00_idx])*(1-np.array(aEM[ccs_factor_idx][be3_lo_00_idx]))                       
                            em_ccs_hi = np.array(aEM[ii][be3_hi_00_idx])*(1-np.array(aEM[ccs_factor_idx][be3_hi_00_idx])) 
                            plt.fill_between(aYear,em_ccs_lo,em_ccs_hi,facecolor='none',hatch=hatch_str,edgecolor=cop_color("BioEnergy"),alpha=1.0)

                            plt.xlim(1950,2102)
                            plt.ylim(0,20)
                            #plt.xticks([2000,2050,2100],["","",""])
                            
                            plt.ylabel("Net Fossil Fuel\nEmissions (Ann.) [PgC yr$^{-1}$]",size=yl_sz)
                            insert_panel_label(plt,"a",2)

                            if label_HD == True: annotate('Historical Data Source: CDIAC',size=hd_sz, xy=(2125,-3.5),ha='right',va='center', annotation_clip=False)

                        else:
                            plt.plot(aYear,emissions_with_ccs,color=cop_color(nScen[j]),ls=cop_style(nScen[j]),
                                     alpha=getalfa(nScen[j]),lw=get_linewidth(nScen[j]),label=nScen[j],zorder=getZ(nScen[j]))

                    elif EMtypes[ii] == "Cumulative Emissions from Fossil Fuels":

                        if do_scatter_2100: scatter([2100,],[aEM[ii][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

                        if "BAU" == nScen[j]:
                            plt.plot(aYear,aEM[ii][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),alpha=getalfa(nScen[j]),label=nScen[j],zorder=getZ(nScen[j]))
                            do_ENE_range(aEM[ii],plt,ecs_str="3C")

                            plt.ylabel("Fossil Fuel\nEmissions (Cum.) [PgC]",size=yl_sz)
                            plt.xlim(1950,2102)
                            plt.ylim(0,1900)
                            plt.grid(True)

                        else:
                            plt.plot(aYear,aEM[ii][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                                     lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                            ax = plt.gca()
                            #leg = ax.legend(loc='best',ncol=2,size=6,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)
        
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.2)

        #ax = plt.gca()
        #leg = ax.legend(loc='best', ncol=2,framealpha=0.9)
    
    if (EMtypes[i] == "Total C Emission from Energy Sector"
        or EMtypes[i] == "Flux Atmosphere to Ocean"
        or EMtypes[i] == "Flux Atmosphere to Land Sink"
        or EMtypes[i] == "Net Emissions"
        or EMtypes[i] == "C Emission from Land Use Change"
        or i == ann_bem_idx
        or i == kaya_cie_idx):
        sns.despine(bottom=True)
    elif "Temperature Anomalies" in EMtypes[i]:
        sns.despine(trim=True)
    elif i != ann_esec_idx: sns.despine()

    plt.grid(True)

    ax = plt.gca()

    if EMtypes[i] == "Total C Emission from Energy Sector":#RCOP
        # Side panel legend:
        handles, labels = plt.gca().get_legend_handles_labels()
        hls,lbs = legend_fliparoo(handles, labels,2)
        leg = plt.legend(hls,lbs,bbox_to_anchor=(0.92,0.32,0.26,0.5),labelspacing=1,fontsize=9,
                         bbox_transform=plt.gcf().transFigure,mode="expand",loc=3,ncol=1,borderpad=0.75,fancybox=True,frameon=True)
        annotate("$\dagger$ ECS = "+ecs_str[0].replace("C","")+"$^{\circ}$C/2xCO$_2$", xy=(0.12,0.0), xycoords=leg.get_frame(),size=8,va="center",ha="left")

    elif EMtypes[i] == "C in Atmosphere":
        handles, labels = plt.gca().get_legend_handles_labels()
        hls,lbs = legend_fliparoo(handles, labels,2)
        leg = ax.legend(hls,lbs,loc='best',labelspacing=1,ncol=1,fontsize=9,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)
    #elif i == temp_anom_idx:
    #    leg = ax.legend(loc='upper left',ncol=2,fontsize=6,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)
    elif EMtypes[i] == "Net Emissions":
        handles, labels = plt.gca().get_legend_handles_labels()
        hls,lbs = legend_fliparoo(handles, labels,2)
        leg = ax.legend(hls,lbs,loc='upper left',labelspacing=0.4,ncol=1,fontsize=9,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)
    elif i == atm_ppm_idx:
        handles, labels = plt.gca().get_legend_handles_labels()
        hls,lbs = legend_fliparoo(handles, labels,2)
        leg = ax.legend(hls,lbs,loc='best',labelspacing=1,ncol=1,fontsize=10,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)

    #elif EMtypes[i] != "Total C Emission from Fossil Fuels":
    #    leg = ax.legend(loc='best',ncol=2,fontsize=6,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)

    plt.draw()
    plt.savefig('figures/biomass_'+EMtypes[i].replace("&","").replace("+","").replace("  ","_").replace(" ","_")+'.pdf',format='pdf', dpi=1200)
    plt.clf()
    plt.close('all')
