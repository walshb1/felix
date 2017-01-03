from pylab import *
import csv
import copy
import prettyplotlib as ppl
import matplotlib.patches as pts
from matplotlib import rc
from matplotlib import colors
from textwrap import wrap
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

import rcp_informations
reload(rcp_informations)
from rcp_informations import *

sns.set()
sns.set_context("paper")
sns.set_style("white")
#sns.set_style("darkgrid", {"grid.linewidth": .5, "axes.facecolor": ".9"})

#############################################
# Conversion Factors
mtoe_to_ej = .041868

# Formatting Controls
plot_errors = False
label_HD = False
dots = 15      # scatter/dot size
yl_sz = 10     # y-axis label size
lf_sz = 7      # label font size
hatch_str ='++++++++++\\\\\\\\\\\\\\\\\\\\\\\////////////'

def insert_panel_label(plt,panel_str,n_subp=2):
    y_val = 1.0
    trans = plt.gca().get_xaxis_transform() # x in data units, y in axes fraction
    annotate(panel_str, fontsize=21, xy=(1937,y_val),xycoords=trans,ha='right',va='center',weight='bold',annotation_clip=False)

def do_BE_range(theEM,plt,start_year=0):
    plt.fill_between(aYear[start_year:],theEM[be_lo_00_idx][start_year:],theEM[be_hi_00_idx][start_year:],facecolor=cop_color("BioEnergy"),edgecolor='none',alpha=0.5)
    plt.fill_between(aYear[start_year:],theEM[be_lo_25_idx][start_year:],theEM[be_hi_25_idx][start_year:],facecolor=cop_color("BioEnergy CCS25"),edgecolor='none',alpha=0.5)
    plt.fill_between(aYear[start_year:],theEM[be_lo_50_idx][start_year:],theEM[be_hi_50_idx][start_year:],facecolor=cop_color("BioEnergy CCS50"),edgecolor='none',alpha=0.5)
    plt.fill_between(aYear[start_year:],theEM[be_lo_75_idx][start_year:],theEM[be_hi_75_idx][start_year:],facecolor=cop_color("BioEnergy CCS75"),edgecolor='none',alpha=0.5)
    
    plt.fill_between(aYear[start_year:],theEM[be2_lo_00_idx][start_year:],theEM[be2_hi_00_idx][start_year:],hatch=hatch_str,facecolor='none',edgecolor=cop_color("BioEnergy"),alpha=1.0)
    plt.fill_between(aYear[start_year:],theEM[be2_lo_25_idx][start_year:],theEM[be2_hi_25_idx][start_year:],hatch=hatch_str,facecolor='none',edgecolor=cop_color("BioEnergy CCS25"),alpha=1.0)
    plt.fill_between(aYear[start_year:],theEM[be2_lo_50_idx][start_year:],theEM[be2_hi_50_idx][start_year:],hatch=hatch_str,facecolor='none',edgecolor=cop_color("BioEnergy CCS50"),alpha=1.0)
    plt.fill_between(aYear[start_year:],theEM[be2_lo_75_idx][start_year:],theEM[be2_hi_75_idx][start_year:],hatch=hatch_str,facecolor='none',edgecolor=cop_color("BioEnergy CCS75"),alpha=1.0)

def insta_scen(iScen,tcs_opt="2.5C"):
    if tcs_opt == "3C":
        if "3C" not in iScen: return False
    elif "3C" in iScen: return False

    if "BAU" in iScen and "CCS" in iScen: return False
    if "hi" in iScen: return False
    if "lo" in iScen: return False
    if "BioEnergy1" in iScen: return False
    if "Historical" in iScen: return False
    if "noUD" in iScen: return False
    #if "FossilBAU" in iScen and "en05" in iScen: return True
    if "FossilBAU" in iScen and "en" in iScen: return False
    if "char" in iScen or "Char" in iScen: return False
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
    elif "RCP" in iScen: return 0.8 
    else: return 0.6

def cop_scen_rep(iScen):
    return iScen.replace(" ","+").replace("BioEnergy2","RE-High").replace("BioEnergy1","RE-Med").replace("BioEnergy","RE-Low").replace("+3C","")

def cop_style(iScen):
    if "BioEnergy1" in iScen: return ':'
    if "BioEnergy2" in iScen: return '-.'
    else: return '-'

def range_with_capitols(pltA,central_val=0,error=0,n_subplot=1,year=2011):
    ylo = central_val-error
    yhi = central_val+error

    scatter([year+0.25,],[central_val,],dots,color='black',zorder=99.9)

    if n_subplot == 1:
        cap_height = pltA.gca().get_ylim()[1]/300
    else: cap_height = pltA.gca().get_ylim()[1]/100

    pltA.gca().add_patch(Rectangle((year,ylo+cap_height/2),0.5,(yhi-ylo-cap_height), color='black',zorder=99.9))

    pltA.gca().add_patch(Rectangle((year-1,ylo),2.5,(cap_height), color='black',zorder=99.9))
    pltA.gca().add_patch(Rectangle((year-1,yhi-cap_height),2.5,(cap_height), color='black',zorder=99.9))    

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
                if row[i] == "FossilBAU": FBAUidx = len(nScen)-1
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
                        or "Captured" in EMtypes[len(EMtypes)-1]
                        or "C Emission from Land Use Change" in EMtypes[len(EMtypes)-1]
                        or "C in Atmosphere" in EMtypes[len(EMtypes)-1]
                        or "Cumulative Uptake by Oceans" in EMtypes[len(EMtypes)-1]
                        or "Flux" in EMtypes[len(EMtypes)-1]
                        or "Land Sink" in EMtypes[len(EMtypes)-1]
                        or "Net C Emission from Energy Sector" in EMtypes[len(EMtypes)-1]
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
    elif EMtypes[i] == "C Captured & Stored": cseq_em = i
    elif EMtypes[i] == "Cumulative Uptake by Oceans": cum_ocn_em = i
    elif EMtypes[i] == "Cumulative Atmosphere to Land Sink": cum_lsk_em = i
    elif EMtypes[i] == "Leeching to Atmosphere": leech_em = i
    elif EMtypes[i] == "CCS Improvement Factor": ccs_factor_idx = i
    elif EMtypes[i] == "Total C Emission from Fossil Fuels": ann_ffem_idx = i
    elif EMtypes[i] == "Total C Emission from Renewables": ann_bem_idx = i
    ##elif EMtypes[i] == "Net Bioenergy Emissions": ann_bem_idx = i
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
    if nScen[j] == "BioEnergy lo": be_lo_00_idx = j
    if nScen[j] == "BioEnergy hi": be_hi_00_idx = j
    if nScen[j] == "BioEnergy lo CCS25": be_lo_25_idx = j
    if nScen[j] == "BioEnergy hi CCS25": be_hi_25_idx = j
    if nScen[j] == "BioEnergy lo CCS50": be_lo_50_idx = j
    if nScen[j] == "BioEnergy hi CCS50": be_hi_50_idx = j
    if nScen[j] == "BioEnergy lo CCS75": be_lo_75_idx = j
    if nScen[j] == "BioEnergy hi CCS75": be_hi_75_idx = j
    if nScen[j] == "BioEnergy1 lo": be1_lo_00_idx = j
    if nScen[j] == "BioEnergy1 hi": be1_hi_00_idx = j
    if nScen[j] == "BioEnergy1 lo CCS25": be1_lo_25_idx = j
    if nScen[j] == "BioEnergy1 hi CCS25": be1_hi_25_idx = j
    if nScen[j] == "BioEnergy1 lo CCS50": be1_lo_50_idx = j
    if nScen[j] == "BioEnergy1 hi CCS50": be1_hi_50_idx = j
    if nScen[j] == "BioEnergy1 lo CCS75": be1_lo_75_idx = j
    if nScen[j] == "BioEnergy1 hi CCS75": be1_hi_75_idx = j
    if nScen[j] == "BioEnergy2 lo": be2_lo_00_idx = j
    if nScen[j] == "BioEnergy2 hi": be2_hi_00_idx = j
    if nScen[j] == "BioEnergy2 lo CCS25": be2_lo_25_idx = j
    if nScen[j] == "BioEnergy2 hi CCS25": be2_hi_25_idx = j
    if nScen[j] == "BioEnergy2 lo CCS50": be2_lo_50_idx = j
    if nScen[j] == "BioEnergy2 hi CCS50": be2_hi_50_idx = j
    if nScen[j] == "BioEnergy2 lo CCS75": be2_lo_75_idx = j
    if nScen[j] == "BioEnergy2 hi CCS75": be2_hi_75_idx = j

