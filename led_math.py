# import time
from apa102 import Apa102PixelStrip
# leds = Apa102PixelStrip(num_pixels)

num_leds = 58 # 14 leds per digital, last 2 leds 2 for hyphen
values = [(0, 0, 0)] * num_leds
leds = Apa102PixelStrip(num_pixels)

leds_per_segment = 14

#       LED BREAKDOWN
#
#           1 2
#           - -
#       12 |   | 3
#       11 |13 | 4
#           - -
#       10 | 14| 5
#       9  |   | 6
#           - -
#           8 7

#       SEGMENT BREAKDOWN
#
#            0
#           - -
#        5 |   | 1
#          | 6 |
#           - -
#        4 |   | 2
#          |   |
#           - -
#           3

led_array = [] #used to append leds at indexes

for i in range(0, num_leds):
    led_array.append(i)

led_digit_0 = [] #digit X0-00
led_digit_1 = [] #digit 0X-00
led_digit_2 = [] #digit 00-X0
led_digit_3 = [] #digit 00-0X

led_digit_pairs = [led_digit_0, led_digit_1, led_digit_2, led_digit_3]

def print_pairs():
    for i in range(0, num_leds, 2): #third parameter increments by 2
    	led_pair =  (led_array[i], led_array[i+1])
    	if i <= 13:
    	    led_digit_0.append(led_pair)
    	elif i <= (13 + (leds_per_segment*1)):
    	    led_digit_1.append(led_pair)
    	elif i <= (13 + (leds_per_segment*2)):
    	    led_digit_2.append(led_pair)
    	elif i <= (13 + (leds_per_segment*3)): #maxes at 55
    	    led_digit_3.append(led_pair)
    return led_digit_pairs

print_pairs() #calls print pairs - returning the array of led arrays divided by placehold digit and seven segments pairs

current_display_numbers = [led_digit_0, led_digit_1, led_digit_2, led_digit_3]

def show_number(num, led_num): #num is placeholder for which digit you want the segment from
    number_0 = num[0], num[1], num[2], num[3], num[4], num[5]
    number_1 = num[0], num[1]
    number_2 = num[0], num[1], num[6], num[4], num[3]
    number_3 = num[0], num[1], num[6], num[2], num[3]
    number_4 = num[5], num[6], num[1], num[2]
    number_5 = num[0], num[5], num[6], num[2], num[3]
    number_6 = num[0], num[5], num[6], num[4], num[2], num[3]
    number_7 = num[0], num[1], num[2]
    number_8 = num[0], num[1], num[2], num[3], num[4], num[5], num[6]
    number_9 = num[0], num[5], num[6], num[1], num[2]
    number_blank = []

    led_numbers = [number_0, number_1, number_2, number_3, number_4, number_5, number_6, number_7, number_8, number_9, number_blank]

    for i in range(0, len(led_numbers)):

        if led_num == i: # if the desired number to get i.e. 1 matches i
            getIndex = current_display_numbers.index(num) # get the digit index
            current_display_numbers[getIndex] = led_numbers[i] #assign the index those leds
            print ("hello")
            print ("i is number_" + str(i) + " and here are the leds that should be turned on: " + str(current_display_numbers[getIndex]))
            return current_display_numbers[getIndex] #return those leds to be turned on

def turn_on_leds(led_pairs):
    values = [(0, 0, 0)] * num_leds
    for pair in led_pairs:
        values[pair[0]] = (1, 0, 0)
        values[pair[1]] = (1, 0, 0)
    leds.value = values


