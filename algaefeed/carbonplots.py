# Set up environment & import pyplot packages
from pylab import *
import csv
import prettyplotlib as ppl
import matplotlib.patches as pts
from matplotlib import rc
from matplotlib import colors
from textwrap import wrap
rc('text', usetex=False)

# Set default parameters for drawn output (plots)
params = {'savefig.bbox': 'tight', #or 'standard'
          #'savefig.pad_inches': 0.1 
          'xtick.labelsize': 10,
          'ytick.labelsize': 10,
          'legend.fontsize': 16,
          'legend.linewidth': 2, 
          'legend.fancybox': True,
          'savefig.facecolor': 'white',   # figure facecolor when saving
          'savefig.edgecolor': 'white'    # figure edgecolor when saving
          }
plt.rcParams.update(params)

# These lines tell the compiler where to look for esm_plotting_tools.py, then load it
import sys
sys.path.insert(0, '/Users/brian/Desktop/Dropbox/python/my_libraries')

import esm_plotting_tools
reload(esm_plotting_tools)
from esm_plotting_tools import *

# The sns package controls aesthetics of output
sns.set()
sns.set_context("paper")
sns.set_style("whitegrid")
#sns.set_style("darkgrid", {"grid.linewidth": .5, "axes.facecolor": ".9"})

#############################################
# Conversion Factors
mtoe_to_ej = .041868 # much of Felix output is in megatons oil equivalent (mtoe)
#mtoe_to_ej = 1.00000

#############################################
# Formatting Controls
lf_sz = 9      # label font size:
dots = 15      # scatter/dot size:
txsz = 8       # tick label font size
title_sz = 16  # plot title size
xl_sz = 14     # x-axis label size
yl_sz = 14     # y-axis label size
hd_sz = 9      # source data label size
#
err_alpha = 0.40 # Transparency of primary error ranges
sec_alpha = 0.20 # Transparency of secondary error ranges
ep_alpha = 0.85  # Transparency of Energy Profile panels

#############################################
# "Show" Switches - set these to true to show the plots as they're being generated
show_temp          = False
show_production    = False
show_energyprofile = False
show_emissions     = False
show_land_cover    = False
show_emissions_II  = False
show_water         = False
#
label_HD = False

#############################################
#############################################
# RCP Info
# - these arrays have RCP info from the IIASA database (http://tntcat.iiasa.ac.at/RcpDb/)

labels_rcps = [["RCP 2.6","RCP 4.5","RCP 6.0","RCP 8.5"],
               ["RCP 2.6","RCP 4.5","RCP 6.0","RCP 8.5"],
               ["RCP 2.6","RCP 4.5","RCP 6.0","RCP 8.5"]]

rcp_time = [ 2000, 2005, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100 ]
rcp_hist_time = [ 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2005 ]
#
rcp_hist_ppm = [ 295.800, 299.700, 303.025, 307.225, 310.375, 310.750, 316.273, 324.985, 338.360, 353.855, 368.865, 378.813 ]
rcp_hist_em = [ 1.187, 1.641, 1.653, 1.949, 2.066, 2.522, 3.769, 5.273, 6.357, 7.463, 7.884, 9.167 ]
#
rcp_ppm_26 = [ 368.865, 378.813, 389.285, 412.068, 430.783, 440.222, 442.700, 441.673, 437.481, 431.617, 426.005, 420.895 ]
rcp_ppm_45 = [ 368.865, 378.813, 389.128, 411.129, 435.046, 460.845, 486.535, 508.871, 524.302, 531.138, 533.741, 538.358 ]
rcp_ppm_60 = [ 368.865, 378.813, 389.072, 409.360, 428.876, 450.698, 477.670, 510.634, 549.820, 594.257, 635.649, 669.723 ]
rcp_ppm_85 = [ 368.865, 378.813, 389.324, 415.780, 448.835, 489.435, 540.543, 603.520, 677.078, 758.182, 844.805, 935.874 ]
#
rcp_em_26 = [ 7.884, 9.167, 9.878, 10.260, 7.946, 5.024, 3.387, 2.035, 0.654, 0.117, -0.269, -0.420 ]
rcp_em_45 = [ 7.884, 9.167, 9.518, 10.212, 11.170, 11.537, 11.280, 9.585, 7.222, 4.190, 4.220, 4.249 ]
rcp_em_60 = [ 7.884, 9.167, 9.389, 9.357, 9.438, 10.840, 12.580, 14.566, 16.477, 17.525, 14.556, 13.935 ]
rcp_em_85 = [ 7.884, 9.167, 9.969, 12.444, 14.554, 17.432, 20.781, 24.097, 26.374, 27.715, 28.531, 28.817 ]
#
#rcp_temp_26 = [ 0.25, 1.00, 1.75 ]
#rcp_temp_45 = [ 1.10, 1.90, 2.60 ]
#rcp_temp_60 = [ 1.80, 2.40, 3.10 ]
#rcp_temp_85 = [ 2.55, 4.10, 4.80 ] 
rcp_temp_26 = [ 0.9, 1.6, 2.3 ]
rcp_temp_45 = [ 1.7, 2.4, 3.2 ]
rcp_temp_60 = [ 2.0, 2.8, 3.7 ]
rcp_temp_85 = [ 3.2, 4.3, 5.4 ] 

#############################################
# GLOBIOM Agricultural Yield Projections
# - these are from [Herrero et al. "African livestock futures", 2014]
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

# End of preamble - start plotting

#############################################
# Temperature relative to preindustrial

# Declare global variables
ct1 = 0
ct2 = 0
nScen_temp = []
aYear = []
aHyr1 = []
aHyr2 = []
aTemp_giss = [[]]
aTemp_had = [[]]

# open .csv file
# - if there's a problem, try changing the next line to "with open("table_new/temp_table.csv", 'rU') as f:"
with open("table_new/temp_table.csv") as f: 
    reader = csv.reader(f)
    for row in reader:
#we are now running through reader, line by line. would be good to make sure you know what the input files look like at this point.

##### TIME INFO
        if ct1 == 0:
            for i in range(1,len(row)-1):
                aYear.append(int(float(row[i])))

##### SCENARIO INFO
        elif ct1 == 1:
            for i in range(1,len(row)-1):
                if row[i] != "": nScen_temp.append(row[i])
        
            for n in range(len(nScen_temp)):
                aTemp_giss.append([])
                aTemp_had.append([])
    
##### 
        elif ct1 >= 2 and ct1 < 2+len(nScen_temp):
            for i in range(1,len(row)-1):
                if "--" not in row[i]:
                    if "Historical" in row[0]: aHyr1.append(aYear[i-1])
                    aTemp_giss[ct2].append(float(row[i]))
            ct2 = ct2+1

        elif ct1 >= 2+len(nScen_temp) and ct1 < 2+2*len(nScen_temp):
            if ct1 == 2+len(nScen_temp): ct2 = 0
            for i in range(1,len(row)-1):
                if "--" not in row[i]:
                    if "Historical" in row[0]: aHyr2.append(aYear[i-1]) 
                    aTemp_had[ct2].append(row[i])
            ct2 = ct2+1
#####
        ct1 = ct1+1

#################################
# Plot Temperature
        
ax = plt.gca()
allYval = []
tempY = 0
plt.cla()

standardize_scenario_names(nScen_temp)

for i in range(len(nScen_temp)):
    y_offset = -15

    if "Historical" in nScen_temp[i]:
        #nScen_temp[i] = "GISS Data"
        #plt.plot(aHyr1,aTemp_giss[i],color=pairs[0],linewidth=2,label=nScen_temp[i])
        nScen_temp[i] = "HadCRUT4 Data"
        plt.plot(aHyr2,aTemp_had[i],color=pairs[4],linewidth=2,label=nScen_temp[i])    
    elif scenario_switch(nScen_temp[i],"CCS",True) == False: continue
    #elif nScen_temp[i] != "BioEnergy" and nScen_temp[i] != "BAU" and nScen_temp[i] != "Alg-Feed" and "Alg-Feed CCS" not in nScen_temp[i]: continue 
    else:
        if "BAU" == nScen_temp[i]:
            plt.plot(aYear,aTemp_giss[i],color=get_color(nScen_temp[i]),linewidth=get_linewidth(nScen_temp[i]),label=nScen_temp[i],zorder=99)
        else: plt.plot(aYear,aTemp_giss[i],color=get_color(nScen_temp[i]),linewidth=get_linewidth(nScen_temp[i]),label=nScen_temp[i])
        scatter([2100,],[aTemp_giss[i][-1],],dots, color=get_color(nScen_temp[i]))

        if nScen_temp[i] == "BAU":
            plt.plot(plt.gca().get_xlim(),[0,0], 'k-', lw=0.75)
            scatter([2128,],[rcp_temp_26[1],],dots, color=get_color("2.6"))
            scatter([2132,],[rcp_temp_45[1],],dots, color=get_color("4.5"))
            scatter([2136,],[rcp_temp_60[1],],dots, color=get_color("6.0"))
            scatter([2140,],[rcp_temp_85[1],],dots, color=get_color("8.5"))
            
            annotate('RCP 2.6',xy=(2129, rcp_temp_26[1]), xycoords='data',xytext=(2,-3), textcoords='offset points', fontsize=8)
            annotate('RCP 4.5',xy=(2133, rcp_temp_45[1]), xycoords='data',xytext=(2,-3), textcoords='offset points', fontsize=8)
            annotate('RCP 6.0',xy=(2137, rcp_temp_60[1]), xycoords='data',xytext=(2,-3), textcoords='offset points', fontsize=8)
            
            plt.gca().add_patch(Rectangle((2127.75,rcp_temp_26[0]),0.5,(rcp_temp_26[2]-rcp_temp_26[0]), color = get_color("2.6")))
            plt.gca().add_patch(Rectangle((2131.75,rcp_temp_45[0]),0.5,(rcp_temp_45[2]-rcp_temp_45[0]), color = get_color("4.5")))
            plt.gca().add_patch(Rectangle((2135.75,rcp_temp_60[0]),0.5,(rcp_temp_60[2]-rcp_temp_60[0]), color = get_color("6.0")))
            plt.gca().add_patch(Rectangle((2139.75,rcp_temp_85[0]),0.5,(rcp_temp_85[2]-rcp_temp_85[0]), color = get_color("8.5")))
            
        #########################
        # Temperature error bars
        low_err = np.array([])
        high_err = np.array([])
        if nScen_temp[i] == "BAU":
            for nn in range(len(nScen_temp)):
                if nScen_temp[nn] == "BAU pop low": low_err = np.array(aTemp_giss[nn])
                elif nScen_temp[nn] == "BAU pop high": high_err = np.array(aTemp_giss[nn])
            plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_bau"),alpha=err_alpha)
        
        if nScen_temp[i] == "Alg-Feed CCS75":
            for nn in range(len(nScen_temp)):
                if nScen_temp[nn] == "AFC 15tph": low_err = np.array(aTemp_giss[nn])
                elif nScen_temp[nn] == "AFC 05tph": high_err = np.array(aTemp_giss[nn])
            plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_afc"),alpha=sec_alpha)
            for nn in range(len(nScen_temp)):
                if nScen_temp[nn] == "AFC pop low": low_err = np.array(aTemp_giss[nn])
                elif nScen_temp[nn] == "AFC pop high": high_err = np.array(aTemp_giss[nn])
            plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_afc"),alpha=err_alpha)

        if nScen_temp[i] == "BAU" or "Alg-Feed" in nScen_temp[i]:   
            tempY = get_y_offset(allYval,float(aTemp_giss[i][-1]),0.075)
            annotate(str(round(float(aTemp_giss[i][-1]),1))+r'$^{\circ}$C',xy=(2100, tempY), xycoords='data',
                     xytext=(3.5,0), textcoords='offset points', fontsize=lf_sz,weight='bold')
    
