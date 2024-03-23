import cv2
import pytesseract

# 이미지 파일을 로드합니다
image = cv2.imread('test.jpg')

# 번호판 인식을 위한 이미지 전처리
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
edged = cv2.Canny(blur, 30, 200)

# 윤곽선 검출
contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 윤곽선을 기반으로 번호판 후보를 찾음
plate = None
for contour in contours:
    # 윤곽선의 근사치를 계산
    approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
    if len(approx) == 4:  # 번호판은 일반적으로 4각형
        plate = approx
        break

# 번호판 영역 추출 및 표시
if plate is not None:
    cv2.drawContours(image, [plate], -1, (0, 255, 0), 3)
    x, y, w, h = cv2.boundingRect(plate)
    plate_image = image[y:y+h, x:x+w]

    # pytesseract를 사용하여 번호판의 텍스트 추출
    plate_text = pytesseract.image_to_string(plate_image, lang='kor')
    print("Detected plate number:", plate_text.strip())
else:
    print("Plate not found")

# 결과 이미지 표시
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
