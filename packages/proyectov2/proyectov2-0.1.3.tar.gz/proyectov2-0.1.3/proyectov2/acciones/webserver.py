import socket
import argparse
import http.server
import socketserver
import socketserver
import functools

def acceder_al_servidor():
    # Servidor web de Python

        host_name = socket.gethostname()
        PaginaWeb = socket.gethostbyname(host_name)
        PuertoServidor = 8080

        class Servidor(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("<html><head><title>Avance Proyecto Bimestral</title></head>", "utf-8"))
                self.wfile.write(bytes("<p>Mensaje: %s</p>" % self.path, "utf-8"))
                self.wfile.write(bytes("<body>", "utf-8"))
                self.wfile.write(bytes("<p>Esta es la pagina web del servidor.</p>", "utf-8"))
                self.wfile.write(bytes("</body></html>", "utf-8"))

        #if __name__ == "__main__":        
        webServer = http.server.HTTPServer((PaginaWeb, PuertoServidor), Servidor)
        print("Servidor inciado http://%s:%s" % (PaginaWeb, PuertoServidor))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Servidor detenido.")

    #Fin del servidor

def acceder_a_los_archivos():
    parser = argparse.ArgumentParser(description='Archivos del servidor del directorio \
                                    directorio.')

    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)

    parser.add_argument('--host', default=ip, type=str, required=False,
                        help='Especifica la ip del servidor.')

    parser.add_argument('--port', default=8080, type=int, required=False,
                        help='Especifica el puerto del servidor.')

    args = parser.parse_args()

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory='/Users/Usuario/OneDrive/Escritorio/Ciclo10/Python/SegundoBimestre/ArchivosPrueba')
    with socketserver.TCPServer((args.host, args.port), handler) as httpd:
        print(f'El servidor funciona en la web {args.host} y en el puerto {args.port}.')
        httpd.serve_forever()