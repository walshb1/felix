import brewer2mpl
import seaborn as sns

import timeit

set1 = brewer2mpl.get_map('Set1', 'qualitative', 9).mpl_colors
set2 = brewer2mpl.get_map('Set2', 'qualitative', 8).mpl_colors
dark2 = brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors
#pairs = brewer2mpl.get_map('Paired', 'qualitative', 12).mpl_colors
pastels = brewer2mpl.get_map('Pastel1', 'qualitative', 9).mpl_colors
pastels2 = brewer2mpl.get_map('Pastel2', 'qualitative', 8).mpl_colors
greens = brewer2mpl.get_map('YlGn', 'sequential',9).mpl_colors
blues = brewer2mpl.get_map('PuBu', 'sequential',9).mpl_colors
bupu = brewer2mpl.get_map('BuPu', 'sequential',9).mpl_colors
reds = brewer2mpl.get_map('Reds', 'sequential',9).mpl_colors
oranges = brewer2mpl.get_map('Oranges', 'sequential',9).mpl_colors
purples = brewer2mpl.get_map('Purples', 'sequential',9).mpl_colors
red_to_green = brewer2mpl.get_map('RdYlGn', 'diverging', 11).mpl_colors
yelo_to_blue = brewer2mpl.get_map('YlGnBu', 'sequential', 9).mpl_colors
gren_to_blue = brewer2mpl.get_map('GnBu', 'sequential', 9).mpl_colors
greys = brewer2mpl.get_map('Greys', 'sequential', 9).mpl_colors
browns = brewer2mpl.get_map('BrBG', 'diverging', 11).mpl_colors

#pairs = sns.color_palette("cubehelix", 12)
pairs = sns.color_palette("Paired", 12)
sns_s1 = sns.color_palette("Set1", 12)
sns_s2 = sns.color_palette("Set2", 12)
sns_s3 = sns.color_palette("Set3", 12)
sns_rgp = sns.color_palette("RdYlGn", 11)
#sns.palplot(current_palette)

#################

def cop_color(iCol):   
    if "Historical" in iCol: return greys[6]
    #
    if "FossilBAU" in iCol: return sns.xkcd_rgb["dirt"]#oranges[8]
    if iCol == "BAU" or iCol == "BAU 3C": return sns.xkcd_rgb["brownish red"]#sns.xkcd_rgb["pale red"]
    if iCol == "BioEnergy" or iCol == "BioEnergy 3C": return sns.xkcd_rgb["mango"]#sns_s1[4]
    if "BioEnergy CCS25" in iCol: return sns.xkcd_rgb["dark sage"]#sns.xkcd_rgb["golden yellow"]
    if "BioEnergy CCS50" in iCol: return sns.xkcd_rgb["flat blue"]#sns.xkcd_rgb["golden yellow"]
    if "BioEnergy CCS75" in iCol: return sns.xkcd_rgb["dark lavender"]#sns.xkcd_rgb["golden yellow"]
    

    if "CCS40" in iCol: return sns.xkcd_rgb["dark sage"]#greens[7]
    if "CCS80" in iCol: return sns.xkcd_rgb["flat blue"]#blues[8]

    if "BioEnergy CCS25" in iCol: return sns.xkcd_rgb["dark sage"]#sns.xkcd_rgb["golden yellow"]
    if "BioEnergy CCS50" in iCol: return sns.xkcd_rgb["flat blue"]#greens[7]

    #if iCol == "face BioEnergy1": return pairs[6]
    #if iCol == "face BioEnergy1 CCS25": return pastels2[5]
    #if iCol == "face BioEnergy1 CCS50": return greens[3]
    #if iCol == "face BioEnergy1 CCS75": return purples[3]#blues[8]

    if iCol == "BioEnergy1" or iCol == "BioEnergy1 3C": return sns.xkcd_rgb["mango"]#sns_s1[4]
    if "BioEnergy1 CCS25" in iCol: return sns.xkcd_rgb["dark sage"]#["golden yellow"]
    if "BioEnergy1 CCS50" in iCol: return sns.xkcd_rgb["flat blue"]#greens[7]
    if "BioEnergy1 CCS75" in iCol: return sns.xkcd_rgb["dark lavender"]#pairs[9]#blues[8]

    #if iCol == "face BioEnergy2": return pairs[6]
    #if iCol == "face BioEnergy2 CCS25": return pastels2[5]
    #if iCol == "face BioEnergy2 CCS50": return greens[3]
    #if iCol == "face BioEnergy2 CCS75": return purples[3]#blues[8]

    #if iCol == "BioEnergy2" or iCol == "BioEnergy2 3C": return sns.xkcd_rgb["mango"]#sns_s1[4]
    #if "BioEnergy2 CCS25" in iCol: return sns.xkcd_rgb["dark sage"]#["golden yellow"]
    #if "BioEnergy2 CCS50" in iCol: return sns.xkcd_rgb["flat blue"]#greens[7]
    #if "BioEnergy2 CCS75" in iCol: return sns.xkcd_rgb["dark lavender"]#pairs[9]#blues[8]

    if iCol == "BioEnergy3" or iCol == "BioEnergy3 3C": return sns.xkcd_rgb["mango"]#sns_s1[4]
    if "BioEnergy3 CCS25" in iCol: return sns.xkcd_rgb["dark sage"]#["golden yellow"]
    if "BioEnergy3 CCS50" in iCol: return sns.xkcd_rgb["flat blue"]#greens[7]
    if "BioEnergy3 CCS75" in iCol: return sns.xkcd_rgb["dark lavender"]#pairs[9]#blues[8]

    return pairs[1]

