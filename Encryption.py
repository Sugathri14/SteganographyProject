import cv2
import os

def encode_message(image_path, output_path, msg, password):
    img = cv2.imread(image_path)  
    if img is None:
        print("Error: Image not found!")
        return

    h, w, _ = img.shape  
    msg_length = len(msg)

    if msg_length > h * w:
        print("Error: Message too long to encode in the given image.")
        return

    # Encode message length in the first 4 pixels
    for i in range(4):
        img[i, 0, 0] = (msg_length >> (i * 8)) & 0xFF

    # Encode password length
    img[4, 0, 0] = len(password)

    # Encode password
    for i in range(len(password)):
        img[5 + i, 0, 0] = ord(password[i])

    # Encode the message
    idx = 0
    for row in range(h):
        for col in range(w):
            if row == 0 and col < 5 + len(password):  
                continue  # Skip password and metadata area
            if idx < msg_length:
                img[row, col, 0] = ord(msg[idx])  
                idx += 1
            else:
                break

    cv2.imwrite(output_path, img)
    print(f"Message encoded successfully in {output_path}")
    os.system(f"start {output_path}")

if __name__ == "__main__":
    image_path = input("Enter image file path: ")
    output_path = "encryptedImage.png"
    msg = input("Enter secret message: ")
    password = input("Enter a passcode: ")
    
    encode_message(image_path, output_path, msg, password)
