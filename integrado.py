import shutil
import os



while (True):

	print("MENU DE OPCIONES. \n")
	print("0- INICIAR EL RECONOCIMIENTO")
	print("1- VER LISTA DE USUARIOS")
	print("2- AGREGAR UN USUARIO")
	print("3- ELIMINAR UN USUARIO")
	print("4- ENTRENAR LA RED")
	print("5- VER EL REGISTRO DE ENTRADAS")
	print("6 -REENTRENAR LA RED")
	print("7 -CAMBIAR LOS PARAMETROS")
	print("8- Salir")
	try:
		modo = int(input('\nIngresar el modo: '))
		if (modo==1):
			f=open("database.txt","r")
			print (f.read())
			anykey=input("\nPresione ENTER para regresar al menu: ")
		elif (modo==0):
			print("\nInicializando  el programa. Espere unos segundos.")
			os.system("python3 reconocimiento.py")
		elif (modo==2):
			os.system("python3 agregar_usuario.py")
			print("\nUsuario agregado con exito")
			print("\nEntrenando al nuevo usuario")
			print("\nEste proceso puede demorar algunos minutos")
			os.system("python3 entrenamiento_diferencial.py")
		elif (modo==3):
			contador=0
			q = True
			modo2="1"
			while q:
				user=input("\nEscriba el nombre del usuario a eliminar:   ")
				if (len(user) > 1):
					if os.path.exists("dataset/"+user): 
						shutil.rmtree("dataset/"+user)
						print("\nUsuario eliminado")
						modo2=input("\n Apriete 1 para eliminar otro usuario o ENTER para continuar con el entrenamiento: ")
					else:
						print("\nEl usuario ingresado no existe")
						contador=contador+1
				else:
					print("\n NO SE INGRESO NINGUN CARACTER")
					contador=contador+1	
				if not (modo2 == "1"): q = False	
				if (contador > 2): q=False
			if not (contador > 2):
				print("\nReentrenando el sistema")
				print("\nEste proceso puede demorar varios minutos")
				os.system("python3 entrenamiento.py")
				print("\nSe reentreno correctamente")
				anykey=input("\nPresione ENTER para regresar al menu: ")
			
				
		elif (modo==4):
			print("\nEntrenando la base de datos")
			print("\nEste proceso puede demorar varios minutos")
			os.system("python3 entrenamiento.py")
			print("\nSe entreno correctamente")
			anykey=input("\nPresione ENTER para regresar al menu: ")
		elif (modo==5):
			f=open("log.txt","r")
			print (f.read())
			anykey=input("\nPresione ENTER para regresar al menu: ")
		elif (modo==6):
			print("\nEntrenando la base de datos")
			print("\nEste proceso puede demorar algunos minutos")
			os.system("python3 entrenamiento_diferencial.py")
			print("\nSe entreno correctamente")
		elif (modo==7):
			os.system("python3 parametros.py")
		elif (modo==8):
			exit()
		else:
			print("Modo no encontrado")
			anykey=input("\nPresione ENTER para regresar al menu: ")
	except ValueError:
		print("\nNo se ha ingresado un numero:")
		anykey=input("\nPresione ENTER para regresar al menu: ")