def set_timer():
    return timeit.default_timer()

def stop_timer(start_time=0):
    run_time = round(timeit.default_timer()-start_time,1) #elapsed time in seconds
    if run_time <= 60:
        print "Run Time = ",run_time," sec"
    else:
        print "Run Time = ",int(run_time/60),"min",int(run_time%60),"sec"

def get_linewidth(scenario_name=""):
    if "Historical" in scenario_name: return 2.0
    elif "noRange" in scenario_name: return 2.0
    elif "Fossil" in scenario_name: return 1.5
    elif "BAU" in scenario_name: return 1.5
    return 1.5

def scenario_switch(scenario_name,plot_set="",print_hidden_scen=False):
    
    if plot_set == "Char":
        return True
        if scenario_name == "BAU": return True
        if scenario_name == "BioEnergy": return True
        if scenario_name == "HistoricalData": return True

        if scenario_name == "CharLS": return True
        if scenario_name == "CharHS": return True
        if scenario_name == "GasLS":  return True
        if scenario_name == "GasHS":  return True
        if scenario_name == "BioEnergy CCS25": return True
        
        if print_hidden_scen == True: 
            print "**"+scenario_name
        return False

    if plot_set == "SI":
        if scenario_name == "BAU": return True
        if scenario_name == "BioEnergy": return False
        if scenario_name == "HistoricalData": return True
        #if "CCS" in scenario_name: return True
        else: return False

    if (plot_set == "CCS" 
        or plot_set == "Land for Animal Food"
        or "Vegetal Food Yield" in plot_set  
        or "FAO" in plot_set):

        if (plot_set == "Land for Animal Food"
            or "Vegetal Food Yield" in plot_set  
            or "FAO" in plot_set): alt_switch = True
        else: alt_switch = False

        if scenario_name == "HistoricalData": return True
        #
        if scenario_name == "BAU": return True
        if scenario_name == "CCS": return True
        if scenario_name == "BioChar": return False
        #
        if scenario_name == "BioEnergy": return True
        if scenario_name == "BioEnergy CCS": return False
        if scenario_name == "BioEnergy BioChar": return False
        if scenario_name == "BioEnergy 10NDD": return False
        #
        if scenario_name == "Alg-Fuel": return True
        if scenario_name == "Alg-Fuel CCS":
            if alt_switch == False: return True
            else: return False
        if scenario_name == "Alg-Fuel BioChar": return False
        if scenario_name == "Alg-Feed" or scenario_name == "Alg-FuelFeed":
            if alt_switch == False: return True
            else: return True
        if "Alg-Feed CCS" in scenario_name or scenario_name == "Alg-FuelFeed CCS":
            if alt_switch == False: return True
            else: return False
    
    #####
    if print_hidden_scen == True: print "**"+scenario_name
    return False

#################

def get_y_offset(val_history, new_y_val, min_offset):

    return new_y_val
    
    val_history.sort()
    tempY = new_y_val
    for iVal in range(len(val_history)):
        if len(val_history) > 1 and tempY == val_history[iVal]: return -100
        if (abs(tempY - val_history[iVal])) < min_offset: 
            if tempY - val_history[iVal] < 0:
                tempY = tempY -  min_offset
            else: tempY = val_history[iVal] + min_offset
    
    val_history.append(tempY)
    val_history.sort()
        
    return tempY

#################

def new_y_offset(in_vals, min_offset=0, group_offset=0):
    # Works if you start from the top and print down:
    total_fuels = len(in_vals)-1
    iFuel = -1
    
    while total_fuels > 0:
        in_vals[iFuel] = in_vals[iFuel] + group_offset
        gap = in_vals[iFuel] - in_vals[iFuel-1]

        if gap < min_offset:
            in_vals[iFuel-1] = in_vals[iFuel]-min_offset

        iFuel = iFuel-1
        total_fuels = total_fuels-1
    
