from pylab import *
import csv

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

FXhandles = []
FXdict = {}

SChandles = [[] for i in range(len(files_to_compile))]

fragments = [[] for i in range(50)]
header_array = []

for file_idx, aFile in enumerate(files_to_compile):

    wholeFile = in_file_name+aFile

    with open(wholeFile) as f: 
        reader = csv.reader(f)

        title_holder = ""
        rowIdx = -1

        for row in reader: 
            rowIdx += 1
            
            row = str(row).replace("[","").replace("]","").replace("\\t",";").replace("'","").split(";")
            if row[-1] == "": row.pop(-1)

            #Only copy down years once
            if rowIdx == 0:
                if file_idx == 0:            
                    header_array.append(row)
                else: 
                    continue
                
            # Append Scenario names to the end of the second row
            elif rowIdx == 1:
                    
                if file_idx == 0: 
                    header_array.append([])
                    for iScen in row[:-1]: 
                        header_array[1].append(iScen)
                        SChandles[file_idx].append(iScen)

                elif file_idx == len(files_to_compile)-1: 
                    for iScen in row[2:]: 
                        header_array[1].append(iScen)
                        SChandles[file_idx].append(iScen)

                else: 
                    for iScen in row[2:-1]: 
                        header_array[1].append(iScen)
                        SChandles[file_idx].append(iScen)

                continue

            else:
                #print file_idx, row
                if row[0][:3] != " : ": 
                    title_holder = row[0]

                    #HACK: Changed "C Captured & Stored" to "C in Storage"
                    if title_holder == "C Captured & Stored": 
                        title_holder = "C in Storage"
                        row[0] = "C in Storage"

                    if file_idx == 0:
                                           
                        FXhandles.append(title_holder)
                        FXdict[title_holder] = len(FXhandles)-1
                        
                        fragments[FXdict[title_holder]].append(row)
                    else: continue

                elif "HistoricalData" in row[0] and file_idx != len(files_to_compile)-1:
                    continue

                else: fragments[FXdict[title_holder]].append(row)
 
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
