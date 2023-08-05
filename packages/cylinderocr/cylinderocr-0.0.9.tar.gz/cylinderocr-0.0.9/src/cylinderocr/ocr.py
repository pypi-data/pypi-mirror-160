import numpy as np
import os
from paddleocr import PaddleOCR
from statistics import mode
import time
from getmac import get_mac_address as gma


def inference(img_path, lang):
    try:
        macadd=gma()
        uniqueadd =["60:e3:2b:34:66:ce"]
        if macadd in uniqueadd:
            print("Configured Sucessfully")
            ocr = PaddleOCR(use_angle_cls=True, lang=lang,use_gpu=False,rec_model_dir='paddleocr/rec/',det_model_dir='paddleocr/det/')
            result = ocr.ocr(img_path, cls=True)
            txts = [line[1][0] for line in result]
            scores = [line[1][1] for line in result]
            for i,j in enumerate(scores):       # if scores are lesser then 70 %
                if float(j)>0.90:
                    pass
                else:
                    scores.pop(i)
                    txts.pop(i)
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
            for i in txts:  
                try:                  # if txts >20
                    if float(i)>=20.0:
                        return "-2",float(0.0) #could not process
                except:
                    pass
            return str(txts[0]),float(scores[0])
        else:
            return "-3",float(0.0)  #could not configured
    except:
        return "-4",float(0.0) # could not process,Exception
    

'''if __name__ == "__main__":
    txts,scores=inference("img2.jpg","en")
    print(txts," ",type(txts)," ",scores," ",type(scores))'''
