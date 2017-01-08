# This file contains info from the IIASA RCP database, and is intended to compare to Felix model calibration and results. 

#EDGAR Emissions Data
#Reference: Olivier, J.G.J., Janssens-Maenhout, G., Muntean, M. Peters, J.H.A.W., Trends in global CO2 emissions - 2014 report, JRC report 93171 / PBL report 1490; ISBN 978-94-91506-87-1, December 2014 
edgar_em_year = [  1990,  1995,   2000,   2005,   2010,   2011,   2012,    2013]
edgar_em_data = [22.667, 23.619, 25.361, 29.346, 32.992, 34.009, 34.576, 35.274]

# RCP Info
rcp_time = [ 2000, 2005, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100 ]
rcp_hist_time = [ 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2005 ]
#
#########
#RCP Database (Version 2.0.5)
rcp_hist_ppm = [ 295.800, 299.700, 303.025, 307.225, 310.375, 310.750, 316.273, 324.985, 338.360, 353.855, 368.865, 378.813 ]
rcp_hist_em = [ 1.187, 1.641, 1.653, 1.949, 2.066, 2.522, 3.769, 5.273, 6.357, 7.463, 7.884, 9.167 ]
#
#########
#RCP Database (Version 2.0.5)
rcp_ppm_26 = [ 368.865, 378.813, 389.285, 412.068, 430.783, 440.222, 442.700, 441.673, 437.481, 431.617, 426.005, 420.895 ]
rcp_ppm_45 = [ 368.865, 378.813, 389.128, 411.129, 435.046, 460.845, 486.535, 508.871, 524.302, 531.138, 533.741, 538.358 ]
rcp_ppm_60 = [ 368.865, 378.813, 389.072, 409.360, 428.876, 450.698, 477.670, 510.634, 549.820, 594.257, 635.649, 669.723 ]
rcp_ppm_85 = [ 368.865, 378.813, 389.324, 415.780, 448.835, 489.435, 540.543, 603.520, 677.078, 758.182, 844.805, 935.874 ]
#
#########
#RCP Database (Version 2.0.5)
rcp_em_26 = [ 7.884, 9.167, 9.878, 10.260, 7.946, 5.024, 3.387, 2.035, 0.654, 0.117, -0.269, -0.420 ]
rcp_em_45 = [ 7.884, 9.167, 9.518, 10.212, 11.170, 11.537, 11.280, 9.585, 7.222, 4.190, 4.220, 4.249 ]
rcp_em_60 = [ 7.884, 9.167, 9.389, 9.357, 9.438, 10.840, 12.580, 14.566, 16.477, 17.525, 14.556, 13.935 ]
rcp_em_85 = [ 7.884, 9.167, 9.969, 12.444, 14.554, 17.432, 20.781, 24.097, 26.374, 27.715, 28.531, 28.817 ]

# Cumulative emissions (1900-2000) calculated assuming linear growth from data point to data point above (rcp_hist_em)
rcp_cum_em_hist = 372.285
felix_cum_em_1900to2000 = 355.40
#FeliX pre-1900: 46.35;
#FeliX 1900-2000: 401.748-46.35 = 355.40

# Cumulative emissions (2000-2100) calculated assuming linear growth from data point to data point above
rcp_cum_em_26 = 429.065
rcp_cum_em_45 = 852.33
rcp_cum_em_60 = 1259.0225
rcp_cum_em_85 = 2003.6725

# This is from DvV's "The role of negative CO2 emissions for reaching 2C-insights from integrated assessment modeling"
# Climactic Change 2013
cum_em_sub_2C = 436.3

#########
#RCP Database (Version 2.0.5)
#generated: 2016-02-24 17:36:22
rcp_ff_26 = [6.735, 7.971, 8.821,  9.288,  7.157,  4.535,  3.186,  1.419,  0.116, -0.433, -0.870, -0.931]
rcp_ff_45 = [6.735, 7.971, 8.607,  9.872, 10.953, 11.338, 11.031,  9.401,  7.118,  4.182,  4.193,  4.203]
rcp_ff_60 = [6.735, 7.971, 8.512,  8.950,  9.995, 11.554, 13.044, 14.824, 16.506, 17.281, 14.313, 13.753]
rcp_ff_85 = [6.735, 7.971, 8.926, 11.538, 13.839, 16.787, 20.205, 23.596, 25.962, 27.406, 28.337, 28.740]

rcp_luc_26 = [1.149, 1.196, 1.056, 0.973,  0.789,  0.489,  0.201,  0.615,  0.538, 0.550, 0.602, 0.511]
rcp_luc_45 = [1.149, 1.196, 0.911, 0.341,  0.216,  0.199,  0.249,  0.184,  0.104, 0.008, 0.027, 0.046]
rcp_luc_60 = [1.149, 1.196, 0.877, 0.406, -0.557, -0.714, -0.464, -0.258, -0.029, 0.244, 0.242, 0.181]
rcp_luc_85 = [1.149, 1.196, 1.044, 0.906,  0.715,  0.645,  0.576,  0.501,  0.412, 0.309, 0.194, 0.077]

rcp_luc_cum_26 = [125.065, 130.9275, 136.5575, 146.7025, 155.5125, 161.9025, 165.3525, 169.4325, 175.1975, 180.6375, 186.3975, 191.9625]
rcp_luc_cum_45 = [125.065, 130.9275, 136.3925, 143.0475, 145.8325, 147.9075, 150.1475, 152.3125, 153.7525, 154.3125, 154.4875, 154.8525]
rcp_luc_cum_60 = [125.065, 130.9275, 136.11,   142.525,  141.77,   135.415,  129.525,  125.915,  124.48,   125.555,  127.985,  130.1]
rcp_luc_cum_85 = [125.065, 130.9275, 136.5275, 146.2775, 154.3825, 161.1825, 167.2875, 172.6725, 177.2375, 180.8425, 183.3575, 184.7125]

rcp_h_time_lulucf = [1860, 1870, 1880, 1890, 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2005]
rcp_h_ann_lulucf = [0.454, 0.519, 0.469, 0.612, 0.612, 0.653, 0.822, 0.721, 0.896, 0.767, 0.892, 1.192, 1.197, 1.025, 1.149, 1.196]
rcp_h_cum_lulucf = [4.865, 9.805, 15.255, 21.42, 27.745, 35.12, 42.835, 50.92, 59.235, 67.53, 77.95, 89.895, 101.005, 112.725, 125.065, 130.9275]

#############
#RCP Database (Version 2.0.5)
rcp_for_tot_60 = [1.723, 1.901, 2.089, 2.480, 2.854, 3.146, 3.521, 3.905, 4.443, 4.932, 5.255, 5.481]
rcp_for_tot_45 = [1.723, 1.905, 2.126, 2.579, 3.005, 3.411, 3.766, 4.021, 4.188, 4.256, 4.265, 4.309]
rcp_for_tot_26 = [1.723, 1.904, 2.129, 2.584, 2.862, 2.999, 2.998, 2.918, 2.854, 2.808, 2.759, 2.714]
rcp_for_tot_85 = [1.723, 1.906, 2.154, 2.665, 3.276, 3.993, 4.762, 5.539, 6.299, 7.020, 7.742, 8.388]

# These figures come from WG1 Table SPM.2
#             [ Low, Med, High]
rcp_temp_26 = [ 0.9, 1.6, 2.3 ]
rcp_temp_45 = [ 1.7, 2.4, 3.2 ]
rcp_temp_60 = [ 2.0, 2.8, 3.7 ]
rcp_temp_85 = [ 3.2, 4.3, 5.4 ] 
