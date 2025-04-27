import serial
import time

def image_to_binary_txt(image_path, output_txt):
    with open(image_path, "rb") as img:
        binary_data = img.read()
    
    with open(output_txt, "w") as f:
        f.write(binary_data.hex())  # Write as hex string

def send_to_serial(txt_file, port='COM3', baudrate=115200):
    ser = serial.Serial(port, baudrate, timeout=1)
    time.sleep(2)

    with open(txt_file, 'r') as f:
        data = f.read()

    ser.write(b'S')  # Start signal to Arduino
    time.sleep(0.1)

    chunk_size = 32
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        ser.write(chunk.encode())
        time.sleep(0.01)  # Small delay to avoid overflow

    # Send end marker
    ser.write(b'IMG_END')
    ser.close()

if __name__ == "__main__":
    input_image = r"D:\nRF24_Image_Transmission\Images\input_images\test2.jpeg"
    output_txt = "image_binary.txt"
    image_to_binary_txt(input_image, output_txt)
    send_to_serial(output_txt)
