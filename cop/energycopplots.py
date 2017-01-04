from pylab import *
import csv
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
          'legend.fontsize': 12,
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
#mtoe_to_ej = 1.00000

#############################################
# Formatting Controls
lf_sz = 7      # label font size:
dots = 15      # scatter/dot size:
txsz = 8       # tick label font size
title_sz = 16  # plot title size
xl_sz = 14     # x-axis label size
yl_sz = 10     # y-axis label size
hd_sz = 9      # source data label size
#
err_alpha = 0.40 # Transparency of primary error ranges
sec_alpha = 0.20 # Transparency of secondary error ranges
ep_alpha = 0.85  # Transparency of Energy Profile panels

#############################################
# "Show" Switches
plot_errors        = False
#
show_production    = False
show_energyprofile = False
#
label_HD = False

#####
def insert_panel_label(plt,panel_str,n_subp=2,equiv_yr=1937):
    y_val = 1.0
    trans = plt.gca().get_xaxis_transform() # x in data units, y in axes fraction
    annotate(panel_str,size=21, xy=(equiv_yr,y_val),xycoords=trans,ha='right',va='center',weight='bold',annotation_clip=False)

#############################################
#############################################
# Market Share
#
iRow = 0
iFuel = -1
iScen = 0
nFuels = 0
fuelTypes = []
nScen = []
aYear = []
aHyr = [[]]
aMkt = [[[]]]

fig = plt.gcf()
size = fig.get_size_inches()
print "\nFigure size =",size,"\n"

with open("tables/energy_table.csv") as f: 
    reader = csv.reader(f)
    allRows = list(reader)
    nRows = len(allRows)

with open("tables/energy_table.csv") as f: 
    reader = csv.reader(f)
    
    for row in reader:

##### TIME INFO
        if iRow == 0:
            for i in range(1,len(row)-1):
                aYear.append(int(float(row[i])))
                
##### SCENARIO INFO
        elif iRow == 1:
            for i in range(1,len(row)):
                if row[i] != "": nScen.append(row[i])
                
            nFuels = (nRows-2)/len(nScen)
            if nFuels%1 != 0: print "Error: Unexpected number of rows!"
                
            for n in range(nFuels):
                aMkt.append([])
                aHyr.append([])
                for m in range(len(nScen)):
                    aMkt[n].append([])
##### SCENARIO DATA
        else:
            if (iRow-2)%len(nScen) == 0:
                fuelTypes.append(row[0])
                iFuel = iFuel+1
                iScen = 0
                
            for i in range(1,len(row)-1):
                if "--" not in row[i] and row[i] != "":
                    if "Historical" in row[0]: aHyr[iFuel].append(aYear[i-1])
                    if "Market Share" in fuelTypes[iFuel]:
                        aMkt[iFuel][iScen].append(float(row[i])*100)
                    # These have units of biomass ton/year, not EJ
                    elif ("Potential Land Based Biomass Production" in fuelTypes[iFuel]
                          or "Arable Land Residue Production" in fuelTypes[iFuel]
                          or "Energy Crops Production" in fuelTypes[iFuel]
                          or "Forest Biomass Production" in fuelTypes[iFuel]):
                        aMkt[iFuel][iScen].append(float(row[i])/1E9)
                    else:
                        aMkt[iFuel][iScen].append(float(row[i])*mtoe_to_ej)
            iScen = iScen+1
                
        iRow = iRow+1

#################################
# Plot Market Share (by Fuel Type)
standardize_scenario_names(nScen)

for ii in range(nFuels):
    if "Market Share" in fuelTypes[ii]:
        if "Biomass" in fuelTypes[ii]: idxB = ii
        elif "Oil" in fuelTypes[ii]:   idxO = ii
        elif "Coal" in fuelTypes[ii]:  idxC = ii
        elif "Gas" in fuelTypes[ii]:   idxG = ii
    elif "Production" in fuelTypes[ii]:
        if "Biomass Land Energy" in fuelTypes[ii]: pidxB = ii
        elif "Oil" in fuelTypes[ii]:   pidxO = ii
        elif "Coal" in fuelTypes[ii]:  pidxC = ii
        elif "Gas" in fuelTypes[ii]:   pidxG = ii
        
    if "Forest Biomass Production" in fuelTypes[ii]: fbio_idx = ii
    if "Potential Land Based Biomass Production" in fuelTypes[ii]: pbio_idx = ii

