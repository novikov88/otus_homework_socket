import socket
from config import *


def generate_response(custom_request):
    """Функция собирает данные из пришедшего запроса"""
    data = []
    temp_request = custom_request.split('\r\n')
    for value in range(len(temp_request)):
        if value == 0:
            temp_request[value] = temp_request[value].split()
            data.append(temp_request[value][2])
            if len(temp_request[value][1]) > 1 and '=' in temp_request[value][1]:
                temp_status = temp_request[value][1].split('=')
                status = temp_status[1]
                if status in STATUS_CODE:
                    data.append(STATUS_CODE[status])
                else:
                    data.append('200 OK')
            else:
                data.append('200 OK')
            data.append(temp_request[value][0])
        else:
            data.append(temp_request[value])
    return data


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
    # для использования одного порта без random
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind(('localhost', 8000))
    ss.listen()
    while True:
        cs, addr = ss.accept()
        request = cs.recv(1024)
        print('Request received from:', addr)
        response = generate_response(request.decode('utf-8'))
        temp_string = ''
        for _ in range(4, len(response) - 2):
            temp_string = temp_string + response[_] + '\n'
        cs.send(f"{response[0]} {response[1]}\n\nRequest Method: {response[2]}\nRequest Source: {addr}\n"
                f"Response Status: {response[1]}\nHeaders:\n{temp_string}".encode('utf-8'))
        print(f'Response sent successfully to the address {addr}')
