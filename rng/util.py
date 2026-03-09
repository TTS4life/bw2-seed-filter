
class Gen5RNG():

	natures = ['Hardy', 'Lonely','Brave','Adamant','Naughty',
			   'Bold','Docile','Relaxed','Impish','Lax',
			   'Timid','Hasty','Serious','Jolly','Naive',
			   'Modest','Mild','Quiet','Bashful','Rash',
			   'Calm','Gentle','Sassy','Careful','Quirky']

	
	@staticmethod
	def rngAdvance(rng) -> int:
		"""Get the next RNG Advancement"""
		next=0x5D588B656C078965 * rng + 0x0000000000269EC3
		return next%0x10000000000000000
	

	@staticmethod
	def rngRAdvance(prev):
		"""Get the previous frame of a seed value"""
		next = 0xdedcedae9638806d * prev + 0x9b1ae6e9a384e6f9
		return next % 0x10000000000000000

	@staticmethod
	def rngOf(seed, num_advances):
		"""Get the rng state in x frames from value `seed`"""
		tmp = seed
		for x in range(0,num_advances):
			tmp = Gen5RNG.rngAdvance(seed)
		return tmp
	
	@staticmethod
	def getUInt(seed, max):
		return ((seed >> 32) * max) >> 32
	

	@staticmethod
	def extra(seed,fc):
		loop = True
		limit = 0
		while loop and limit<100:
			loop = False
			tmp = [0,0,0]
			fc+=3
			for x in range (0,3):
				seed = Gen5RNG.rngAdvance(seed)
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
	
	@staticmethod
	def pokeGen(seed,frame):
		trigger = Gen5RNG.rngOf(seed,frame+2)
		slot = Gen5RNG.rngAdvance(trigger)
		ability = Gen5RNG.rngAdvance(slot)
		ability = Gen5RNG.rngAdvance(ability)
		pokenat = Gen5RNG.rngAdvance(ability)
		isEncounter = int((((trigger>>32)*0xFFFF)>>32)/0x290)
		if isEncounter < 14:
			appear = True
		else:
			appear = False
		sel =((slot>>32)*100)>>32
		natsel = ((pokenat>>32)*25)>>32
		ability = ((ability>>32^0x10000^0x80000000)>>16)&1
		return [appear,frame,isEncounter,Gen5RNG.getLandSlot(sel),Gen5RNG.natures[natsel],ability]
	
	@staticmethod
	def getLandSlot(sel):
		parts=[20, 40, 50, 60, 70, 80, 85, 90, 94, 98, 99, 100]
		for x in range(0,12):
			if sel<parts[x]:
				return x
			
	
			


def illegal_keypresses(keypresses):
    return ( 'Up' in keypresses and 'Down' in keypresses ) or ( 'Left' in keypresses and 'Right' in keypresses )
