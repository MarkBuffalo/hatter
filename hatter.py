from PIL import Image
from collections import Counter
import os
from os import listdir
from colorama import Fore
from math import sqrt


class MadAsAHatter:
    def __init__(self):
        # The game has 7 columns
        self.columns = 7
        # And 5 rows.
        self.rows = 5

        # The first tile's X coordinates.
        # This is based on the iPhone X screenshot length. Everything else is subject to calculation.
        self.base_width = 1125
        # And the first tile's Y coordinates.
        self.base_height = 2436
        # This is based on the iPhone X resolution. Everything else is subject to calculation.
        self.base_x = 99
        self.base_y = 1094

        # Where the middle of the next icon starts. For iPhone X. Everything else is subject to calculation.
        self.base_increment_amount = 154

        self.current_width = 0
        self.current_height = 0

        # Get our base distance calculations so we can update based on new resolutions.
        self.base_distance_x = self.base_x / self.base_width
        self.base_distance_y = self.base_y / self.base_height

        # We would update these values later.
        self.new_distance_x = 0
        self.new_distance_y = 0
        self.new_increment_amount = 0

        # This is to make sure the colors don't bleed all over the terminal.
        self.reset = Fore.RESET

        # Our dictionary:tuple of colors. And actual foreground colors.
        self.tile_colors = {
            "red": (255, 0, 0, Fore.LIGHTRED_EX),
            "green": (0, 255, 0, Fore.LIGHTGREEN_EX),
            "blue": (0, 0, 255, Fore.BLUE),
            "yellow": (255, 255, 0, Fore.LIGHTYELLOW_EX),
            "purple": (148, 0, 211, Fore.MAGENTA)
        }
        # The current list of each individual screenshot.
        self.current_list = []

        # The total accumulated value list of all parsed images.
        self.all_values = []

    # Called once per image, at the beginning, before any processing.
    def reset_image_coordinates(self):
        self.new_distance_x = int(round(self.current_width * self.base_distance_x))
        self.new_distance_y = int(round(self.current_height * self.base_distance_y))
        self.new_increment_amount = int(round(self.current_width * (self.base_increment_amount / self.base_width)))

    # For the iPhone X screenshots.
    # Edit for your own (see start_x and start_y). Good luck because I didn't calculate
    # the positions based on screenshot size).
    def scan_images(self):
        print(self.base_distance_x)
        print(self.base_distance_y)
        # Take the current directory and append "/shots/". Put all your screenshots in the "/shots/" directory.
        # Yeah, I could just use argparse, but whatever.
        current_directory = os.path.dirname(os.path.realpath(__file__)) + "/shots/"
        print(current_directory)
        file_list = listdir(current_directory)

        for file in file_list:
            img = Image.open(current_directory + file)
            pixel_map = img.load()
            print(f"\nChecking {file}...")

            # Now, set the size of the screenshot so we can perform insane calculations later.
            self.current_width, self.current_height = img.size
            # Reset the coordinates each time we load a new image.
            self.reset_image_coordinates()
            # Reset the current list each time so it doesn't fill up.
            self.current_list = []
            # Now let's traverse the grid to see what data we can glean from it.
            self.traverse_grid(pixel_map)
        # And then print the final results.
        eq = "=" * 98
        print(f"\n{eq}\nFinished parsing images!\n{eq}\n\n"
              f"For these screenshots, your most common colors are as follows:\n")
        self.compute_current_average(self.all_values)
        print("\n")

    # Find tile data within the grid.
    def traverse_grid(self, pixel_map):
        cur_y = self.new_distance_y

        for row in range(self.rows):
            print(f"Current row: {row+1}")
            self.traverse_columns(cur_y, row, pixel_map)
            cur_y += self.new_increment_amount
        # Print out the average values in dictionary format.
        self.compute_current_average(self.current_list)

    def traverse_columns(self, cur_y, row, pixel_map):
        # Now we're going to traverse horizontally.
        cur_x = self.new_distance_x

        for i in range(self.columns):
            # Convert the tuple to a list so we can edit it.
            tile_rgb_list = list(pixel_map[cur_x, cur_y])
            # We're going to get rid of the 'a' value in the rgba result by only combining RED[0], GREEN[1] and BLUE[2].
            current_tile = (tile_rgb_list[0], tile_rgb_list[1], tile_rgb_list[2])
            color_name = self.closest_tile_color(current_tile)

            print(f"Tile [{row+1},{i+1}] - [{cur_x},{cur_y}] - Closest color for {tile_rgb_list} is {color_name}")

            # Store rol, col and color name for later parse.
            # Update current list. It will get reset later.
            self.current_list.append([row, i, color_name])
            # Update total list. It will not be reset.
            self.all_values.append([row, i, color_name])
            # Increment the current X coordinate by however much we determined earlier.
            cur_x += self.new_increment_amount

    # We get our average this way...
    def compute_current_average(self, values):
        new_list = []
        for i in values:
            new_list.append(i[2])

        sorted_order = self.get_sorted_list(new_list)
        current_position = 0
        for key, val in sorted_order.items():
            current_position += 1
            print(f"{current_position}) {key}: {val} occurrences.")

    # This is our sorted dictionary. Get average values for each tile on each image parsed.
    @staticmethod
    def get_sorted_list(counter_list):
        counted_list = Counter(counter_list)
        # Sort list by highest occurrence to smallest occurrence.
        # e.g.: {'green': 10, 'purple': 8, 'yellow': 8, 'red': 7, 'blue': 2}
        return dict(sorted(counted_list.items(), key=lambda x: x[1], reverse=True))

    def closest_tile_color(self, color):
        # Unpack Tuple into RGB values
        red, green, blue = color
        differences = []
        # Iterate through tile_colors and compare differences.
        for color_name, color_tuple in self.tile_colors.items():
            r, g, b, fore = color_tuple
            color_difference = sqrt(abs(red - r) ** 2 + abs(green - g) ** 2 + abs(blue - b) ** 2)
            differences.append((color_difference, color_tuple))

        # Unpack differences tuple and get the closest match.
        r, g, b, fore = min(differences)[1]

        # Now match the tuples to our tile_colors...
        for color_name, color_tuple in self.tile_colors.items():
            nr, ng, nb, fore = color_tuple
            # Compare the Tuple values and return the color name.
            if r == nr and g == ng and b == nb:
                return f"{fore}{color_name.upper()}{self.reset}"


if __name__ == "__main__":
    mad = MadAsAHatter()
    mad.scan_images()

