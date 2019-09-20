from imutils import paths
import cv2
import os
from decimal import Decimal
import numpy 
import pickle
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

data2 = pickle.loads(open("parametros.pickle", "rb").read())
face_id = input('\n Ingresar nombre: ')
q = True
cantidad=data2["parametros"][0]
imagePaths = list(paths.list_images("dataset"))
usuarioExistente=0 #Buscamos un usuario con el mismo nombre, si existe, agregaremos la foto ahí.
fotosUsuarioExistente=0 #Debemos saber la cantidad de fotos por un tema de numeración.

for (i, imagePath) in enumerate(imagePaths):

    name = imagePath.split(os.path.sep)[-2]
    if(face_id==name): #Veo si el usuario ya esta en la base de datos
        fotosUsuarioExistente=len(list(paths.list_images("dataset/"+name))) #SI lo esta, tenemos que saber cuantas fotos tenemos de el o ella.

if not os.path.exists("dataset/"+face_id): #Nos fijamos si es que haycarpeta del usuario
    os.mkdir("dataset/"+face_id) #SI no existe, entonces la creamos
    
    
print("\n MIRAR A LA CAMARA")

count = 0

while(True):
    
    ret, img = cam.read()
    ret, backupImage=cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
            valorDeBlurry=cv2.Laplacian(img[y-10:y+h+10,x-10:x+w+10], cv2.CV_64F).var() #Detección de Blurry
            cv2.putText(img,str(round(Decimal(valorDeBlurry),0)), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)	
            cv2.putText(img,"%s/%s"%(count,cantidad), (400, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
            img_lab = cv2.cvtColor(img[y-10:y+h+10,x-10:x+w+10], cv2.COLOR_BGR2HSV) #HSV 
            img_lab_new=img_lab[:,:,2]
            img_lab_numpy=numpy.array(img_lab_new)
            img_lab_intensidad=numpy.average(img_lab_numpy)
            cv2.putText(img,str(round(Decimal(img_lab_intensidad),0)), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)	
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)  
            if(valorDeBlurry > 100 and img_lab_intensidad > 70):
                cv2.imwrite("dataset/"+ face_id + '/' + str(count+fotosUsuarioExistente) + ".jpg",backupImage[y-20:y+h+20,x-20:x+w+20])
                count += 1
        
    cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff 
    if k == 27:
        break
    elif count >= cantidad: 
         break

print("Fotos agregadas con exito")
cam.release()
cv2.destroyAllWindows()


