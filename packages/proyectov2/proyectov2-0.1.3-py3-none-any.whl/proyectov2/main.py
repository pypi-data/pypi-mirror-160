#import click
from proyectov2.acciones.webserver import acceder_al_servidor, acceder_a_los_archivos
#@click.command()
#@click.option('--proyecto', default = "Segundo avance", help='informacion del proyecto')

def main():
    print("Bienvenido al sistema periférico pc - celular")
    print("Elija una opción:")
    print ("1. Acceder al sistema.")
    print ("2. Salir.")
    opcion=input()
    while opcion == "1":

        print("A continuación escoja que hacer en el sistema:")
        print("1. Acceder al servidor.")
        print("2. Acceder a los archivos.")

        opcion1=input()

        if opcion1 == "1":
            acceder_al_servidor()
        elif opcion1 == "2":
            acceder_a_los_archivos()
        else:
            print("Se ha ingresado una opción incorrecta.")
        
        print("¿Desea continuar?")
        print("1. Sí.")
        print("2. No.")

        opcion=input()

    print("Gracias por usar el sistema, buen día.")

if __name__ == '__main__':
	main()