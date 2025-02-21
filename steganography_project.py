 
# Secure Data Hiding in Image Using Steganography
# Developed in Python using LSB Steganography

from PIL import Image
import numpy as np

# Function to encode message into an image
def encode_message(image_path, secret_message, output_path):
    img = Image.open(image_path).convert("RGB")
    pixels = np.array(img)

    secret_message += "####"
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
    
    flat_pixels = pixels.flatten()
    if len(binary_message) > len(flat_pixels):
        raise ValueError("Message is too long to hide in this image.")
    
    for i in range(len(binary_message)):
        flat_pixels[i] = (flat_pixels[i] & 0xFE) | int(binary_message[i])
    
    new_pixels = flat_pixels.reshape(pixels.shape)
    new_img = Image.fromarray(new_pixels.astype(np.uint8))
    new_img.save(output_path)

# Function to decode the hidden message from an image
def decode_message(image_path):
    img = Image.open(image_path).convert("RGB")
    pixels = np.array(img).flatten()

    binary_message = ''.join(str(pixels[i] & 1) for i in range(len(pixels)))
    
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        char = chr(int(byte, 2))
        if message.endswith("####"):
            break
        message += char

    return message.replace("####", "")

# Example usage
if __name__ == "__main__":
    input_image = "sample_image.png"
    encoded_image = "encoded_image.png"
    secret_msg = "Confidential Data!"

    encode_message(input_image, secret_msg, encoded_image)
    decoded_text = decode_message(encoded_image)

    print("Decoded Message:", decoded_text)
