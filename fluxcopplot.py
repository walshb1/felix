from pylab import *
import csv
import copy
import prettyplotlib as ppl
import matplotlib.patches as pts
from matplotlib import rc
from matplotlib import colors
from textwrap import wrap
import matplotlib.ticker as mtick
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

def insert_panel_label(plt,panel_str,n_subp=2,equiv_yr=1937):
    y_val = 1.0
    trans = plt.gca().get_xaxis_transform() # x in data units, y in axes fraction
    annotate(panel_str,size=21, xy=(equiv_yr,y_val),xycoords=trans,ha='right',va='center',weight='bold',annotation_clip=False)

ecs_str = "3C"
if len(sys.argv) >=2 and sys.argv[1][-1] == "C":
    ecs_str = sys.argv[1]
print "Running ECS = ",ecs_str
if ecs_str == "25C": ecs_str = "gc"

year_int = 2100
if len(sys.argv) >=3:
    year_int = int(sys.argv[2])
print "Running Fluxes in year",year_int

with open("tables/emissions_table_fluxes.csv") as f: 
    reader = csv.reader(f)
    allRows = list(reader)
    nRows = len(allRows)

flux_array = [["Scenario"]]
with open("tables/emissions_table_fluxes.csv") as f: 
    reader = csv.reader(f)
    
    for row in reader:
        
        if "Time" in row[0]:
            for aYear in row[1:]:
                aYear_int = int(float(aYear))
                if aYear_int == year_int: year_idx = row.index(aYear)
        
        if row[0] == "Selected Variables Runs:":
            for iScen in row[1:]:
                if iScen != '' and iScen != "HistoricalData" and (ecs_str == iScen[-2:] or iScen == 'BAU'):
                    flux_array.append([iScen])

        for iFlux in flux_array:
            if row[0][3:] in iFlux: 
                iFlux.append(float(row[year_idx])/1E9)
                
        if "Time" not in row[0] and "Selected" not in row[0] and "Historical" not in row[0]:
            if "BAU" not in row[0]:
                flux_array[0].append(row[0])
                flux_array[1].append(float(row[-2])/1E9)

denom_idx = -1
for iFlux in flux_array:
    print iFlux    
    if (iFlux[0] == 'BAU_10pgc' or iFlux[0] == 'BAU_10pgc_3C'): denom_idx = flux_array.index(iFlux)

# X-values
tot_em_idx = flux_array[0].index('Total C Emission')
xax_vals = [(xFlux[tot_em_idx]/flux_array[denom_idx][tot_em_idx]-1)*100 for xFlux in flux_array[2:]]
xax_pgc = [xFlux[tot_em_idx]-0.4 for xFlux in flux_array[2:]]

# Y-values
############
# Ocean Flux
atm_to_ocean_idx = flux_array[0].index('Flux Atmosphere to Ocean')
#
ocean_flux_vals = [(yFlux[atm_to_ocean_idx]/flux_array[denom_idx][atm_to_ocean_idx]-1)*100 for yFlux in flux_array[2:]]
ocean_flux_pgc = [-1*yFlux[atm_to_ocean_idx] for yFlux in flux_array[2:]]

############
# Biomass Net Flux
atm_to_bio_idx = flux_array[0].index('Flux Atmosphere to Biomass')
bio_to_atm_idx = flux_array[0].index('Flux Biomass to Atmosphere')
bio_to_hum_idx = flux_array[0].index('Flux Biomass to Humus') 
#
bio_net_flux_vals = [((yFlux[atm_to_bio_idx]-yFlux[bio_to_atm_idx]-yFlux[bio_to_hum_idx])/(flux_array[denom_idx][atm_to_bio_idx]-flux_array[denom_idx][bio_to_atm_idx]-flux_array[denom_idx][bio_to_hum_idx])-1)*100 for yFlux in flux_array[2:]]
bio_gross_flux_vals = [(yFlux[atm_to_bio_idx]/flux_array[denom_idx][atm_to_bio_idx]-1)*100 for yFlux in flux_array[2:]]
bio_net_flux_pgc = [-1*(yFlux[atm_to_bio_idx]-yFlux[bio_to_atm_idx]-yFlux[bio_to_hum_idx]) for yFlux in flux_array[2:]]

############
# Humus Net Flux
bio_to_hum_idx = flux_array[0].index('Flux Biomass to Humus')
hum_to_atm_idx = flux_array[0].index('Flux Humus to Atmosphere')
#
hum_net_flux_vals = [((yFlux[bio_to_hum_idx]-yFlux[hum_to_atm_idx])/(flux_array[denom_idx][bio_to_hum_idx]-flux_array[denom_idx][hum_to_atm_idx])-1)*100 for yFlux in flux_array[2:]]
hum_gross_flux_vals = [(yFlux[bio_to_hum_idx]/flux_array[denom_idx][bio_to_hum_idx]-1)*100 for yFlux in flux_array[2:]]
hum_net_flux_pgc = [-1*(yFlux[bio_to_hum_idx]-yFlux[hum_to_atm_idx]) for yFlux in flux_array[2:]]

############
# Land Sink Net Flux
atm_to_land_idx = flux_array[0].index('Flux Atmosphere to Land Sink')
#
land_net_flux_vals = [(yFlux[atm_to_land_idx]/flux_array[denom_idx][atm_to_land_idx]-1)*100 for yFlux in flux_array[2:]]
land_net_flux_pgc = [-1*yFlux[atm_to_land_idx] for yFlux in flux_array[2:]]

############
# Atmospheric Net Flux
atm_net_idx = flux_array[0].index('Total Atmospheric Carbon Flux')
#
atm_net_flux_vals = [(yFlux[atm_net_idx]/flux_array[denom_idx][atm_net_idx]-1)*100 for yFlux in flux_array[2:]]
atm_net_flux_pgc = [yFlux[atm_net_idx] for yFlux in flux_array[2:]]

