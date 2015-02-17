# Basic test of OpenCV python wrapper, from:
# https://help.ubuntu.com/community/OpenCV

from cv2.cv import *

img = LoadImage("ms.png")
NamedWindow("opencv")
ShowImage("opencv",img)
WaitKey(0)
