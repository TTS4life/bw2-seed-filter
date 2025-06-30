from numba_pokemon_prngs.lcrng import BWRNG
import numpy as np
from numba_pokemon_prngs.sha1 import SHA1
from numba_pokemon_prngs.enums import Language, Game, DSType

test = False

ranges = (
    (-5, 5, -5, 5), # default case
    (0, 5, -5, 5), #Right of player
    (-5, 0, -5, 5), #left of player
    (-5, 5, -5, 0), #above player
    (-5, 5, 0, 5) #below player
)

def illegal_keypresses(keypresses):
    return ( 'Up' in keypresses and 'Down' in keypresses ) or ( 'Left' in keypresses and 'Right' in keypresses )


def compute_times(user_hour, user_min):
    times = []
    for i in range(max(user_hour - 2, 0), min(user_hour + 2, 24)):
        for j in range(max(user_min - 10, 0), min(user_min + 10, 60)):
           for k in range(5,7):
                  time1 = (i, j, k)
                  times.append(time1)
    return times

def compute_times_whole():
    times = []
    for i in range(0, 24):
        for j in range(0, 60):
            for k in range(5, 7):
                 times.append((i, j, k)) 
    return times

def compute_times_tospring():
    times = []
    for i in range(23, 24):
        for j in range(15, 40):
            for k in range(5, 10):
                 times.append((i, j, k)) 
    return times

def rngAdvance(prev):
	next=0x5D588B656C078965 * prev + 0x0000000000269EC3
	return next % 0x10000000000000000

def rngRAdvance(prev):
    next = 0xdedcedae9638806d * prev + 0x9b1ae6e9a384e6f9
    return next % 0x10000000000000000

def generate_seed(
        sha1: SHA1,
        button: np.uint32,
        timer0: np.uint32,
        vcount: np.uint32,
        date: tuple[np.uint16],
        time: tuple[np.uint8],
    ) -> int:
        # not setting button/timer0/date/time causes undefined behaviour as the data array is empty
        # and these values would always otherwise be present
        sha1.set_button(button)
        sha1.set_timer0(timer0, vcount)
        sha1.set_date(*date)
        sha1.set_time(*time)
        return sha1.hash_seed(sha1.precompute())


def cloud_location_finder(rngstate, coords, tileset):
    # global test

    rng = BWRNG(np.uint64(rngstate))
    player_x = coords[0]
    player_y = coords[1]
    #player_x, player_y = 46, 6
    if rng.next_rand(1000) < 100:
        # TODO: when does default case actually happen
        quadrant = rng.next_rand(4) + 1

        # if test is True:
        # print("quadrant ", quadrant, ["Right", "Left", "Up", "Down"][quadrant - 1])

        x_min, x_max, y_min, y_max = ranges[quadrant]


        x_min_in_chunk = max((player_x % 32) + x_min, 0)
        x_max_in_chunk = min((player_x % 32) + x_max, 31)
        y_min_in_chunk = max((player_y % 32) + y_min, 0)
        y_max_in_chunk = min((player_y % 32) + y_max, 31)

        x_min = x_min_in_chunk + player_x - (player_x % 32)
        x_max = x_max_in_chunk + player_x - (player_x % 32)
        y_min = y_min_in_chunk + player_y - (player_y % 32)
        y_max = y_max_in_chunk + player_y - (player_y % 32)

        # if test is True:
        #     print(x_min, y_min, x_max, y_max)

        possible = []
        possible_x = []
        possible_y = []
        for dust_y in range(y_min, y_max + 1):
            for dust_x in range(x_min, x_max + 1):
                if (dust_x, dust_y) in tileset:
                    possible.append((dust_x, dust_y))
                    possible_x.append(dust_x)
                    possible_y.append(dust_y)
                    
        rand_tile = rng.next_rand(len(possible))
        dust_cloud_x, dust_cloud_y = possible[rand_tile]
    else:
        return "No dust cloud"
    if test is True:
        print("cloud spawns at ", (dust_cloud_x, dust_cloud_y), " from coords ", coords, " rand tile ", rand_tile, " possible ", possible, len(possible)
              )
    
    return ((dust_cloud_x, dust_cloud_y), quadrant)


def write_seed_output(file, seed_info, cloud_sets):
    file.write(seed_info)

    for i, clouds in enumerate(cloud_sets):
        file.write(f"{i+1}: ")
        for cloud in clouds:
            file.write(f"{cloud} ")
        file.write("\n")

    file.write("\n")