import cv2

def decode_message(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found!")
        return

    stored_length = sum(img[i, 0, 0] << (i * 8) for i in range(4))

    password_length = img[4, 0, 0]

    stored_password = ""
    for i in range(password_length):
        stored_password += chr(img[5 + i, 0, 0])

    entered_password = input("Enter passcode for decryption: ")
    
    if entered_password != stored_password:
        print("❌ Incorrect passcode! Access Denied.")
        return

    message = ""
    idx = 0
    h, w, _ = img.shape
    for row in range(h):
        for col in range(w):
            if row == 0 and col < 5 + password_length:
                continue  
            if idx < stored_length:
                message += chr(img[row, col, 0])  
                idx += 1
            else:
                break

    print("✅ Decrypted message:", message)

if __name__ == "__main__":
    image_path = input("Enter encrypted image file path: ")
    decode_message(image_path)
