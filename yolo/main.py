from ultralytics import YOLO
import cv2
from paddleocr import PaddleOCR
import re  # Import thư viện re để sử dụng regex
import matplotlib.pyplot as plt  # Dùng matplotlib để hiển thị ảnh trong Colab

# Khởi tạo PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Chế độ nhận diện góc và ngôn ngữ là tiếng Anh

# Load model YOLO
license_plate_detector = YOLO(r"number-plate-recognition-using-yolov11\models\best_final.pt")

# Load image (ảnh bạn muốn xử lý)
image_path = "car_entry_1745730968.jpg"  # Đường dẫn đến ảnh
image = cv2.imread(image_path)

# Detect license plates
license_plates = license_plate_detector(image)

# Annotate the image with detected license plates and perform OCR on the detected plates
for plate in license_plates:
    for bbox in plate.boxes:
        x1, y1, x2, y2 = bbox.xyxy[0]  # Get bounding box coordinates

        # Convert to integers
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

        # Draw rectangle around the detected license plate
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Crop the detected license plate region from the image
        plate_image = image[y1:y2, x1:x2]

        # Use PaddleOCR to read the text from the cropped license plate image
        result = ocr.ocr(plate_image, cls=True)

        # Extract text from the OCR result
        plate_text = ""
        for line in result[0]:
            plate_text += line[1][0] + " "  # Add detected text in each line

        # Clean the detected text using regex to remove any characters that are not letters or digits
        clean_plate_text = re.sub(r'[^A-Za-z0-9]', '', plate_text.strip())

        # Show the detected and cleaned text on the image
        print("Detected license plate text:", clean_plate_text)  # Print the recognized license plate text
        cv2.putText(image, clean_plate_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

# Save the annotated image with detected text
output_image_path = "./data/output/annotated_license_plate_image_with_text_paddleocr.jpg"
cv2.imwrite(output_image_path, image)

# Convert BGR to RGB for displaying in matplotlib
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Display the annotated image with detected text using matplotlib
plt.imshow(image_rgb)
plt.axis('off')  # Hide axes
plt.show()
