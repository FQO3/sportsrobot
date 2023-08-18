# coding:utf-8 
import socket
import os
 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
server_socket.bind(('192.168.4.1', 8080))
 
server_socket.listen(128)
print('server is running ar 192.168.4.1:{}'.format(8080))
 
while True:
    client_socket, client_addr = server_socket.accept()
    data = client_socket.recv(1024).decode('gbk')
    path = ''
    if data:
        path=data.splitlines()[0].split()[1]
        print('请求的路径是：{}'.format(path))
    if path=='/a':
        os.system("python play/a.py")
    elif path=='/b':
        os.system("python play/b.py")
    elif path=='/c':
        os.system("python play/c.py")
    elif path=='/d':
        os.system("python play/d.py")
    elif path=='/pushup':
        os.system("python act/pushup.py")
    elif path=='/armup':
        os.system("python act/armup.py")
    elif path=='/follow':
        os.system("python act/follow/follow.py")
    else:
        response_header = 'HTTP/1.1 404 Page Not Found\n'
    
    response_header = 'HTTP/1.1 200 OK\n'
    response_header+='Content-Type: text/html\n'
    response_header+='Connection: close\n'
    response_header+='\n'

    response=response_header
    client_socket.send(response.encode('utf8'))