##################

def standardize_scenario_names(list_scenarios,var=""):

    if var=="char":
        for iName in range(len(list_scenarios)):
            list_scenarios[iName] = list_scenarios[iName].replace("_"," ")
            list_scenarios[iName] = list_scenarios[iName].replace("HS","")
            list_scenarios[iName] = list_scenarios[iName].replace("LS","")
            list_scenarios[iName] = list_scenarios[iName].replace("char","(Char)")
            list_scenarios[iName] = list_scenarios[iName].replace("gas","(Gas)")
            list_scenarios[iName] = list_scenarios[iName].replace("BEplus1","Low Bio")
            list_scenarios[iName] = list_scenarios[iName].replace("BEplus2","Med Bio")
            list_scenarios[iName] = list_scenarios[iName].replace("BEplus3","High Bio")
            #if ("Char" not in list_scenarios[iName] 
            #    and list_scenarios[iName] != "" 
            #    and list_scenarios[iName][-1] != ")"
            #    and "Historical" not in list_scenarios[iName]): 
            #    list_scenarios[iName] = list_scenarios[iName]+" (Cmb)"
        
    else:
        for iName in range(len(list_scenarios)):
            #if list_scenarios[iName] == "GasLS": list_scenarios[iName] = "Gasification"
            #if list_scenarios[iName] == "CharLS": list_scenarios[iName] = "BioChar"        
            if "_" in list_scenarios[iName]: list_scenarios[iName] = list_scenarios[iName].replace("_"," ")
            if "gas" in list_scenarios[iName]: list_scenarios[iName] = list_scenarios[iName].replace("gas","gas")
            if "CCS" in list_scenarios[iName]: list_scenarios[iName] = list_scenarios[iName].replace("_CCS"," & CCS")
            if "BEplus" in list_scenarios[iName]: list_scenarios[iName] = list_scenarios[iName].replace("BEplus","BioEnergy")
            if "BAU & CCS" in list_scenarios[iName]: list_scenarios[iName] = list_scenarios[iName].replace("BAU & ","")
            if "AlgaeFeed" in list_scenarios[iName]: list_scenarios[iName] = list_scenarios[iName].replace("AlgaeFeed","Alg-Feed")
            if "Algae Feed" in list_scenarios[iName]: list_scenarios[iName] = list_scenarios[iName].replace("Algae Feed","Alg-Feed")
            elif "AlgaeFuel" in list_scenarios[iName]: list_scenarios[iName] = list_scenarios[iName].replace("AlgaeFuel","Alg-Fuel")
            elif "Algae" in list_scenarios[iName]: list_scenarios[iName] = list_scenarios[iName].replace("Algae","Alg-Fuel")
        
###################

def char_colors(iCol):
    if iCol == "FossilBAU 3C": return sns_s1[0]
    if iCol == "BAU 3C": return sns_s1[1]
    if "Bio 3C" in iCol: return sns_s1[2]
    if "Bio (Char) 3C" in iCol: return sns_s1[3]
    if "Bio Alg40 (Char) 3C" in iCol: return sns_s1[4]
    if "Bio Alg40 BECCS75 3C" in iCol: return sns_s1[5]
    if "Bio Alg40 3C" in iCol: return sns_s1[6]
    if "Bio BECCS75 3C" in iCol: return sns_s1[7]
    #if iCol == "High BM (Gas)": return sns_s1[8]
    #if iCol == "High BM (Cmb)": return greens[8]
    else: 
        print "\nNo color assigned to",iCol
        return browns[2]

