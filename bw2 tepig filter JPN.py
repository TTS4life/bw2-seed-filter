#!/usr/bin/python3
import os

dir = os.getcwd()
path = dir+"/result.txt"

frame_entering_route20 = 430
frame_exiting_route20 = 490
frame_entering_ranch = 530
frame_exiting_ranch = 620


def rngAdvance(prev):
	next=0x5D588B656C078965 * prev + 0x0000000000269EC3
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
	if isEncounter <20:
		appear = True
	else:
		appear = False
	sel =((slot>>32)*100)>>32
	natsel = ((pokenat>>32)*25)>>32
	ability = ((ability>>32^0x10000^0x80000000)>>16)&1
	return [appear,frame,isEncounter,getLandSlot(sel),natures[natsel],ability]

def getBirds(seed):
	table1 = ["lv2 pidove","lv2 sewaddle","lv3 patrat", "lv3 purrloin", "lv3 patrat", "lv3 sewaddle", "lv4 pidove", "lv4 sewaddle", "lv4 purrloin", "lv3 sunkern", "lv4 sunkern", "lv4 sunkern"]
	table3 = ["lv2 pidove","lv2 sewaddle","lv3 patrat", "lv3 purrloin", "lv3 patrat", "lv3 sewaddle", "lv4 pidove", "lv4 sewaddle", "lv4 purrloin", "lv4 sunkern", "lv4 purrloin", "lv4 sunkern"]
	birds  = [ ]
	for x in range(frame_entering_route20,frame_exiting_route20):
		res = pokeGen(seed["seed"], x)
		if res[0] and res[3]==0 and res[4] not in [natures[1],natures[11],natures[16],natures[21]]:
			if seed["month"] % 4 == 3:
				if res[2]<5:
					birds.append(str(res[1])+"\t"+table3[int(res[3])]+"\t"+res[4]+"\t"+str(res[5])+" Low")
				else:
					birds.append(str(res[1])+"\t"+table3[int(res[3])]+"\t"+res[4]+"\t"+str(res[5])+" High")
			if seed["month"] %4 == 1:
				if res[2]<5:
					birds.append(str(res[1])+"\t"+table1[int(res[3])]+"\t"+res[4]+"\t"+str(res[5])+" Low")
				else:
					birds.append(str(res[1])+"\t"+table1[int(res[3])]+"\t"+res[4]+"\t"+str(res[5])+" High")
	return birds

def getDucks(seed):
	table2 = ["lv4 lillipup","lv5 azurill","lv5 patrat", "lv5 mareep", "lv5 lillipup", "lv5 psyduck", "lv6 lillipup", "lv7 pidove", "lv5 riolu", "lv7 lillpup", "lv7 riolu", "lv7 lillipup"]
	ducks=[]
	for x in range(frame_entering_ranch,frame_exiting_ranch):
		res = pokeGen(seed["seed"], x)
		if res[0] and res[3]==5 and res[5]==0:
			if res[2]<5:
				ducks.append(str(res[1])+"\t"+table2[int(res[3])]+"\t"+res[4]+"\t"+str(res[5])+" Low")
			else:
				ducks.append(str(res[1])+"\t"+table2[int(res[3])]+"\t"+res[4]+"\t"+str(res[5])+" High")
	return ducks

def getTID(seed, ivframe, challenge_mode = False):
	
	initial_frame = get_init_frame_id(seed, challenge_mode)
	extra_advances = ivframe - 14 # 1 extra advancement is always made from init_frame for TID 
	tmp = rngOf(seed, initial_frame + extra_advances) 
	rand = ((tmp >> 32) * 0xffffffff) >> 32
	tid = rand & 0xffff
	sid = rand >> 16
	return tid

def getPassword(TID):
	passwords = ["RESHIRAM", "ZEKROM", "9909", "7707", "2202"]
	return passwords[TID % 256 % 5]

def getUInt(seed, max):
    return ((seed >> 32) * max) >> 32

