import os

dir = os.getcwd()
path = dir+"\\search.txt"

def rngAdvance(prev):
	next=0x5D588B656C078965 * prev + 0x0000000000269EC3
	return next%0x10000000000000000

def rngOf(seed,frame):
	prev=seed
	for x in range(0,frame):
		prev=rngAdvance(prev)
	return prev

natures=['Hardy','Lonely','Brave','Adamant','Naughty','Bold','Docile','Relaxed','Impish','Lax','Timid','Hasty','Serious','Jolly','Naive','Modest','Mild','Quiet','Bashful','Rash','Calm','Gentle','Sassy','Careful','Quirky']
badDates=[[],[3,4,5,11,12,13,20,21,27,28,29],[],[4,5,12,13,20,21,28,29],[1,2,3,4,5,9,10,11,13,14,18,19,20,21,22,25,28,30],[3,4,5,11,12,13,20,21,27,28,29],[],[4,5,12,13,20,21,28,29],[1,2,3,5,8,9,10,11,14,18,19,21,22,25,28,30,31],[3,4,5,11,12,13,20,21,27,28,29],[],[4,5,12,13,20,21,28,29],[1,2,3,5,8,9,11,14,18,21,22,25,28,30,31]]
def getLandSlot(sel):
    parts=[20, 40, 50, 60, 70, 80, 85, 90, 94, 98, 99, 100]
    for x in range(0,12):
        if sel<parts[x]:
            return x

def dustGen(seed,frame):
    trigger = rngOf(seed,frame+2)
    slot = rngAdvance(trigger)
    slot = rngAdvance(slot)
    ability = rngAdvance(slot)
    ability = rngAdvance(ability)
    pokenat = rngAdvance(ability)
    isEncounter = int((((trigger>>32)*1000)>>32))
    if isEncounter <400:
        appear = True
    else:
        appear = False
    sel =((slot>>32)*100)>>32
    natsel = ((pokenat>>32)*25)>>32
    id = ability>>32^0x10000^0x80000000
    ability = id>>16&1
    gender = (id&255)
    return [appear,frame,isEncounter,getLandSlot(sel),natures[natsel],ability,gender]

def drilSearch(seed,min,max):
    drills=[]
    for x in range(min,max+1):
        poke = dustGen(seed,x)
        if poke[0] == True and poke[3] in [6,7,8,9,10,11] and poke[5]==1 and poke[5]<128 and poke[4]=="Adamant":
            drills.append(poke)
    return drills

ptable = [[50,100,100,100,100],[50,50,100,100,100],[30,50,100,100,100],[25,30,50,100,100],[20,25,33,50,100],[100,100,100,100,100]]

def getInitialFrame(seed):
    fc = 0
    for x in range (0,5):
        for y in range(0,6):
            for z in range (0,5):
                if ptable[y][z] == 100:
                    break
                fc+=1
                seed=rngAdvance(seed)
                rng = seed>>32
                rng = rng*101
                rng = rng>>32
                if rng <= ptable[y][z]:
                    break
        if x == 0:
            adv = 3
            for j in range (0,adv):
                fc+=1
                seed = rngAdvance(seed)
    fc = extra(seed,fc)
    return fc




def extra(seed,fc):
    loop = True
    limit = 0
    while loop and limit<100:
        loop = False
        tmp = [0,0,0]
        fc+=3
        for x in range (0,3):
            seed = rngAdvance(seed)
            rng = seed>>32
            rng = rng*15
            rng = rng>>32
            tmp[x] = rng
        for i in range (0,3):
            for j in range (0,3):
                if i==j:
                    continue
                if tmp[i] == tmp[j]:
                    loop = True
        limit+=1
    return fc


def dustSearch(seed,min,max):
    clouds = []
    rng = rngOf(seed,min-1)
    for x in range(min,max+1):
        rng = rngAdvance(rng)
        if rng>>60 == 0:
            clouds.append(x)
    return clouds


outputDir=dir+"\\drilbur.txt"
seedLst = open(path, "r+", encoding = "UTF-8")
output = open(outputDir,"w",encoding = "UTF-8")
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
    init = getInitialFrame(seed)
    month = int(parsed[2])
    if month in [2,6,10]:
        continue
    date = int(parsed[3])
    if date in badDates[month]:
        continue

    dusts = dustSearch(seed,init+26,init+30)
    if len(dusts) == 0:
        continue
    else:
        drills = drilSearch(seed,dusts[0]+4,dusts[0]+20)
        if len(drills) == 0:
            continue
        else:
            output.write("Seed: "+hex(seed)[2:]+"\n")
            output.write("Time: "+timestr+"\n")
            output.write("Timer0: "+timer0+"\n")
            output.write("Keypresses: "+keys+"\n")
            output.write("IVs: "+str(ivs)+"\n")
            output.write("Initial PIDRNG Frame: " + str(init)+"\n")
            output.write("Dust Clouds: ")
            for x in dusts:
                output.write(str(x)+" ")
            output.write("\n")
            output.write("Drilburs: ")
            for x in drills:
                output.write(str(x[1])+" ")
            output.write("\n\n")
seedLst.close()
output.close()