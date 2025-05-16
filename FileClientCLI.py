import socket
import json
import base64
import logging
import os

IP = '0.0.0.0'
PORT = 6666

server_address=(IP, PORT)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    
    logging.warning(f"connecting to {server_address}")
    
    try:
        logging.warning(f"sending message: {command_str[:10]}...") 
        sock.sendall(command_str.encode())
        
        data_received="" 
        while True:
            
            data = sock.recv(4096)
            if data:
                
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
            
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False


def remote_list():
    command_str=f"LIST"
    command_str = command_str + "\r\n\r\n"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print("\n\nDaftar File yang Tersedia:")
        print("=============================")
        for nmfile in hasil['data']:
            print(f"  • {nmfile}")
        print("=============================\n\n")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    command_str = command_str + "\r\n\r\n"
    hasil = send_command(command_str)
    
    if (hasil['status']=='OK'):
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile, 'wb+')
        fp.write(isifile)
        fp.close()
        print(f"File {filename} berhasil didownload")
        return True
    else:
        print("Gagal")
        return False
    
def remote_add(filename=""):
    isFileExist = os.path.exists(filename)

    if not isFileExist:
        print(f"File {filename} tidak ditemukan...")
        return False
    
    content = open(filename, 'rb').read()
    decodedContent = base64.b64encode(content).decode()  
    
    command_str = f"ADD {filename} "
    fullCommand = command_str + decodedContent + "\r\n\r\n"
    
    result = send_command(fullCommand)
    
    if (result['status']=='OK'):
        print(f"File {filename} berhasil diupload")
        return True
    else:
        print("Gagal")
        return False
    
def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    command_str = command_str + "\r\n\r\n"
    hasil = send_command(command_str)
    
    if (hasil['status']=='OK'):
        print(f"File {filename} berhasil dihapus")
        return True
    else:
        print("Gagal")
        return False


if __name__=='__main__':
    server_address=('localhost', 6666)
    
    while True:
        print("File Transfer Client")
        print("====================")
        print("1. List file")
        print("2. Download file")
        print("3. Upload file")
        print("4. Delete file")
        print("5. Exit")
        print("====================")
        
        cmd = input("Pilih menu: ")
        if cmd == '1':
            remote_list()
        elif cmd == '2':
            filename = input("Masukkan nama file: ")
            remote_get(filename)
        elif cmd == '3':
            filename = input("Masukkan nama file: ")
            remote_add(filename)
        elif cmd == '4':
            filename = input("Masukkan nama file: ")
            remote_delete(filename)
        elif cmd == '5':
            print("Keluar dari program")
            break
        else:
            print("Menu tidak dikenali")
    
