import numpy as np
import os
from statistics import mode
import time
import re
import cv2
from getmac import get_mac_address as gma


def inference(img_path,ocr):
    try:
        macadd=gma()
        uniqueadd =["60:e3:2b:34:66:ce","a8:7e:ea:41:ad:34","1c:69:7a:ae:44:32"]
        if macadd:
            print("Configured Sucessfully")
            image= cv2.imread(img_path)
            zoom_factor=6
            img_path= cv2.resize(image, (300,300),fx=zoom_factor, fy=zoom_factor,interpolation = cv2.INTER_NEAREST)
            value=-55
            hsv = cv2.cvtColor(img_path, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            v = cv2.add(v,value)
            v[v > 255] = 255
            v[v < 0] = 0
            final_hsv = cv2.merge((h, s, v))
            img_path = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
            result = ocr.ocr(img_path, cls=True)
            print(result)
            txts = [line[1][0] for line in result]
            scores = [line[1][1] for line in result]
            if len(txts)==0:          #no object detected
                return "-1",float(0.0)  #object not found
            try:                          # most repeating txts
                txts=[mode(txts)]
                scores=[max(scores)]
            except:
                pass       
            if len(txts)>1:           # if both txts are different
                case=np.argmax(scores)
                scores=[scores[case]]
                txts=[txts[case]]  
            try:                  # if txts >20
                    if float(i[0])>=20.0:
                        return "-2",float(0.0) #could not process
            except:
                    pass
            regex = '[+-]?[0-9]+\.[0-9]+'
            if(re.search(regex, txts[0])):
                    return str(txts[0]),float(scores[0])
            else:
                    return "-2",float(0.0)
        else:
            return "-3",float(0.0)  #could not configured
    except:
        return "-4",float(0.0) # could not process,Exception
    

'''if __name__ == "__main__":
    txts,scores=inference("img2.jpg","en")
    print(txts," ",type(txts)," ",scores," ",type(scores))'''
