import cv2
import numpy as np
from matplotlib import pyplot as plt
from sys import argv
import math
import os
try:
    from PIL import Image
except ImportError:
    import Image    
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

nameImagesPath = [
    'FotosPlacas/Slide1.jpg',
    'FotosPlacas/Slide2.jpg',
    'FotosPlacas/Slide3.jpg',
    'FotosPlacas/Slide4.jpg',
    'FotosPlacas/Slide5.jpg',
    'FotosPlacas/Slide6.jpg',
    'FotosPlacas/Slide7.jpg',
    'FotosPlacas/Slide8.jpg',
    'FotosPlacas/Slide9.jpg',
    'FotosPlacas/Slide10.jpg',
    'FotosPlacas/Slide11.jpg',
    'FotosPlacas/Slide12.jpg',
    'FotosPlacasComErro/Slide1.jpg',
    'FotosPlacasComErro/Slide2.jpg',
    'FotosPlacasComErro/Slide3.jpg',
    'FotosPlacasComErro/Slide4.jpg',
    'FotosPlacasComErro/Slide5.jpg',
    'FotosPlacasComErro/Slide6.jpg',
    'FotosPlacasComErro/Slide7.jpg',
    'FotosPlacasComErro/Slide8.jpg',
    'FotosPlacasComErro/Slide9.jpg',
    'FotosPlacasComErro/Slide10.jpg',
    'FotosPlacasComErro/Slide11.jpg',
    'FotosPlacasComErro/Slide12.jpg'
]
gabaritoPath = [
    "Gabarito/Gabarito AB01.jpg",
    "Gabarito/Gabarito AB02.jpg",
    "Gabarito/Gabarito AC01.jpg",
    "Gabarito/Gabarito AC02.jpg"
]
tolerance = 0.1
imagePath = []
imageModel = []
logSystem = []
colorDefault = "\033[0m"
colorYellow = "\033[33m"
colorGreen = "\033[32m"
colorRed = "\033[31m"
colorTitle = "\033[1m"
colorPercentual = "\033[90m"

def printPercentual(type):
    if type == 0:
        print(colorPercentual + "\033[K", "[ {:<50} ] {}%".format("." * round((imageIndex * (50 / len(nameImagesPath)))), round((imageIndex * (100 / len(nameImagesPath))))) + colorDefault, end="\r") #barrinha de porcentagem
    elif type == 1:
        print(colorPercentual + "\033[K", "[ {:<50} ] {}%".format("." * round((imageIndex * (50 / len(imagePath)))), round((imageIndex * (100 / len(imagePath))))) + colorDefault, end="\r") # carregamento iniciado

def printPercentualFull(type):
    if type == 0:        
        print(colorPercentual + "\033[K", "[ {:<50} ] {}%\n\n".format("." * 50, 100) + colorDefault, end="\r") #carregamento em 100%    
    elif type == 1:
        print(colorPercentual + "\033[K", "[ {:<50} ] {}%\n\n".format("." * 50, 100) + colorDefault, end="\r") # termina contador em 100%

def coordTest(x_coord,y_coord, message, invertPos, duplicate): 
    x=x_coord
    y=y_coord 
    if invertPos == True:
        (b,g,r) = duplicate[x,y]
    else:               
        (b,g,r) = duplicate[y,x]
    #cv2.circle(duplicate, (y,x), 1, (0, 255, 0), -1)
    if (b==0 and g==0 and r==255): 
        auxT.append(message)
        return False                     
    else:
        return True

def showResults():  
    width = 30  
    print("-" * width)
    for i in range(0, len(nameImagesPath)):
        print("{:.<20} {:.^10}".format(
            nameImagesPath[i][11:].replace("/", "").replace(".jpg", ""), 
            logSystem[i]
        ))
    print("-" * width)
    print("\n\n")

os.system('cls' if os.name == 'nt' else 'clear')
print(colorTitle + 'Processando imagens, por favor aguarde!...' + colorDefault)

for imageIndex in range(0, len(nameImagesPath)):
    printPercentual(0)    
    cv2.destroyAllWindows()
    original = cv2.imread(nameImagesPath[imageIndex])
    originalBackup = cv2.imread(nameImagesPath[imageIndex])
    img = cv2.imread(nameImagesPath[imageIndex],0)
    (height, width) = img.shape[:2]
    ret, imgT = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY)

    p1=0
    p2=0
    xi=width
    inc=0
    for y in range (0,height,1):
        for x in range (0,width,1):
            cor = imgT[y,x] 
            if cor!=255 and(p1==0): 
                ponto1=(x,y)
                xi=x
                p1=1
                if x>(width/2):
                    inc=1                           
            if (p1==1) and (inc==1) and (cor!=255) and (x<xi):
                ponto2=(x,y)
                xi=x                
            if (p1==1) and (inc==0) and (cor!=255) and (x>xi):
                ponto2=(x,y)
                xi=x
    cv2.circle(original, (ponto1), 2, (0, 0, 255), -1)
    cv2.circle(original, (ponto2), 2, (0, 0, 255), -1)
    #cv2.imshow("Imagem original com marcações", original)
                        
    angulo = math.atan2 (ponto1[1]-ponto2[1],ponto1[0]-ponto2[0])
    if inc==1:
        angulo = math.degrees(angulo)
    if inc==0:
        angulo = math.degrees(angulo)+180
        aux=ponto1
        ponto1=ponto2
        ponto2=aux        
    
    M = cv2.getRotationMatrix2D(ponto1, angulo, 1.0) 
    imgRotacionada = cv2.warpAffine(imgT, M, (width, height))
    originalRotacionada = cv2.warpAffine(original, M, (width, height))
    originalBackupRotacionada = cv2.warpAffine(originalBackup, M, (width, height))
    pontoInicial=ponto1
    larguraPlaca = 602
    alturaPlaca = 295
    xi=pontoInicial[0]-larguraPlaca+1
    xf=pontoInicial[0]+1
    yi=pontoInicial[1]
    yf=pontoInicial[1]+alturaPlaca
    recorte = originalBackupRotacionada[yi:yf,xi:xf]

    if recorte.shape[0] != 295: 
        recorte = originalBackupRotacionada[yi-4:yf,xi:xf]

    cv2.imwrite("New-%s"%nameImagesPath[imageIndex].replace("/", "-"), recorte)
    custom_config = r'-c tessedit_char_whitelist=ABC012 --psm 3'
    plateText = pytesseract.image_to_string("New-%s"%nameImagesPath[imageIndex].replace("/", "-"), config=custom_config).replace(" ", "").replace("\n","")
    imagePath.append("New-%s"%nameImagesPath[imageIndex].replace("/", "-"))
    imageModel.append(plateText[:4])

