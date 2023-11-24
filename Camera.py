import numpy as np
import pafy
import cv2

ph = pafy.new("https://www.youtube.com/watch?v=2wqpy036z24")


k = ph.getbest(preftype="mp3")

cap = cv2.VideoCapture(k.url)

while True:
    success, img = cap.read()
    print(img)

cap.release()
cv2.destroyAllWindows()