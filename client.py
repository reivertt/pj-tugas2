import sys
import socket
import logging

def send_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning("membuka socket")

    server_address = ('localhost', 56000)
    logging.warning(f"opening socket {server_address}")
    sock.connect(server_address)

    try:
        # Send data
        message = "TIME QUIT"
        logging.warning(f"[CLIENT] sending {message}")
        message += "\r\n\r\n"
        sock.sendall(message.encode())
        full_data = []
        while True:
                data = sock.recv(1024)
                if not data: break
                logging.warning(f"[DITERIMA DARI SERVER] {data}")
                full_data.append(data)
                # if b"\r\n\r\n" in b"".join(full_data): break
            
        logging.warning(f"[DITERIMA DARI SERVER] {b"".join(full_data).decode('utf-8')}")
    except Exception as e:
        logging.error(f"Error {e}")
    finally:
        logging.warning("closing")
        sock.close()
    return


if __name__=='__main__':
    send_data()
