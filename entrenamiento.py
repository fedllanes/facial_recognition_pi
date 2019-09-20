from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import shutil


print("Procesando las imagenes")
imagePaths = list(paths.list_images("dataset"))
data2 = pickle.loads(open("parametros.pickle", "rb").read())

knownEncodings = []
knownNames = []
identificadores = []
nombresFicheros = []
valores=1000
bandera=0
valores2=1000
imagenesEliminadas=0
# loopeas sobre todas las imagenes
for (i, imagePath) in enumerate(imagePaths):
	reconocimiento=0
	# extract the person name from the image path
	print(" Trabajando en la imagen {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]
	#print(name)
	if(i==0): #Si la bandera es cero, es el primer reconocimiento que hace el programa
		anterior=name #Asignamos a la variable anterior el primer nombre
		nombresFicheros.append(name)
		f=open("database.txt","w+")
		f.write("ID: %s  " % valores)
		f.write("Nombre: %s \n" % (name).ljust(10))
		f.close()
	else:
		if(name != anterior):
			valores=valores+1
			anterior=name
			nombresFicheros.append(name)
			f=open("database.txt","a")
			f.write("ID: %s  " % valores)
			f.write("Nombre: %s \n" % (name).ljust(10))
			f.close()


	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# Detectar la caja que contiene la cara
	boxes = face_recognition.face_locations(rgb,
		model="hog")

	# Procesar las caracteristicas faciales
	encodings = face_recognition.face_encodings(rgb, boxes)

	# Para cada cara detectada
	for encoding in encodings:
		# Lo agregamos
		if(bandera==0):
			anterior2=name
			bandera=1
		else:
			if(anterior2 != name):
				anterior2=name
				valores2=valores2+1
		
		
		
		
		reconocimiento=1
		knownEncodings.append(encoding)
		knownNames.append(name)
		identificadores.append(valores2)
	if (reconocimiento==0):
		os.remove(imagePath)
		print(" Imagen perteneciente a %s eliminada" % name)
		imagenesEliminadas=1
		



		
		
	
	
	
	
	
f=open("database.txt","w+")
retraso=0
numeroCarpetas=len(nombresFicheros)
for i in range(numeroCarpetas): #Escribo los valores en la base de dato al final, para lograr que los ID queden en orden.
	loopid=1000+i
	if identificadores.count(loopid): #Existe un problema donde si todas las fotos salen mal, entonces el usuario será agregado, pero no el encoding, entonces el identificadores.index(loopid) no tendrá matches. COn esta línea, nos aseguramos primero que exista.
		index=identificadores.index(loopid)
		f.write("ID: %s  " % loopid)
		f.write("Nombre: %s \n" % (knownNames[index]).ljust(10))


		
noreconocimiento=0
for i in range(numeroCarpetas):
	if not knownNames.count(nombresFicheros[i]):
		print("No se reconocio a %s" %nombresFicheros[i])
		noreconocimiento=1		

if(noreconocimiento==1):
	modo=data2["parametros"][3]
	if (modo == 1):
		for i in range(numeroCarpetas):
			if not knownNames.count(nombresFicheros[i]):
				shutil.rmtree("dataset/"+nombresFicheros[i])
		print("Ficheros eliminados")
	else:
		print("Cerrando el programa sin eliminarlas")		


imagePaths = list(paths.list_images("dataset"))		
contador=0
for i in nombresFicheros:
	#print (i)
	imagePaths = list(paths.list_images("dataset/"+i))
	for (j, imagePath) in enumerate(imagePaths):
		os.rename(imagePath,"dataset/"+i+"/"+"FHY"+str(j)+".jpg")#Cambio el nombre para evitar sobreescritura
	imagePaths = list(paths.list_images("dataset/"+i))
	for (j, imagePath) in enumerate(imagePaths):
		os.rename(imagePath,"dataset/"+i+"/"+str(j)+".jpg")		
		
		
print("Guardando la informacion")
data = {"encodings": knownEncodings, "names": knownNames, "Identificadores": identificadores}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()