#plt.title('Temperature Change from Preindustrial', fontsize=title_sz)
plt.xlim(1900,2150)
if label_HD == True:
    annotate('Sources: Met Office Hadley Center', fontsize=hd_sz, xy=(2150, -0.55), xycoords='data', 
             ha='right',va='center', annotation_clip=False)

xticks = ax.xaxis.get_major_ticks()
xticks[-1].label1.set_visible(False)

plt.ylim(-0.25,3.5)
#plt.xlabel('Year',fontsize=xl_sz)
plt.ylabel(r'Temperature Anomaly [$^{\circ}$C]', fontsize=yl_sz)
leg = ax.legend(loc='upper left', ncol=2,fontsize=10)
leg.get_frame().set_alpha(0.5)
plt.grid(True)
#plt.figure().set_tight_layout(True)
sns.despine(bottom=True,trim=True)
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(6.4,4.4)
plt.draw()
plt.savefig('figures/temperature.pdf',format='pdf', dpi=1500)
plt.savefig('figures/temperature.png',format='png', dpi=1500)
if show_temp == True: plt.show()
plt.clf()
print "Finished: Temperature Change"

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

with open("table_new/production_table.csv") as f: 
    reader = csv.reader(f)
    allRows = list(reader)
    nRows = len(allRows)

with open("table_new/production_table.csv") as f: 
    reader = csv.reader(f)
    
    for row in reader:

##### TIME INFO
        if iRow == 0:
            for i in range(1,len(row)-1):
                aYear.append(int(float(row[i])))
                
##### SCENARIO INFO
        elif iRow == 1:
            for i in range(1,len(row)-1):
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
                    else:
                        aMkt[iFuel][iScen].append(float(row[i])*mtoe_to_ej)
            iScen = iScen+1
                
        iRow = iRow+1

#################################
# Plot Market Share (by Fuel Type)
standardize_scenario_names(nScen)

idxB = -1
idxO = -1
idxC = -1
idxG = -1

pidxB = -1
pidxO = -1
pidxC = -1
pidxG = -1

for ii in range(nFuels):
    if "Market Share" in fuelTypes[ii]:
        if "Biomass" in fuelTypes[ii]: idxB = ii
        elif "Oil" in fuelTypes[ii]:   idxO = ii
        elif "Coal" in fuelTypes[ii]:  idxC = ii
        elif "Gas" in fuelTypes[ii]:   idxG = ii
    elif "Production" in fuelTypes[ii]:
        if "Biomass" in fuelTypes[ii]: pidxB = ii
        elif "Oil" in fuelTypes[ii]:   pidxO = ii
        elif "Coal" in fuelTypes[ii]:  pidxC = ii
        elif "Gas" in fuelTypes[ii]:   pidxG = ii
        

idxBAU = -1
idxHIS = -1

for jj in range(len(nScen)):
    if "BAU" == nScen[jj]: idxBAU = jj
    elif "Historical" in nScen[jj]: idxHIS = jj

