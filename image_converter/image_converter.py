import os
from PIL import Image
import argparse
import json
from dataclasses import dataclass

# include (for the funny ZPixmap)
# image1
# image2
# image3
# percentage: image pointer

parser = argparse.ArgumentParser()
parser.add_argument("--output")
parser.add_argument("--input")
args = parser.parse_args()


@dataclass
class ImageData:
    array_definition: str
    width: int
    height: int

def sort_by_percentage(listing):
    percentage_to_image_path = {}

    for entry in listing:
        path = entry["image_path"]
        percentage = entry["battery_percentage"]
        if percentage in percentage_to_image_path:
            raise Exception(f"Percentage {percentage} occurs twice")
        percentage_to_image_path[percentage] = path

    return percentage_to_image_path

def generate_by_image(percentage_to_image_path):
    percentage_to_image_data = {}
    last_image_number = 0
    for percentage, image_path in percentage_to_image_path:
        array_name = f"IMG{last_image_number}"
        last_image_number += 1
        image_data = generate(image_path, array_name)
        percentage_to_image_data[percentage] = image_data
    return percentage_to_image_data

def main():
    # This is done to prevent variable leak
    with open(args.input, encoding="utf-8") as f:
        listing = json.loads(f.read())
    percentage_to_image_path = sort_by_percentage(listing)
    percentage_to_image_data = generate_by_image(percentage_to_image_path)

def generate(image_path, array_name):
    array_definition = f"unsigned char {array_name}[] = {{\n"
    image = Image.open(image_path)
    for pixel in image.getdata():
        red, green, blue, opacity = pixel
        for color_value in [red, green, blue, opacity]:
            array_definition += str(color_value)
            array_definition += ","
        array_definition += "\n"
    array_definition += "};"
    return ImageData(
        array_definition=array_definition,
        width=image.width,
        height=image.height,
    )

X11_INCLUSION = "#include <X11/Xlib.h>"

IMAGE_STRUCTURE_DEFINITION = """
struct BatteryIndicatorImage {
    unsigned int depth;
    int format;
    int offset;
    unsigned int width;
    unsigned int height;
    int bitmap_pad;
    int bytes_per_line;
    unsigned char data[];
}
""".strip()

LEVEL_STRUCTURE_DEFINITION = """
struct BatteryIndicatorLevel {
    unsigned char battery_percentage;
    struct BatteryIndicatorImage* image;
}
""".strip()

output = [X11_INCLUSION, IMAGE_STRUCTURE_DEFINITION, LEVEL_STRUCTURE_DEFINITION]

last_image_number = 0

def process_image(file_path) -> dict:
    global last_image_number
    return {}

listing_directory, _ = os.path.split(args.input)

path_to_array_name = {}

images = []
for image_data in listing:
    if image_data["file_path"] not in path_to_array_name:
        array_name = f"IMG{last_image_number}"
        last_image_number += 1
        array_definition = f"unsigned char {array_name}[] = {{\n"
        file_path = os.path.join(listing_directory, image_data["file_path"])
        image = Image.open(file_path)
        for pixel in image.getdata():
            red, green, blue, opacity = pixel
            for color_value in [red, green, blue, opacity]:
                array_definition += str(color_value)
                array_definition += ","
            array_definition += "\n"
        array_definition += "};"
        output.append(array_definition)
    images.append({
        "battery_percentage": image_data["battery_percentage"],
        "array_name": array_name,
        "width": image.width,
        "height": image.height
    })

struct_definitions = []
for image in images:
    members = []
    members.append(image["battery_percentage"]) # Battery percentage
    members.append(32) # Depth
    members.append("ZPixmap") # Format
    members.append(0) # Offset
    members.append("(char *) " + image["array_name"]) # Data
    members.append(image["width"]) # Width
    members.append(image["height"]) # Height
    members.append(32) # Bitmap pad
    members.append(4 * image["width"]) # Bytes per line
    struct_definitions.append("{" + ",".join(map(str, members)) + "},")

struct_definitions = "\n    ".join(struct_definitions)

image_array_definition = f"""
struct {{
    unsigned char battery_percentage;
    struct BatteryIndicatorImage* image;
}} battery_percentages[] = {{
    {struct_definitions}
}};
""".strip()
output.append(image_array_definition)

with open(args.output, "w", encoding="utf-8") as f:
    f.write("\n\n".join(output))

main()
