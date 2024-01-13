#!/usr/bin/python3

import itertools


base = 0xff2f0000
R =  0x10000
L =  0x20000
X =  0x40000
Y =  0x80000
A = 0x1000000
B = 0x2000000
Select = 0x4000000
Start = 0x8000000
Right = 0x10000000
Left = 0x20000000
Up = 0x40000000
Down =0x80000000

value_array = [R, L, X, Y, A, B, Select, Start, Right, Left, Up, Down]
value_array_names = ["R", "L", "X", "Y", "A", "B", "Select", "Start", "Right", "Left", "Up", "Down"]
keypress_values = [base]

def illegal_keypresses(keypresses):
    return ( 'Up' in keypresses and 'Down' in keypresses ) or ( 'Left' in keypresses and 'Right' in keypresses ) or (
        'L' in keypresses and 'R' in keypresses and 'Start' in keypresses and 'Select' in keypresses)
    

def keypress_generator():
    keypress_list = []
    for buttons_pressed in itertools.product(*((False, True) for _ in range(12))):
        keypress_value = base
        array = []
        for button_index, button_pressed in enumerate(buttons_pressed):
            if button_pressed:
                keypress_value -= value_array[button_index]

                array.append(value_array_names[button_index])
        if(illegal_keypresses(array)):
            continue
        if 0 < buttons_pressed.count(True) < 9:
            #print(hex(keypress_value), array)
            #keypress_list[hex(keypress_value)] = array
            t = [str(keypress_value), str(array)]
            keypress_list.append(t)
    return keypress_list
            
        

keypress_generator()

all_presses = keypress_generator()

#print(keypresses)
#print(keypresses_lite)

with open("readme.txt", "w") as txt_file:
    for line in all_presses:
        txt_file.write("["+", ".join(line) + "]\n" +",")