############
# Total Sink Net Flux
all_sink_net_flux_vals = [((yFlux[atm_to_land_idx]+yFlux[atm_to_ocean_idx])/(flux_array[denom_idx][atm_to_land_idx]+flux_array[denom_idx][atm_to_ocean_idx])-1)*100 for yFlux in flux_array[2:]]
all_sink_net_flux_pgc = [-1*(yFlux[atm_to_land_idx]+yFlux[atm_to_ocean_idx]) for yFlux in flux_array[2:]]

########################
plt.plot(xax_vals, atm_net_flux_vals, color=pairs[0],label="Atmosphere (Net)")
plt.plot(xax_vals, ocean_flux_vals, color=pairs[1],label="Ocean (Net)")
plt.plot(xax_vals, bio_gross_flux_vals, color=greens[6],label="Biomass (Gross)")
plt.plot(xax_vals, bio_net_flux_vals, color=pairs[2],label="Biomass (Net)")
plt.plot(xax_vals, hum_gross_flux_vals, color=browns[1],label="Humus (Gross)")
plt.plot(xax_vals, hum_net_flux_vals, color=browns[2],label="Humus (Net)")
plt.plot(xax_vals, land_net_flux_vals, color=purples[7],label="Land Sink (Net)")
plt.plot(xax_vals, all_sink_net_flux_vals, color=pairs[5],label="All Sinks (Net)")

########################
plt.plot(plt.gca().get_xlim(),[0,0],'k-',color='black',lw=1.0,zorder=1)
plt.plot([0,0],plt.gca().get_ylim(),'k-',color='black',lw=1.0,zorder=1)
sns.despine(bottom=True,left=True)

plt.xlim(-125,125)
plt.xlabel("Net Anthropogenic Emissions [PgC yr$^{-1}$]\n(constant after 2015)")
plt.ylabel("Carbon Flux Response in "+str(year_int)+" [%]")
insert_panel_label(plt,"b",1,-145)

ax = plt.gca()
####################
# x-axis ticks
major_ticks = [-125,-100,-75,-50,-25,0,+25,+50,+75,+100,+125]
ax.set_xticks(major_ticks)

labels = [str(major_ticks[ax.get_xticklabels().index(item)])+"%" for item in ax.get_xticklabels()]
for ilabel in labels: 
    if ilabel[0] != "-": 
        labels[labels.index(ilabel)]="+"+labels[labels.index(ilabel)]
labels[5] = '10 PgC/yr'

ax.set_xticklabels(labels)

plt.tick_params(axis='both', which='major', labelsize=6)
zed = [tick.label.set_fontsize(8) for tick in ax.xaxis.get_major_ticks() if ax.xaxis.get_major_ticks().index(tick)==5]

ax.grid(which='major', alpha=0.5)  

####################
# y-axis ticks
fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
yticks = mtick.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(yticks)

leg = ax.legend(loc='best', ncol=1,borderpad=0.75,fancybox=True, frameon=True)
leg.get_frame().set_alpha(0.9)
annotate("ECS = "+ecs_str[:-1].replace('g','2.5')+"$^{\circ}$C / 2xCO$_2$", xy=(0.98,0.03),xycoords='axes fraction',size=8,va="center",ha="right")
plt.draw()
plt.savefig('figures/fluxes/rel_fluxes_'+str(year_int)+'.pdf',format='pdf')
print 'SAVING AS figures/fluxes/rel_fluxes_'+str(year_int)+'.pdf'
plt.cla()

#####################
# Absolute Values Plot
wd_par = 0.8

plt.bar(xax_pgc, atm_net_flux_pgc,width=wd_par,color=pairs[0],label="Atmosphere")
plt.bar(xax_pgc, ocean_flux_pgc,width=wd_par,color=pairs[1],label="Ocean",bottom=0)
plt.bar(xax_pgc, bio_net_flux_pgc,width=wd_par,color=pairs[2],label="Biomass",bottom=ocean_flux_pgc)
plt.bar(xax_pgc, hum_net_flux_pgc,width=wd_par,color=browns[2],label="Humus",bottom=(np.array(ocean_flux_pgc)+np.array(bio_net_flux_pgc)))
#plt.bar(xax_pgc, land_net_flux_pgc,width=wd_par,color=purples[7],label="Land Sink")

major_ticks = [-4,-2,0,2,4,6,8,10,12,14,16,18,20,22]
ax.set_xticks(major_ticks)
major_ticks = [-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14,16]
ax.set_yticks(major_ticks)

plt.xlim(-5,23)
plt.ylim(-10,16)
plt.xlabel("Net Anthropogenic Emissions [PgC yr$^{-1}$]\n(constant after 2015)")
plt.ylabel("Net Carbon Flux in "+str(year_int)+" [PgC yr$^{-1}$]")
insert_panel_label(plt,"a",1,-7)
ax.grid(which='major', alpha=0.5) 

plt.plot(plt.gca().get_xlim(),[0,0],'k-',color='black',lw=1.0,zorder=1)

leg = ax.legend(loc='best', ncol=1,borderpad=0.75,fancybox=True, frameon=True)
leg.get_frame().set_alpha(0.9)

sns.despine(bottom=True,left=False)
annotate("ECS = "+ecs_str[:-1].replace('g','2.5')+"$^{\circ}$C / 2xCO$_2$", xy=(0.98,0.03),xycoords='axes fraction',size=8,va="center",ha="right")

plt.draw()
plt.savefig('figures/fluxes/fluxes_abs_'+str(year_int)+'.pdf',format='pdf', dpi=1200)
plt.cla()
