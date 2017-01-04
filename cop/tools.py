cumEM_x_ax_val_dict = {
    "FossilBAU 3C":1.7,
    "BAU 3C":2.7,
    "BioEnergy 3C":3.7,
    "BioEnergy CCS40p 3C":4.7,
    "BioEnergy CCS80p 3C":5.7,
    "BioEnergy3 3C":6.7,
    "BioEnergy3 CCS40p 3C":7.7,
    "BioEnergy3 CCS80p 3C":8.7
    }

def legend_fliparoo(h,l,start_pos):

    newh2 = []
    newl2 = []

    switch_ord = [0,2,4,1,3,5]

    for ih in h[:start_pos]:
        newh2.append(ih)

    for il in l[:start_pos]:
        newl2.append(il)

    for ix in switch_ord:
        newh2.append(h[start_pos+ix])
        newl2.append(l[start_pos+ix])

    for ih in h[start_pos+6:]:
        newh2.append(ih)

    for il in l[start_pos+6:]:
        newl2.append(il)       

    return newh2, newl2
