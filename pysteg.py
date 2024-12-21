#!/usr/bin/env python3


import argparse
from PIL import Image


def print_banner():
    print(r"""
                     _____ __               
        ____  __  __/ ___// /____  ____ _   
       / __ \/ / / /\__ \/ __/ _ \/ __ `/   
      / /_/ / /_/ /___/ / /_/  __/ /_/ /    
     / .___/\__, //____/\__/\___/\__, /     
    /_/    /____/               /____/      
                                             
    """)


def get_args():
    parser = argparse.ArgumentParser(description="Embed/Extract data to/from images")

    parser.add_argument("command", help="embed/extract")
    parser.add_argument("image", help="image for embedding/extracting data to/from")
    parser.add_argument("-s","--secret", help="secret text to be embedded")

    args = parser.parse_args()

    if args.command == "embed" and not args.secret:
        parser.error("enter the secret text to be embedded")

    return args


def secret_to_binary(secret):
    secret += "\x00"
    binary_secret = ""

    for char in secret:
        binary_secret += format(ord(char), "08b")
        
    return binary_secret


def image_to_pixels(image):
    image = Image.open(image, "r")

    pixels = list(image.getdata())

    pixel_list = []

    for pixel in pixels:
        pixel_list.extend(list(pixel))
    
    return pixel_list


def modify_pixel_list(pixel_list, binary_secret):
    data_length = len(binary_secret)

    for bit in range(data_length):
        if binary_secret[bit] == "0" and pixel_list[bit]%2 != 0:
            pixel_list[bit] -= 1
    
        if binary_secret[bit] == "1" and pixel_list[bit]%2 == 0:
            pixel_list[bit] -= 1
    
    return pixel_list


def make_secret_pixels(modified_pixel_list):
    secret_pixels = []

    pixel = 0

    while pixel < len(modified_pixel_list):
        secret_pixels.append(tuple(modified_pixel_list[pixel:pixel+3]))

        pixel += 3
    
    return secret_pixels


def pixel_to_image(image, secret_pixels):
    image = Image.open(image, "r")

    image_length = image.size[0]

    (x_coordinate, y_coordinate) = (0, 0)

    for pixel in secret_pixels:
        image.putpixel((x_coordinate, y_coordinate), pixel)

        if (x_coordinate == image_length-1):
            x_coordinate = 0
            y_coordinate += 1
        
        else:
            x_coordinate += 1
    
    return image


def pixel_to_secret(pixel_list):
    secret_text = ""
    binary_secret = ""
    
    pixel = 0

    while True:
        if (pixel_list[pixel]%2 == 0):
            binary_secret += "0"
        
        else:
            binary_secret += "1"
        
        if (pixel+1)%8 == 0:
            ascii = int(binary_secret, 2)

            if ascii == 0:
                break
            
            else:
                secret_text += chr(ascii)
                binary_secret = ""
        
        pixel += 1
    
    return secret_text


def embed(image, secret):
    binary_secret = secret_to_binary(secret)

    pixel_list = image_to_pixels(image)

    modified_pixel_list = modify_pixel_list(pixel_list, binary_secret)

    secret_pixels = make_secret_pixels(modified_pixel_list)

    secret_image = pixel_to_image(image, secret_pixels)

    secret_image.save("secret_image.png")

    print(f"The given data has been embedded into {image}")


def extract(image):
    pixel_list = image_to_pixels(image)

    secret_text = pixel_to_secret(pixel_list)

    for char in secret_text:
        if ord(char) not in range(0, 256):
            print(f"No embedded data found inside {image}")
            
            return
    
    print(f"The secret data inside {image} is\n{secret_text}") 


def main():
    print_banner()

    args = get_args()

    if args.command == "embed":
        embed(args.image, args.secret)
    
    if args.command == "extract":
        extract(args.image)
        

if __name__ == "__main__":
    main()