def get_color(iCol):

    if iCol == "animal_dmd": return browns[2]
    if iCol == "vegetal_dmd": return greens[5]
    if iCol == "animal_hd": return browns[0]
    if iCol == "vegetal_hd": return greens[8]   
    #
    if iCol == "water_dmd": return pairs[9]
    if iCol == "water_sup": return pairs[1]

    if iCol == "other": return pairs[10]
    if iCol == "forest": return pairs[2]
    if iCol == "agriculture": return pairs[6]
    if iCol == "other_hd": return pairs[11]
    if iCol == "forest_hd": return pairs[3]
    if iCol == "agriculture_hd": return pairs[7]
    #
    # First Set of Scenarios
    #
    if iCol == "Population": return browns[3]
    if iCol == "GLOBIOM": return greys[4]
    if iCol == "errrng_afchar": return greens[5]
    #
    #BioChar scenarios
    if iCol == "GasLS":              return greens[4]
    if iCol == "GasHS":              return greens[5]
    if iCol == "CharLS":             return greens[6]
    if iCol == "CharHS":             return greens[8]
    if iCol == "BioEnergy CCS25":    return sns.xkcd_rgb["golden yellow"]
    if iCol == "BioEnergy AF":       return sns.xkcd_rgb["denim blue"]
    if iCol == "BioEnergy CCS25 AF": return dark2[4]

    #Colorful Scheme
    #if iCol == "BAU": return pairs[5]
    #if iCol == "CCS": return pairs[1]
    #if iCol == "BioChar": return pairs[4]
    #
    #if iCol == "BioEnergy": return pairs[7]
    #if iCol == "BioEnergy CCS": return pairs[3]
    #if iCol == "BioEnergy BioChar": return pairs[6]
    #if iCol == "BioEnergy 10NDD": return pairs[2]
    #
    #if iCol == "Alg-Fuel": return sns_s2[5]
    #if iCol == "Alg-Feed": return blues[8]
    #if iCol == "Alg-Fuel CCS": return greens[7]
    #if iCol == "Alg BioChar": return greens[3]
    #if iCol == "Alg-Feed CCS": return pairs[9]#blues[8]
    # pairs[9] = dark purple
    #
    if iCol == "BAU" or iCol == "errrng_bau": return sns.xkcd_rgb["pale red"]#sns_s1[0]
    if iCol == "CCS": return sns.xkcd_rgb["denim blue"]#blues[7]
    if iCol == "BioEnergy": return sns_s1[4]
    if iCol == "Alg-Fuel": return sns.xkcd_rgb["golden yellow"]#sns_s2[5]
    if iCol == "Alg-Feed" or iCol == "errrng_af1": return dark2[4]
    #
    if iCol == "BioEnergy CCS25": return pairs[0]
    if iCol == "BioEnergy CCS50": return greens[7]
    if iCol == "BioEnergy CCS75" or iCol == "errrng_afc": return pairs[9]#blues[8]
    if iCol == "Alg-Feed CCS25": return pairs[0]
    if iCol == "Alg-Feed CCS50": return greens[7]
    if iCol == "Alg-Feed CCS75" or iCol == "errrng_afc": return pairs[9]#blues[8]
    #
    if "Historical" in iCol: return greys[6]
    #
    if "2.6" in iCol: return sns.color_palette()[1]
    elif "4.5" in iCol: return sns.color_palette()[0]
    elif "6.0" in iCol: return sns.color_palette()[4]
    elif "8.5" in iCol: return sns.color_palette()[2]
    #
    if "labBiomass" in iCol:   return dark2[4]
    elif "Biomass" in iCol:    return sns_s3[6]
    elif "Algae" in iCol:      return greens[7]
    elif "labAlgae" in iCol:   return greens[8]
    elif "labSolar" in iCol:   return sns_s1[7]
    elif "Solar" in iCol:      return sns_s3[7]
    elif "labWind" in iCol:    return blues[7]#sns_s1[3] 
    elif "Wind" in iCol:       return sns_s3[4]#sns_s3[2]
    elif "labCoal" in iCol:    return greys[6]#blues[7]
    elif "Coal" in iCol:       return greys[4]#sns_s3[4] 
    elif "labGas" in iCol:     return sns_s1[0] 
    elif "Gas" in iCol:        return sns_s3[3]
    elif "labNuclear" in iCol: return dark2[6] 
    elif "Nuclear" in iCol:    return sns_s3[1]
    elif "labOil" in iCol:     return sns_s1[4]  
    elif "Oil" in iCol:        return sns_s3[5]

    #if "Biomass" in iCol:   return greens[6]
    #elif "Algae" in iCol:   return greens[8]
    #elif "Solar" in iCol:   return sns_s1[7]
    #elif "Wind" in iCol:    return sns_s1[3] 
    #elif "Coal" in iCol:    return sns_s1[8]
    #elif "Gas" in iCol:     return red_to_green[0] 
    #elif "Nuclear" in iCol: return sns_s3[4]
    #elif "Oil" in iCol:     return browns[0]

    #
    return pairs[0]

def get_population_coloring(pCol = 0.0):
    
    if pCol >= 1.50: return sns_rgp[0]
    if pCol >= 1.45: return sns_rgp[1]
    if pCol >= 1.40: return sns_rgp[2]
    if pCol >= 1.35: return sns_rgp[3]
    if pCol >= 1.30: return sns_rgp[4]
    if pCol >= 1.25: return sns_rgp[5]
    if pCol >= 1.20: return sns_rgp[6]
    if pCol >= 1.15: return sns_rgp[7]
    if pCol >= 1.10: return sns_rgp[8]
    if pCol >= 1.05: return sns_rgp[9]
    if pCol < 1.05 and pCol >=0.9999: return sns_rgp[10]
    else: return greys[0]
