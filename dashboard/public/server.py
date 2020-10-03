import http.server
import socketserver

PORT = 8088
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(('', PORT), Handler)
print('Server running at the port: ', PORT)
httpd.serve_forever()