# save_received_image.py
import serial
import cv2
import numpy as np
from io import BytesIO

def save_from_serial(port='COM9', baudrate=115200, output_path=r"Images/received_images/output.jpg"):
    ser = serial.Serial(port, baudrate, timeout=1)
    received_data = bytearray()
    window_name = "Live Image Construction"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    print("Receiving...")

    while True:
        if ser.in_waiting:
            chunk = ser.read(ser.in_waiting)
            if b'IMG_END' in chunk:
                chunk = chunk.replace(b'IMG_END', b'')
                received_data.extend(chunk)
                break
            received_data.extend(chunk)
            
            # Try to display partial image as it's being received
            try:
                binary_data = bytes.fromhex(received_data.decode())
                img_array = np.frombuffer(binary_data, dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                if img is not None:
                    cv2.imshow(window_name, img)
                    cv2.waitKey(1)
            except:
                # Ignore errors from incomplete image data
                pass

    ser.close()

    # Convert hex back to binary for final save
    binary_data = bytes.fromhex(received_data.decode())
    
    # Display final image
    img_array = np.frombuffer(binary_data, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is not None:
        cv2.imshow(window_name, img)
        cv2.waitKey(0)
    
    # Save to file
    with open(output_path, 'wb') as f:
        f.write(binary_data)

    print(f"Image saved to {output_path}")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    save_from_serial()