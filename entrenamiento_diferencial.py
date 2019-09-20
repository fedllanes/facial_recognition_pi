from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import shutil
from pathlib import Path


print("Procesando las imagenes")
imagePaths = list(paths.list_images("dataset"))
data2 = pickle.loads(open("parametros.pickle", "rb").read())
# Cargamos los datos anteriores
knownEncodings = []
knownNames = []
identificadores = []
nombresFicheros = []
my_file = Path("encodings.pickle")
if my_file.is_file():
	data = pickle.loads(open("encodings.pickle", "rb").read())
	numeroDeImagenesAnterior=len(data["names"])
else:
	numeroDeImagenesAnterior=0
valores=1000
valores2=1000
bandera=0

idMaximo=0
#La manera en la que funcionan estos arrays, es que se agrega un índice con su ID, su nombre y su encoding por cada foto. O sea 10 fotos
#De la misma persona, va a tener 10 encodings, y se compara cada foto entre sí. Y luego se cuentan cuantas veces salió el nombre.
#Entonces, no hay necesidad de que tengan un orden predeterminado. SImplemente agregamos las fotos nuevas al final del nuevo array. 
for i in range(numeroDeImagenesAnterior): #Loopeo todo los datos que cargué y le asignó el valor a los nuevos datos el de los viejos.
	knownEncodings.append(data["encodings"][i]) 
	knownNames.append(data["names"][i])
	identificadores.append(data["Identificadores"][i])
	if(i==0): #Busco el ID máximo para saber que usuario darles a los nuevos usuarios
		idMaximo=data["Identificadores"][i]

	else:
		if(idMaximo < data["Identificadores"][i]): #SImplemente esto me dará el ID más alto que se encuentra en la base de datos
			idMaximo=data["Identificadores"][i]

			

	
usuarios=idMaximo-1000+1 	

noDetectar=1
contador=1
nuevoUsuario=0
imagenesEliminadas=0
bandera=0
valores2=0
for (i, imagePath) in enumerate(imagePaths):
	reconocimiento=0
	print("Trabajando en la imagen  {}/{}".format(i + 1,
		len(imagePaths)))
	# Sacamos el nombre de la persona por la carpeta
	name = imagePath.split(os.path.sep)[-2]
	ocu=knownNames.count(name) #Cuando cuantas veces esta el usuario en la base de datos, si no está es uno nuevo.
	if(ocu > 0):
		index=knownNames.index(name) #Nos va a tirar la posicion donde hay una occurencia. O sea, que una de las posiciones donde está el nombre
		valores=identificadores[index] #Es una persona que ya estaba en nuestra base de datos, buscamos cual era su ID
	else:
		nuevoUsuario=nuevoUsuario+1 #No estaba en la base de dato, agregamos uno al valor de usuario nuevo
		#valores=idMaximo+nuevoUsuario #Como siempre, el valor empieza en mil. 

	if(i==0): #Si la bandera es cero, es el primer reconocimiento que hace el programa
		anterior=name #Asignamos a la variable anterior el primer nombre
		nombresFicheros.append(name)


	else: #Todo este loop se hace para evitar hace el proceso de tratamiento de imagen, si ya se trató.
		if(name != anterior): #Primero preguntamos si la imagen que tratamos era del usuario que veníamos tratando o no.
			anterior=name #Si no lo era, ponemos nuestra variable anterior como el nombre
			contador=1 #Contador en uno
			nombresFicheros.append(name)

	
	if(contador <= ocu):  #Ocu es la cantidad de veces que esa persona esta en la base de datos. O sea, la cantidad de veces que no hace falta reconocer.
		contador=contador+1  

			
	else: #Si teníamos 20 fotos, y agregamos 10. ENtonces solo va a reconocer cuando pasemos la foto numero 20.
		contador=contador+1 #OCU va a aumentar su valor.
		image = cv2.imread(imagePath)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	# Armar la caja que encierre la cara de la persona
		boxes = face_recognition.face_locations(rgb,
			model="hog")

	# Caracteristicas faciales
		encodings = face_recognition.face_encodings(rgb, boxes)
	# loop sobre todos los reconocimientos
		for encoding in encodings:
		# Lo agregamos a la lista

			if knownNames.count(name):
				index=knownNames.index(name) 
				valores=identificadores[index]
			else:
				valores2=valores2+1
				valores=idMaximo+valores2
			reconocimiento=1
			knownEncodings.append(encoding)
			knownNames.append(name)
			identificadores.append(valores) 
		if(reconocimiento==0):
			os.remove(imagePath)
			print(" Imagen perteneciente a %s eliminada" % name)
			imagenesEliminadas=1
			










f=open("database.txt","w+")
retraso=0
for i in range(nuevoUsuario+usuarios): #Escribo los valores en la base de dato al final, para lograr que los ID queden en orden.
	loopid=1000+i
	if identificadores.count(loopid): #Existe un problema donde si todas las fotos salen mal, entonces el usuario será agregado, pero no el encoding, entonces el identificadores.index(loopid) no tendrá matches. COn esta línea, nos aseguramos primero que exista.
		index=identificadores.index(loopid)
		f.write("ID: %s  " % (loopid))
		f.write("Nombre: %s \n" % (knownNames[index]).ljust(10))


noreconocimiento=0


	
numeroCarpetas=len(nombresFicheros)
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
		os.rename(imagePath,"dataset/"+i+"/"+"FHY"+str(j)+".jpg") #Cambio el nombre antes para evitar la sobreescritura
	imagePaths = list(paths.list_images("dataset/"+i))
	for (j, imagePath) in enumerate(imagePaths):
		os.rename(imagePath,"dataset/"+i+"/"+str(j)+".jpg")
	 




f.close()
		
		


print("Guardando la informacion")
data = {"encodings": knownEncodings, "names": knownNames, "Identificadores": identificadores}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()
