from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--output")
parser.add_argument("--input")
parser.add_argument("--variable-name")

args = parser.parse_args()

with open(args.output, "w") as output:
    image = Image.open(args.input)
    output.write(f"int {args.variable_name}_WIDTH = {image.width};\n")
    output.write(f"int {args.variable_name}_HEIGHT = {image.height};\n")
    output.write(f"int {args.variable_name}_DEPTH = 32;\n\n")
    output.write(f"unsigned char {args.variable_name}[] = {{\n")
    for pixel in image.getdata():
        red, green, blue, opacity = pixel
        output.write("    ")
        for color_value in [red, green, blue, opacity]:
            output.write(str(color_value))
            output.write(",")
        output.write("\n")
    output.write("};")