printPercentualFull(0)
print(colorTitle + "Analisando modelos de placa!..." + colorDefault)

for imageIndex in range(0, len(imagePath)):    
    printPercentual(1)

    duplicate = cv2.imread(imagePath[imageIndex].replace("/", "-"))
    model = imageModel[imageIndex]
    
    if imageModel[imageIndex] == "AB01":
        gabaritoModel = gabaritoPath[0]
    elif imageModel[imageIndex] == "AB02":
        gabaritoModel = gabaritoPath[1]
    elif imageModel[imageIndex] == "AC01":
        gabaritoModel = gabaritoPath[2]
    elif imageModel[imageIndex] == "AC02":
        gabaritoModel = gabaritoPath[3]

    gabaritoImage = cv2.imread(gabaritoModel)
    difference = gabaritoImage - duplicate
    b, g, r = cv2.split(difference)

    for y in range (0,gabaritoImage.shape[0],1):
        for x in range (0,gabaritoImage.shape[1],1):
            if b[y,x] > 255*tolerance or g[y,x] > 255*tolerance or r[y,x] > 255*tolerance:
                duplicate [y,x]=(0,0,255)

    if cv2.countNonZero(b) != 0 or cv2.countNonZero(g) != 0 or cv2.countNonZero(r) != 0:        
        auxT=[]
        aux=""

        if model == "AB01": 
            a = coordTest(81,  82,  "Q", False, duplicate)
            b = coordTest(62,  58,  "Q", False, duplicate)
            c = coordTest(90,  108, "Q", False, duplicate)
            d = coordTest(234, 302, "R", True,  duplicate)
            e = coordTest(210, 401, "R", True,  duplicate)
            f = coordTest(101, 401, "E", True,  duplicate)
            g = coordTest(194, 503, "R", True,  duplicate)

            if a and b and c and d and e and f and g == True:
                aux = colorGreen + "Aceitavel" + colorDefault
            else:       
                aux = colorRed + " ".join(sorted(set(auxT))) + colorDefault        
            logSystem.append(aux)

        if model == "AB02":
            a = coordTest(122, 121, "Q", False, duplicate)
            b = coordTest(148, 83,  "Q", False, duplicate)
            c = coordTest(173, 64,  "Q", False, duplicate)
            d = coordTest(127, 283, "R", True,  duplicate)
            e = coordTest(151, 401, "R", True,  duplicate)
            f = coordTest(174, 501, "R", True,  duplicate)

            if a and b and c and d and e and f == True:
                aux = colorGreen + "Aceitavel" + colorDefault
            else:
                aux = colorRed + " ".join(sorted(set(auxT))) + colorDefault 
            logSystem.append(aux)

        if model == "AC01":
            a = coordTest(221, 110, "Q", False, duplicate)
            b = coordTest(194, 84,  "Q", False, duplicate)
            c = coordTest(101, 84,  "E", False, duplicate)
            d = coordTest(244, 134, "Q", False, duplicate)
            e = coordTest(58,  454, "R", True,  duplicate)
            f = coordTest(151, 431, "R", True,  duplicate)
            g = coordTest(233, 406, "R", True,  duplicate)
            
            if a and b and c and d and e and f and g == True:
                aux = colorGreen + "Aceitavel" + colorDefault
            else:
                aux = colorRed + " ".join(sorted(set(auxT))) + colorDefault 
            logSystem.append(aux)

        if model == "AC02":
            a = coordTest(161, 180, "Q", False, duplicate)
            b = coordTest(125, 260, "Q", False, duplicate)
            c = coordTest(125, 101, "E", False, duplicate)
            d = coordTest(175, 310, "Q", True,  duplicate)
            e = coordTest(55,  460, "E", True,  duplicate)
            f = coordTest(150, 436, "R", True,  duplicate)
            g = coordTest(245, 410, "R", True,  duplicate)
            
            if a and b and c and d and e and f and g == True:
                aux = colorGreen + "Aceitavel" + colorDefault
            else:
                aux = colorRed + " ".join(sorted(set(auxT))) + colorDefault 
            logSystem.append(aux)

    cv2.imwrite("Draw-%s"%nameImagesPath[imageIndex].replace("/", "-"), duplicate)
    #cv2.imshow("Original-%d-%s"%(imageIndex, gabaritoModel), gabaritoImage)
    #cv2.imshow("Duplicate-%d-%s"%(imageIndex, gabaritoModel), duplicate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

printPercentualFull(1)
print(colorTitle + "Resultados:" + colorDefault)
showResults()