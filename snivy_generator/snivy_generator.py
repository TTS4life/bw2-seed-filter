#!/usr/bin/python3

from PIDRNG import PIDRNG
import numpy as np
from numba_pokemon_prngs.mersenne_twister import MersenneTwister
from numba_pokemon_prngs.sha1 import SHA1
from numba_pokemon_prngs.enums import Language, Game, DSType
from keypresses import keypresses
import time

file = None
seeds = []

mac = 0x9BF3f2a97

version = Game.BLACK
language = Language.ENGLISH
dsType = DSType.DS

hour = 4
min = 22
sec = 32

timer0 = 0xc7c

day = 19
month = 12
year = 2011
dow = 1

natures = ['Hardy','Lonely','Brave','Adamant',
         'Naughty','Bold','Docile','Relaxed',
         'Impish','Lax','Timid','Hasty',
         'Serious','Jolly','Naive','Modest',
         'Mild','Quiet','Bashful','Rash',
         'Calm','Gentle','Sassy','Careful','Quirky']

def check_seed_for_snivy(seed):
    rng = MersenneTwister(np.uint64(seed) >> np.uint32(32))
    rng.advance(1)
    rng.advance(9)

    stat1 = rng.next() >> np.uint32(27)
    stat2 = rng.next() >> np.uint32(27)
    stat3 = rng.next() >> np.uint32(27)
    stat4 = rng.next() >> np.uint32(27)
    stat5 = rng.next() >> np.uint32(27)
    stat6 = rng.next() >> np.uint32(27)
    
    if(stat2 < 30 or stat6 < 24):
        return None

    seed = PIDRNG(seed)
    seed.calculateInitialPIDRNG()

    frame = seed.frame
 
    nature = get_starter_nature(seed)
    if nature in  ["Naive", "Hasty", "Jolly"]:
        return [12, [stat1, stat2, stat3, stat4, stat5, stat6], nature, frame]

def get_starter_nature(seed):
    seed.advance(2)
    nature_id = ((seed.seed >> 32) * 25) >> 32
    return natures[nature_id]

def mine_seeds(sha1, precompute):
    seeds_found = 0
    seeds = []

    time = (hour, min, sec)

    for presses in keypresses:
        seed = {}
        sha1.set_button(presses[0])
        sha1.set_time(*time)

        seed["SEED"] = sha1.hash_seed(precompute)

        seed["SNIVY_INFO"] = check_seed_for_snivy(seed["SEED"])

        if(seed["SNIVY_INFO"] is None):
            continue

        seed["MONTH"] = month

        seed["TIMER0"] = timer0
        seed["TIME"] = time
        seed["KEYPRESSES"] = presses[1]

        seeds.append(seed)
        seeds_found = seeds_found + 1

    return seeds



def main():
    
    start = time.time()
    sha1 = SHA1(version=version, language=language, ds_type=dsType, mac = mac, soft_reset=False, v_frame=8, gx_state=6)

    sha1.set_timer0(timer0, 0x60)

    date = (year, month, day, dow)

    sha1.set_date(*date)

    precompute = sha1.precompute()

    print("Precompute Complete")

    try:
        file = open("output.txt", "w+")
    except IOError:
        print("Error with file")

    seeds = mine_seeds(sha1, precompute)

    for seed in seeds:
        file.write(
		f"Seed: {hex(seed['SEED'])}\n" + 
		"Time: "+"{:02d}".format(int(seed["TIME"][0]))+":"+"{:02d}".format(int(seed["TIME"][1]))+":"+"{:02d}".format(int(seed["TIME"][2]))+"\n" +
		f"Timer0: {hex(seed['TIMER0'])}\n" +
		f"Key Presses: {seed['KEYPRESSES']}\n"
		f"Snivy:\n" +
		str(seed["SNIVY_INFO"]) + "\n")

        file.write("\n\n")

    file.close()


def test():
    seed = 0x80981f55d5e91451
    output = check_seed_for_snivy(seed)
    print(output)

if __name__ == '__main__':
    main()