# USAGE
# python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import RPi.GPIO as GPIO
from time import sleep
from decimal import Decimal
import datetime

data2 = pickle.loads(open("parametros.pickle", "rb").read())

#### PARAMETROS DEL PROGRAMA ###

minimoDeteccion=data2["parametros"][1]/100 #El porcentage mínimo de confianza, en este caso 70%
framesMinimos=data2["parametros"][4] #LA CANTIDAD DE FRAMES NECESARIOS ANTES QUE SE ENCENDER EL LED.
pinLed=data2["parametros"][2]
tiempo=data2["parametros"][5]
##########################
dormir=0


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinLed, GPIO.OUT, initial=GPIO.LOW) 

framesDetectados=0 #Para exigir que se reconozca una persona solo despues de una cantidad determinada de frames

data = pickle.loads(open("encodings.pickle", "rb").read())
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

print(" Iniciando la camara")
vs = VideoStream(src=0).start()
time.sleep(2.0)
nombreAnterior="Hola"

fps = FPS().start()
GPIO.output(pinLed, GPIO.LOW) #POnemos el pin del led en cero por seguridad
# loopear cada frame
while True:
	# Cambiamos al tamaño a 500pixeles del feed de la camara
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	backupImage=frame
	counter=0 #Con esto vamos a contar la cantidad de veces que "adivinó" una cara
	totalCounter=0 #Acá contamos lo anterior, pero también las veces que considera que no es ninguna de las que tiene en la base de dato
	detection=0 #Cada vez que detecte una cara, vamos a poner la bandera de detección en 1
	
	if (dormir==1) :
		cv2.imwrite("log/"+ datetime.datetime.now().strftime("%d-%m-%Y %H:%M")+ "  ID:"+ str(id)+ "  Nombre:" + nombreDetectado +".jpg", backupImage) #Solo entra aquí, si ya detectó una cara. Por lo tanto, lo imprimimos al principio para evitar que haya texto en nuestra imagen.
		dormir=2
	elif (dormir==2):
		dormir=0
		sleep(tiempo)    #Por alguna razón, para que la imagen quede con el texto, hay que esperar que termine el frame donde detecta, y uno más.
		GPIO.output(pinLed, GPIO.LOW) #Pnerlo en cero para que se apague luego de imprimir el mensaje
	

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# Detectar Caratas
	rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)

	# Reordenamiento de las coordenadas
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

	# Computaciones de las caracteristicas faciales
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []
	# Loop en cada cara
	for encoding in encodings:
		# Se intenta matchear cada cara con la informacion de nuestra base de datos
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown" 
		#if False in matches:
			#totalCounter=totalCounter+1 #No hubo match.
		if True in matches:
			# Buscamos los indices de todos los matches
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}
			counts2 = {}

			# Loopeamos en todos los indices, para contar cual fue el mas comun
			for i in matchedIdxs:
				counter=counter+1
				totalCounter=totalCounter+1
				name = data["names"][i]
				id = data["Identificadores"][i]
				counts[name] = counts.get(name, 0) + 1
				counts2[id] = counts2.get(id, 0) + 1

			# Determinamos quien fue el "ganador"
			name = max(counts, key=counts.get)
			id= max(counts2, key=counts2.get)
			totalCounter=data["names"].count(name)
			#print(counts[name])
			#print(totalCounter)

		
		#  Actualizamos la lista de nombres
		names.append(name)
		detection=1 #Significa que detectó algo
		framesDetectados=framesDetectados+1
		if (counter != 0 and counts.get(name, 0)/totalCounter > minimoDeteccion and counts.get(name, 0)/counter > minimoDeteccion):  #Nos aseguramos que que la deteccion pasé el mínimo
			if (framesDetectados == 1): nombreAnterior=name #Si es el primer frame que detecta, no lo puede comparar con el anterior, así que a nombre anterior le ponemos el que detectó
			if (framesDetectados > 1 and nombreAnterior!=name ): framesDetectados=0 #Si ya detectó uno antes pero no coincide con el nuevo, entonces lo ponemos en cero
		else: 
			framesDetectados = 0 #No detectó ninguna cara, ponemos el contador en cero
		#El detector de frame se podría poner cuando dibuja la imagen, para evitar hacer el mismo for varias veces, se lo pone acá para hacer la lectura y modificacion del código más fácil
			if 	(counter != 0 and counts.get(name, 0)/totalCounter > 0.7): 
				counts[name] = 0
				name2 = max(counts, key=counts.get)
				totalCounter2=data["names"].count(name2)
				#print(counts[name2])
				if (counts.get(name2, 0)/totalCounter2 > 0.7): 
					print("HAY UNA POSIBLE DUPLICACION EN LA BASE DE DATOS ENTRE %s y %s" % (name, name2))
				
		
	# loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		y = top - 15 if top - 15 > 15 else top + 15
		if (counter != 0): ## Preguntamos esto, porque si es cero, el if siguiente dará error
			if(counts.get(name, 0)/totalCounter < minimoDeteccion): #Preguntamos si la cantidad de veces que detectó a nuestro candidato es menor al 70%
				cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
				cv2.putText(frame, "Unknown", (left, y-30), cv2.FONT_HERSHEY_SIMPLEX, #Como es menor al 70%, vamos a decirle que lo tome como un extraño, podemos aumentar este parámetro a gusto, por defecto, si no pasamos por este loop, el valor es 50% que es muy bajo a mi gusto
				0.75, (0, 0, 255), 1)
			else: #La detección tiene una confianza superior al minimo
				cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255-850*((counts.get(name, 0)/totalCounter)-minimoDeteccion)), 2)
				cv2.putText(frame, name, (left, y-30), cv2.FONT_HERSHEY_SIMPLEX,
				0.75, (0, 255, 0), 1)
				cv2.putText(frame, str(round(Decimal(counts.get(name, 0)/counter),2)), (left, y), cv2.FONT_HERSHEY_SIMPLEX, #Acá nos da la probabilidad de que el usuario "adivinado" sea el, SI asumimos que es alguien de la base de datos
				0.75, (0, 255, 255-850*((counts.get(name, 0)/totalCounter)-minimoDeteccion)), 1)
				cv2.putText(frame, str(round(Decimal(counts.get(name, 0)/totalCounter),2)), (left+65, y), cv2.FONT_HERSHEY_SIMPLEX, #Acá la probabilidad de el usuario adivinado sea el, SIN asumir que es necesariamente alguien de la base de datos(cuenta las veces que adivinó unknown)
				0.75, (0, 255, 255-850*((counts.get(name, 0)/totalCounter)-minimoDeteccion)), 1)
		else: #Acá vio una cara, pero el coutner es cero, porque nunca pensó que era alguien de la base de dato, si llegamos acá, name será unknown.
				cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
				cv2.putText(frame, name, (left, y-30), cv2.FONT_HERSHEY_SIMPLEX,
				0.75, (0, 0, 255), 1)


	fps.stop() #Paramos el contador de FPS
	cv2.putText(frame,"FPS:{:.2f}".format(fps.fps()), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1) #Mostramos el framerate
	cv2.putText(frame,str(framesDetectados), (440, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1) #Mostramos cuantos frames va detectando
	fps = FPS().start() #Reiniciamos el contador
	
	
	key = cv2.waitKey(1) & 0xFF
	
	
	# Si aprietan q se sale del loop
	if key == ord("q"):
		GPIO.output(pinLed, GPIO.LOW) 
		break
		
		
	if(detection==1):
		if (framesDetectados >= framesMinimos):
			nombreDetectado=nombreAnterior
			GPIO.output(pinLed, GPIO.HIGH)
			cv2.putText(frame,"Se ha correctamente", (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)	
			cv2.putText(frame,"identificado a %s" % nombreDetectado, (30, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
			framesDetectados=0
			f=open("log.txt","a") #Abrimos nuestro archivo de log para escribir los datos de la sesion 
			f.write("ID: %s  " % id)
			f.write("Nombre: %s " % (nombreDetectado).ljust(10))
			f.write("Horario: %s \n" % datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
			f.close()
			if (dormir==0): dormir=1
	else:
		GPIO.output(pinLed, GPIO.LOW) 
		framesDetectados = 0 #No detectó a Nadie, ponemos el contador en cero
		
	cv2.imshow("Frame", frame)
		

	# Actualizar el contador FPS
	fps.update()
	




GPIO.output(8, GPIO.LOW)
cv2.destroyAllWindows()
vs.stop()
