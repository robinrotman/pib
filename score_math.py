
from led_math import *
import numpy as np

#digits_array = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

#digits_leds_array = [number_0, number_1, number_2, number_3, number_4, number_5, number_6, number_7, number_8, number_9]

# led_digit_0 = [] #digit X0-00
# led_digit_1 = [] #digit 0X-00
# led_digit_2 = [] #digit 00-X0
# led_digit_3 = [] #digit 00-0X

def update_leds(score): #score a and score b #use show_number to parse
    #p1_score = [digit_1, digit_2]
    #p2_score = [digit_1, digit_2]

    #led_set = [[a,b],[c,d]]
    #a = str(score).split(",")
    #b = int(a)

    #print (current_display_numbers)

    score_array = np.asarray(score)
    print (score_array)
    print (score_array[0])
    print (score_array[1])

    #score = [score[0], score[1]]
    #p1_score = score[0]
    #p2_score = score[1]


#   for i in range(0,1):


    if score_array[0] <= 9:
        show_number(led_digit_0, number_blank) #FIX refer to elif
        show_number(led_digit_1, score_array[0])
    elif score_array[0] >= 9:
        print score_array[0]
        split_double_digits = [int(dig) for dig in str(score_array[0])]
        print (split_double_digits)
        show_number(led_digit_0, split_double_digits[0])
        show_number(led_digit_1, split_double_digits[1])

    if score_array[1] <= 9:
        show_number(led_digit_2, number_blank) #FIX refer to elif
        show_number(led_digit_3, score_array[1])
    elif score_array[1] >= 9:
        print score_array[1]
        split_double_digits = [int(dig) for dig in str(score_array[1])]
        print (split_double_digits)
        show_number(led_digit_2, split_double_digits[0])
        show_number(led_digit_3, split_double_digits[1])


score = [22,5]
update_leds(score)
