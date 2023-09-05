from PIL import Image
import sys
import os.path as path

chunk_size = 0
width = 0
height = 0

def extract_rgb(file_path):
    global chunk_size
    global width
    global height
    img = Image.open(file_path)
    img = img.convert("RGB")
    width, height = img.size
    chunk_size = int(width / 8)
    rgb_values = []

    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            row.append((r, g, b))
        rgb_values.append(row)
    
    return rgb_values

def format_as_avg_arduino_array(rgb_values):
    global chunk_size
    global width
    global height
    bin_str = ""
    output = ""
    bit = 0
    chunk = 0

    for row in rgb_values:
        for pixel in row:
            if (pixel[0] + pixel[1] + pixel[2]) / 3 < 128:
                bin_str = bin_str + "0"
            else:
                bin_str = bin_str + "1"

            if bit % 8 == 7:
                bin_str = "0b" + bin_str.zfill(8)
                output = output + bin_str + ","
                if chunk % chunk_size == chunk_size - 1:
                    output = output + "\n"
                chunk += 1
                bin_str = ""
            bit += 1
    
    return "#define LOGO_HEIGHT   " + str(height) + "\n#define LOGO_WIDTH    " + str(width) + "\nstatic const unsigned char PROGMEM logo_bmp[] ={\n" + output[:-2] + " };\n"

def main(arguments):
    #check if file passed as argument exists
    if not path.exists(arguments[0]):
        print("File does not exist")
        sys.exit(1)
    
    rgb_values = extract_rgb(arguments[0])
    print(format_as_avg_arduino_array(rgb_values))

if __name__ == "__main__":
    # sys.argv = ["png2bin.py", "world-32.png"]
    main(sys.argv[1:])
