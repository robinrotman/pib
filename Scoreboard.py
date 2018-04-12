from Helpers import color_name_to_rgb_tuple
from apa102 import Apa102PixelStrip
from Digit import Digit

class Scoreboard:
    num_leds = 58
    led_strip = Apa102PixelStrip(num_leds)

    def __init__(self, home_color, away_color):
        self.led_values = []
        self.hyphen_color_value = (1, 1, 1)
        self.home_color_value = color_name_to_rgb_tuple[home_color]
        self.away_color_value = color_name_to_rgb_tuple[away_color]
        self.digits = []
        self.reset_led_values()
        for i in range(4):
            self.digits.append(Digit(i))

    def reset_led_values(self):
        self.led_values = [(0, 0, 0)] * self.num_leds
        self.led_values[-1] = self.hyphen_color_value
        self.led_values[-2] = self.hyphen_color_value

    def score_to_digits(self, score):
        #return [score // 10, score % 10]
        digits = [score // 10, score % 10]
        print(digits)
        return digits

    def show_score(self, home_score, away_score):
        self.reset_led_values()
        numbers_to_display = self.score_to_digits(home_score)
        numbers_to_display += self.score_to_digits(away_score)

        leds_to_display = []
        for i in range(len(numbers_to_display)):
            leds_to_display += self.digits[i].leds_for_display_number(numbers_to_display[i])

        for led in leds_to_display:
            self.led_values[led] = self.hyphen_color_value

        self.led_strip.value = self.led_values

    def sleep(self):
        self.led_values = [(0, 0, 0)] * self.num_leds
        self.led_strip.value = self.led_values
