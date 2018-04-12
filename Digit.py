from Helpers import number_to_segment
import Segment

class Digit:
    segments = []

    def __init__(self, index):
        self.index = index
        create_segments()

    def create_segments(self):
        for i in range(8):
            first_led = (self.index * 14) + i
            self.segments.append(Segment(first_led, first_led + 1))

    def leds_for_display_number(self, display_number):
        segments_for_display_number = number_to_segment[str(display_number)]

        leds = []
        for segment_index in segments_for_display_number:
            leds += self.segments[segment_index].leds
        return leds