for i in range(nEM):

    allYval = []
    tempY = 0
    plt.clf()    

    if (i != ann_bem_idx and i != atm_ppm_idx
        and EMtypes[i] != "Flux Atmosphere to Land Sink"
        and EMtypes[i] != "Total C Emission from Fossil Fuels"
        and EMtypes[i] != "C Emission from Land Use Change"
        and EMtypes[i] != "Flux Atmosphere to Ocean"
        and EMtypes[i] != "C in Atmosphere"
        and EMtypes[i] != "Net C Emission from Energy Sector"
        and EMtypes[i] != "Net Emissions"
        and EMtypes[i] != "Total Radiative Forcing"
        and EMtypes[i] != "Cumulative Emissions"
        and "Temperature Anomalies" not in EMtypes[i]
        and i != kaya_pop_idx and i != kaya_gdp_idx and i != kaya_eig_idx and i != kaya_cie_idx 
        and i != cum_lsk_em and i != cum_ocn_em): 
        print "*** SKIP:",EMtypes[i]
        continue
    print EMtypes[i]
        
    if (EMtypes[i] != "Total Radiative Forcing" 
        and EMtypes[i] != "Net Emissions"
        and EMtypes[i] != "Cumulative Emissions"
        and "Temperature Anomalies" not in EMtypes[i]):
        fig = plt.figure(figsize=(6.4,5.0))

    if i == cum_lsk_em or i == cum_ocn_em:
        plt.xlim(300,750)
        plt.ylim(0,550)      

        plt.xlabel("Atmospheric Carbon Concentration [ppm]")
        if i == cum_lsk_em:
            plt.ylabel("Cumulative Land Sink Uptake [PgC]")
        elif i == cum_ocn_em:
            plt.ylabel("Cumulative Ocean Uptake [PgC]")

        for j in range(len(nScen)):
            if "Historical" in nScen[j]: continue
                    
            elif insta_scen(nScen[j]) == True:
                plt.plot(aEM[atm_ppm_idx][j],aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
            
                if nScen[j] == "BAU":
                    plt.scatter(aEM[atm_ppm_idx][j][yr2000idx],aEM[i][j][yr2000idx],15,marker="x",linewidth=2,color=greys[6],zorder=100)
                    annotate("Year 2000",xy=(aEM[atm_ppm_idx][j][yr2000idx],aEM[i][j][yr2000idx]),xycoords='data',
                             xytext=(aEM[atm_ppm_idx][j][yr2000idx]+10,aEM[i][j][yr2000idx]-20), textcoords='data',
                             color=greys[6],va='center',ha='left',fontsize=7,arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=0.5"))
                    annotate("2050",xy=(aEM[atm_ppm_idx][FBAUidx][yr2050idx],aEM[i][FBAUidx][yr2050idx]),xycoords='data',
                             xytext=(aEM[atm_ppm_idx][FBAUidx][yr2050idx]+10,aEM[i][FBAUidx][yr2050idx]-20), textcoords='data',
                             color=greys[6],va='center',ha='left',fontsize=7,arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=0.5"))
                    annotate("2100",xy=(aEM[atm_ppm_idx][FBAUidx][-1],aEM[i][FBAUidx][-1]),xycoords='data',
                             xytext=(aEM[atm_ppm_idx][FBAUidx][-1]+05,aEM[i][FBAUidx][-1]-25), textcoords='data',
                             color=greys[6],va='center',ha='left',fontsize=7,arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=0.5"))

                plt.scatter(aEM[atm_ppm_idx][j][yr2050idx],aEM[i][j][yr2050idx],10,marker="s",color=cop_color(nScen[j]),zorder=getZ(nScen[j]))
                plt.scatter(aEM[atm_ppm_idx][j][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))

    if EMtypes[i] == "Cumulative Emissions":

        # First, make a CumEm bar plot to keep it interesting
        plt.ylim(0,1600)
        plt.ylabel("Cumulative Anthropogenic Emissions [PgC]")
        
        x_ax_labels = [[],[]]
        x_ax_val = 0.3

        plt.bar([x_ax_val],[rcp_cum_em_hist],width=0.8,label=cop_scen_rep("Historical"),facecolor=cop_color(nScen[j]),edgecolor='none',alpha=0.66)
        plt.plot([x_ax_val+0.4-0.5,x_ax_val+0.4+0.5],[felix_cum_em_1900to2000,felix_cum_em_1900to2000],'k-',lw=1.5,color='black',zorder=100)
        plt.plot([x_ax_val+0.4,x_ax_val+0.4],[felix_cum_em_1900to2000-50,felix_cum_em_1900to2000],'k-',lw=1.5,color='black',zorder=100)
        annotate("FeliX",xy=(x_ax_val+0.4,felix_cum_em_1900to2000-75), xycoords='data',ha='center',va='top',fontsize=8,rotation=90,weight='bold')

        x_ax_labels[0].append(x_ax_val+0.4)
        x_ax_labels[1].append(cop_scen_rep("Historical\n(1901-2000)"))
        plt.plot([1.4,1.4],plt.gca().get_ylim(),'k-',lw=1.5,color='black',zorder=1)
        x_ax_val+=1.4

        for j in range(len(nScen)):
            if nScen[j] == "HistoricalData": continue
            
            if insta_scen(nScen[j]) == True:
                if "BioEnergy2" in nScen[j]:
                    plt.bar([x_ax_val],[(aEM[i][j][-1]-aEM[i][j][yr2000idx])],width=0.8,label=cop_scen_rep(nScen[j]),hatch=hatch_str,facecolor='none',edgecolor=cop_color(nScen[j]),alpha=1.0)
                    x_ax_labels[0].append(x_ax_val+0.4)
                    x_ax_labels[1].append(cop_scen_rep(nScen[j]))
                    x_ax_val+=1
                elif "BioEnergy" in nScen[j]:
                    plt.bar([x_ax_val],[(aEM[i][j][-1]-aEM[i][j][yr2000idx])],width=0.8,label=cop_scen_rep(nScen[j]),facecolor=cop_color(nScen[j]),edgecolor='none',alpha=0.66)
                    x_ax_labels[0].append(x_ax_val+0.4)
                    x_ax_labels[1].append(cop_scen_rep(nScen[j]))
                    x_ax_val+=1
                else:
                    plt.bar([x_ax_val],[(aEM[i][j][-1]-aEM[i][j][yr2000idx])],width=0.8,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),label=cop_scen_rep(nScen[j]))
                    x_ax_labels[0].append(x_ax_val+0.4)
                    x_ax_labels[1].append(cop_scen_rep(nScen[j]))
                    x_ax_val+=1

        plt.plot([1.4,plt.gca().get_xlim()[1]],[cum_em_sub_2C,cum_em_sub_2C],'k-',lw=0.75,color=greys[4],zorder=1)
        annotate("Limit for $\Delta$T<2$^{\circ}$C",xy=(plt.gca().get_xlim()[1]-0.15,rcp_cum_em_26+10),va='bottom',ha='right',color=greys[4],fontsize=7)

        plt.plot([1.4,plt.gca().get_xlim()[1]],[rcp_cum_em_26,rcp_cum_em_26],'k-',lw=0.75,color=greys[6],zorder=1)#marker="s",ms=4)
        annotate("RCP 2.6",xy=(plt.gca().get_xlim()[1]-0.15,rcp_cum_em_26-10),color=greys[6],va='top',ha='right',fontsize=7)

        plt.plot([1.4,plt.gca().get_xlim()[1]],[rcp_cum_em_45,rcp_cum_em_45],'k-',lw=0.75,color=greys[6],zorder=1)#marker=">",ms=4)
        annotate("RCP 4.5",xy=(plt.gca().get_xlim()[1]-0.15,rcp_cum_em_45-10),color=greys[6],va='top',ha='right',fontsize=7)

        plt.plot([1.4,plt.gca().get_xlim()[1]],[rcp_cum_em_60,rcp_cum_em_60],'k-',lw=0.75,color=greys[6],zorder=1)#marker="d",ms=4)
        annotate("RCP 6.0",xy=(plt.gca().get_xlim()[1]-0.15,rcp_cum_em_60-10),color=greys[6],va='top',ha='right',fontsize=7)
        
        plt.gca().set_xticks(x_ax_labels[0])
        plt.gca().set_xticklabels(x_ax_labels[1],rotation=30,ha='right')

        plt.draw()
        plt.savefig('figures/biomass_Cumulative_Emissions_barplot.pdf',format='pdf', dpi=1200)
        plt.clf()
        plt.close('all')

        plt.ylim(0,2000)
        plt.ylabel("Cumulative Anthropogenic Emissions [PgC]")

        for j in range(len(nScen)):
            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1:
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="HadCRUT4 Data",marker="x",zorder=getZ(nScen[j]))
                    plt.scatter(aHyr[i][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))
                    
            elif insta_scen(nScen[j]) == True:
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                annotate(int(round(aEM[i][j][-1],0)),xy=(2102,aEM[i][j][-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',fontsize=8,weight='bold')

    if i == kaya_pop_idx or i == kaya_gdp_idx or i == kaya_cie_idx or i == kaya_eig_idx:
        # Kaya Factors: Compare these plots to Fig. 6.1 in ipcc_wg3_ar5_chapter6.pdf (pg 425)
        plt.xlim(1980,2102)
        plt.plot(plt.gca().get_xlim(),[1,1],'k-',ls=':',color=greys[5],zorder=1,lw=1.5)
        
        if i == kaya_pop_idx:
            plt.ylim(0,2)
            plt.ylabel("Population (Index: 2010=1)")

            # Plot WPP population projection variants
            BAU_index_value = aEM[kaya_pop_idx][BAUidx][yr2010idx]
            for anIndex, aValue in enumerate(aEM[pop_lovar_idx][HDidx]):
                aEM[pop_lovar_idx][HDidx][anIndex] = float(aValue)*1E9/BAU_index_value
            for anIndex, aValue in enumerate(aEM[pop_mdvar_idx][HDidx]):
                aEM[pop_mdvar_idx][HDidx][anIndex] = float(aValue)*1E9/BAU_index_value
            for anIndex, aValue in enumerate(aEM[pop_hivar_idx][HDidx]):
                aEM[pop_hivar_idx][HDidx][anIndex] = float(aValue)*1E9/BAU_index_value
                      
            plt.plot(aHyr[pop_lovar_idx],aEM[pop_lovar_idx][HDidx],color=greys[7],lw=1.5,ls="--",label="WPP Low Var",zorder=1.0)          
            plt.plot(aHyr[pop_mdvar_idx],aEM[pop_mdvar_idx][HDidx],color=greys[7],lw=1.5,ls="--",label="WPP Med Var",zorder=1.0)     
            plt.plot(aHyr[pop_hivar_idx],aEM[pop_hivar_idx][HDidx],color=greys[7],lw=1.5,ls="--",label="WPP High Var",zorder=1.0)     

        elif i == kaya_gdp_idx:
            plt.ylim(0,5)
            plt.ylabel("GPD per Capita (Index: 2010=1)")

            hist_change_year = [1980+iPower for iPower in xrange(2100-1979)]
            hist_change_rate = [math.pow((1+0.014),iPower-30) for iPower in xrange(2100-1979)]
            plt.plot(hist_change_year,hist_change_rate,color=greys[7],lw=1.5,ls="--",label="Historical Rate of Decline",zorder=1.0)


        elif i == kaya_cie_idx:
            plt.ylim(-0.25,1.25)
            plt.ylabel("Carbon Intensity of Energy (Index: 2010=1)")
            plt.plot(plt.gca().get_xlim(),[0,0],'k-',color=greys[4],zorder=1,lw=1.0)
            plt.fill_between(plt.gca().get_xlim(),[0,0],[-1,-1], facecolor=greys[4], alpha=0.15)
            annotate("Carbon Net-Negative Energy Sector",xy=(plt.gca().get_xlim()[0]+2,-0.02),ha='left',va='top',fontsize=7)

        elif i == kaya_eig_idx:
            plt.ylim(0.0,2.)
            plt.ylabel("Energy Intensity of GDP (Index: 2010=1)")         

            hist_change_year = [1980+iPower for iPower in xrange(2100-1979)]
            hist_change_rate = [math.pow((1-0.008),iPower-30) for iPower in xrange(2100-1979)]
            plt.plot(hist_change_year,hist_change_rate,color=greys[7],lw=1.5,ls="--",label="Historical Rate of Decline",zorder=1.0)

            #hist_change_year = [1980+iPower for iPower in xrange(2100-1979)]
            #hist_change_rate = [aEM[i][HDidx][-1]/aEM[i][BAUidx][yr2010idx]*math.pow((1-0.008),iPower-26) for iPower in xrange(2100-1979)]
            #plt.plot(hist_change_year,hist_change_rate,color=greys[7],lw=1.5,ls="--",label="Historical Rate of Decline",zorder=1.0)
            
        BAU_index_value = aEM[i][BAUidx][yr2010idx]

        for j in range(len(nScen)):

            for anIndex, aValue in enumerate(aEM[i][j]):
                aEM[i][j][anIndex] = float(aValue)/BAU_index_value

            if "Historical" in nScen[j] and len(aHyr[i]) > 1:
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="Historical Data",marker="x",zorder=getZ(nScen[j]))
                    plt.scatter(aHyr[i][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))

            elif insta_scen(nScen[j]) == True:
                    plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                             label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                    scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                    #annotate(int(round(aEM[i][j][-1],0)),xy=(2102,aEM[i][j][-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',fontsize=8,weight='bold')
        
        do_BE_range(aEM[i],plt)

    if i == rad_for_idx:
        plt.xlim(1950,2102)
        plt.ylim(0,6)
        plt.ylabel("Total Radiative Forcing [W m$^{-2}$]")
        sns.despine()       

        for j in range(len(nScen)):
            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1:
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="HadCRUT4 Data",marker="x",zorder=getZ(nScen[j]))
                    plt.scatter(aHyr[i][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))

            elif insta_scen(nScen[j]) == True:
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                annotate(round(aEM[i][j][-1],2),xy=(2102,aEM[i][j][-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',fontsize=8,weight='bold')
        
        plt.plot(rcp_time[1:],rcp_for_tot_26[1:],color=greys[6],ls='-',lw=1,marker="8",ms=4,label='RCP 2.6',alpha=getalfa("RCP"),zorder=01)
        plt.plot(rcp_time[1:],rcp_for_tot_45[1:],color=greys[6],ls='-',lw=1,marker="s",ms=4,label='RCP 4.5',alpha=getalfa("RCP"),zorder=01)
        plt.plot(rcp_time[1:],rcp_for_tot_60[1:],color=greys[6],ls='-',lw=1,marker=">",ms=4,label='RCP 6.0',alpha=getalfa("RCP"),zorder=01)
        plt.plot(rcp_time[1:],rcp_for_tot_85[1:],color=greys[6],ls='-',lw=1,marker="d",ms=4,label='RCP 8.5',alpha=getalfa("RCP"),zorder=01)

        do_BE_range(aEM[i],plt)

    if i == atm_ppm_idx:
        plt.xlim(1950,2102)
        plt.ylim(300,750)
        plt.ylabel("Atmospheric CO$_2$ Concentration [ppm]")
        sns.despine()

        for j in range(len(nScen)):
            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1:
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="HadCRUT4 Data",marker="x",zorder=getZ(nScen[j]))
                    plt.scatter(aHyr[i][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))

            elif insta_scen(nScen[j]) == True:
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                annotate(int(round(aEM[i][j][-1],0)),xy=(2102,aEM[i][j][-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',fontsize=8,weight='bold')
        
        plt.plot(rcp_time[2:],rcp_ppm_26[2:],color=greys[6],ls='-',lw=1,marker="8",ms=4,label='RCP 2.6',alpha=getalfa("RCP"),zorder=01)
        plt.plot(rcp_time[2:],rcp_ppm_45[2:],color=greys[6],ls='-',lw=1,marker="s",ms=4,label='RCP 4.5',alpha=getalfa("RCP"),zorder=01)
        plt.plot(rcp_time[2:],rcp_ppm_60[2:],color=greys[6],ls='-',lw=1,marker=">",ms=4,label='RCP 6.0',alpha=getalfa("RCP"),zorder=01)
        plt.plot(rcp_time[2:],rcp_ppm_85[2:],color=greys[6],ls='-',lw=1,marker="d",ms=4,label='RCP 8.5',alpha=getalfa("RCP"),zorder=01)

        do_BE_range(aEM[i],plt)

        insert_panel_label(plt,"B",1)

    if "Net Emissions" in EMtypes[i]:
        for j in range(len(nScen)):
            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1: 
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="HadCRUT4 Data",marker="x",zorder=getZ(nScen[j]))
                    plt.scatter(aHyr[i][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))

            elif insta_scen(nScen[j]) == True:
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                annotate(round(aEM[i][j][-1],1),xy=(2102,aEM[i][j][-1]), xycoords='data',xytext=(2,-3), textcoords='offset points',fontsize=8,weight='bold')

        plt.plot(rcp_hist_time, rcp_hist_em,color=get_color('HistoricalData'),linewidth=get_linewidth("HistoricalData"),label='RCP Data',marker="x",zorder=100)
        plt.scatter(rcp_hist_time[-1],rcp_hist_em[-1],10,color=cop_color("HistoricalData"),zorder=getZ("HistoricalData"))
                    
        plt.plot(rcp_time[1:],rcp_em_26[1:],color=greys[6],ls='-',lw=1,marker="8",ms=4,label='RCP 2.6',alpha=getalfa("RCP"),zorder=01)
        plt.plot(rcp_time[1:],rcp_em_45[1:],color=greys[6],ls='-',lw=1,marker="s",ms=4,label='RCP 4.5',alpha=getalfa("RCP"),zorder=01)
        plt.plot(rcp_time[1:],rcp_em_60[1:],color=greys[6],ls='-',lw=1,marker=">",ms=4,label='RCP 6.0',alpha=getalfa("RCP"),zorder=01)
        plt.plot(rcp_time[1:],rcp_em_85[1:],color=greys[6],ls='-',lw=1,marker="d",ms=4,label='RCP 8.5',alpha=getalfa("RCP"),zorder=01)
        #scatter([2100,],[rcp_em_26[-1],],dots, color=get_color("2.6"),zorder=0)
        #scatter([2100,],[rcp_em_45[-1],],dots, color=get_color("4.5"),zorder=0)
        #scatter([2100,],[rcp_em_60[-1],],dots, color=get_color("6.0"),zorder=0)
        #scatter([2100,],[rcp_em_85[-1],],dots, color=get_color("8.5"),zorder=0)

        do_BE_range(aEM[i],plt)

        plt.xlim(1950,2102)
        plt.plot([1950,2100],[0,0],'k-',color='black',zorder=1,lw=1.0)
        plt.ylim(-5,20)
        plt.ylabel("Net Anthropogenic Emissions [PgC yr$^{-1}$]")

    if "Temperature Anomalies" in EMtypes[i]:
        plt.xlim(1950,2135)
        plt.ylim(0,3.0)
        plt.ylabel("Temperature Anomaly [$^{\circ}$C]")

        plt.fill_between([2080,2100],[0,0],[3,3], facecolor=greys[4], alpha=0.15)

        for j in range(len(nScen)):
            
            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1: 

                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="HadCRUT4 Data",marker="x",zorder=getZ(nScen[j]))
                    plt.scatter(aHyr[i][-1],aEM[i][j][-1],10,color=cop_color(nScen[j]),zorder=getZ(nScen[j]))

                # RCP Projections
                #plt.plot(plt.gca().get_xlim(),[0,0],'k-',color='black',zorder=1,lw=1.0)
                rcp_temp_26 = [ 0.9, 1.6, 2.3 ]
                rcp_temp_45 = [ 1.7, 2.4, 3.2 ]
                rcp_temp_60 = [ 2.0, 2.8, 3.7 ]
                rcp_temp_85 = [ 3.2, 4.3, 5.4 ] 

                scatter([2120,],[rcp_temp_26[1],],dots,marker="8",color=get_color("2.6"))
                scatter([2124,],[rcp_temp_45[1],],dots,marker="s",color=get_color("4.5"))
                scatter([2128,],[rcp_temp_60[1],],dots,marker=">",color=get_color("6.0"))
                scatter([2132,],[rcp_temp_85[1],],dots,marker="d",color=get_color("8.5"))
            
                annotate('RCP 2.6',xy=(2121, rcp_temp_26[1]), xycoords='data',xytext=(2,-3), textcoords='offset points',fontsize=8,weight='bold')
                annotate('RCP 4.5',xy=(2125, rcp_temp_45[1]), xycoords='data',xytext=(2,-3), textcoords='offset points',fontsize=8,weight='bold')
                annotate('RCP 6.0',xy=(2129, rcp_temp_60[1]), xycoords='data',xytext=(2,-3), textcoords='offset points',fontsize=8,weight='bold')
                
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

            elif insta_scen(nScen[j]) == True:
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
                
                if nScen[j] != "BioEnergy CCS25":
                    annotate(str(round(avgTempAnom,1))+"$^{\circ}$C",xy=(2110,aEM[i][j][-1]),xycoords='data',ha='center',va='center',fontsize=7,weight='bold')

        do_BE_range(aEM[i],plt)

        annotate("$\Delta$T [2081-2100]",xy=(2117.5,0.55),xycoords='data',ha='center',va='center',fontsize=7) 
        plt.plot([2103,2132],[0.64,0.64],'k-',color='black',lw=1.5)
        plt.plot([2103,2103],[0.64,0.67],'k-',color='black',lw=1.5)
        plt.plot([2132,2132],[0.64,0.67],'k-',color='black',lw=1.5)

    if EMtypes[i] == "Net C Emission from Energy Sector":

        # Transient Climate Sensitivity switch
        tcs_str = ["2.5C",0]

        #while tcs_str[1] < 2:
        plt.ylim(-0.5,2)
        
        xTM = 2116
        xTMpmA = 1
        xTMpm = 1.5
        xTMtxt =  xTMpmA+5.5
        
        for j in range(len(nScen)):
            
            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1: 
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label=nScen[j],marker="x",zorder=getZ(nScen[j]))
            else:
                
                master_numerator = np.array(aEM[i][j])
                master_denominator = np.array(aEM[i][j])
                master_denominator -= np.array(aEM[i][j])
                
                for ij in range(nEM):
                    if EMtypes[ij] == "Afforestation":
                        master_numerator -= np.array(aEM[ij][j])
                    if EMtypes[ij] == "C Emission from Land Use Change":
                        master_numerator += np.array(aEM[ij][j])
                    if EMtypes[ij] == "Leeching to Atmosphere":
                        master_numerator += np.array(aEM[ij][j])
                    if EMtypes[ij] == "Flux Atmosphere to Ocean":
                        master_denominator += np.array(aEM[ij][j])
                    if EMtypes[ij] == "Flux Atmosphere to Land Sink":
                        master_denominator += np.array(aEM[ij][j])

                    if "Temperature Anomalies" in EMtypes[ij]:
                        #temperature_string = "$\Delta$T = "+str(round(aEM[ij][j][-1],1))+"$^{\circ}$C"
                        temperature_string = str(round(aEM[ij][j][-1],1))
                        
                master_quotient = master_numerator/master_denominator
                
                if tcs_str[0] == "3C" and "3C" not in nScen[j]: continue
                elif tcs_str[0] != "3C" and "3C" in nScen[j]: continue
                temp_label_str = nScen[j].replace("3C","")
                
                # Not using char scenarios at all right now
                if "char" in nScen[j]: continue

                if insta_scen(nScen[j],tcs_str[0]) == True:
                    if "BAU" in nScen[j]:
                        plt.plot(aYear,master_quotient,color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                                 label=temp_label_str,alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                        plt.plot([xTM-xTMpm,xTM+xTMpm],[master_quotient[-1],master_quotient[-1]], 'k-', color=cop_color(nScen[j]),lw=3.0)
                        annotate(temperature_string,xy=(xTM-xTMtxt,master_quotient[-1]),fontsize=lf_sz, va='center',ha='center',weight='bold')

                    else:
                        #HACK - here and below: denominator goes negative (sinks begin outgassing) so ratio flips to positive...
                        if "CCS75" in nScen[j]:
                            print "--> running the fix on RCOP plots to fix scenarios that flip positive"
                            holdRatio = master_quotient[0]
                            for iRatio in range(len(master_quotient)):
                                if holdRatio < 0 and master_quotient[iRatio] > 0:
                                    master_quotient[iRatio]*=-1
                                holdRatio = master_quotient[iRatio]
                        
                        plt.plot(aYear,master_quotient,color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                                 label=cop_scen_rep(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                        #print " ",nScen[j], master_quotient[-1]
                    scatter([2100,],[master_quotient[-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

                elif "BioEnergy lo CCS25" in nScen[j]: 
                    ccs25_lo_bound = master_quotient
                    xtmp = xTM + 2*xTMpmA
                    annotate(temperature_string,xy=(xtmp+xTMtxt,master_quotient[-1]), fontsize=lf_sz, va='center',ha='center',weight='bold')
                elif "BioEnergy hi CCS25" in nScen[j]: 
                    ccs25_hi_bound = master_quotient
                    
                elif "BioEnergy lo CCS50" in nScen[j]: 
                    ccs50_lo_bound = master_quotient
                    xtmp = xTM - 2*xTMpmA
                    annotate(temperature_string,xy=(xtmp-xTMtxt,master_quotient[-1]), fontsize=lf_sz, va='center',ha='center',weight='bold')
                elif "BioEnergy hi CCS50" in nScen[j]: 
                    ccs50_hi_bound = master_quotient
                    
                elif "BioEnergy lo CCS75" in nScen[j]: 
                    ccs75_lo_bound = master_quotient
                    xtmp = xTM + 2*xTMpmA
                    #annotate(temperature_string,xy=(xtmp+xTMtxt,master_quotient[-1]), fontsize=lf_sz, va='center',ha='center',weight='bold')
                elif "BioEnergy hi CCS75" in nScen[j]: 
                    ccs75_hi_bound = master_quotient

                    # Hack
                    holdRatio = ccs75_hi_bound[0]
                    for iRatio in range(len(ccs75_hi_bound)):
                        if holdRatio < 0 and ccs75_hi_bound[iRatio] > 0:
                            ccs75_hi_bound[iRatio]*=-1
                        holdRatio = ccs75_hi_bound[iRatio]

                elif "BioEnergy lo" in nScen[j]:
                    ccs00_lo_bound = master_quotient
                    xtmp = xTM - 2*xTMpmA
                    print "-->",nScen[j],temperature_string
                    annotate(temperature_string,xy=(xtmp-xTMtxt,master_quotient[-1]), fontsize=lf_sz, va='center',ha='center',weight='bold')
                elif "BioEnergy hi" in nScen[j]: 
                    ccs00_hi_bound = master_quotient

                elif "BioEnergy lo char" in nScen[j]: char_lo_bound = master_quotient
                elif "BioEnergy hi char" in nScen[j]: char_hi_bound = master_quotient

                elif "BioEnergy2 lo CCS25" in nScen[j]: be2ccs25_lo_bound = master_quotient
                elif "BioEnergy2 hi CCS25" in nScen[j]: 
                    be2ccs25_hi_bound = master_quotient
                    xtmp = xTM + 2*xTMpmA
                    annotate(temperature_string,xy=(xtmp+xTMtxt,master_quotient[-1]), fontsize=lf_sz, va='center',ha='center',weight='bold')
                    plt.plot([xtmp,xtmp],[ccs25_lo_bound[-1],be2ccs25_hi_bound[-1]], 'k-', color=cop_color("BioEnergy CCS25"),lw=3.0)
                    plt.plot([xtmp-xTMpm,xtmp+xTMpm],[be2ccs25_hi_bound[-1],be2ccs25_hi_bound[-1]], 'k-', color=cop_color("BioEnergy CCS25"),lw=3.0)
                    plt.plot([xtmp-xTMpm,xtmp+xTMpm],[ccs25_lo_bound[-1],ccs25_lo_bound[-1]], 'k-', color=cop_color("BioEnergy CCS25"),lw=3.0)

                elif "BioEnergy2 lo CCS50" in nScen[j]: be2ccs50_lo_bound = master_quotient
                elif "BioEnergy2 hi CCS50" in nScen[j]: 
                    be2ccs50_hi_bound = master_quotient
                    # Hack
                    holdRatio = be2ccs50_hi_bound[0]
                    for iRatio in range(len(be2ccs50_hi_bound)):
                        if holdRatio < 0 and be2ccs50_hi_bound[iRatio] > 0:
                            be2ccs50_hi_bound[iRatio]*=-1
                        holdRatio = be2ccs50_hi_bound[iRatio]
                            
                    xtmp = xTM - 2*xTMpmA
                    #annotate(temperature_string,xy=(xtmp-xTMtxt,master_quotient[-1]), fontsize=lf_sz, va='center',ha='center',weight='bold')
                    plt.plot([xtmp,xtmp],[ccs50_lo_bound[-1],plt.gca().get_ylim()[0]+0.02], 'k-', color=cop_color("BioEnergy CCS50"),lw=3.0,clip_on=True)
                    plt.plot([xtmp-xTMpm,xtmp+xTMpm],[be2ccs50_hi_bound[-1],be2ccs50_hi_bound[-1]], 'k-', color=cop_color("BioEnergy CCS50"),lw=3.0)
                    plt.plot([xtmp-xTMpm,xtmp+xTMpm],[ccs50_lo_bound[-1],ccs50_lo_bound[-1]], 'k-', color=cop_color("BioEnergy CCS50"),lw=3.0)
                    
                    plt.plot([xtmp-xTMpm,xtmp+xTMpm],[plt.gca().get_ylim()[0]+0.05,plt.gca().get_ylim()[0]+0.05], 'k-', color=cop_color("BioEnergy CCS50"),lw=3.0)
                    plt.plot([xtmp,xtmp-xTMpm],[plt.gca().get_ylim()[0]+0.02,plt.gca().get_ylim()[0]+0.05], 'k-', color=cop_color("BioEnergy CCS50"),lw=3.0)
                    plt.plot([xtmp,xtmp+xTMpm],[plt.gca().get_ylim()[0]+0.02,plt.gca().get_ylim()[0]+0.05], 'k-', color=cop_color("BioEnergy CCS50"),lw=3.0)

                elif "BioEnergy2 lo CCS75" in nScen[j]: 
                    be2ccs75_lo_bound = master_quotient
                    
                    holdRatio = be2ccs75_lo_bound[0]
                    for iRatio in range(len(be2ccs75_lo_bound)):
                        if holdRatio < 0 and be2ccs75_lo_bound[iRatio] > 0:
                            be2ccs75_lo_bound[iRatio]*=-1
                        holdRatio = be2ccs75_lo_bound[iRatio]

                elif "BioEnergy2 hi CCS75" in nScen[j]: 
                    be2ccs75_hi_bound = master_quotient

                    holdRatio = be2ccs75_hi_bound[0]
                    for iRatio in range(len(be2ccs75_hi_bound)):
                        if holdRatio < 0 and be2ccs75_hi_bound[iRatio] > 0:
                            be2ccs75_hi_bound[iRatio]*=-1
                        holdRatio = be2ccs75_hi_bound[iRatio]

                    # this goes below (right side?)
                    xtmp = xTM + 2*xTMpmA
                    #trans = ax.get_xaxis_transform() # x in data units, y in axes fraction
                    #below--annotate("$\leq$ 1.5",xy=(2095,-0.05), xycoords=trans,fontsize=lf_sz, va='center',ha='center',weight='bold',clip_on=False)
                    annotate("$\leq$ 1.5",xy=(2120,-0.46),fontsize=lf_sz, va='center',ha='left',weight='bold',clip_on=False)

                    plt.plot([xtmp,xtmp],[plt.gca().get_ylim()[0]+0.05,plt.gca().get_ylim()[0]+0.02], 'k-', color=cop_color("BioEnergy CCS75"),lw=3.0)
                    plt.plot([xtmp-xTMpm,xtmp+xTMpm],[plt.gca().get_ylim()[0]+0.05,plt.gca().get_ylim()[0]+0.05], 'k-', color=cop_color("BioEnergy CCS75"),lw=3.0)
                    plt.plot([xtmp,xtmp-xTMpm],[plt.gca().get_ylim()[0]+0.02,plt.gca().get_ylim()[0]+0.05], 'k-', color=cop_color("BioEnergy CCS75"),lw=3.0)
                    plt.plot([xtmp,xtmp+xTMpm],[plt.gca().get_ylim()[0]+0.02,plt.gca().get_ylim()[0]+0.05], 'k-', color=cop_color("BioEnergy CCS75"),lw=3.0)

                elif "BioEnergy2 lo" in nScen[j]: 
                    be2ccs00_lo_bound = master_quotient
                elif "BioEnergy2 hi" in nScen[j]: 
                    be2ccs00_hi_bound = master_quotient
                    xtmp = xTM - 2*xTMpmA
                    annotate(temperature_string,xy=(xtmp-xTMtxt,master_quotient[-1]), fontsize=lf_sz, va='center',ha='center',weight='bold')
                    plt.plot([xtmp,xtmp],[ccs00_lo_bound[-1],be2ccs00_hi_bound[-1]], 'k-', color=cop_color("BioEnergy"),lw=3.0)
                    plt.plot([xtmp-xTMpm,xtmp+xTMpm],[be2ccs00_hi_bound[-1],be2ccs00_hi_bound[-1]], 'k-', color=cop_color("BioEnergy"),lw=3.0)
                    plt.plot([xtmp-xTMpm,xtmp+xTMpm],[ccs00_lo_bound[-1],ccs00_lo_bound[-1]], 'k-', color=cop_color("BioEnergy"),lw=3.0)

        annotate("Temperature\nAnomaly [$^{\circ}$C]\n(2100)$\dagger$",xy=(2116,2.10), fontsize=lf_sz, va='bottom',ha='center',clip_on=False,weight='bold')
            
        plt.fill_between(aYear,ccs00_lo_bound,ccs00_hi_bound,edgecolor='none',facecolor=cop_color("BioEnergy"),alpha=0.5)
        plt.fill_between(aYear,ccs25_lo_bound,ccs25_hi_bound,edgecolor='none',facecolor=cop_color("BioEnergy CCS25"),alpha=0.5)
        plt.fill_between(aYear,ccs50_lo_bound,ccs50_hi_bound,edgecolor='none',facecolor=cop_color("BioEnergy CCS50"),alpha=0.5)
        plt.fill_between(aYear,ccs75_lo_bound,ccs75_hi_bound,edgecolor='none',facecolor=cop_color("BioEnergy CCS75"),alpha=0.5)

        plt.fill_between(aYear,be2ccs00_lo_bound,be2ccs00_hi_bound,facecolor='none',alpha=1.0,hatch=hatch_str,edgecolor=cop_color("BioEnergy"))
        plt.fill_between(aYear,be2ccs25_lo_bound,be2ccs25_hi_bound,facecolor='none',alpha=1.0,hatch=hatch_str,edgecolor=cop_color("BioEnergy CCS25"))
        plt.fill_between(aYear,be2ccs50_lo_bound,be2ccs50_hi_bound,facecolor='none',alpha=1.0,hatch=hatch_str,edgecolor=cop_color("BioEnergy CCS50"))
        plt.fill_between(aYear,be2ccs75_lo_bound,be2ccs75_hi_bound,facecolor='none',alpha=1.0,hatch=hatch_str,edgecolor=cop_color("BioEnergy CCS75"))
            
        # For period 2002-2011:
        # A = 8.3 pm 0.7 (FF & cement)
        # B = 0.9 pm 0.8 (LUC)
        # C = 2.4 pm 0.7 (Oceans)
        # D = 2.5 pm 1.3 (Land Sink)
        # T = 4.3 pm 0.2 (Net Atm Flux)
        # (8.3+0.9)/(2.4+2.5) = 1.878
        # Err = 0.22 (propagated quadratically, use T = A+B-C-D to replace C and D in denominator
        range_with_capitols(plt,1.971,0.273,n_subplot=1,year=1984.5)
        range_with_capitols(plt,1.646,0.144,n_subplot=1,year=1994.5)
        range_with_capitols(plt,1.878,0.205,n_subplot=1,year=2006.5)
        
        plt.plot([0,2100],[1,1],'k-',color='black',lw=1.0)
        plt.plot([0,2100],[0,0],'k-',color=greys[6],ls="--",lw=1.25)
        plt.fill_between([2100,2132],[-1,-1],[3,3], facecolor=greys[4], alpha=0.15)
        
        annotate("Net Negative Atmospheric Flux\n(COP target)",xy=(1980,0.95), fontsize=lf_sz, va='top',ha='center')
        annotate("Net Positive Atmospheric Flux",xy=(1980,1.05), fontsize=lf_sz, va='bottom',ha='center')
        annotate("Net Negative Anthropogenic\nEmissions",xy=(1980,-0.05), fontsize=lf_sz, va='top',ha='center')
            
        plt.xlim(1950,2132)
        plt.ylim(-0.5,2.3)
        plt.ylabel("R$_{COP}$", fontsize=yl_sz)
        #plt.ylabel("Ratio of Energy and Land Use Emissions\nto Land, Ocean, and Soil Sink", fontsize=yl_sz)

    if EMtypes[i] == "Flux Atmosphere to Land Sink":

        for j in range(len(nScen)):
            
            plt.subplot(211)
            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1: 
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label=nScen[j],marker="x",zorder=getZ(nScen[j]))
                range_with_capitols(plt,1.5,1.1,n_subplot=2,year=1984)  
                range_with_capitols(plt,2.6,1.2,n_subplot=2,year=1994)
                #range_with_capitols(plt,2.6,1.2,n_subplot=2,year=2004)        
                range_with_capitols(plt,2.5,1.3,n_subplot=2,year=2006)        
                
            elif insta_scen(nScen[j]) == True:
                plt.subplot(211)
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),alpha=getalfa(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

                plt.subplot(212)
                plt.plot(aYear,aEM[cum_lsk_em][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         alpha=getalfa(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                scatter([2100,],[aEM[cum_lsk_em][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

        plt.subplot(211)
        do_BE_range(aEM[i],plt)

        plt.grid(True)
        plt.xlim(1950,2102)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color='black',lw=1.0,zorder=1,clip_on=False)
        plt.ylabel("Land Sink Carbon\nUptake [PgC yr$^{-1}$]", fontsize=yl_sz)

        plt.subplot(212)
        do_BE_range(aEM[cum_lsk_em],plt)

        plt.grid(True)
        plt.xlim(1950,2102)
        plt.ylim(0,600)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color='black',lw=1.0,zorder=1,clip_on=False)
        range_with_capitols(plt,160,90,n_subplot=2,year=2011) 
        plt.ylabel("Cumulative Land Sink\nUptake [PgC]", fontsize=yl_sz)
    
    if EMtypes[i] == "Flux Atmosphere to Ocean":
        
        for j in range(len(nScen)):
            
            plt.subplot(211)
            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1: 
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label=nScen[j],marker="x",zorder=getZ(nScen[j]))
                range_with_capitols(plt,2.0,0.7,n_subplot=2,year=1984)  
                range_with_capitols(plt,2.2,0.7,n_subplot=2,year=1994)
                #range_with_capitols(plt,2.3,0.7,n_subplot=2,year=2004)        
                range_with_capitols(plt,2.4,0.7,n_subplot=2,year=2006)        
                
            elif insta_scen(nScen[j]) == True:
                plt.subplot(211)
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                         lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

                plt.subplot(212)
                plt.plot(aYear,aEM[cum_ocn_em][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                         lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                scatter([2100,],[aEM[cum_ocn_em][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

        plt.subplot(211)
        do_BE_range(aEM[i],plt)
        insert_panel_label(plt,"C")

        plt.grid(True)
        sns.despine(bottom=True)
        plt.xlim(1950,2102)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color='black',lw=1.0,zorder=1,clip_on=False)

        plt.ylabel("Oceanic Carbon\nUptake [PgC yr$^{-1}$]", fontsize=yl_sz)

        plt.subplot(212)
        do_BE_range(aEM[cum_ocn_em],plt)

        range_with_capitols(plt,155,30,n_subplot=2,year=2011)  
        plt.grid(True)
        plt.xlim(1950,2102)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color='black',lw=1.0,zorder=1,clip_on=False)
        plt.ylim(0,600)
        plt.ylabel("Cumulative Oceanic\nUptake [PgC]", fontsize=yl_sz)

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
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label=nScen[j],marker="x",zorder=getZ(nScen[j]))
                # IPCC Range: is there data?             
                        
            elif insta_scen(nScen[j]) == True:
                plt.subplot(211)
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                         lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                #annotate(round(aEM[i][j][-1],1),xy=(2102,aEM[i][j][-1]), fontsize=lf_sz, va='center',ha='left',weight='bold')

                plt.subplot(212)
                plt.plot(aYear,aEM[cseq_em][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                         lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                scatter([2100,],[aEM[cseq_em][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

        plt.subplot(211)    
        do_BE_range(aEM[i],plt)

        plt.ylabel("Annual Renewables\nNet Emissions [PgC yr$^{-1}$]", fontsize=yl_sz)
        plt.xlim(1950,2102)
        #plt.ylim(-6,1)
        plt.grid(True)
        #sns.despine(bottom=True)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color='black',zorder=1,lw=1.0)

        plt.subplot(212)
        do_BE_range(aEM[cseq_em],plt)

        plt.xlim(1950,2102)
        plt.ylim(0,1000)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color='black',lw=1.0,zorder=1,clip_on=False)
        plt.ylabel("Cumulative\nSequestration [PgC]", fontsize=yl_sz)

    if EMtypes[i] == "C in Atmosphere":
                
        for j in range(len(nScen)):

            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1: 
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label=nScen[j],marker="x",zorder=getZ(nScen[j]))
                # IPCC Range: 230-250; C(preind,FeliX) = 606.411
                range_with_capitols(plt,846.411,10,n_subplot=1)                
            
            elif insta_scen(nScen[j]) == True:
                scatter([2100,],[aEM[i][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                         lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))

            elif "BioEnergy lo CCS25" in nScen[j]: ccs25_lo_bound = aEM[i][j]
            elif "BioEnergy hi CCS25" in nScen[j]: ccs25_hi_bound = aEM[i][j]
            elif "BioEnergy lo CCS50" in nScen[j]: ccs50_lo_bound = aEM[i][j]
            elif "BioEnergy hi CCS50" in nScen[j]: ccs50_hi_bound = aEM[i][j]
            elif "BioEnergy lo CCS75" in nScen[j]: ccs75_lo_bound = aEM[i][j]
            elif "BioEnergy hi CCS75" in nScen[j]: ccs75_hi_bound = aEM[i][j]
            elif nScen[j] == "BioEnergy lo": ccs00_lo_bound = aEM[i][j]
            elif nScen[j] == "BioEnergy hi": ccs00_hi_bound = aEM[i][j]
            elif "BioEnergy1 lo CCS25" in nScen[j]: be1ccs25_lo_bound = aEM[i][j]
            elif "BioEnergy1 hi CCS25" in nScen[j]: be1ccs25_hi_bound = aEM[i][j]
            elif "BioEnergy1 lo CCS50" in nScen[j]: be1ccs50_lo_bound = aEM[i][j]
            elif "BioEnergy1 hi CCS50" in nScen[j]: be1ccs50_hi_bound = aEM[i][j]
            elif "BioEnergy1 lo CCS75" in nScen[j]: be1ccs75_lo_bound = aEM[i][j]
            elif "BioEnergy1 hi CCS75" in nScen[j]: be1ccs75_hi_bound = aEM[i][j]
            elif nScen[j] == "BioEnergy1 lo": be1ccs00_lo_bound = aEM[i][j]
            elif nScen[j] == "BioEnergy1 hi": be1ccs00_hi_bound = aEM[i][j]
            elif "BioEnergy2 lo CCS25" in nScen[j]: be2ccs25_lo_bound = aEM[i][j]
            elif "BioEnergy2 hi CCS25" in nScen[j]: be2ccs25_hi_bound = aEM[i][j]
            elif "BioEnergy2 lo CCS50" in nScen[j]: be2ccs50_lo_bound = aEM[i][j]
            elif "BioEnergy2 hi CCS50" in nScen[j]: be2ccs50_hi_bound = aEM[i][j]
            elif "BioEnergy2 lo CCS75" in nScen[j]: be2ccs75_lo_bound = aEM[i][j]
            elif "BioEnergy2 hi CCS75" in nScen[j]: be2ccs75_hi_bound = aEM[i][j]
            elif nScen[j] == "BioEnergy2 lo": be2ccs00_lo_bound = aEM[i][j]
            elif nScen[j] == "BioEnergy2 hi": be2ccs00_hi_bound = aEM[i][j]

        plt.fill_between(aYear,ccs00_lo_bound,ccs00_hi_bound,facecolor=cop_color("BioEnergy"),edgecolor='none',alpha=0.5)
        plt.fill_between(aYear,ccs25_lo_bound,ccs25_hi_bound,facecolor=cop_color("BioEnergy CCS25"),edgecolor='none',alpha=0.5)
        plt.fill_between(aYear,ccs50_lo_bound,ccs50_hi_bound,facecolor=cop_color("BioEnergy CCS50"),edgecolor='none',alpha=0.5)
        plt.fill_between(aYear,ccs75_lo_bound,ccs75_hi_bound,facecolor=cop_color("BioEnergy CCS75"),edgecolor='none',alpha=0.5)
        #
        plt.fill_between(aYear,be2ccs00_lo_bound,be2ccs00_hi_bound,facecolor='none',edgecolor=cop_color("BioEnergy"),hatch=hatch_str,alpha=1.0)
        plt.fill_between(aYear,be2ccs25_lo_bound,be2ccs25_hi_bound,facecolor='none',edgecolor=cop_color("BioEnergy CCS25"),hatch=hatch_str,alpha=1.0)
        plt.fill_between(aYear,be2ccs50_lo_bound,be2ccs50_hi_bound,facecolor='none',edgecolor=cop_color("BioEnergy CCS50"),hatch=hatch_str,alpha=1.0)
        plt.fill_between(aYear,be2ccs75_lo_bound,be2ccs75_hi_bound,facecolor='none',edgecolor=cop_color("BioEnergy CCS75"),hatch=hatch_str,alpha=1.0)
        plt.ylabel("Atmospheric Carbon [PgC]", fontsize=yl_sz)

    if EMtypes[i] == "C Emission from Land Use Change":

        for j in range(len(nScen)):

            if "Historical" in nScen[j]:
                if len(aHyr[i]) > 1: 
                    plt.subplot(211)
                    plt.plot(aHyr[i],aEM[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label=nScen[j],marker="x",zorder=getZ(nScen[j]))
                    range_with_capitols(plt,0.9,0.8,n_subplot=2)
                    range_with_capitols(plt,1.4,0.8,n_subplot=2,year=1984)
                    range_with_capitols(plt,1.5,0.8,n_subplot=2,year=1994)
                    range_with_capitols(plt,1.1,0.8,n_subplot=2,year=2004)

                plt.subplot(212)
                range_with_capitols(plt,180,80,n_subplot=2)
                if len(aHyr[cum_luc_em]) > 1: 
                    plt.plot(aHyr[cum_luc_em],aEM[cum_luc_em][j],color=cop_color(nScen[j]),
                             lw=get_linewidth(nScen[j]),label=nScen[j],marker="x",zorder=getZ(nScen[j]))

            elif insta_scen(nScen[j]) == True: 
            #elif nScen[j] == "BAU" or nScen[j] == "BioEnergy" or nScen[j] == "BioEnergy lo" or nScen[j] == "BioEnergy hi":
                plt.subplot(211)
                plt.plot(aYear,aEM[i][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         alpha=getalfa(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))

                plt.subplot(212)
                plt.plot(aYear,aEM[cum_luc_em][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),lw=get_linewidth(nScen[j]),
                         alpha=getalfa(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))


 
        plt.subplot(211) 
        plt.fill_between(aYear,aEM[i][be_lo_75_idx],aEM[i][be_hi_00_idx],facecolor=cop_color("BioEnergy"),alpha=0.5)
        #plt.fill_between(aYear,aEM[i][be_lo_25_idx],aEM[i][be_hi_25_idx],facecolor=cop_color("BioEnergy CCS25"),alpha=0.5)
        #plt.fill_between(aYear,aEM[i][be_lo_50_idx],aEM[i][be_hi_50_idx],facecolor=cop_color("BioEnergy CCS50"),alpha=0.5)
        #plt.fill_between(aYear,aEM[i][be_lo_75_idx],aEM[i][be_hi_75_idx],facecolor=cop_color("BioEnergy CCS75"),alpha=0.5)
        #plt.fill_between(aYear,aEM[i][be_lo_char_idx],aEM[i][be_hi_char_idx],facecolor='gray',alpha=0.5)

        plt.plot(rcp_time[0:],rcp_luc_26[0:],color=greys[6],ls='-',lw=1,marker="8",ms=4,label='RCP 2.6',alpha=getalfa("RCP"),zorder=01)
        plt.plot(rcp_time[0:],rcp_luc_45[0:],color=greys[6],ls='-',lw=1,marker="s",ms=4,label='RCP 4.5',alpha=getalfa("RCP"),zorder=01)
        plt.plot(rcp_time[0:],rcp_luc_60[0:],color=greys[6],ls='-',lw=1,marker=">",ms=4,label='RCP 6.0',alpha=getalfa("RCP"),zorder=01)
        plt.plot(rcp_time[0:],rcp_luc_85[0:],color=greys[6],ls='-',lw=1,marker="d",ms=4,label='RCP 8.5',alpha=getalfa("RCP"),zorder=01)        
 
        plt.grid(True)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color='black',zorder=1,lw=1.0)
        plt.xlim(1950,2102) 
        plt.ylabel("Annual LULUC\nEmissions [PgC yr$^{-1}$]", fontsize=yl_sz)
            
        plt.subplot(212)
        plt.fill_between(aYear,aEM[cum_luc_em][be_lo_00_idx],aEM[cum_luc_em][be_hi_00_idx],facecolor=cop_color("BioEnergy"),alpha=0.5)
        #plt.fill_between(aYear,aEM[cum_luc_em][be_lo_25_idx],aEM[cum_luc_em][be_hi_25_idx],facecolor=cop_color("BioEnergy CCS25"),alpha=0.5)
        #plt.fill_between(aYear,aEM[cum_luc_em][be_lo_50_idx],aEM[cum_luc_em][be_hi_50_idx],facecolor=cop_color("BioEnergy CCS50"),alpha=0.5)
        #plt.fill_between(aYear,aEM[cum_luc_em][be_lo_75_idx],aEM[cum_luc_em][be_hi_75_idx],facecolor=cop_color("BioEnergy CCS75"),alpha=0.5)
        #plt.fill_between(aYear,aEM[cum_luc_em][be_lo_char_idx],aEM[cum_luc_em][be_hi_char_idx],facecolor='gray',alpha=0.5)

        plt.grid(True)
        plt.xlim(1950,2102)
        plt.plot(plt.gca().get_xlim(),[0,0],'k-',color='black',zorder=1,lw=1.0,clip_on=False)
        plt.ylim(0,)
        plt.ylabel("Cumulative LULUC\nEmissions [PgC]", fontsize=yl_sz)
        
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
                        plt.plot(aHyr[ii],aEM[ii][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label=nScen[j],marker="x",zorder=getZ(nScen[j]))
                    if EMtypes[ii] == "Total C Emission from Fossil Fuels": 
                        range_with_capitols(plt,9.5,0.8,n_subplot=2)
                        # Average Concrete (1980-1989): 1.334E8/yr
                        range_with_capitols(plt,5.3666,0.4,n_subplot=2,year=1984)
                        # Average Concrete (1990-1999): 1.882E8/yr
                        range_with_capitols(plt,6.2118,0.5,n_subplot=2,year=1994)
                        # Average Concrete (2000-2009): 3.146E8/yr
                        range_with_capitols(plt,7.4854,0.6,n_subplot=2,year=2004)
                        
                    if ii == cum_ff_em: range_with_capitols(plt,366,30,n_subplot=2)   

                elif insta_scen(nScen[j]) == True:

                    if EMtypes[ii] == "Total C Emission from Fossil Fuels": 

                        emissions_with_ccs = np.array(aEM[ii][j])*(1-np.array(aEM[ccs_factor_idx][j]))
                        scatter([2100,],[emissions_with_ccs[-1],],dots,alpha=getalfa(nScen[j]),color=cop_color(nScen[j]),zorder=getZ(nScen[j]))

                        #if "BioEnergy1" not in nScen[j]:
                        #    annotate(str(round(float(emissions_with_ccs[-1]),1))+r' PgC yr$^{-1}$',xy=(2102,float(emissions_with_ccs[-1])), fontsize=lf_sz-2, va='center',ha='left')

                        if "BAU" == nScen[j]:

                            plt.plot(rcp_time[1:],rcp_ff_26[1:],color=greys[6],ls='-',lw=1,marker="8",ms=4,label='RCP 2.6',alpha=getalfa("RCP"),zorder=01)
                            plt.plot(rcp_time[1:],rcp_ff_45[1:],color=greys[6],ls='-',lw=1,marker="s",ms=4,label='RCP 4.5',alpha=getalfa("RCP"),zorder=01)
                            plt.plot(rcp_time[1:],rcp_ff_60[1:],color=greys[6],ls='-',lw=1,marker=">",ms=4,label='RCP 6.0',alpha=getalfa("RCP"),zorder=01)
                            plt.plot(rcp_time[1:],rcp_ff_85[1:],color=greys[6],ls='-',lw=1,marker="d",ms=4,label='RCP 8.5',alpha=getalfa("RCP"),zorder=01)        

                            plt.plot(aYear,emissions_with_ccs,color=cop_color(nScen[j]),ls=cop_style(nScen[j]),
                                     alpha=getalfa(nScen[j]),lw=get_linewidth(nScen[j]),label=nScen[j],zorder=getZ(nScen[j]))

                            em_ccs_lo = np.array(aEM[ii][be_lo_00_idx])*(1-np.array(aEM[ccs_factor_idx][be_lo_00_idx]))                       
                            em_ccs_hi = np.array(aEM[ii][be_hi_00_idx])*(1-np.array(aEM[ccs_factor_idx][be_hi_00_idx])) 
                            plt.fill_between(aYear,em_ccs_lo,em_ccs_hi,edgecolor='none',facecolor=cop_color("BioEnergy"),alpha=0.5)
                            
                            em_ccs_lo = np.array(aEM[ii][be_lo_25_idx])*(1-np.array(aEM[ccs_factor_idx][be_lo_25_idx]))                       
                            em_ccs_hi = np.array(aEM[ii][be_hi_25_idx])*(1-np.array(aEM[ccs_factor_idx][be_hi_25_idx]))
                            plt.fill_between(aYear,em_ccs_lo,em_ccs_hi,edgecolor='none',facecolor=cop_color("BioEnergy CCS25"),alpha=0.5)
                            
                            em_ccs_lo = np.array(aEM[ii][be_lo_50_idx])*(1-np.array(aEM[ccs_factor_idx][be_lo_50_idx]))                       
                            em_ccs_hi = np.array(aEM[ii][be_hi_50_idx])*(1-np.array(aEM[ccs_factor_idx][be_hi_50_idx])) 
                            plt.fill_between(aYear,em_ccs_lo,em_ccs_hi,edgecolor='none',facecolor=cop_color("BioEnergy CCS50"),alpha=0.5)
                            
                            em_ccs_lo = np.array(aEM[ii][be_lo_75_idx])*(1-np.array(aEM[ccs_factor_idx][be_lo_75_idx]))                       
                            em_ccs_hi = np.array(aEM[ii][be_hi_75_idx])*(1-np.array(aEM[ccs_factor_idx][be_hi_75_idx])) 
                            plt.fill_between(aYear,em_ccs_lo,em_ccs_hi,edgecolor='none',facecolor=cop_color("BioEnergy CCS75"),alpha=0.5)

                            em_ccs_lo = np.array(aEM[ii][be2_lo_00_idx])*(1-np.array(aEM[ccs_factor_idx][be2_lo_00_idx]))                       
                            em_ccs_hi = np.array(aEM[ii][be2_hi_00_idx])*(1-np.array(aEM[ccs_factor_idx][be2_hi_00_idx])) 
                            plt.fill_between(aYear,em_ccs_lo,em_ccs_hi,facecolor='none',hatch=hatch_str,edgecolor=cop_color("BioEnergy"),alpha=1.0)

                            em_ccs_lo = np.array(aEM[ii][be2_lo_25_idx])*(1-np.array(aEM[ccs_factor_idx][be2_lo_25_idx]))                       
                            em_ccs_hi = np.array(aEM[ii][be2_hi_25_idx])*(1-np.array(aEM[ccs_factor_idx][be2_hi_25_idx])) 
                            plt.fill_between(aYear,em_ccs_lo,em_ccs_hi,facecolor='none',hatch=hatch_str,edgecolor=cop_color("BioEnergy CCS25"),alpha=1.0)

                            em_ccs_lo = np.array(aEM[ii][be2_lo_50_idx])*(1-np.array(aEM[ccs_factor_idx][be2_lo_50_idx]))                       
                            em_ccs_hi = np.array(aEM[ii][be2_hi_50_idx])*(1-np.array(aEM[ccs_factor_idx][be2_hi_50_idx])) 
                            plt.fill_between(aYear,em_ccs_lo,em_ccs_hi,facecolor='none',hatch=hatch_str,edgecolor=cop_color("BioEnergy CCS50"),alpha=1.0)

                            em_ccs_lo = np.array(aEM[ii][be2_lo_75_idx])*(1-np.array(aEM[ccs_factor_idx][be2_lo_75_idx]))                       
                            em_ccs_hi = np.array(aEM[ii][be2_hi_75_idx])*(1-np.array(aEM[ccs_factor_idx][be2_hi_75_idx])) 
                            plt.fill_between(aYear,em_ccs_lo,em_ccs_hi,facecolor='none',hatch=hatch_str,edgecolor=cop_color("BioEnergy CCS75"),alpha=1.0)

                            plt.xlim(1950,2102)
                            plt.ylim(0,20)
                            #plt.xticks([2000,2050,2100],["","",""])
                            
                            plt.ylabel("Annual Fossil Fuel\nEmissions [PgC yr$^{-1}$]", fontsize=yl_sz)
                            insert_panel_label(plt,"A",2)

                            if label_HD == True: annotate('Historical Data Source: CDIAC', fontsize=hd_sz, xy=(2125,-3.5),ha='right',va='center', annotation_clip=False)

                        else:
                            plt.plot(aYear,emissions_with_ccs,color=cop_color(nScen[j]),ls=cop_style(nScen[j]),
                                     alpha=getalfa(nScen[j]),lw=get_linewidth(nScen[j]),label=nScen[j],zorder=getZ(nScen[j]))

                    elif EMtypes[ii] == "Cumulative Emissions from Fossil Fuels":

                        scatter([2100,],[aEM[ii][j][-1],],dots,color=cop_color(nScen[j]),alpha=getalfa(nScen[j]),zorder=getZ(nScen[j]))

                        if "BAU" == nScen[j]:
                            plt.plot(aYear,aEM[ii][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),alpha=getalfa(nScen[j]),label=nScen[j],zorder=getZ(nScen[j]))
                            do_BE_range(aEM[ii],plt)

                            plt.ylabel("Cumulative Fossil\nFuel Emissions [PgC]", fontsize=yl_sz)
                            plt.xlim(1950,2102)
                            plt.ylim(0,1900)
                            plt.grid(True)

                        else:
                            plt.plot(aYear,aEM[ii][j],color=cop_color(nScen[j]),ls=cop_style(nScen[j]),alpha=getalfa(nScen[j]),
                                     lw=get_linewidth(nScen[j]),label=cop_scen_rep(nScen[j]),zorder=getZ(nScen[j]))
                            ax = plt.gca()
                            #leg = ax.legend(loc='best',ncol=2,fontsize=6,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)
        
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.2)

        #ax = plt.gca()
        #leg = ax.legend(loc='best', ncol=2,framealpha=0.9)
    
    if (EMtypes[i] == "Net C Emission from Energy Sector"
        or EMtypes[i] == "Flux Atmosphere to Ocean"
        or EMtypes[i] == "Flux Atmosphere to Land Sink"
        or EMtypes[i] == "Net Emissions"
        or EMtypes[i] == "C Emission from Land Use Change"
        or i == ann_bem_idx
        or i == kaya_cie_idx):
        sns.despine(bottom=True)
    elif "Temperature Anomalies" in EMtypes[i]:
        sns.despine(trim=True)
    else: 
        #plt.xlim(1950,2102)
        sns.despine()

    plt.grid(True)

    ax = plt.gca()

    if EMtypes[i] == "Net C Emission from Energy Sector":
        # Legend on bottom:
        #plt.legend(bbox_to_anchor=(0.25, -0.18,0.50,0),bbox_transform=plt.gcf().transFigure,mode="expand",loc=3,ncol=2,borderpad=0.75,fancybox=True,frameon=True)
        # Side panel legend:
        leg = plt.legend(bbox_to_anchor=(0.94, 0.48,0.24,0.5),bbox_transform=plt.gcf().transFigure,mode="expand",loc=3,ncol=1,borderpad=0.75,fancybox=True,frameon=True)
        annotate("$\dagger$ TCS = "+tcs_str[0].replace("C","")+"$^{\circ}$C / 2xCO$_2$", xy=(0.12,0.0), xycoords=leg.get_frame(),fontsize=6,va="center",ha="left")
        #annotate("$\dagger$ ECS = 3.75", xy=(0.5,0.0), xycoords=leg.get_frame(),xytext=(-5,0), textcoords="offset points",fontsize=8,weight='bold',va="top", ha="center")

    elif EMtypes[i] == "C in Atmosphere":
        leg = ax.legend(loc='best',ncol=1,fontsize=6,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)
    elif i == temp_anom_idx:
        leg = ax.legend(loc='upper left',ncol=2,fontsize=6,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)
    elif EMtypes[i] == "Net Emissions":
        leg = ax.legend(loc='best',ncol=3,fontsize=6,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)
    elif i == atm_ppm_idx:
        leg = ax.legend(loc='best',ncol=1,fontsize=9,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)

    #elif EMtypes[i] != "Total C Emission from Fossil Fuels":
    #    leg = ax.legend(loc='best',ncol=2,fontsize=6,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)

    plt.draw()
    plt.savefig('figures/biomass_'+EMtypes[i].replace("&","").replace("+","").replace("  ","_").replace(" ","_")+'.pdf',format='pdf', dpi=1200)
    plt.clf()
    plt.close('all')
