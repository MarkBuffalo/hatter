import webcolors
from PIL import Image
from collections import Counter
import os
from os import listdir


class MadAsAHatter:
    def __init__(self):
        # Currently only supports the iPhone X resolution. Tweak for your own settings.
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

        # Dictionary map of web colors to closest RGBYP value. e.g.: olivedrab = green.
        self.color_names = {
            "sandybrown": "yellow",
            "burlywood": "yellow",
            "royalblue": "blue",
            "purple": "purple",  # Shut up! I'm too lazy to write an if statement.
            "olivedrab": "green",
            "darkolivegreen": "green",
            "firebrick": "red",
            "brown": "red",
            "darkred": "red",
            "forestgreen": "green",
            "goldenrod": "yellow",
            "indigo": "blue",
            "darkgreen": "green",
            "dodgerblue": "blue",
            "darkred": "red",
            "darkgoldenrod": "yellow"
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

            # Now, set the size of the screenshot so we can perform insane calculations later.
            self.current_width, self.current_height = img.size
            # Reset the coordinates each time we load a new image.
            self.reset_image_coordinates()
            # Reset the current list each time so it doesn't fill up.
            self.current_list = []
            # Now let's traverse the grid to see what data we can glean from it.
            self.traverse_grid(pixel_map)
        # And then print the final results.
        print("\nTotal value collection:")
        print(self.compute_current_average(self.all_values))

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
            color_name = self.closest_color(current_tile)

            print(f"Row: {row+1}. Column: {i+1}. Position: [{cur_x},{cur_y}]. "
                  f"Color (rgba): {tile_rgb_list}. "
                  f"Closest RGB color name: {color_name}")

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
        for key, val in sorted_order.items():
            if key is not None and val is not None:
                print(f"{key.upper()}: {val} occurrences.")

    # This is our sorted dictionary. Get average values for each tile on each image parsed.
    @staticmethod
    def get_sorted_list(counter_list):
        counted_list = Counter(counter_list)
        # Sort list by highest occurrence to smallest occurrence.
        # e.g.: {'green': 10, 'purple': 8, 'yellow': 8, 'red': 7, 'blue': 2}
        return dict(sorted(counted_list.items(), key=lambda x: x[1], reverse=True))

    # Get nearest web color based on euclidean distance
    def closest_color(self, requested_color):
        min_colors = {}
        for key, name in webcolors.css3_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_color[0]) ** 2
            gd = (g_c - requested_color[1]) ** 2
            bd = (b_c - requested_color[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        # Now we're going to convert the nearest web color to the nearest RGBYP value.
        # e.g.: red, green, blue, yellow, purple.
        return self.closest_rgb(min_colors[min(min_colors.keys())])

    # Map our current color name to something readable by a 4 year old.
    def closest_rgb(self, color):
        for k, v in self.color_names.items():
            if color is k:
                return v
        # It's not mapped. Return color so we can fix it.
        return color

    # Get closest web color name
    def get_color_name(self, requested_color):
        try:
            closest_name = actual_name = webcolors.rgb_to_name(requested_color)
        # An exception was thrown, meaning we couldn't find the right color.
        except ValueError:
            # We found an error, so let's conjure euclidean horrors.
            closest_name = self.closest_color(requested_color)
            actual_name = None
        return actual_name, closest_name


if __name__ == "__main__":
    mad = MadAsAHatter()
    mad.scan_images()