for jj in range(len(nScen)):
    if "BAU" == nScen[jj]: idxBAU = jj
    elif "Historical" in nScen[jj]: idxHIS = jj
    elif "BAU lo" == nScen[jj]: idxBAUlo = jj
    elif "BAU hi" == nScen[jj]: idxBAUhi = jj
    elif "FossilBAU lo" == nScen[jj]: idxFBAUlo = jj
    elif "FossilBAU hi" == nScen[jj]: idxFBAUhi = jj
    elif "BioEnergy lo" == nScen[jj]: idxBElo = jj
    elif "BioEnergy hi" == nScen[jj]: idxBEhi = jj
    elif "BioEnergy1 lo" == nScen[jj]: idxBE1lo = jj
    elif "BioEnergy1 hi" == nScen[jj]: idxBE1hi = jj
    elif "BioEnergy2 lo" == nScen[jj]: idxBE2lo = jj
    elif "BioEnergy2 hi" == nScen[jj]: idxBE2hi = jj
    elif "BioEnergy3 lo" == nScen[jj]: idxBE3lo = jj
    elif "BioEnergy3 hi" == nScen[jj]: idxBE3hi = jj

for i in range(nFuels):
    continue
    plt.cla()
    for j in range(len(nScen)):

        if "Market Share" in fuelTypes[i]:
            if "BAU" not in nScen[j] and "Historical" not in nScen[j]: continue

            if i != idxB:            
                if "Historical" in nScen[j] and len(aMkt[i]) > 1:
                    plt.plot(aHyr[i],aMkt[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
                else:
                    plt.plot(aYear,aMkt[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
                    plt.ylabel(fuelTypes[i]+" (%)", fontsize=yl_sz)
            elif j == idxBAU:
                # BAU Market Share of Fossil Fuels error bars
                if plot_errors == True:
                    for nn in range(len(nScen)):
                        if nScen[nn] == "BAU pop low": 
                            low_coal = np.array(aMkt[idxC][nn])
                            low_gas  = np.array(aMkt[idxG][nn])
                            low_oil  = np.array(aMkt[idxO][nn])
                        elif nScen[nn] == "BAU pop high": 
                            high_coal = np.array(aMkt[idxC][nn])
                            high_gas  = np.array(aMkt[idxG][nn])
                            high_oil  = np.array(aMkt[idxO][nn])
                    plt.fill_between(aYear,high_coal,low_coal,facecolor=get_color(fuelTypes[idxC]),alpha=err_alpha)
                    plt.fill_between(aYear,high_gas,low_gas,facecolor=get_color(fuelTypes[idxG]),alpha=err_alpha)
                    plt.fill_between(aYear,high_oil,low_oil,facecolor=get_color(fuelTypes[idxO]),alpha=err_alpha)

                plt.plot(aYear,aMkt[idxC][idxBAU],color=get_color(fuelTypes[idxC]),linewidth=get_linewidth(nScen[j]),label="Coal")
                plt.plot(aYear,aMkt[idxG][idxBAU],color=get_color(fuelTypes[idxG]),linewidth=get_linewidth(nScen[j]),label="Gas")
                plt.plot(aYear,aMkt[idxO][idxBAU],color=get_color(fuelTypes[idxO]),linewidth=get_linewidth(nScen[j]),label="Oil")
                plt.plot(aHyr[idxC],aMkt[idxC][idxHIS],color=get_color(nScen[idxHIS]),linewidth=get_linewidth("HistoricalData"),label="HistoricalData")
                plt.plot(aHyr[idxG],aMkt[idxG][idxHIS],color=get_color(nScen[idxHIS]),linewidth=get_linewidth("HistoricalData"))
                plt.plot(aHyr[idxO],aMkt[idxO][idxHIS],color=get_color(nScen[idxHIS]),linewidth=get_linewidth("HistoricalData"))
                plt.ylabel("Fossil Fuel Market Share (%)", fontsize=yl_sz)
                if label_HD == True:
                    annotate('Source: IEA - Key World Energy Statistics 2013', fontsize=hd_sz, xy=(2100, -8), xycoords='data', 
                             horizontalalignment='right',verticalalignment='center', annotation_clip=False)
                

        elif "Historical" in nScen[j] and len(aMkt[i]) > 1:
            plt.plot(aHyr[i],aMkt[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
        else:
            plt.plot(aYear,aMkt[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
    
    plt.xlim(1900,2100)
    #plt.xlabel('Year',fontsize=xl_sz)
    if "Market Share" not in fuelTypes[i]: 
        plt.ylabel(fuelTypes[i]+" [EJ y"+r'$^{-1}$]', fontsize=yl_sz)

    ax = plt.gca()
    leg = ax.legend(loc='best', ncol=1,borderpad=0.75,fancybox=True, frameon=True,framealpha=0.9)
    plt.grid(True)
    sns.despine()
    #plt.figure().set_tight_layout(True)
    plt.draw()
    plt.savefig('figures/production_'+fuelTypes[i].replace(" ","_").replace("&","").replace("+","").replace("_Energy_Production","").replace("_Production","")+'.pdf',format='pdf', dpi=1000)
    if show_production == True: plt.show()
    plt.clf()
    plt.close('all')
    print "Finished: production_"+fuelTypes[i]

#################################
# Plot Market Share (by Scenario)
standardize_scenario_names(nScen)

for j in range(len(nScen)):
    #continue # For now, skip running energy plots  
    if "CCS" in nScen[j]: continue
    elif "lo" in nScen[j]: continue
    elif "hi" in nScen[j]: continue
    elif "char" in nScen[j]: continue

    tempMkt = np.array(aMkt[0][j])
    plt.cla()
    plt.clf()
    demandIdx = -1
    supplyIdx = -1
    minYstep = 27
    fFuel = []
    fFuelCol = []
    fFuel_y_us = []

    if not "Historical" in nScen[j]:
        for k in range(nFuels):
            if "Energy Demand" == fuelTypes[k]:
                demandIdx = k

                # Hack:
                if nScen[j] == "BAU" or "Fossil" in nScen[j]:
                    #aMkt[k][j] = [0 for j_hack in range(len(aMkt[k][j]))]
                    for k_hack in range(nFuels):
                        if "Energy Production EIA" == fuelTypes[k_hack]:
                            aMkt[k][j] = np.array(aMkt[k_hack][j])
                            print "--> For (Fossil*)BAU PE profile, setting energy demand equal to production"
                # End of hack
                            
                plt.plot(aYear,aMkt[k][j],color='black',linewidth=1,linestyle="--",label=fuelTypes[k],zorder=100)
                if "Fossil" in nScen[j]:
                    annotate("Nominal", xy=(2100,aMkt[k][j][-1]+25),fontsize=lf_sz,ha='right',va='bottom',color='black',zorder=100)

                # Uncomment these lines to annotate total energy demand
                #ftFuel = str(int(round(aMkt[k][j][-1],0)))+' EJ'
                #annotate(str(ftFuel), xy=(2110,aMkt[k][j][-1]+10), xycoords='data',fontsize=lf_sz,horizontalalignment='center',color='black')
                if "Alg" in nScen[j] and label_HD == True:
                    annotate('Source: IEA - Key World Energy Statistics 2013', fontsize=hd_sz, xy=(2120, -100), xycoords='data', 
                             ha='right',va='center', annotation_clip=False)

            elif "Energy Production EIA" == fuelTypes[k]:
                supplyIdx = k
    
    for jj in range(len(nScen)):
        for ii in range(nFuels):
            if "Historical" in nScen[jj] and "Energy Demand" == fuelTypes[ii]:
                plt.plot(aHyr[ii],aMkt[ii][jj],color=get_color(nScen[jj]),linewidth=get_linewidth(nScen[jj]),linestyle="-",label="Total demand (IEA)",marker="x",zorder = 101)

    fuel_index = -1
    fuel_stack_baulo = 0
    fuel_stack_bauhi = 0  
    fuel_stack_fbaulo = 0
    fuel_stack_fbauhi = 0  
    fuel_stack_belo = 0
    fuel_stack_behi = 0    
    fuel_stack_be1lo = 0
    fuel_stack_be1hi = 0
    fuel_stack_be2lo = 0
    fuel_stack_be2hi = 0 
    fuel_stack_be3lo = 0
    fuel_stack_be3hi = 0 

    fuel_stack_baulo_lo = 0
    fuel_stack_bauhi_lo = 0 
    fuel_stack_fbaulo_lo = 0
    fuel_stack_fbauhi_lo = 0 
    fuel_stack_belo_lo = 0
    fuel_stack_behi_lo = 0 
    fuel_stack_be1lo_lo = 0
    fuel_stack_be1hi_lo = 0 
    fuel_stack_be2lo_lo = 0
    fuel_stack_be2hi_lo = 0 
    fuel_stack_be3lo_lo = 0
    fuel_stack_be3hi_lo = 0 

    for i in range(nFuels):

        if "Historical" in nScen[j] and "Energy Demand" != fuelTypes[i]: continue
        elif "Energy Demand" == fuelTypes[i] and "Historical" not in nScen[j]: continue
        elif "Production" not in fuelTypes[i] or "Energy Production" == fuelTypes[i] or "EIA" in fuelTypes[i]: continue
        elif "Arable Land" in fuelTypes[i] or "Energy Crops" in fuelTypes[i] or "Potential Land Based Biomass" in fuelTypes[i] or "Forest Biomass" in fuelTypes[i]: continue
        else:  
            
            fuel_label_string = str(int(round(aMkt[i][j][-1],0)))+' EJ'
            if fuel_label_string != "0 EJ" or "Oil" in fuelTypes[i]:

            #Stack Hack
                if i != 0:
                    tempMkt = tempMkt + np.array(aMkt[i][j])
                plt.plot(aYear,tempMkt,color=get_color(fuelTypes[i]),linewidth=get_linewidth(fuelTypes[i]),
                         label=fuelTypes[i].replace(" Production","").replace("Energy","").replace(" Land","").replace("Nuclear","Nuc. & Hydro."))
                plt.fill_between(aYear,tempMkt-np.array(aMkt[i][j]),tempMkt,facecolor=get_color(fuelTypes[i]),alpha=ep_alpha)

                ########
                # Hack: these lines plot the contribution of forest plantations to biomass production
                #   the darker shaded region goes on bottom within the biomass range, and represents plantation production
                #   the lighter shaded region goes on top within the biomass range, and represents energy crop + residue production
                if i == pidxB:
                    plt.plot(aYear,tempMkt-np.array(aMkt[i][j])*(1-np.array(aMkt[fbio_idx][j])/np.array(aMkt[pbio_idx][j])),
                             color=get_color(fuelTypes[i]),lw=get_linewidth(fuelTypes[i]))
                    plt.fill_between(aYear,tempMkt-np.array(aMkt[i][j]),tempMkt-np.array(aMkt[i][j])*(1-np.array(aMkt[fbio_idx][j])/np.array(aMkt[pbio_idx][j])),
                                     facecolor=get_color(fuelTypes[i]),alpha=ep_alpha)
                ########

                if nScen[j] == "BAU":
                    fuel_stack_baulo += aMkt[i][idxBAUlo][-1]
                    fuel_stack_bauhi += aMkt[i][idxBAUhi][-1]

                    plt.plot([2105,2120],[fuel_stack_baulo,fuel_stack_baulo], 'k-', color=get_color(fuelTypes[i]),lw=1.5)
                    plt.plot([2130,2145],[fuel_stack_bauhi,fuel_stack_bauhi], 'k-', color=get_color(fuelTypes[i]),lw=1.5)

                    plt.fill_between([2105,2120],fuel_stack_baulo_lo,fuel_stack_baulo,facecolor=get_color(fuelTypes[i]),alpha=err_alpha)
                    plt.fill_between([2130,2145],fuel_stack_bauhi_lo,fuel_stack_bauhi,facecolor=get_color(fuelTypes[i]),alpha=err_alpha)
                    
                    y_offset_hack = 10
                    if ("Wind" in fuelTypes[i]): y_offset_hack = -15

                    annotate(str(int(round(aMkt[i][idxBAUlo][-1],0))), xy=(2112.5,fuel_stack_baulo-y_offset_hack), xycoords='data',
                             fontsize=lf_sz,ha='center',va='top',color=get_color("lab"+fuelTypes[i]),weight='bold',zorder=100)
                    annotate(str(int(round(aMkt[i][idxBAUhi][-1],0))), xy=(2137.5,fuel_stack_bauhi-y_offset_hack), xycoords='data',
                             fontsize=lf_sz,ha='center',va='top',color=get_color("lab"+fuelTypes[i]),weight='bold',zorder=100)

                    fuel_stack_baulo_lo = fuel_stack_baulo
                    fuel_stack_bauhi_lo = fuel_stack_bauhi

                if nScen[j] == "FossilBAU":
                    fuel_stack_fbaulo += aMkt[i][idxFBAUlo][-1]
                    fuel_stack_fbauhi += aMkt[i][idxFBAUhi][-1]

                    plt.plot([2105,2120],[fuel_stack_fbaulo,fuel_stack_fbaulo], 'k-', color=get_color(fuelTypes[i]),lw=1.5)
                    plt.plot([2130,2145],[fuel_stack_fbauhi,fuel_stack_fbauhi], 'k-', color=get_color(fuelTypes[i]),lw=1.5)

                    plt.fill_between([2105,2120],fuel_stack_fbaulo_lo,fuel_stack_fbaulo,facecolor=get_color(fuelTypes[i]),alpha=err_alpha)
                    plt.fill_between([2130,2145],fuel_stack_fbauhi_lo,fuel_stack_fbauhi,facecolor=get_color(fuelTypes[i]),alpha=err_alpha)
                    
                    y_offset_hack = 10
                    if ("Biomass" in fuelTypes[i] or "Wind" in fuelTypes[i]): y_offset_hack = -15
                    if ("Solar" in fuelTypes[i]): y_offset_hack = 10
                    if ("Oil" in fuelTypes[i]): y_offset_hack = 20

                    annotate(str(int(round(aMkt[i][idxFBAUlo][-1],0))), xy=(2112.5,fuel_stack_fbaulo-y_offset_hack), xycoords='data',
                             fontsize=lf_sz,ha='center',va='top',color=get_color("lab"+fuelTypes[i]),weight='bold',zorder=100)
                    annotate(str(int(round(aMkt[i][idxFBAUhi][-1],0))), xy=(2137.5,fuel_stack_fbauhi-y_offset_hack), xycoords='data',
                             fontsize=lf_sz,ha='center',va='top',color=get_color("lab"+fuelTypes[i]),weight='bold',zorder=100)

                    fuel_stack_fbaulo_lo = fuel_stack_fbaulo
                    fuel_stack_fbauhi_lo = fuel_stack_fbauhi

                if nScen[j] == "BioEnergy":
                    fuel_stack_belo += aMkt[i][idxBElo][-1]
                    fuel_stack_behi += aMkt[i][idxBEhi][-1]

                    plt.plot([2105,2120],[fuel_stack_belo,fuel_stack_belo], 'k-', color=get_color(fuelTypes[i]),lw=1.5)
                    plt.plot([2130,2145],[fuel_stack_behi,fuel_stack_behi], 'k-', color=get_color(fuelTypes[i]),lw=1.5)

                    plt.fill_between([2105,2120],fuel_stack_belo_lo,fuel_stack_belo,facecolor=get_color(fuelTypes[i]),alpha=err_alpha)
                    plt.fill_between([2130,2145],fuel_stack_behi_lo,fuel_stack_behi,facecolor=get_color(fuelTypes[i]),alpha=err_alpha)
                    
                    annotate(str(int(round(aMkt[i][idxBElo][-1],0))), xy=(2112.5,fuel_stack_belo-10), xycoords='data',
                             fontsize=lf_sz,ha='center',va='top',color=get_color("lab"+fuelTypes[i]),weight='bold',zorder=100)
                    annotate(str(int(round(aMkt[i][idxBEhi][-1],0))), xy=(2137.5,fuel_stack_behi-10), xycoords='data',
                             fontsize=lf_sz,ha='center',va='top',color=get_color("lab"+fuelTypes[i]),weight='bold',zorder=100)

                    fuel_stack_belo_lo = fuel_stack_belo
                    fuel_stack_behi_lo = fuel_stack_behi

                elif nScen[j] == "BioEnergy1":
                    fuel_stack_be1lo += aMkt[i][idxBE1lo][-1]
                    fuel_stack_be1hi += aMkt[i][idxBE1hi][-1]

                    plt.plot([2105,2120],[fuel_stack_be1lo,fuel_stack_be1lo], 'k-', color=get_color(fuelTypes[i]),lw=1.5)
                    plt.plot([2130,2145],[fuel_stack_be1hi,fuel_stack_be1hi], 'k-', color=get_color(fuelTypes[i]),lw=1.5)

                    plt.fill_between([2105,2120],fuel_stack_be1lo_lo,fuel_stack_be1lo,facecolor=get_color(fuelTypes[i]),alpha=err_alpha)
                    plt.fill_between([2130,2145],fuel_stack_be1hi_lo,fuel_stack_be1hi,facecolor=get_color(fuelTypes[i]),alpha=err_alpha)

                    annotate(str(int(round(aMkt[i][idxBE1lo][-1],0))), xy=(2112.5,fuel_stack_be1lo-10), xycoords='data',
                             fontsize=lf_sz,ha='center',va='top',color=get_color("lab"+fuelTypes[i]),weight='bold',zorder=100)
                    annotate(str(int(round(aMkt[i][idxBE1hi][-1],0))), xy=(2137.5,fuel_stack_be1hi-10), xycoords='data',
                             fontsize=lf_sz,ha='center',va='top',color=get_color("lab"+fuelTypes[i]),weight='bold',zorder=100)

                    fuel_stack_be1lo_lo = fuel_stack_be1lo
                    fuel_stack_be1hi_lo = fuel_stack_be1hi

                elif nScen[j] == "BioEnergy2":
                    fuel_stack_be2lo += aMkt[i][idxBE2lo][-1]
                    fuel_stack_be2hi += aMkt[i][idxBE2hi][-1]

                    plt.plot([2105,2120],[fuel_stack_be2lo,fuel_stack_be2lo], 'k-', color=get_color(fuelTypes[i]),lw=1.5)
                    plt.plot([2130,2145],[fuel_stack_be2hi,fuel_stack_be2hi], 'k-', color=get_color(fuelTypes[i]),lw=1.5)

                    plt.fill_between([2105,2120],fuel_stack_be2lo_lo,fuel_stack_be2lo,facecolor=get_color(fuelTypes[i]),alpha=err_alpha)
                    plt.fill_between([2130,2145],fuel_stack_be2hi_lo,fuel_stack_be2hi,facecolor=get_color(fuelTypes[i]),alpha=err_alpha)

                    annotate(str(int(round(aMkt[i][idxBE2lo][-1],0))), xy=(2112.5,fuel_stack_be2lo-10), xycoords='data',
                             fontsize=lf_sz,ha='center',va='top',color=get_color("lab"+fuelTypes[i]),weight='bold',zorder=100)
                    annotate(str(int(round(aMkt[i][idxBE2hi][-1],0))), xy=(2137.5,fuel_stack_be2hi-10), xycoords='data',
                             fontsize=lf_sz,ha='center',va='top',color=get_color("lab"+fuelTypes[i]),weight='bold',zorder=100)

                    fuel_stack_be2lo_lo = fuel_stack_be2lo
                    fuel_stack_be2hi_lo = fuel_stack_be2hi

                elif nScen[j] == "BioEnergy3":
                    fuel_stack_be3lo += aMkt[i][idxBE3lo][-1]
                    fuel_stack_be3hi += aMkt[i][idxBE3hi][-1]

                    plt.plot([2105,2120],[fuel_stack_be3lo,fuel_stack_be3lo], 'k-', color=get_color(fuelTypes[i]),lw=1.5)
                    plt.plot([2130,2145],[fuel_stack_be3hi,fuel_stack_be3hi], 'k-', color=get_color(fuelTypes[i]),lw=1.5)

                    plt.fill_between([2105,2120],fuel_stack_be3lo_lo,fuel_stack_be3lo,facecolor=get_color(fuelTypes[i]),alpha=err_alpha)
                    plt.fill_between([2130,2145],fuel_stack_be3hi_lo,fuel_stack_be3hi,facecolor=get_color(fuelTypes[i]),alpha=err_alpha)

                    y_offset_hack = 10
                    #if ("Biomass" in fuelTypes[i] or "Nuc" in fuelTypes[i]): y_offset_hack = 12
                    if ("Oil" in fuelTypes[i] or "Coal" in fuelTypes[i]): y_offset_hack = -8

                    annotate(str(int(round(aMkt[i][idxBE3lo][-1],0))), xy=(2112.5,fuel_stack_be3lo-y_offset_hack), xycoords='data',
                             fontsize=lf_sz,ha='center',va='top',color=get_color("lab"+fuelTypes[i]),weight='bold',zorder=100)
                    annotate(str(int(round(aMkt[i][idxBE3hi][-1],0))), xy=(2137.5,fuel_stack_be3hi-y_offset_hack), xycoords='data',
                             fontsize=lf_sz,ha='center',va='top',color=get_color("lab"+fuelTypes[i]),weight='bold',zorder=100)

                    fuel_stack_be3lo_lo = fuel_stack_be3lo
                    fuel_stack_be3hi_lo = fuel_stack_be3hi

            # Annotate: total supply by fuel type in EJ

                fFuel.append(fuel_label_string)
                fFuelCol.append(get_color("lab"+fuelTypes[i]))
                fFuel_y_us.append(tempMkt[-1])

        fuel_index *=-1
    
    #Sort and then Annotate
    ann_val = [2100,'right']
    
    new_y_offset(fFuel_y_us,35,-5)

    for iii in range(len(fFuel_y_us)):
        annotate(str(fFuel[iii]), xy=(ann_val[0],fFuel_y_us[iii]), xycoords='data',fontsize=lf_sz+1,ha=ann_val[1],va='top',color=fFuelCol[iii],weight='bold',zorder=100)

    if "Historical" not in nScen[j]:
        if supplyIdx != -1:

            with open("atmospheric_co2_ppm.csv") as atm_co2_file: 
                ppm_reader = csv.reader(atm_co2_file)

                for ppm_row in ppm_reader:
                    if ppm_row[0] != nScen[j]+" 3C": continue
                    
                    for iYear in range(len(aYear)):
                        if aYear[iYear] > 1950 and aYear[iYear]%25 == 0:
                            ff_mkt_share = int(100*(aMkt[pidxC][j][iYear]+aMkt[pidxO][j][iYear]+aMkt[pidxG][j][iYear])/aMkt[supplyIdx][j][iYear])
                            annotate(str(ff_mkt_share)+"%",xy=(aYear[iYear],-150),xycoords='data',fontsize=lf_sz+2,va='center',ha='center',annotation_clip=False)
                            annotate(int(round(float(ppm_row[iYear+1]),0)),xy=(aYear[iYear],-275),xycoords='data',fontsize=lf_sz+2,va='center',ha='center',annotation_clip=False)

        annotate("Fossil Fuels\nMarket Share", xy=(1900,-140), xycoords='data', fontsize=lf_sz+2,va='center',ha='left',color='black',annotation_clip=False)
        annotate("Atmospheric\nCO$_2$ [ppm]", xy=(1900,-280), xycoords='data', fontsize=lf_sz+2,va='center',ha='left',color='black',annotation_clip=False)

        plt.ylim(0,1400)
        plt.ylabel("Primary Energy [EJ yr$^{-1}$]", fontsize=yl_sz)
        #plt.ylabel(nScen[j].replace("BioEnergy2","RE (High)").replace("BioEnergy1","RE (Medium)").replace("BioEnergy","RE (Low)")+" Scenario"+r' [EJ yr$^{-1}$]', fontsize=yl_sz)

        ax = plt.gca()
        legend_title_string = nScen[j].replace("BioEnergy3","RE-High").replace("BioEnergy2","RE-High").replace("BioEnergy1","RE-Med").replace("BioEnergy","RE-Low").replace("FossilBAU","Fossil Fuels")+"\nScenario"

        if "Hold this place for a scenario that does not want LO and HI shifts to be shown" not in nScen[j]:
            plt.xlim(1900,2150)
            xticks = ax.xaxis.get_major_ticks()
            xticks[-1].label1.set_visible(False)
            
            plt.plot([2110,2145],[-41,-41], 'k-', color='black',lw=1.0,clip_on=False)
            plt.plot([2145,2145],[-31,-51], 'k-', color='black',lw=1.0,clip_on=False)

            if nScen[j] == "BAU":
                yval_belo = fuel_stack_baulo
                yval_behi = fuel_stack_bauhi
            elif nScen[j] == "FossilBAU":
                yval_belo = fuel_stack_fbaulo
                yval_behi = fuel_stack_fbauhi
                annotate("Energy Demand Shift", xy=(2112.5,yval_behi+75),fontsize=lf_sz,
                         ha='center',va='bottom',color='black',weight='bold',zorder=100)
                annotate("Low", xy=(2112.5,yval_belo+25),fontsize=lf_sz,ha='center',va='bottom',color='black',zorder=100)
                annotate("High", xy=(2137.5,yval_behi+25),fontsize=lf_sz,ha='center',va='bottom',color='black',zorder=100)
            elif nScen[j] == "BioEnergy":
                yval_belo = fuel_stack_belo
                yval_behi = fuel_stack_behi
            elif nScen[j] == "BioEnergy1":
                yval_belo = fuel_stack_be1lo
                yval_behi = fuel_stack_be1hi
            elif nScen[j] == "BioEnergy2":
                yval_belo = fuel_stack_be2lo
                yval_behi = fuel_stack_be2hi
            elif nScen[j] == "BioEnergy3":
                yval_belo = fuel_stack_be3lo
                yval_behi = fuel_stack_be3hi
            else: 
                yval_belo = 1135
                yval_behi = 1135

            leg = ax.legend([],title=legend_title_string,loc='upper left')

        if "FossilBAU" in nScen[j]:
            #annotate("Nominal\n(2100)", xy=(2113,1150),fontsize=lf_sz,ha='center',va='bottom',color='black',zorder=100)
            #plt.xlim(1900,2125)

            handles, labels = ax.get_legend_handles_labels()

            handles = handles[::-1]
            handles = [handles.pop(-1)] + handles            

            labels = labels[::-1]
            labels = [labels.pop(-1)] + labels
                        
            leg = ax.legend(handles,labels,loc='best', ncol=1,fontsize=10,title=legend_title_string,borderpad=0.75,fancybox=True,frameon=True)

        leg.get_frame().set_alpha(0.9)

        plt.grid(True)
        sns.despine()
        #plt.figure().set_tight_layout(True)
        
        #print nScen[j]
        if nScen[j] == "FossilBAU": insert_panel_label(plt,"a",n_subp=1,equiv_yr=1875)
        elif nScen[j] == "BAU": insert_panel_label(plt,"b",n_subp=1,equiv_yr=1875)
        elif nScen[j] == "BioEnergy": insert_panel_label(plt,"c",n_subp=1,equiv_yr=1875)
        elif nScen[j] == "BioEnergy3": insert_panel_label(plt,"d",n_subp=1,equiv_yr=1875)

        plt.draw()
        plt.savefig('figures/energyprofile_'+nScen[j].replace(" ","_").replace("&","").replace("+","")+'.pdf',format='pdf')
        if show_energyprofile == True: plt.show()
        plt.clf()
        plt.close('all')
        print "Finished energyprofile_"+nScen[j]

#############################################
#Land Use/Yield plot
#############################################
# GLOBIOM Land Yield Projections
glo_yld = [ [  8.31,  8.56,  8.81 ], #2000
            [  9.59,  9.84,  9.99 ], #2010
            [ 10.97, 11.27, 11.47 ], #2020
            [ 11.83, 12.53, 12.86 ], #2030
            [ 12.48, 13.70, 14.23 ], #2040
            [ 13.05, 14.71, 15.43 ], #2050
            [ 13.60, 15.62, 16.51 ], #2060
            [ 14.16, 16.46, 17.48 ], #2070
            [ 14.68, 17.22, 18.36 ], #2080
            [ 15.19, 17.90, 19.20 ], #2090
            [ 15.69, 18.53, 20.00 ] ]#2100
#############################################

print "Starting LAND plots"

iRow = 0
iLand = -1
iScen = 0
nLands = 0
landTypes = []
nScen = []
aYear = []
aLandHyr = [[]]
aLand = [[[]]]

with open("tables/land_table.csv") as f: 
    reader = csv.reader(f)
    allRows = list(reader)
    nRows = len(allRows)

with open("tables/land_table.csv") as f: 
    reader = csv.reader(f)
    
    for row in reader:

##### TIME INFO
        if iRow == 0:
            for i in range(1,len(row)-1):
                aYear.append(int(float(row[i])))
                
##### SCENARIO INFO
        elif iRow == 1:
            for i in range(1,len(row)):
                if row[i] != "": 
                    nScen.append(row[i])
                    if   row[i] == "FossilBAU_agyld_lo": fsl_agyld_lo = len(nScen)-1
                    elif row[i] == "FossilBAU_agyld_hi": fsl_agyld_hi = len(nScen)-1
                    elif row[i] ==       "BAU_agyld_lo": bau_agyld_lo = len(nScen)-1
                    elif row[i] ==       "BAU_agyld_hi": bau_agyld_hi = len(nScen)-1                        
                
            nLands = (nRows-2)/len(nScen)
            if nLands%1 != 0: print "Error: Unexpected number of rows!"
                
            for n in range(nLands):
                aLand.append([])
                aLandHyr.append([])
                for m in range(len(nScen)):
                    aLand[n].append([])

##### SCENARIO DATA
        else:
            if (iRow-2)%len(nScen) == 0:
                landTypes.append(row[0])
                iLand = iLand+1
                iScen = 0
                
            for i in range(1,len(row)-1):
                if "--" not in row[i] and row[i] != "":
                    if "Historical" in row[0]: aLandHyr[iLand].append(aYear[i-1])
                    
                    if landTypes[-1] == "GLOBIOM Vegetal Food Yield": aLand[iLand][iScen].append(float(row[i])/1E6)
                    elif landTypes[-1] == "Vegetal Food Yield": aLand[iLand][iScen].append(float(row[i])/1E6*(2./3.))
                    else: aLand[iLand][iScen].append(float(row[i]))
            iScen = iScen+1
                
        iRow = iRow+1

for i in range(nLands):
    if (landTypes[i] != "GLOBIOM Vegetal Food Yield" 
        and landTypes[i] != "Vegetal Food Yield"): continue
    
    print "now running landuse_"+landTypes[i]

    plt.cla()
    for j in range(len(nScen)):

        if "CCS" in nScen[j] or "agyld" in nScen[j]: continue

        if "Historical" in nScen[j]:
            if len(aLand[i][j]) > 1:
                plt.plot(aLandHyr[i],aLand[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label="FAO Data")
        elif nScen[j] == "BAU":
            print " ",nScen[j]
            plt.plot(aYear,aLand[i][j],color=cop_color(nScen[j]),lw=get_linewidth(nScen[j]),label=nScen[j])
            scatter([aYear[-1],],[aLand[i][j][-1],],10,color=cop_color(nScen[j]),zorder=99.9)
    
    if landTypes[i] == "GLOBIOM Vegetal Food Yield" or landTypes[i] == "Vegetal Food Yield":

        plt.ylabel("Food Crop Yield [10$^{6}$ kCal ha$^{-1}$ yr$^{-1}$]", fontsize=yl_sz)
        plt.ylim(0,21)
        insert_panel_label(plt,"b",n_subp=1,equiv_yr=1940)

        ax = plt.gca()
        leg = ax.legend(loc='best',ncol=1,fontsize=9,borderpad=0.75,fancybox=True,frameon=True,framealpha=0.9)

        #plt.fill_between(aYear,aLand[i][fsl_agyld_lo],aLand[i][fsl_agyld_hi],facecolor=cop_color("FossilBAU"),alpha=err_alpha,zorder=2)
        plt.fill_between(aYear,aLand[i][bau_agyld_lo],aLand[i][bau_agyld_hi],facecolor=cop_color("BAU"),alpha=err_alpha,zorder=2)

        # GLOBIOM techno-economic ranges
        for ii_yr in xrange(11):
            ij_yr = 2000+ii_yr*10
            plt.plot([ij_yr,ij_yr],[glo_yld[ii_yr][0],glo_yld[ii_yr][2]],color='black',lw=1.5,zorder=1)
            plt.plot([ij_yr-.5,ij_yr+.5],[glo_yld[ii_yr][0],glo_yld[ii_yr][0]],color='black',lw=1.5,zorder=1)
            plt.plot([ij_yr-.5,ij_yr+.5],[glo_yld[ii_yr][2],glo_yld[ii_yr][2]],color='black',lw=1.5,zorder=1)

            if ij_yr == 2020:
                annotate("Independent econometric projection\nof input-neutral yield growth",
                         xy=(ij_yr,glo_yld[ii_yr][0]), xycoords='data',xytext=(25,-13), textcoords='offset points',size=6,
                         ha='left',va='bottom',
                         arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=-0.2"))
            if ij_yr == 2050:
                annotate("",
                         xy=(ij_yr,glo_yld[ii_yr][0]), xycoords='data',xytext=(5,-25), textcoords='offset points',size=6,
                         ha='left',va='bottom',
                         arrowprops=dict(arrowstyle="->",shrinkB=5,connectionstyle="arc3,rad=0.2"))

    # Controls for all plots
    plt.xlim(1950,2102)

    plt.grid(True)
    sns.despine()
    #plt.figure().set_tight_layout(True)
    plt.draw()
    plt.savefig('figures/land_'+landTypes[i].replace(" ","_").replace("&","").replace("+","")+'.pdf',format='pdf')
    plt.clf()
    plt.close('all')
    