for i in range(nFuels):
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
                plt.plot(aHyr[idxC],aMkt[idxC][idxHIS],color=get_color("labCoal"),linewidth=get_linewidth("HistoricalData"),label="Coal (IEA)")
                plt.plot(aHyr[idxG],aMkt[idxG][idxHIS],color=get_color("labGas"),linewidth=get_linewidth("HistoricalData"),label="Gas (IEA)")
                plt.plot(aHyr[idxO],aMkt[idxO][idxHIS],color=get_color("labOil"),linewidth=get_linewidth("HistoricalData"),label="Oil (IEA)")
                plt.ylabel("Share of Primary Energy:\nFossil Fuels [%]", fontsize=yl_sz)
                if label_HD == True:
                    annotate('Source: IEA - Key World Energy Statistics 2013', fontsize=hd_sz, xy=(2100, -8), xycoords='data', 
                             ha='right',va='center', annotation_clip=False)
                

        elif "Historical" in nScen[j] and len(aMkt[i]) > 1:
            plt.plot(aHyr[i],aMkt[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label="IEA Data")
        else:
            plt.plot(aYear,aMkt[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
    
    plt.xlim(1900,2100)
    plt.ylim(0,60)
    #plt.xlabel('Year',fontsize=xl_sz)
    if "Market Share" not in fuelTypes[i]: 
        plt.ylabel(fuelTypes[i]+" [EJ/yr]", fontsize=yl_sz)

    ax = plt.gca()
    leg = ax.legend(loc='best', ncol=2,fontsize=10)
    leg.get_frame().set_alpha(0.5)
    plt.grid(True)
    sns.despine()
    #plt.figure().set_tight_layout(True)
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(6.4,4.4)
    plt.draw()
    plt.savefig('figures/production_'+fuelTypes[i].replace(" ","_").replace("&","").replace("+","").replace("_Energy_Production","").replace("_Production","")+'.pdf',format='pdf', dpi=1500)
    if show_production == True: plt.show()
    plt.clf()
print "Finished: Market share by fuel type"

#################################
# Plot Market Share (by Scenario)
standardize_scenario_names(nScen)

for j in range(len(nScen)):
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
                plt.plot(aYear,aMkt[k][j],color='black',linewidth=1,linestyle="--",label=fuelTypes[k], zorder = 100)  
                ftFuel = str(int(round(aMkt[k][j][-1],0)))+' EJ'
                #annotate(str(ftFuel), xy=(2110,aMkt[k][j][-1]+10), xycoords='data',fontsize=lf_sz,ha='center',color='black')
                if "Alg" in nScen[j] and label_HD == True:
                    annotate('Source: IEA - Key World Energy Statistics 2013', fontsize=hd_sz, xy=(2120, -100), xycoords='data', 
                             ha='right',va='center', annotation_clip=False)

            elif "Energy Production" == fuelTypes[k]:
                supplyIdx = k
    
    for jj in range(len(nScen)):
        for ii in range(nFuels):
            if "Historical" in nScen[jj] and "Energy Demand" == fuelTypes[ii]:
                plt.plot(aHyr[ii],aMkt[ii][jj],color=get_color(nScen[jj]),linewidth=get_linewidth(nScen[jj]),linestyle="-",label="IEA Data",marker="x",zorder = 101)

    for i in range(nFuels):

        if "Historical" in nScen[j] and "Energy Demand" != fuelTypes[i]: continue
        elif "Energy Demand" == fuelTypes[i] and "Historical" not in nScen[j]: continue
        elif "Production" not in fuelTypes[i] or "Energy Production" == fuelTypes[i]: continue
        else:  

            fuel_label_string = str(int(round(aMkt[i][j][-1],0)))+' EJ'
            if fuel_label_string != "0 EJ" or "Oil" in fuelTypes[i]:

            #Stack Hack
                if i != 0:
                    tempMkt = tempMkt + np.array(aMkt[i][j])
                plt.plot(aYear,tempMkt,color=get_color(fuelTypes[i]),linewidth=get_linewidth(fuelTypes[i]),
                         label=fuelTypes[i].replace(" Production","").replace("Energy","").replace(" Land","").replace("Biomass","Agro-Biomass").replace("Nuclear","Nuclear & Hydro."))
                plt.fill_between(aYear,tempMkt-np.array(aMkt[i][j]),tempMkt,facecolor=get_color(fuelTypes[i]),alpha=ep_alpha)
            #scatter([2100,],[tempMkt[-1],],dots, color=get_color(fuelTypes[i]))

            # Annotate: market share (% of supply)
            #fFuel.append(int(round(100 * aMkt[i][j][-1] / aMkt[supplyIdx][j][-1],0)))
            # Annotate: total supply by fuel type in EJ

                fFuel.append(fuel_label_string)
                fFuelCol.append(get_color("lab"+fuelTypes[i]))
                fFuel_y_us.append(tempMkt[-1])
    
    #Sort and then Annotate
    new_y_offset(fFuel_y_us,60,0)
    for iii in range(len(fFuel_y_us)):
        annotate(str(fFuel[iii]), xy=(2112.5,fFuel_y_us[iii]), xycoords='data',fontsize=lf_sz+2,ha='center',va='center',color=fFuelCol[iii],weight='bold')

    if "Historical" not in nScen[j] and demandIdx != -1 and supplyIdx != -1:
        annotate("Fossil Fuels", xy=(1900,-80), xycoords='data', fontsize=lf_sz+2,va='center',ha='left',color='black',annotation_clip=False)
        annotate("Market Share", xy=(1900,-120), xycoords='data', fontsize=lf_sz+2,va='center',ha='left',color='black',annotation_clip=False)
        for iYear in range(len(aYear)):
            if aYear[iYear] > 1950 and aYear[iYear]%25 == 0:
                ff_mkt_share = int(100*(aMkt[pidxC][j][iYear]+aMkt[pidxO][j][iYear]+aMkt[pidxG][j][iYear])/aMkt[supplyIdx][j][iYear])
                annotate(str(ff_mkt_share)+"%", xy=(aYear[iYear],-100), xycoords='data', fontsize=lf_sz+3,va='center',ha='center', color='black',annotation_clip=False)

    if "Historical" not in nScen[j]:
        #if "BAU" in nScen[j] or "BioEnergy" in nScen[j]: 
            #plt.suptitle("Primary Energy Production",fontsize=title_sz)
            #plt.title("Primary Energy Production",fontsize=title_sz)
        #else: plt.title(nScen[j], fontsize=title_sz)
        plt.xlim(1900,2120)
        plt.ylim(0,1000)
        #plt.xlabel('Year',fontsize=xl_sz)
        plt.ylabel(nScen[j]+" Primary Energy "+r'[EJ y$^{-1}$]', fontsize=yl_sz+1)
        ax = plt.gca()

        plt.grid(True)
        sns.despine()
        #plt.figure().set_tight_layout(True)
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(6.4,4.4)
        if nScen[j] == "BAU":
            leg = ax.legend(loc='best', ncol=2,fontsize=10)
            if leg: leg.get_frame().set_alpha(0.5)
            annotate("A",xy=(0.04,0.95),xycoords='figure fraction',color='black',fontsize=15,ha='center',va='center',rotation=0,zorder=99,weight='bold',clip_on=False)
        elif nScen[j] == "BioEnergy":
            annotate("B",xy=(0.04,0.95),xycoords='figure fraction',color='black',fontsize=15,ha='center',va='center',rotation=0,zorder=99,weight='bold',clip_on=False)
        elif nScen[j] == "Alg-Fuel":
            annotate("C",xy=(0.04,0.95),xycoords='figure fraction',color='black',fontsize=15,ha='center',va='center',rotation=0,zorder=99,weight='bold',clip_on=False)
        elif nScen[j] == "Alg-Feed":
            annotate("D",xy=(0.04,0.95),xycoords='figure fraction',color='black',fontsize=15,ha='center',va='center',rotation=0,zorder=99,weight='bold',clip_on=False)
        plt.draw()
        plt.savefig('figures/energyprofile_'+nScen[j].replace(" ","_").replace("&","").replace("+","")+'.pdf',format='pdf', dpi=1500)
        if show_energyprofile == True: plt.show()
        plt.clf()

print "Finished: Energy Profiles"
#############################################
#############################################
# Emissions
#
iRow = 0
marker = 1000
iScen = 0
nScen = []
aYear = []
aHyr = []
anEM = [[]]
anAF = [[]]
anAG = [[]]
netEM = [[]]

scenEM = False
scenAF = False
scenAG = False
scenNEM = False

with open("table_new/emissions_table_1.csv") as f: 
    reader = csv.reader(f)
    allRows = list(reader)
    nRows = len(allRows)

with open("table_new/emissions_table_1.csv") as f: 
    reader = csv.reader(f)
    
    for row in reader:

###### TIME INFO
        if iRow == 0:
            for i in range(1,len(row)-1):
                aYear.append(int(float(row[i])))
            
##### SCENARIO INFO
        elif iRow == 1:
            for i in range(1,len(row)-1):
                if row[i] != "": nScen.append(row[i])
                
            for n in range(len(nScen)):
                anEM.append([])
                anAF.append([])
                anAG.append([])
                netEM.append([])

###### SCENARIO DATA
        if row[0] == "Net Emissions":
            scenNEM = True
            scenEM = False
            scenAF = False
            scenAG = False
            marker = iRow
            iScen = 0

        if row[0] == "Total C Emission":
            scenNEM = False
            scenEM = True
            scenAF = False
            scenAG = False
            marker = iRow
            iScen = 0

        if scenEM == True and iRow >= marker and iRow < marker+len(nScen):
            for i in range(1,len(row)-1):
                if "--" not in row[i] and row[i] != "":
                    if "Historical" in row[0]: aHyr.append(aYear[i-1])
                    anEM[iScen].append(float(row[i])/1000000000)
            iScen = iScen+1

        if row[0] == "Afforestation":
            scenNEM = False
            scenEM = False
            scenAF = True
            scenAG = False
            marker = iRow
            iScen = 0
        
        if scenAF == True and iRow >= marker and iRow < marker+len(nScen):
            for i in range(1,len(row)-1):
                if "--" not in row[i] and row[i] != "":
                    if "Historical" in row[0]: aHyr.append(aYear[i-1])
                    anAF[iScen].append(-1*float(row[i])/1000000000)
            iScen = iScen+1

        if row[0] == "Algae C Abatement":
            scenNEM = False
            scenEM = False
            scenAF = False
            scenAG = True
            marker = iRow
            iScen = 0

        if scenNEM == True and iRow >= marker and iRow < marker+len(nScen):
            for i in range(1,len(row)-1):
                if "--" not in row[i] and row[i] != "":
                    netEM[iScen].append(float(row[i])/1E009)
            iScen = iScen+1
        
        if scenAG == True and iRow >= marker and iRow < marker+len(nScen):
            for i in range(1,len(row)-1):
                if "--" not in row[i] and row[i] != "":
                    if "Historical" in row[0]: aHyr.append(aYear[i-1])
                    anAG[iScen].append(-1*float(row[i])/1E009)
            iScen = iScen+1
                         
        iRow = iRow+1

#################################
# Plot Emissions
#
standardize_scenario_names(nScen)

allYval1 = []
allYval2 = []
allYval3 = []

plt.cla()
for i in range(len(nScen)):

    if "Historical" in nScen[i]: continue

    # Negative emissions includes Algae here:
    gross_AF_AG = np.array(anAF[i]) + np.array(anAG[i])

    if scenario_switch(nScen[i],"CCS") == False: continue
    
    if "Historical" in nScen[i]:
        if len(aHyr) > 1:
            plt.plot(aHyr,anEM[i],color=get_color(nScen[i]),linewidth=get_linewidth(nScen[i]),label=nScen[i])
        else: continue
    else: 
        plt.plot(aYear,anEM[i],color=get_color(nScen[i]),linewidth=get_linewidth(nScen[i]),label=nScen[i])
        plt.plot(aYear,gross_AF_AG,color=get_color(nScen[i]),linewidth=get_linewidth(nScen[i]))
        plt.plot(plt.gca().get_xlim(),[0,0], 'k-', lw=0.5)

        tempY1 = get_y_offset(allYval1,float(anEM[i][-1]),(plt.gca().get_ylim()[1]-plt.gca().get_ylim()[0])/35)
        tempY2 = get_y_offset(allYval2,float(gross_AF_AG[-1]),(plt.gca().get_ylim()[1]-plt.gca().get_ylim()[0])/35)
        #tempY3 = get_y_offset(allYval3,float(anAG[i][-1]),(plt.gca().get_ylim()[1]-plt.gca().get_ylim()[0])/35)
        
        scatter([2100,],[anEM[i][-1],],dots, color=get_color(nScen[i]))
        scatter([2100,],[gross_AF_AG[-1],],dots, color=get_color(nScen[i]))
        #scatter([2100,],[anAG[i][-1],],dots, color=get_color(nScen[i]))

        annotate(str(round(float(anEM[i][-1]),1))+r' PgC y$^{-1}$',
                 xy=(2100, tempY1), xycoords='data',ha='center',va='center',
                 xytext=(3,0), textcoords='offset points', fontsize=lf_sz)
        annotate(str(round(float(gross_AF_AG[-1]),1))+r' PgC y$^{-1}$',
                 xy=(2100, tempY2), xycoords='data',ha='center',va='center',
                 xytext=(3,0), textcoords='offset points', fontsize=lf_sz)

annotate("Energy Consumption:", xy=(1975,11), xycoords='data',ha='center')
annotate("Carbon Emissions", xy=(1975,9), xycoords='data',ha='center')
annotate("Energy Production:", xy=(1975,-9), xycoords='data',ha='center')
annotate("Carbon Uptake", xy=(1975,-11), xycoords='data',ha='center')
plt.title('Gross Emissions', fontsize=title_sz)
#plt.xlabel('Year',fontsize=xl_sz)
plt.ylabel("PgC y"+r'$^{-1}$', fontsize=yl_sz)

ax = plt.gca()
leg = ax.legend(loc='best', ncol=2)
leg.get_frame().set_alpha(0.5)
plt.xlim(1950,2125)
plt.ylim(-25,25)

plt.grid(True)
#plt.figure().set_tight_layout(True)
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(6.4,4.4)
plt.draw()
plt.savefig('figures/gross_emissions.pdf',bbox_inches='tight',format='pdf', dpi=1500)
if show_emissions == True: plt.show()
plt.clf()

#####
plt.cla()
allYval = []
tempY = 0

for i in range(len(nScen)):
    
    if "Historical" in nScen[i]: continue
    if scenario_switch(nScen[i],"CCS") == False: continue
    elif "CCS" in nScen[i]: continue
    else: 
        if "Feed" in nScen[i]: gross_AF_AG = np.array(anAF[i])
        else: gross_AF_AG = np.array(anAF[i]) + np.array(anAG[i])

        if "BAU" == nScen[i]:
            plt.plot(aYear,gross_AF_AG,color=get_color(nScen[i]),linewidth=get_linewidth(nScen[i]),label=nScen[i],zorder=99)
        else: plt.plot(aYear,gross_AF_AG,color=get_color(nScen[i]),linewidth=get_linewidth(nScen[i]),label=nScen[i])
       
for i in range(len(nScen)):

    if "Historical" in nScen[i]: continue
    elif scenario_switch(nScen[i],"CCS") == False: continue
    elif "CCS" in nScen[i]: continue
    else:
        if "Feed" in nScen[i]: gross_AF_AG = np.array(anAF[i]) # hack because C stored in algae-feed returns immediately to atmosphere. (in model, via "Leeching") 
        else: gross_AF_AG = np.array(anAF[i]) + np.array(anAG[i])

        scatter([2100,],[gross_AF_AG[-1],],dots, color=get_color(nScen[i]))

        tempY = get_y_offset(allYval,float(gross_AF_AG[-1]),(plt.gca().get_ylim()[1]-plt.gca().get_ylim()[0])/40)
        annotate(str(round(float(gross_AF_AG[-1]),1))+r' PgC y$^{-1}$',
                 xy=(2116, tempY), xycoords='data',ha='center',va='center',xytext=(0,0), textcoords='offset points', fontsize=lf_sz,weight='bold')
       
#plt.title('C Sink: Biomass Increment', fontsize=title_sz)
sns.despine(top=False,bottom=True)
#plt.xlabel('Year',fontsize=xl_sz)
plt.ylabel("Gross C Sequestration:\nBiofuels [PgC y"+r'$^{-1}$]', fontsize=yl_sz,labelpad=0.9)

#ax = plt.gca()
#leg = ax.legend(loc='best',ncol=1,fontsize=10)
#leg.get_frame().set_alpha(0.5)
plt.xlim(1950,2125)
plt.ylim(-20,0)

plt.grid(True)
#plt.figure().set_tight_layout(True)
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(6.4,4.4)
plt.draw()
plt.savefig('figures/afforestation.pdf',format='pdf', dpi=1500)
if show_emissions == True: plt.show()
plt.clf()

#####
plt.cla()
allYval = []
tempY = 0

for i in range(len(nScen)):

    if "Historical" in nScen[i]: continue
    elif scenario_switch(nScen[i],"CCS") == False: continue
    #elif nScen[i] != "BioEnergy" and nScen[i] != "BAU" and nScen[i] != "Alg-Feed" and "Alg-Feed CCS" not in nScen[i]: continue 
    else:         
        #tempEM = np.array(anEM[i]) + np.array(anAF[i]) - np.array(anAG[i])
        tempEM = np.array(netEM[i])
        if "BAU" in nScen[i]:
            plt.plot(aYear,tempEM,color=get_color(nScen[i]),linewidth=get_linewidth(nScen[i]),label=nScen[i],zorder=99)
        else: plt.plot(aYear,tempEM,color=get_color(nScen[i]),linewidth=2,label=nScen[i])
        plt.plot(plt.gca().get_xlim(),[0,0], 'k-', lw=0.5)

        scatter([2100,],[tempEM[-1],],dots, color=get_color(nScen[i]))

        if "Feed" in nScen[i] or "BAU" in nScen[i]:
            tempY = get_y_offset(allYval,float(tempEM[-1]),plt.gca().get_ylim()[1]/10)
            annotate(str(round(float(tempEM[-1]),1))+r' PgC y$^{-1}$',
                     xy=(2102, tempY), xycoords='data',fontsize=lf_sz+1,ha='left',va='center',weight='bold')

        ############################
        # Net Emissions error bars
        low_err = np.array([])
        high_err = np.array([])
        if nScen[i] == "BAU":
            for nn in range(len(nScen)):
                if nScen[nn] == "BAU pop low": low_err = np.array(netEM[nn])
                elif nScen[nn] == "BAU pop high": high_err = np.array(netEM[nn])
            plt.fill_between(aYear,low_err,high_err,facecolor=get_color("BAU"),alpha=err_alpha)
        
        if nScen[i] == "Alg-Feed CCS75":
            for nn in range(len(nScen)):
                if nScen[nn] == "AFC 15tph": low_err = np.array(netEM[nn])
                elif nScen[nn] == "AFC 05tph": high_err = np.array(netEM[nn])
            plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_afc"),alpha=sec_alpha)
            for nn in range(len(nScen)):
                if nScen[nn] == "AFC pop low": low_err = np.array(netEM[nn])
                elif nScen[nn] == "AFC pop high": high_err = np.array(netEM[nn])
            plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_afc"),alpha=err_alpha)
        
plt.plot(rcp_hist_time, rcp_hist_em,color=get_color('HistoricalData'),linewidth=get_linewidth("HistoricalData"),label='CDIAC Data',marker="x",zorder=100)
plt.plot(rcp_time,rcp_em_26,color=get_color('2.6'),linestyle="--",linewidth=2,label='RCP 2.6',zorder=0)
plt.plot(rcp_time,rcp_em_45,color=get_color('4.5'),linestyle="--",linewidth=2,label='RCP 4.5',zorder=0)
plt.plot(rcp_time,rcp_em_60,color=get_color('6.0'),linestyle="--",linewidth=2,label='RCP 6.0',zorder=0)
plt.plot(rcp_time,rcp_em_85,color=get_color('8.5'),linestyle="--",linewidth=2,label='RCP 8.5',zorder=0)
scatter([2100,],[rcp_em_26[-1],],dots, color=get_color("2.6"),zorder=0)
scatter([2100,],[rcp_em_45[-1],],dots, color=get_color("4.5"),zorder=0)
scatter([2100,],[rcp_em_60[-1],],dots, color=get_color("6.0"),zorder=0)
scatter([2100,],[rcp_em_85[-1],],dots, color=get_color("8.5"),zorder=0)

if label_HD == True:
    annotate('Source: Carbon Dioxide Information Analysis Center', fontsize=hd_sz, xy=(2115, -14), xycoords='data', 
             ha='right',va='center', annotation_clip=False)

#plt.title('Net Emissions', fontsize=title_sz)
#plt.xlabel('Year',fontsize=xl_sz)
plt.ylabel("Net Emissions [PgC y"+r'$^{-1}$]', fontsize=yl_sz)
#plt.ylabel(r'$\mathrm{10}^{\mathrm{9}}\times$'+" tonC/y", fontsize=20)

ax = plt.gca()
leg = ax.legend(loc='best', ncol=2,fontsize=9)
leg.get_frame().set_alpha(0.5)
plt.xlim(1950,2115)
plt.ylim(-10,30)
sns.despine(bottom=True)
plt.grid(True)
#plt.figure().set_tight_layout(True)
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(6.4,4.4)
plt.draw()
plt.savefig('figures/net_carbon.pdf',format='pdf', dpi=1500)
if show_emissions == True: plt.show()
plt.clf()

print "Finished: Emissions"
#############################################
#############################################
# Land Cover Data (Background info)
#

iRow = 0
iScen = 0
nScen = []
aYear = []
aHyr = [[]]
nLUD = 0
LUDtypes = []
aLUD = [[[]]]

with open("table_new/land_cover_table.csv") as f: 
    reader = csv.reader(f)
    allRows = list(reader)
    nRows = len(allRows)

with open("table_new/land_cover_table.csv") as f: 
    reader = csv.reader(f)
    
    for row in reader:

##### TIME INFO
        if iRow == 0:
            for i in range(1,len(row)-1):
                aYear.append(int(float(row[i])))
                
##### SCENARIO INFO
        elif iRow == 1:
            for i in range(1,len(row)-1):
                if row[i] != "": nScen.append(row[i])
                
            nLUD  = (nRows-2)/len(nScen)
            if nLUD%1 != 0: print "Error: Unexpected number of rows!"
                
            for n in range(nLUD):
                aLUD.append([])
                aHyr.append([])
                for m in range(len(nScen)):
                    aLUD[n].append([])
##### SCENARIO DATA
        else:
            if (iRow-2)%len(nScen) == 0:
                LUDtypes.append(row[0])
                iScen = 0
                
            for i in range(1,len(row)-1):
                if "--" not in row[i] and row[i] != "":
                    if "Historical" in row[0]: aHyr[len(LUDtypes)-1].append(aYear[i-1])
                    
                    if LUDtypes[-1] == "Food Crop Land Residual Production"       : aLUD[len(LUDtypes)-1][iScen].append(float(row[i])/1e009) 
                    elif LUDtypes[-1] == "GLOBIOM Vegetal Food Yield"             : aLUD[len(LUDtypes)-1][iScen].append(float(row[i])/1e006)#
                    elif LUDtypes[-1] == "Actual Forest Land Harvested"           : aLUD[len(LUDtypes)-1][iScen].append(float(row[i])/1e009)
                    elif LUDtypes[-1] == "Forest Biomass Production"              : aLUD[len(LUDtypes)-1][iScen].append(float(row[i])/1e009)
                    elif LUDtypes[-1] == "Energy Crops Production"                : aLUD[len(LUDtypes)-1][iScen].append(float(row[i])/1e009)
                    elif LUDtypes[-1] == "Land for Vegetal Food"                  : aLUD[len(LUDtypes)-1][iScen].append(float(row[i])/1e006)#
                    elif LUDtypes[-1] == "Land for Animal Food"                   : aLUD[len(LUDtypes)-1][iScen].append(float(row[i])/1e009)#
                    elif LUDtypes[-1] == "Population"                             : aLUD[len(LUDtypes)-1][iScen].append(float(row[i])/1e009)
                    elif LUDtypes[-1] == "FAO Agricultural area ha"               : aLUD[len(LUDtypes)-1][iScen].append(float(row[i])/1e009)
                    elif LUDtypes[-1] == "FAO Forest area ha"                     : aLUD[len(LUDtypes)-1][iScen].append(float(row[i])/1e009)
                    elif LUDtypes[-1] == "FAO Other land ha"                      : aLUD[len(LUDtypes)-1][iScen].append(float(row[i])/1e009)
                    elif LUDtypes[-1] == "FAO Permanent meadows and pastures ha"  : aLUD[len(LUDtypes)-1][iScen].append(float(row[i])/1e009)
                    elif LUDtypes[-1] == "FAO Arable land and permanent crops ha" : aLUD[len(LUDtypes)-1][iScen].append(float(row[i])/1e009)
                    elif LUDtypes[-1] == "FAO Permanent crops ha"                 : aLUD[len(LUDtypes)-1][iScen].append(float(row[i])/1e009)
                    else: aLUD[len(LUDtypes)-1][iScen].append(float(row[i]))
    
            iScen = iScen+1
                
        iRow = iRow+1

#################################
# Plot Land Cover Data
standardize_scenario_names(nScen)

copp_idx = -1
tree_idx = -1
agro_idx = -1
othr_idx = -1
#
FRbm_idx = -1
ECbm_idx = -1
CRbm_idx = -1
#
VF_idx = -1
AF_idx = -1
PC_idx = -1
#
pop_idx = -1
vfs_idx = -1
dmd_idx = -1
#
bau_idx = -1
beplus_idx = -1
algfd_idx = -1
algfu_idx = -1

for i in range(nLUD):
    if "Forest Biomass Production"             == LUDtypes[i]: FRbm_idx = i
    elif "Energy Crops Production"             == LUDtypes[i]: ECbm_idx = i
    elif "Food Crop Land Residual Production"  == LUDtypes[i]: CRbm_idx = i
    elif "Population"                          == LUDtypes[i]: pop_idx = i
    elif "FAO Forest area ha"                  == LUDtypes[i]: tree_idx = i
    elif "Actual Forest Land Harvested"        == LUDtypes[i]: copp_idx = i
    elif "FAO Agricultural area ha"            == LUDtypes[i]: agro_idx = i
    elif "FAO Other land ha"                   == LUDtypes[i]: othr_idx = i
    elif "Ratio of Crops Land Needed to Available" == LUDtypes[i]: vfs_idx = i
    elif "SCEN Demand Vegetal Calor Consum per Capita per Day" == LUDtypes[i]: dmd_idx = i
    ##elif "Vegetal Food supply kcal capita day"     == LUDtypes[i]: vfs_idx = i
    #elif "Land for Vegetal Food"               == LUDtypes[i]: VF_idx = i
    #elif "Land for Animal Food"                == LUDtypes[i]: AF_idx = i
    elif "FAO Arable land and permanent crops ha" == LUDtypes[i]: VF_idx = i
    elif "FAO Permanent crops ha"                 == LUDtypes[i]: PC_idx = i
    elif "FAO Permanent meadows and pastures ha"  == LUDtypes[i]: AF_idx = i
    
#################################
# Setup POPULATION histogram
population_time_data = []
population_data = []
vf_ratio = []
dmd_pcap = []
vfcol_data = []
#
for i in range(nLUD):
    for j in range(len(nScen)):
        if LUDtypes[i] == "Population" and nScen[j] == "BAU":
            for datai in range(len(aYear)):
                if aYear[datai] %10 == 0:
                    population_time_data.append(aYear[datai]-2.5)
                    population_data.append(aLUD[i][j][datai])
                    if vfs_idx != -1:
                        vf_ratio.append(aLUD[vfs_idx][j][datai])
                        vfcol_data.append(get_population_coloring(aLUD[vfs_idx][j][datai]))
                    if dmd_idx != -1:
                        dmd_pcap.append(aLUD[dmd_idx][j][datai])

for i in range(nLUD):
    plt.cla()
    allYval = []
    secYval = []
    thrYval = []
    forYval = []
    tempY = 0

    for j in range(len(nScen)):
        if nScen[j] == "BAU": bau_idx = j
        elif nScen[j] == "BioEnergy": beplus_idx = j
        elif nScen[j] == "Alg-Feed": algfd_idx = j
        elif nScen[j] == "Alg-Fuel": algfu_idx = j

        if "Historical" in nScen[j] and i != tree_idx and AF_idx != i and "GLOBIOM Vegetal Food Yield" != LUDtypes[i]:
            if len(aLUD[i][j]) > 1:
                plt.plot(aHyr[i],aLUD[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
            else: continue
        elif scenario_switch(nScen[j],LUDtypes[i]) == False: continue
        
        if tree_idx == i:
            plt.subplot(311)
            if "Historical" in nScen[j]:
                plt.plot(aHyr[agro_idx],aLUD[agro_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j],marker="x",zorder=100)
            else: 
                if "BAU" == nScen[j]:
                    plt.plot(aYear,aLUD[agro_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j],zorder=99)
                else: plt.plot(aYear,aLUD[agro_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
                ##############################
                # Global Land Use Error Bars
                if nScen[j] == "BAU":
                    for nn in range(len(nScen)):
                        if nScen[nn] == "BAU pop low": low_err = np.array(aLUD[agro_idx][nn])
                        elif nScen[nn] == "BAU pop high": high_err = np.array(aLUD[agro_idx][nn])
                    plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_bau"),alpha=err_alpha)
                        
                if nScen[j] == "Alg-Feed":
                    for nn in range(len(nScen)):
                        if nScen[nn] == "AF pop low": low_err = np.array(aLUD[agro_idx][nn])
                        elif nScen[nn] == "AF pop high": high_err = np.array(aLUD[agro_idx][nn])
                    plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_af1"),alpha=err_alpha)       

                scatter([2100,],[aLUD[agro_idx][j][-1],],dots, color=get_color(nScen[j]))
                if "BAU" in nScen[j] or "Feed" in nScen[j]:
                    tempY = get_y_offset(allYval,aLUD[agro_idx][j][-1],plt.gca().get_ylim()[1]/40)
                    annotate(str(round(float(aLUD[agro_idx][j][-1]),1))+" Bha",
                             xy=(2112.5, tempY), xycoords='data',ha='center',va='center',
                             xytext=(0,0), textcoords='offset points', fontsize=lf_sz,weight='bold')
            #plt.title("Global Land Use", fontsize=title_sz)
            plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.2)
            plt.ylabel("Agricultural\nLand [Bha]", fontsize=yl_sz-1)
            plt.xlim(1950,2125)
            plt.ylim(3.5,6.0)
            plt.grid(True)
            ax = plt.gca()
            ax.get_xaxis().set_ticklabels([])
            
            plt.subplot(312)
            if "Historical" in nScen[j]:
                plt.plot(aHyr[tree_idx],aLUD[tree_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label="FAOSTAT",marker="x",zorder=100)
            else:
                if nScen[j] == "BAU":
                    plt.plot(aYear,aLUD[tree_idx][j],color=get_color(nScen[j]),label=nScen[j],linewidth=get_linewidth(nScen[j]),zorder=99)
                else: plt.plot(aYear,aLUD[tree_idx][j],color=get_color(nScen[j]),label=nScen[j],linewidth=get_linewidth(nScen[j]))

                ##############################
                # Global Land Use Error Bars
                if nScen[j] == "BAU":
                    for nn in range(len(nScen)):
                        if nScen[nn] == "BAU pop low": low_err = np.array(aLUD[tree_idx][nn])
                        elif nScen[nn] == "BAU pop high": high_err = np.array(aLUD[tree_idx][nn])
                    plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_bau"),alpha=err_alpha)
                        
                if nScen[j] == "Alg-Feed":
                    for nn in range(len(nScen)):
                        if nScen[nn] == "AF pop low": low_err = np.array(aLUD[tree_idx][nn])
                        elif nScen[nn] == "AF pop high": high_err = np.array(aLUD[tree_idx][nn])
                    plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_af1"),alpha=err_alpha)   

                scatter([2100,],[aLUD[tree_idx][j][-1],],dots, color=get_color(nScen[j]))
                if "BAU" in nScen[j] or "Feed" in nScen[j]:
                    tempY = get_y_offset(secYval,aLUD[tree_idx][j][-1],plt.gca().get_ylim()[1]/40)
                    annotate(str(round(float(aLUD[tree_idx][j][-1]),1))+" Bha",
                             xy=(2112.5, tempY), xycoords='data',ha='center',va='center',
                             xytext=(0,0), textcoords='offset points', fontsize=lf_sz,weight='bold')
            plt.ylabel("Forest\n[Bha]", fontsize=yl_sz)
            plt.xlim(1950,2125)
            plt.ylim(3.5,5.5)
            ax = plt.gca()
            leg = ax.legend(loc='best', ncol=2)
            leg.get_frame().set_alpha(0.5)
            ax.get_xaxis().set_ticklabels([])
            plt.grid(True)
            
            plt.subplot(313)
            if "Historical" in nScen[j]:
                plt.plot(aHyr[othr_idx],aLUD[othr_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label="FAOSTAT",marker="x",zorder=100)
            else: 
                if nScen[j] == "BAU":
                    plt.plot(aYear,aLUD[othr_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]), label=nScen[j], zorder=99)  
                else: plt.plot(aYear,aLUD[othr_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]), label=nScen[j]) 

                ##############################
                # Global Land Use Error Bars
                if nScen[j] == "BAU":
                    for nn in range(len(nScen)):
                        if nScen[nn] == "BAU pop low": low_err = np.array(aLUD[othr_idx][nn])
                        elif nScen[nn] == "BAU pop high": high_err = np.array(aLUD[othr_idx][nn])
                    plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_bau"),alpha=err_alpha)
                        
                #if nScen[j] == "Alg-Feed":
                #    for nn in range(len(nScen)):
                #        if nScen[nn] == "AF pop low": low_err = np.array(aLUD[othr_idx][nn])
                #        elif nScen[nn] == "AF pop high": high_err = np.array(aLUD[othr_idx][nn])
                #    plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_af1"),alpha=err_alpha)   

                scatter([2100,],[aLUD[othr_idx][j][-1],],dots, color=get_color(nScen[j]))
                if "BAU" in nScen[j] or "Alg-Feed" in nScen[j]:
                    tempY = get_y_offset(thrYval,aLUD[othr_idx][j][-1],plt.gca().get_ylim()[1]/40)
                    annotate(str(round(float(aLUD[othr_idx][j][-1]),1))+" Bha",
                             xy=(2112.5, tempY), xycoords='data',ha='center',va='center',
                             xytext=(0,0), textcoords='offset points', fontsize=lf_sz,weight='bold')        
            #plt.xlabel('Year',fontsize=xl_sz)
            plt.ylabel("Other Land\n[Bha]", fontsize=yl_sz-1)
            plt.xlim(1950,2125)
            plt.ylim(3.0,5.0)
            if nScen[j] == "BAU" and label_HD == True:
                annotate('Source: FAOSTAT', fontsize=hd_sz, xy=(2125, 3.1), xycoords='data', 
                         ha='right',va='center', annotation_clip=False)
            plt.grid(True)
            #ax = plt.gca()
            #leg = ax.legend(loc='best', ncol=2)
            #leg.get_frame().set_alpha(0.5)

        if AF_idx == i:

            #if beplus_idx != -1 and beplus_idx != j and "Historical" not in nScen[j]: continue
            #if ((algfd_idx != -1 and algfd_idx != j) and bau_idx != j) and "Historical" not in nScen[j]: continue

            plt.subplot(311)
            if "Historical" in nScen[j]:
                plt.plot(aHyr[AF_idx],aLUD[AF_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label="FAOSTAT",marker="x",zorder=100)
            else:
                if nScen[j] == "BAU":
                    plt.plot(aYear,aLUD[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j], zorder=99)
                else: plt.plot(aYear,aLUD[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
                scatter([2100,],[aLUD[i][j][-1],],dots, color=get_color(nScen[j]))

                # Agricultural Land Error Ranges
                if nScen[j] == "BAU":
                    for nn in range(len(nScen)):
                        if nScen[nn] == "BAU pop low": low_err = np.array(aLUD[i][nn])
                        elif nScen[nn] == "BAU pop high": high_err = np.array(aLUD[i][nn])
                    plt.fill_between(aYear,low_err,high_err,facecolor=get_color(nScen[j]),alpha=err_alpha)
                        
                if nScen[j] == "Alg-Feed":
                    for nn in range(len(nScen)):
                        if nScen[nn] == "AF pop low": low_err = np.array(aLUD[i][nn])
                        elif nScen[nn] == "AF pop high": high_err = np.array(aLUD[i][nn])
                    plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_af1"),alpha=err_alpha)

                if "Alg-Feed" == nScen[j] or "BAU" == nScen[j]: # HACK: Overlaps with other scenarios in this plot
                    tempY = get_y_offset(secYval,aLUD[i][j][-1],plt.gca().get_ylim()[1]/40)
                    annotate(str(round(aLUD[i][j][-1],1))+" Bha",
                             xy=(2112.5, tempY), xycoords='data',ha='center',va='center',
                             xytext=(0,0), textcoords='offset points', fontsize=lf_sz ,weight='bold')   

            plt.xlim(1950,2125)
            plt.ylim(2.0,4.5) 
            plt.ylabel("\n".join(wrap("Perm. Pastures & Meadows [Bha]", 20)), fontsize=yl_sz-1)

            plt.grid(True)

            ax1 = plt.gca()
            leg = ax1.legend(loc='upper left', ncol=2,fontsize=10)
            leg.get_frame().set_alpha(0.5)
            ax1.get_xaxis().set_ticklabels([])

            plt.subplot(312)            
            if "Historical" in nScen[j]:
                plt.plot(aHyr[VF_idx],aLUD[VF_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j],marker="x",zorder=100)
            else:
                if "BAU" in nScen[j]:
                    plt.plot(aYear,aLUD[VF_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j], zorder=99)
                else: plt.plot(aYear,aLUD[VF_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
                scatter([2100,],[aLUD[VF_idx][j][-1],],dots, color=get_color(nScen[j]))

                if nScen[j] == "BAU":
                    for nn in range(len(nScen)):
                        if nScen[nn] == "BAU pop low": low_err = np.array(aLUD[VF_idx][nn])
                        elif nScen[nn] == "BAU pop high": high_err = np.array(aLUD[VF_idx][nn])
                    plt.fill_between(aYear,low_err,high_err,facecolor=get_color(nScen[j]),alpha=err_alpha)

                if nScen[j] == "Alg-Feed":
                    for nn in range(len(nScen)):
                        if nScen[nn] == "AF pop low": low_err = np.array(aLUD[VF_idx][nn])
                        elif nScen[nn] == "AF pop high": high_err = np.array(aLUD[VF_idx][nn])
                    plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_af1"),alpha=err_alpha)
                
                if "Alg-Feed" == nScen[j] or "BAU" == nScen[j]: # HACK: Overlaps with other scenarios in this plot
                    tempY = get_y_offset(allYval,aLUD[VF_idx][j][-1],plt.gca().get_ylim()[1]/40)
                    annotate(str(round(float(aLUD[VF_idx][j][-1]),1))+" Bha",
                             xy=(2112.5, tempY), xycoords='data',ha='center',va='center',
                             xytext=(0,0), textcoords='offset points', fontsize=lf_sz,weight='bold')    

            plt.xlim(1950,2125)
            plt.ylim(1.0,2.0)
            ax2 = plt.gca()
            ax2.get_xaxis().set_ticklabels([])
            plt.ylabel("\n".join(wrap("Arable Land & Perm. Crops [Bha]", 18)), fontsize=yl_sz-1)  
            #annotate("B",xy=(0.02,0.63),xycoords='figure fraction',color='black',fontsize=15,ha='center',va='center',rotation=0,zorder=99,weight='bold',clip_on=False)
            plt.grid(True)                    

            plt.subplot(313)            
            if "Historical" in nScen[j]:
                plt.plot(aHyr[copp_idx],aLUD[copp_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j],marker="x",zorder=100)
            else:
                if "BAU" in nScen[j]:
                    plt.plot(aYear,aLUD[copp_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j], zorder=99)
                else: plt.plot(aYear,aLUD[copp_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
                scatter([2100,],[aLUD[copp_idx][j][-1],],dots, color=get_color(nScen[j]))

                if nScen[j] == "BAU":
                    for nn in range(len(nScen)):
                        if nScen[nn] == "BAU pop low": low_err = np.array(aLUD[copp_idx][nn])
                        elif nScen[nn] == "BAU pop high": high_err = np.array(aLUD[copp_idx][nn])
                    plt.fill_between(aYear,low_err,high_err,facecolor=get_color(nScen[j]),alpha=err_alpha)

                if nScen[j] == "Alg-Feed":
                    for nn in range(len(nScen)):
                        if nScen[nn] == "AF pop low": low_err = np.array(aLUD[copp_idx][nn])
                        elif nScen[nn] == "AF pop high": high_err = np.array(aLUD[copp_idx][nn])
                    plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_af1"),alpha=err_alpha)
                
                if "Alg-Feed" == nScen[j] or "BAU" == nScen[j]: # HACK: Overlaps with other scenarios in this plot
                    tempY = get_y_offset(allYval,aLUD[copp_idx][j][-1],plt.gca().get_ylim()[1]/40)
                    annotate(str(round(float(aLUD[copp_idx][j][-1]),1))+" Bha",
                             xy=(2112.5, tempY), xycoords='data',ha='center',va='center',
                             xytext=(0,0), textcoords='offset points', fontsize=lf_sz, weight='bold')      
                    
            plt.xlim(1950,2125)
            plt.ylim(0.0,2.5)
            plt.ylabel("Forest Plantations\n[Bha]", fontsize=yl_sz-1)
            #annotate("C",xy=(0.02,0.31),xycoords='figure fraction',color='black',fontsize=15,ha='center',va='center',rotation=0,zorder=99,weight='bold',clip_on=False)
            plt.grid(True)

            if nScen[j] == "BAU" and label_HD == True:
                annotate('Source: FAOSTAT', fontsize=hd_sz, xy=(2125, 0.8), xycoords='data', 
                         ha='right',va='center', annotation_clip=False)   

        if "GLOBIOM Vegetal Food Yield" == LUDtypes[i]:
            if j == 0: # be careful with this; it is easily broken. need to find better way to get lowest j ( min(j) = first scenario plotted )
                one_ax = plt.gca()
                two_ax = one_ax.twinx()
                 
            if nScen[j] == "BAU":
                plt.sca(two_ax)
                # Use this plot command for Population bar chart colors:
                #plt.bar(population_time_data,population_data,color=vfcol_data,width=5,zorder=0)
                # Use this plot commant for GRAY Population bar chart
                plt.bar(population_time_data,population_data,color=get_color("Population"),width=5,zorder=0)
                
                for datai in range(len(population_time_data)):
                    if vfs_idx != -1 and dmd_idx != -1 and (population_time_data[datai]+2.5) % 20 == 0 and (population_time_data[datai]+2.5) > 1951:
                        annotate(str(float(round(population_data[datai],1))),
                                 xy=((population_time_data[datai]+2.5), (population_data[datai]+0.3)), 
                                 xycoords='data',ha='center',va='center',
                                 xytext=(0,0.1), textcoords='offset points', fontsize=lf_sz)
                #        annotate(str(int(dmd_pcap[datai])), 
                #                 xy=((population_time_data[datai]+2.5), (population_data[datai]+0.3)), 
                #                 xycoords='data',horizontalalignment='center',verticalalignment='center',
                #                 xytext=(0,0.1), textcoords='offset points', fontsize=lf_sz)
                        
                plt.ylim(0,20)
                plt.ylabel("Population (in billions)", fontsize=yl_sz)
                plt.sca(one_ax)
            
            if "Historical" in nScen[j]:
                if len(aLUD[i][j]) > 1:
                    one_ax.plot(aHyr[i],aLUD[i][j],color=get_color(nScen[j]),label=nScen[j],marker="x",linewidth=get_linewidth(nScen[j]),zorder=99)
            else:
                if "BAU" == nScen[j]:
                    one_ax.plot(aYear,aLUD[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j],zorder=98)
                else: one_ax.plot(aYear,aLUD[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j],zorder=97)
                scatter([2100,],[aLUD[i][j][-1],],dots, color=get_color(nScen[j]),zorder=100)
                
                if "BAU" == nScen[j] or "Alg-Feed" == nScen[j]:
                    tempY = get_y_offset(forYval,aLUD[i][j][-1],plt.gca().get_ylim()[1]/40)
                    annotate(str(round(float(aLUD[i][j][-1]),1))+"\nGCal ha"+r'$^{-1}$',
                             xy=(2112, tempY), xycoords='data',ha='center',va='center',
                             xytext=(0,-1), textcoords='offset points',fontsize=lf_sz,weight='bold',zorder=99) 

                    # Plot GLOBIOM agricultural crop yields here:
                    if "BAU" == nScen[j]:
                        iz = 0
                        init_year = 2000
                        bar_width = 1.5
                        while iz <= 10:
                            plt.gca().add_patch(Rectangle(((init_year-bar_width/2),glo_yld[iz][0]),
                                                          bar_width,(glo_yld[iz][2]-glo_yld[iz][0]), color = get_color("GLOBIOM")))
                            iz = iz+1
                            init_year = init_year+10

                plt.ylim(0,20)
                plt.ylabel("Cropland Yield [GCal ha"+r'$^{-1}$'+" y"+r'$^{-1}$]', fontsize=yl_sz) 
            
            ax = plt.gca()
            leg = ax.legend(loc='upper left', ncol=1, fontsize=10)
            leg.get_frame().set_alpha(0.5)
            plt.grid(True)
            plt.xlim(1950,2125)
        
        if "Historical" not in nScen[j] and tree_idx != i and AF_idx != i and "GLOBIOM Vegetal Food Yield" != LUDtypes[i]:
 
                if i == FRbm_idx or i == ECbm_idx or i == CRbm_idx:
                    plt.subplot(111)
                    if "Food Crop Land Residual Production" == LUDtypes[i]: 
                        alt_array = np.array(aLUD[i][j]) + np.array(aLUD[ECbm_idx][j]) + np.array(aLUD[FRbm_idx][j])
                    else: alt_array =np.array(aLUD[i][j])
                    
                    scatter([2100,],[alt_array[-1],],dots, color=get_color(nScen[j]))
                    plt.plot(aYear,alt_array,color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
                    
                    if "Forest Biomass Production"            == LUDtypes[i]: 
                        plt.title(LUDtypes[i], fontsize=title_sz)
                        plt.ylim(0,20)

                        tempY = get_y_offset(allYval,float(alt_array[-1]),plt.gca().get_ylim()[1]/20)                    
                        annotate(str(round(float(alt_array[-1]),1))+r' PgC y$^{-1}$',
                                 xy=(2112.5, tempY), xycoords='data',horizontalalignment='center',verticalalignment='center',
                                 xytext=(0,0), textcoords='offset points', fontsize=lf_sz)

                    elif "Energy Crops Production"            == LUDtypes[i]: 
                        plt.title(LUDtypes[i], fontsize=title_sz)
                        plt.ylim(0,2)
                        tempY = get_y_offset(allYval,float(alt_array[-1]),plt.gca().get_ylim()[1]/20)                    
                        annotate(str(round(float(alt_array[-1]),1))+r' PgC y$^{-1}$',
                                 xy=(2112.5, tempY), xycoords='data',horizontalalignment='center',verticalalignment='center',
                                 xytext=(0,0), textcoords='offset points', fontsize=lf_sz)

                    elif "Food Crop Land Residual Production" == LUDtypes[i]: 
                        plt.ylim(0,30)
                        plt.ylabel("\n".join(wrap("Land-Based Biomass for Energy Production [PgC y"+r'$^{-1}$]', 30)), fontsize=yl_sz)                    
                        if "BioEnergy CCS" == nScen[j] or "CCS" == nScen[j] or "Alg-Feed CCS75" == nScen[j]:
                            tempY = get_y_offset(allYval,float(alt_array[-1]),plt.gca().get_ylim()[1]/40)             
                            annotate(str(round(float(alt_array[-1]),1))+r' PgC y$^{-1}$',
                                     xy=(2112.5, tempY), xycoords='data',horizontalalignment='center',verticalalignment='center',
                                     xytext=(0,0), textcoords='offset points', fontsize=lf_sz)                      

                else:
                    plt.plot(aYear,aLUD[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
                    scatter([2100,],[aLUD[i][j][-1],],dots, color=get_color(nScen[j]))

                    if "Actual Forest Land Harvested" == LUDtypes[i]:
                        if nScen[j] != "Alg-Fuel" and nScen[j] != "CCS" and nScen[j] != "Alg-Fuel CCS" and nScen[j] != "BioEnergy":
                            annotate(str(round(float(aLUD[i][j][-1]),1))+" Bha",
                                     xy=(2112.5, aLUD[i][j][-1]), xycoords='data',horizontalalignment='center',verticalalignment='center',
                                     xytext=(0,0), textcoords='offset points', fontsize=lf_sz)
                    else: annotate(str(round(float(aLUD[i][j][-1]),1))+" Bha",
                                   xy=(2112.5, aLUD[i][j][-1]), xycoords='data',horizontalalignment='center',verticalalignment='center',
                                   xytext=(0,0), textcoords='offset points', fontsize=lf_sz)
                    plt.ylabel(LUDtypes[i], fontsize=yl_sz)
                    plt.ylim(0,)
            
                plt.xlim(1950,2125)
                #plt.xlabel('Year',fontsize=xl_sz)

                if "Actual Forest Land Harvested" == LUDtypes[i]:
                    #plt.title("Cumulative Conversion Forest to Plantation", fontsize=title_sz)
                    plt.ylim(0,1.5)
                    plt.ylabel("Biomass Plantations (Billion ha)",fontsize=yl_sz-2)
    
                ax = plt.gca()
                leg = ax.legend(loc='best', ncol=2)
                leg.get_frame().set_alpha(0.5)
                plt.grid(True)
    
                for j in range(len(nScen)):
                    if "Food Crop Land Residual Production" == LUDtypes[i] and "Historical" not in nScen[j] and scenario_switch(nScen[j],"CCS") == True:
                        plt.plot(aYear,aLUD[FRbm_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),linestyle="--")
    
    if "Vegetal Food Yield" in LUDtypes[i]: sns.despine(right=False)
    else: sns.despine()

    fig = matplotlib.pyplot.gcf()
    if AF_idx == i:
        fig.set_size_inches(6.4,4.4*3/2)
        #print fig.get_size_inches()
    else: fig.set_size_inches(6.4,4.4)
    plt.draw()

    plt.savefig('figures/production_'+LUDtypes[i].replace(" ","_").replace("&","").replace("+","")+'.pdf',bbox_inches='tight',format='pdf', dpi=1500)
    if show_land_cover == True: plt.show()
    plt.clf()
print "Finished: Land Use plots"

#############################################
#############################################
# Emissions II
#

iRow = 0
iScen = 0
nScen = []
aYear = []
aHyr = [[]]
nEM = 0
EMtypes = []
aEM = [[[]]]
marker1 = -1

with open("table_new/emissions_table_1.csv") as f: 
    reader = csv.reader(f)
    allRows = list(reader)
    nRows = len(allRows)

with open("table_new/emissions_table_1.csv") as f: 
    reader = csv.reader(f)
    
    for row in reader:

##### TIME INFO
        if iRow == 0:
            for i in range(1,len(row)-1):
                aYear.append(int(float(row[i])))
                
##### SCENARIO INFO
        elif iRow == 1:
            for i in range(1,len(row)-1):
                if row[i] != "": nScen.append(row[i])
                
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
                EMtypes.append(row[0])
                iScen = 0
                
            for i in range(1,len(row)-1):
                if "--" not in row[i] and row[i] != "":
                    if "Historical" in row[0]: aHyr[len(EMtypes)-1].append(aYear[i-1])
                    if (EMtypes[len(EMtypes)-1] != "Atmospheric Concentration CO2" and EMtypes[len(EMtypes)-1] != "New Forest ha"):
                        aEM[len(EMtypes)-1][iScen].append(float(row[i])/1e009)
                        if EMtypes[len(EMtypes)-1] == "C Emission from Biomass Energy": marker1 = len(EMtypes)-1
                        if EMtypes[len(EMtypes)-1] == "Total Additional Emissions":
                            if marker == -1: assert False 
                            aEM[marker1][iScen][i-1] += float(row[i])/1e009
                    else: aEM[len(EMtypes)-1][iScen].append(float(row[i]))
            iScen = iScen+1                
        iRow = iRow+1

#################################
# Plot Emissions II Data
standardize_scenario_names(nScen)

for i in range(nEM):
    allYval = []
    tempY = 0
    plt.cla()

    for j in range(len(nScen)):

        if "Historical" in nScen[j]:
            if len(aHyr[i]) > 1:
                plt.plot(aHyr[i],aEM[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label="CDIAC Data",marker="x",zorder=100)
            else: continue
        elif scenario_switch(nScen[j],"CCS") == False: continue
        elif "Gross C Emission Biomass" == EMtypes[i]: 
            if "BAU" in nScen[j]:
                plt.plot(aYear,aEM[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j],zorder=99)
            else: continue

        else:

            if "BAU" in nScen[j]:
                plt.plot(aYear,aEM[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j],zorder=99)
            elif EMtypes[i] != "Atmospheric Concentration CO2":
                if "CCS" not in nScen[j]: plt.plot(aYear,aEM[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
            else: 
                #if nScen[j] != "BAU" and nScen[j] != "Alg-Feed" and "Alg-Feed CCS" not in nScen[j]: continue 
                plt.plot(aYear,aEM[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
        
            if (EMtypes[i] == "Total C Emission from Fossil Fuels" or EMtypes[i] == "C Emission from Biomass Energy"):

                if "Total C Emission from Fossil Fuels" in EMtypes[i]:
                    if "CCS" not in nScen[j] and "Historical" not in nScen[j]:
                        tempY = get_y_offset(allYval,float(aEM[i][j][-1]),plt.gca().get_ylim()[1]/40)
                        annotate(str(round(float(aEM[i][j][-1]),1))+r' PgC y$^{-1}$',xy=(2115, tempY), xycoords='data',xytext=(3,0), textcoords='offset points',
                                 ha='center',va='center',fontsize=lf_sz,weight='bold')

                    if "BAU" == nScen[j]:
                        plt.ylabel("Gross C Emissions:\nFossil Fuels [PgC y"+r'$^{-1}$]', fontsize=yl_sz)
                        plt.ylim(0,12)
                        if label_HD == True:
                            annotate('Source: Carbon Dioxide Information Analysis Center', fontsize=hd_sz, xy=(2125, -3.5), xycoords='data', 
                                     ha='right',va='center', annotation_clip=False)

                if "C Emission from Biomass Energy" in EMtypes[i]:
                    plt.ylabel("Gross C Emissions:\nBiofuels [PgC y"+r'$^{-1}$]', fontsize=yl_sz)
                    plt.ylim(0,20)
                    if "CCS" not in nScen[j]:
                        tempY = get_y_offset(allYval,float(aEM[i][j][-1]),plt.gca().get_ylim()[1]/40)
                        annotate(str(round(float(aEM[i][j][-1]),1))+r' PgC y$^{-1}$',xy=(2115, tempY), xycoords='data',
                                 xytext=(3,0), textcoords='offset points', fontsize=lf_sz,va='center',ha='center',weight='bold')

                if "CCS" not in nScen[j] and "Historical" not in nScen[j]:
                    scatter([2100,],[aEM[i][j][-1],],dots, color=get_color(nScen[j]))

            elif "Concentration" in EMtypes[i]:
                ####################################
                # Atm C Concentration error bars
                low_err = np.array([])
                high_err = np.array([])
                if nScen[j] == "BAU":
                    for nn in range(len(nScen)):
                        if nScen[nn] == "BAU pop low": low_err = np.array(aEM[i][nn])
                        elif nScen[nn] == "BAU pop high": high_err = np.array(aEM[i][nn])
                    plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_bau"),alpha=err_alpha)
                        
                if nScen[j] == "Alg-Feed CCS75":
                    low_err = np.array([])
                    high_err = np.array([])                    
                    for nn in range(len(nScen)):
                        if nScen[nn] == "AFC 15tph": low_err = np.array(aEM[i][nn])
                        elif nScen[nn] == "AFC 05tph": high_err = np.array(aEM[i][nn])
                    plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_afc"),alpha=sec_alpha)

                    low_err = np.array([])
                    high_err = np.array([])   
                    for nn in range(len(nScen)):
                        if nScen[nn] == "AFC pop low": low_err = np.array(aEM[i][nn])
                        elif nScen[nn] == "AFC pop high": high_err = np.array(aEM[i][nn])
                    plt.fill_between(aYear,low_err,high_err,facecolor=get_color("errrng_afc"),alpha=err_alpha)

                plt.ylabel(r'Atmospheric CO$_2$ [ppm]',fontsize=yl_sz)
                scatter([2100,],[aEM[i][j][-1],],dots, color=get_color(nScen[j]))

                if nScen[j] == "BAU" or "Alg-Feed" in nScen[j]:  
                    tempY = get_y_offset(allYval,float(aEM[i][j][-1]),plt.gca().get_ylim()[1]/40)
                    annotate(str(int(aEM[i][j][-1]))+' ppm', xy=(2100, tempY), xycoords='data',
                             xytext=(3,0), textcoords='offset points', va='center', fontsize=lf_sz, weight='bold')
                
                if "BAU" in nScen[j] and label_HD == True:
                    annotate('Source: Carbon Dioxide Information Analysis Center', fontsize=hd_sz, xy=(2112.5, 120), xycoords='data', 
                             ha='right',va='center', annotation_clip=False)
                plt.ylim(200,900)
            else:
                plt.ylabel(EMtypes[i], fontsize=yl_sz)
                #plt.ylim(0,)

    if "Concentration" in EMtypes[i]:
        plt.plot(rcp_time,rcp_ppm_26,color=get_color('2.6'),linestyle="--",linewidth=2,label='RCP 2.6',zorder=0)      
        plt.plot(rcp_time,rcp_ppm_45,color=get_color('4.5'),linestyle="--",linewidth=2,label='RCP 4.5',zorder=0)     
        plt.plot(rcp_time,rcp_ppm_60,color=get_color('6.0'),linestyle="--",linewidth=2,label='RCP 6.0',zorder=0)     
        plt.plot(rcp_time,rcp_ppm_85,color=get_color('8.5'),linestyle="--",linewidth=2,label='RCP 8.5',zorder=0)    
        plt.xlim(1950,2112.5)
    else: plt.xlim(1950,2125)
    ax = plt.gca()
    leg = ax.legend(loc='best', ncol=2,fontsize=10)
    leg.get_frame().set_alpha(0.5)
    #plt.xlabel('Year',fontsize=xl_sz)
    sns.despine()
    plt.grid(True)
    #plt.figure().set_tight_layout(True)

    plt.draw()
    plt.savefig('figures/emissions_'+EMtypes[i].replace(" ","_").replace("&","").replace("+","")+'.pdf',format='pdf', dpi=1500)
    if show_emissions_II == True: plt.show()
    plt.clf()

print "Finished Emissions II"

#################################
# Plot Temperature vs CO2s
#
#for i in range(nEM):
#    plt.cla()
#
#    if "Concentration" in EMtypes[i]:
#        for j in range(len(nScen)):
#            for k in range(len(nScen_temp)):
#
#                if "BAU" in nScen[j] and "BAU" in nScen_temp[k]:
#                    plt.plot(aEM[i][j],aTemp_giss[0][k],color=get_color(nScen_temp[k]),linewidth=2,label=nScen[j])
#
#                else: continue
#
#        ax = plt.gca()
#        leg = ax.legend(loc='best', ncol=2)
#        leg.get_frame().set_alpha(0.5)
#        plt.grid(True)
#        plt.draw()
#        plt.savefig('figures/CO2_vs_temp.pdf',format='pdf', dpi=1500)
#        if show_emissions_II == True: plt.show()

#############################################
#############################################
# WATER Data (Background info)
#

iRow = 0
iScen = 0
nScen = []
aYear = []
aHyr = [[]]
nH2O = 0
H2Otypes = []
aH2O = [[[]]]

with open("table_new/water_table.csv") as f: 
    reader = csv.reader(f)
    allRows = list(reader)
    nRows = len(allRows)

with open("table_new/water_table.csv") as f: 
    reader = csv.reader(f)
    
    for row in reader:

##### TIME INFO
        if iRow == 0:
            for i in range(1,len(row)-1):
                aYear.append(int(float(row[i])))
                
##### SCENARIO INFO
        elif iRow == 1:
            for i in range(1,len(row)-1):
                if row[i] != "": nScen.append(row[i])
                
            nH2O  = (nRows-2)/len(nScen)
            if nH2O%1 != 0: print "Error: Unexpected number of rows!"
                
            for n in range(nH2O):
                aH2O.append([])
                aHyr.append([])
                for m in range(len(nScen)):
                    aH2O[n].append([])
##### SCENARIO DATA
        else:
            if (iRow-2)%len(nScen) == 0:
                H2Otypes.append(row[0])
                iScen = 0
                
            for i in range(1,len(row)-1):
                if "--" not in row[i] and row[i] != "":
                    if "Historical" in row[0]: aHyr[len(H2Otypes)-1].append(aYear[i-1])
                    
                    if H2Otypes[-1] == "Agricultural Water Demand" : aH2O[len(H2Otypes)-1][iScen].append(float(row[i])/1e009) 
                    else: aH2O[len(H2Otypes)-1][iScen].append(float(row[i])/1e009)
    
            iScen = iScen+1
                
        iRow = iRow+1

#################################
# Plot WATER DATA

# Historical FAO data
hist_irri_time = [  1800,  1900,  1950,  1961,  1965,  1970,  1975,  1979,  1980,  1985,  1990,  1994,  1996]
hist_irri_area = [ 0.008, 0.040, 0.094, 0.139, 0.151, 0.169, 0.190, 0.209, 0.211, 0.226, 0.239, 0.249, 0.263]

#######
standardize_scenario_names(nScen)

rain_idx = -1
irri_idx = -1
agdm_idx = -1
agland_idx = -1

for i in range(nH2O):
    if "Rainfed Agriculture Land" == H2Otypes[i]: rain_idx = i
    elif "Irrigated Agriculture Land" == H2Otypes[i]: irri_idx = i
    elif "Agricultural Water Demand" == H2Otypes[i]: agdm_idx = i
    
for i in range(nH2O):
    plt.cla()
    allYval = []
    tempY = 0
    hist_switch = False

    for j in range(len(nScen)):

        if scenario_switch(nScen[j],"CCS") == False: continue
        if "Historical" not in nScen[j]:
            if i == agdm_idx:

                # Plot Irrigated Agricultural Land
                plt.subplot(211)
                plt.plot(aYear,aH2O[irri_idx][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]),label=nScen[j])
                if nScen[j] == "Alg-Fuel CCS" and hist_switch == False:
                    plt.plot(hist_irri_time, hist_irri_area, color=get_color("Historical"),marker="x",linewidth=get_linewidth(nScen[j]),label="HistoricalData", zorder=100)
                    hist_switch = True
                scatter([2100,],[aH2O[irri_idx][j][-1],],dots, color=get_color(nScen[j]))

                if "BAU" in nScen[j] or "Feed" in nScen[j]:
                    tempY = get_y_offset(allYval,float(aH2O[irri_idx][j][-1]),plt.gca().get_ylim()[1]/25)
                    annotate(str(round(float(aH2O[irri_idx][j][-1]),1))+" Bha",
                         xy=(2112.5, tempY), xycoords='data',horizontalalignment='center',verticalalignment='center',
                             xytext=(0,0), textcoords='offset points', fontsize=7)

                plt.title("Agricultural Water Usage", fontsize=title_sz)
                plt.xlim(1950,2125)
                plt.ylim(0.0,2.0)
                plt.ylabel("Irrigated Land [Bha]", fontsize=yl_sz-1)
                plt.grid(True)
                ax1 = plt.gca()
                leg = ax1.legend(loc='best', ncol=2)
                leg.get_frame().set_alpha(0.5)
                ax1.get_xaxis().set_ticklabels([])
                plt.subplots_adjust(hspace=0.075)

                # Plot Agricultural Water Demand
                plt.subplot(212)
                plot(aYear,aH2O[i][j],color=get_color(nScen[j]),linewidth=get_linewidth(nScen[j]))
                plt.xlim(1950,2125)
                plt.grid(True)
                plt.ylim(0,6000)
                plt.ylabel("Demand (km"+r'$^{3}$'+" y"+r'$^{-1}$)', fontsize=yl_sz-1)

                if "BAU" in nScen[j] or "Feed" in nScen[j]:
                    tempY = get_y_offset(allYval,float(aH2O[i][j][-1]),plt.gca().get_ylim()[1]/25)
                    annotate(str(int(aH2O[i][j][-1]))+" km"+r'$^3$',
                             xy=(2112.5, tempY), xycoords='data',horizontalalignment='center',verticalalignment='center',
                             xytext=(0,0), textcoords='offset points', fontsize=lf_sz)  
                scatter([2100,],[aH2O[i][j][-1],],dots, color=get_color(nScen[j]))
                if nScen[j] == "BAU" and label_HD == True:
                    annotate('Source: UNESCO International Hydrological Programme', fontsize=hd_sz, xy=(2125, -1000), xycoords='data', 
                             horizontalalignment='right',verticalalignment='center', annotation_clip=False)

        elif "Historical" in nScen[j] and len(aH2O[i][j]) > 1:
            plt.plot(aHyr[i],aH2O[i][j],color=get_color(nScen[j]),marker="x",linewidth=get_linewidth(nScen[j]),zorder=100)
            #ax = plt.gca()
            #leg = ax.legend(loc=2, ncol=2)
            #leg.get_frame().set_alpha(0.5)
            plt.grid(True)
                
        if "Irrigated Agriculture Land"== H2Otypes[i]: 
            plt.ylim(0.0,2.0)
            plt.title("Irrigated Agricultural Land",fontsize=title_sz)
            plt.ylabel("Billion ha", fontsize=yl_sz)

    #plt.figure().set_tight_layout(True)
    sns.despine()
    plt.draw()

    plt.savefig('figures/water_'+H2Otypes[i].replace(" ","_").replace("&","").replace("+","")+'.pdf',format='pdf', dpi=1500)
    if show_water == True: plt.show()
    plt.clf()
