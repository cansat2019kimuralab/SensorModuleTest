import numpy as np
import cv2
from PIL import Image

def IMGtoBYTES(img):
    img_string = img.tobytes()
    #print (img_string)
    return img_string

def BYTEStoIMG(img_string):
    img_array = np.fromstring(img_string,dtype ='uint8') #バイトデータ→ndarray変換
    img_array = np.reshape(img_array,(240,320))

    #dec_img = cv2.imdecode(img_array, 0)
    pil_img = Image.fromarray(img_array)

    #cv2.imshow("decoded_image", dec_img)
    #pil_img.show()
    pil_img.save("decoded_target15.jpg")
    return pil_img

if __name__ == "__main__":
    img = cv2.imread("target15.jpg",0) #cv2.imreadで画像ファイルを開いてnumpy.ndarrayを取得
    str = IMGtoBYTES(img)
    BYTEStoIMG(str)