def get_init_frame_id(seed, challenge_mode = False):
	count = 7 if challenge_mode else 10

	for i in range(0, 3):
		# Round 1
		count += 1
		seed = rngOf(seed, 1)

		# Round 2
		count += 1
		seed = rngAdvance(seed)
		if ( getUInt(seed, 101) > 50):
			count += 1
			seed = rngOf(seed, 1)

		# Round 3
		count += 1
		seed = rngAdvance(seed)
		if (getUInt(seed, 101) > 30):    
			count += 1
			seed = rngOf(seed, 1)

		# Round 4
		count += 1
		seed = rngAdvance(seed) 
		if (getUInt(seed, 101) > 25):
			count += 1
			seed = rngAdvance(seed)
			if (getUInt(seed, 101) > 30):
				count += 1
				seed = rngOf(seed, 1)

		# Round 5
		count += 1
		seed = rngAdvance(seed)
		if (getUInt(seed, 101) > 20):
			count += 1
			seed = rngAdvance(seed) 
			if (getUInt(seed, 101) > 25):
				count += 1
				seed = rngAdvance(seed)
				if (getUInt(seed, 101) > 33):
					count += 1
					seed = rngOf(seed, 1)

		if( i == 0 ):
			seed = rngOf(seed, 1 if challenge_mode else 2)
		elif (i == 1):
			seed = rngOf(seed, 2 if challenge_mode else 4)

	return count

def main():
	outputDir=dir+"/test.txt"

	try:
		seedLst = open(path, "r+", encoding="Shift-JIS")
	except IOError:
		print("Error attempting to open file:", path)
		exit()

	seedLst.readline()
	try:
		output = open(outputDir,"w",encoding="UTF-8")
	except IOError:
		print("error trying to write to file:", outputDir)
		exit()

	for line in seedLst:
		parsed = line.split(",")
		seed = {
			"seed" : int(parsed[16], 16),
			"ivframe" : int(parsed[7]) - 1,
			"timer0" : str(parsed[6]),
			"year" : int(parsed[0]) + 2000,
			"month" : int(parsed[1]),
			"day" : int(parsed[2]),
			"hour" : int(parsed[3]),
			"minute" : int(parsed[4]),
			"second" : int(parsed[5]),
			"key_presses" : str(parsed[17]).strip(),
			"stats": [ int(parsed[8]), int(parsed[9]), int(parsed[10]), int(parsed[11]), int(parsed[12]), int(parsed[13]) ]
		}

		seed["NMTID"] = getTID(seed["seed"], seed["ivframe"])
		seed["NMPASS"] = getPassword(seed["NMTID"])

		seed["CMTID"] = getTID(seed["seed"], seed["ivframe"], True)
		seed["CMPASS"] = getPassword(seed["CMTID"])

		seed["ducks"] = getDucks(seed)
		seed["birds"] = getBirds(seed)
		
		if len(seed["birds"]) == 0 or len(seed["ducks"]) == 0:
			continue
		#婵?闂?闂?闂?闂?缂?Timer0,婵犵數鍋為崹鐢告偋閹邦厾鈻旂€广儱顦弸?H,A,B,C,D,S,闂備線娼ч悧鍛存⒔瀹ュ棛顩烽煫鍥ㄧ☉鍞?濠电姷鏁搁崑妯肩矆娴ｈ鍙?闂備礁鎲＄敮妤冩崲閸愵煉鑰挎い锛勵劋ed,闂備線娼ч悧婊堝储瑜版帒绀傛俊銈呮噹缁€鍌炴煏婢跺牆鍔氭い?
		output.write("Seed: " + str(hex(seed["seed"]))+"\n")
		output.write("Time: "+ str(seed["year"]) +"/"+ str(seed["month"]) + "/" + str(seed["day"]) +" "+"{:02d}".format(int(seed["hour"]))+":"+"{:02d}".format(int(seed["minute"]))+":"+"{:02d}".format(int(seed["second"]))+"\n")
		output.write("Timer0: "+seed["timer0"]+"\n")
		output.write("Key Presses: "+seed["key_presses"]+"\n")
		output.write(f"TID: {seed['NMTID']} ({seed['NMPASS']}), CM: {seed['CMTID']} ({seed['CMPASS']})\n")
		output.write("Tepig:"+"\n")
		output.write(str(seed["ivframe"])+" "+str([parsed[8],parsed[9],parsed[10],parsed[11],parsed[12],parsed[13]])+"\n")
		for x in seed["birds"]:
			output.write(x+"\n")
		for y in seed["ducks"]:
			output.write(y+"\n")
		output.write("\n\n")
	seedLst.close()
	output.close()

if __name__ == '__main__':
	main()
