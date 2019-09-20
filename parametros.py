import pickle
data = pickle.loads(open("parametros.pickle", "rb").read())
parametros = []

for i in range(len(data["parametros"])):
	parametros.append(data["parametros"][i])

while True:
	print("\nParámetros del sistema")
	print("\n1.Cantidad de fotos a sacar para usuarios nuevos. \nDefecto 30. Valor actual %s" %parametros[0])
	print("\n2.El porcentaje minimo de deteccion. De cero a cien. \nDefecto 80. Valor actual %s" %parametros[1])
	print("\n3.El Numero fisico del PIN GPIO a prender. \nDefecto 8. Valor actual %s" %parametros[2])
	print("\n4.Borrar automaticamente carpetas que no sirvan. 1 para sí. Otro no. \nDefecto 1.  Valor actual %s" % parametros[3])
	print("\n5.La cantidad de frames que debe detectar el sistema para que acepte el reconocimiento. \nDefecto 5. Valor actual %s" %parametros[4])
	print("\n6. La cantidad de segundos que duerme despues de una deteccion\nDefecto 5. Valor actual %s" %parametros[5])
	k=True
	while (k):
		try:
			modo=int(input("\n Escriba el numero del parametros que desee cambiar. Otro para salir:  "))
			if (modo >=1 and modo <= 6):
				k=False
			else:
				print("\n Saliendo del programa")
				exit()
		except ValueError:
				print("\n Saliendo del programa")
				exit()
	
	if(modo==1):
		print("\n1.Cantidad de fotos a sacar para usuarios nuevos. \nDefecto 30. Valor actual %s" %parametros[0])
	if(modo==2):
		print("\n2.El porcentaje minimo de deteccion. De cero a cien. \nDefecto 80. Valor actual %s" %parametros[1])
	if(modo==3):
		print("\n3.El Numero fisico del PIN GPIO a prender. \nDefecto 8. Valor actual %s" %parametros[2])
	if(modo==4):
		print("\n4.Borrar automaticamente carpetas que no sirvan. 1 para sí. Otro no. \nDefecto 1.  Valor actual %s" % parametros[3])
	if(modo==5):
		print("\n5.La cantidad de frames que debe detectar el sistema para que acepte el reconocimiento. \nDefecto 5. Valor actual %s" %parametros[4])
	if(modo==6):
		print("\n6. La cantidad de segundos que duerme despues de una deteccion\nDefecto 5. Valor actual %s" %parametros[5])
	k= True
	while (k):
		try:
			valor=int(input("Ingrese el nuevo valor  "))
			if(valor > 0 and valor < 101):
				parametros[modo-1]=valor
				k=False
			else:
				print("\nEl valor ingresado está fuera de los límites")
				anykey=input("\nPresione ENTER para volver a intentar: ")
		except ValueError:
			print("\nNo se ingreso ningún numero. Intente de nuevo")
			anykey=input("\nPresione ENTER para volver a intentar: ")

				 
	data = {"parametros": parametros}
	f = open("parametros.pickle", "wb")
	f.write(pickle.dumps(data))
	f.close()
	
	q=True
	while (q):
		try:
			modo=int(input("\nDesea cambiar otro valor?. 1 para sí:    "))
			if (modo==1):
				q=False
			else:
				exit()
		except ValueError:
				print("\nSaliendo del programa")
				exit()
