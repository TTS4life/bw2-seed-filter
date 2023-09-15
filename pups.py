#!/usr/bin/python3

def rngAdvance(prev):
	next= 0x5D588B656C078965 * prev + 0x0000000000269EC3
	return next%0x10000000000000000

def rngOf(seed,frame):
	prev=seed
	for x in range(0,frame):
		prev=rngAdvance(prev)
	return prev

natures=['Hardy','Lonely','Brave','Adamant','Naughty','Bold','Docile','Relaxed','Impish','Lax','Timid','Hasty','Serious','Jolly','Naive','Modest','Mild','Quiet','Bashful','Rash','Calm','Gentle','Sassy','Careful','Quirky']

def getLandSlot(sel):
    parts=[20, 40, 50, 60, 70, 80, 85, 90, 94, 98, 99, 100]
    for x in range(0,12):
        if sel<parts[x]:
            return x

def pokeGen(seed,frame):
	trigger = rngOf(seed,frame+2)
	slot = rngAdvance(trigger)
	ability = rngAdvance(slot)
	ability = rngAdvance(ability)
	pokenat = rngAdvance(ability)
	isEncounter = int((((trigger>>32)*0xFFFF)>>32)/0x290)
	if isEncounter < 14:
		appear = True
	else:
		appear = False
	sel =((slot>>32)*100)>>32
	natsel = ((pokenat>>32)*25)>>32
	ability = ((ability>>32^0x10000^0x80000000)>>16)&1
	return [appear,frame,isEncounter,getLandSlot(sel),natures[natsel],ability]

badDates=[[],[],[],[],[1,2,3,4,9,10,13,14,19,20,24,30],[],[],[],[1,2,8,9,10,11,18,19,23,24,29,30],[],[],[],[1,2,3,8,9,12,13,14,18,22,23,24,29,30]]

def pickup(seed, initial_frame):
    pickup = []

    for i in range(260):
        seed = rngAdvance(seed)

    for i in range(261, 700):
        seed = rngAdvance(seed)
        tmp1 = (seed >> 32) * 100
        tmp2 = (tmp1 >> 32)

        # print(i, tmp2)

        if(tmp2 < 10):
            next_frame = rngAdvance(seed)
            tmp1 = (next_frame >> 32) * 100
            tmp2 = (tmp1 >> 32)

            if(tmp2 == 98):
                pickup.append([f"{i}", tmp2])
    return pickup

def getPups(seed, initial_frame):
    
    cur_seed = rngOf(seed, initial_frame)
    pups = []
    for x in range(initial_frame + 10, initial_frame + 40):
        res = pokeGen(cur_seed, x)


        
        if(res[0]                       #encounterable
            and res[3] in [9,11]        #encounter slots
            and res[4] == "Adamant"     #nature
            and res[-1] == 1):          #ability

            pups.append(f"{res[1]} {res[-2:]}")
        
        cur_seed = rngAdvance(seed)

    return pups

table = [[50, 100, 100, 100], [50, 50, 100, 100], [30, 50, 100, 100],[25, 30, 50, 100], [20, 25, 33, 50]]

def advance_table(prng):
    count = 0
    for i in range(5):
        for j in range(4):
            if table[i][j] == 100:
                break

            count += 1
            prng = rngAdvance(prng)
            rand = ((prng >> 32) * 101) >> 32
            if rand <= table[i][j]:
                break

    return prng, count

def initial_frame_bw(prng):
    count = 0

    for i in range(5):
        prng, num = advance_table(prng)
        count += num

    return count
          

def main(infile, outfile):
    seedLst = open(infile, "r+", encoding = "UTF-8")
    output = open(outfile,"w",encoding = "UTF-8")
    for line in seedLst:
        parsed = line.split("\t")
        seed = int(parsed[0],16)
        seed = rngAdvance(seed)
        year = parsed[1]
        year = int(year)%100
        keys = parsed[19].strip()
        timestr = parsed[1] + "/"+parsed[2]+"/"+parsed[3]+" "+"{:02d}".format(int(parsed[4]))+":"+"{:02d}".format(int(parsed[5]))+":"+"{:02d}".format(int(parsed[6]))
        timer0 = parsed[8]
        ivs = [parsed[12],parsed[13],parsed[14],parsed[15],parsed[16],parsed[17]]
        if keys[0] == " ":
            continue

        initial_frame = initial_frame_bw(seed)


        month = int(parsed[2])
        if month % 4 != 0:
            continue
        date = int(parsed[3])
        if date in badDates[month]:
            continue

        pickups = pickup(seed, initial_frame)
        if len(pickups) == 0:
            continue

        pups = getPups(seed, initial_frame)
        if(len(pups) == 0):
            continue


        output.write("Seed: "+hex(seed)[2:]+"\n")
        output.write("Time: "+timestr+"\n")
        output.write("Timer0: "+timer0+"\n")
        output.write("Keypresses: "+keys+"\n")
        output.write("IVs: "+str(ivs)+"\n")
        output.write("Initial Frame: "+str(initial_frame)+"\n")
        output.write("Lillipups: \n")
        for x in pups:
            output.write(f"{str(pups)}\n")

        output.write("Pickup: ")
        for x in pickups:
            output.write(f"{str(x)} \n")
        output.write("\n")
        output.write("\n\n")

    seedLst.close()
    output.close()

if __name__ == '__main__':    

    in_file = input("file to read: ")
    out_file = input("file to write results to: ")
    main(in_file, out_file)