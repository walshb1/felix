from pylab import *
import csv

# This file can combine separate Vensim output files of any sort, as long as they are all in the "Table" (NOT time table) format
# There are a few conditions:
# - The first scenario in each file should be the same. I have used "Fossil_BAU", but you can use any scenario. 
# - This was a good solution for the fact that the output file doesn't treat the first scenario exacty the same as the rest.
# - Historical Data should be the last scenario in each file.
# - This would be easy to change below if you want to get 15 (up from 14) scenarios in each file.

# To use this, put it in the same folder as the files you want to combine. Set in_file_name to the root name (the portion of the file 
# - name that all the files have in common; can also be ""). Change files_to_compile to list each of the files you want to combine. I 
# - left 4 examples of file sets that I used. 

in_file_name = "emissions_table_"
files_to_compile = ["6_BAU.txt","6_BE.txt","6_BE_3C.txt","6_BE12.txt","6_BE3.txt","6_BE3_3C.txt",
                    "7_CCS4080_1.txt","7_CCS4080_2.txt","7_CCS4080_3.txt","7_CCS4080_4.txt","7_altRCPs.txt"]

#in_file_name = "energy_table_"
#files_to_compile = ["6_BAU.txt","6_BE.txt","6_BE_3C.txt","6_BE12.txt","6_BE3.txt","6_BE3_3C.txt",
#                    "7_CCS4080_1.txt","7_CCS4080_2.txt","7_CCS4080_3.txt","7_CCS4080_4.txt"]

#in_file_name = "land_table_"
#files_to_compile = [".txt"]

#in_file_name = "emissions_table_fluxes_"
#files_to_compile = ["25C.txt","3C.txt"]

# Define empty, global arrays to collect and store the info from each file.
FXhandles = []
FXdict = {}

SChandles = [[] for i in range(len(files_to_compile))]

fragments = [[] for i in range(50)]
header_array = []

# Start loop over files...
for file_idx, aFile in enumerate(files_to_compile):

    # Put file name back together
    wholeFile = in_file_name+aFile

    # Open that file
    with open(wholeFile) as f: 
        reader = csv.reader(f)

        title_holder = ""
        rowIdx = -1

        # Loop over rows
        for row in reader: 
            rowIdx += 1
            
            # Row will be read as string, and each entry is separated by a semicolon
            row = str(row).replace("[","").replace("]","").replace("\\t",";").replace("'","").split(";")
            if row[-1] == "": row.pop(-1)

            # The first row of each file is the list of years for which the simulation was run. 
            # - Only copy down years once -- you're going to have big issues if different scenarios run over unique year ranges.
            # - years stored in header_array[0]
            if rowIdx == 0:
                if file_idx == 0:            
                    header_array.append(row)
                else: 
                    continue
            
            # Scenarios included in each file will be listed in the second row of each file
            # - scenarios stored in header_array[1]
            elif rowIdx == 1:
                    
                # First file: append every scenario name except the last
                if file_idx == 0: 
                    header_array.append([])
                    for iScen in row[:-1]: 
                        header_array[1].append(iScen)
                        SChandles[file_idx].append(iScen)
  
                # Last file: store all scenario names except the first
                elif file_idx == len(files_to_compile)-1: 
                    for iScen in row[2:]: 
                        header_array[1].append(iScen)
                        SChandles[file_idx].append(iScen)

                # Files 2 through n-1: store all scenario names except the first and the last
                else: 
                    for iScen in row[2:-1]: 
                        header_array[1].append(iScen)
                        SChandles[file_idx].append(iScen)

                continue

            # Main body of each FeliX output handle gets processed here
            else:
                # This grabs the name of the output handle (e.g. "Temperature Anomaly", "C in Atmosphere", etc.)
                if row[0][:3] != " : ": 
                    title_holder = row[0]

                    #HACK: Changed "C Captured & Stored" to "C in Storage" in FeliX
                    if title_holder == "C Captured & Stored": 
                        title_holder = "C in Storage"
                        row[0] = "C in Storage"

                    # For first file, append title_holder to FXhandles array and set its FXdict correspondent to its index in this array 
                    if file_idx == 0:
                                           
                        FXhandles.append(title_holder)
                        FXdict[title_holder] = len(FXhandles)-1
                        
                        # This is where all the work is done--fragments is a 2D array
                        # - accepts the index value corresponding to each title_holder as an argument
                        # - stores all the values [1900-2100] associated with each scenario
                        fragments[FXdict[title_holder]].append(row)
                    else: continue

                # Don't record historical data until the last file//because it appears in every file
                elif "HistoricalData" in row[0] and file_idx != len(files_to_compile)-1:
                    continue

                # Catch all the files that aren't the first or the last
                else: fragments[FXdict[title_holder]].append(row)
 
# Open new file to write out compiled data
compiled_file = open(in_file_name[:-1]+".csv", 'w')

for row in header_array:
    output_str = ""
    for item in row:
        output_str += str(item)+","

    compiled_file.write(output_str[:-1]+"\n")
    
# Loop over Felix handles
print "Compiling the following:"
for aFrag in fragments:

    if len(aFrag) == 0: continue
    print " ",aFrag[0][0]

    # Loop over scenario outputs
    for aFraggle in aFrag:

        output_str = ""

        #Loop over years
        for aFraggleito in aFraggle:
            output_str += str(aFraggleito)+","

        compiled_file.write(output_str[:-1]+"\n")

compiled_file.close()
