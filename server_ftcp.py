import socket
import configparser
import threading
import signal
import sys

# file init
config = configparser.ConfigParser()
config.read("config.ini")

UDP_PORT = int(config["SERVER"]["udp_port"])
TCP_START = int(config["SERVER"]["tcp_port_range_start"])
TCP_END = int(config["SERVER"]["tcp_port_range_end"])
FILE_A = config["SERVER"]["file_a"]
FILE_B = config["SERVER"]["file_b"]

SERVER_IP = "0.0.0.0"  # every ip

# # fechando serrvidor com teclado C
# server_running = True
# def signal_handler(sig, frame):
#     print('pressing C to exit!')
#     global server_running
#     print("\n[SERVER] Shutting down...")
#     server_running = False

# handshake tcp
def handle_tcp_connection(tcp_port, filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.bind((SERVER_IP, tcp_port))
        tcp_socket.listen(1)
        print(f"[TCP] Aguardando conexão na porta {tcp_port}...")

        conn, addr = tcp_socket.accept()
        with conn:
            print(f"[TCP] Conectado por {addr}")
            try:
                with open(filename, "rb") as file:
                    data = file.read()
                    conn.sendall(data)
                    print(f"[TCP] Arquivo '{filename}' enviado.")
            except FileNotFoundError:
                conn.sendall("ERRO: Arquivo não encontrado.".encode("utf-8"))
                return

            # cliente aceitando
            confirmation = conn.recv(1024).decode()
            if confirmation.strip().upper() == "RECEBIDO":
                print("[TCP] Cliente confirmou recebimento.")
            else:
                print("[TCP] Confirmação inválida ou não recebida.")


# iniciar servidor com udp
def start_udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind((SERVER_IP, UDP_PORT))
        print(f"[UDP] Servidor escutando na porta {UDP_PORT}...")

        while True:
            # udp_socket.settimeout(1) # loop inf

            data, client_addr = udp_socket.recvfrom(1024)
            message = data.decode().strip()
            print(f"[UDP] Mensagem recebida de {client_addr}: {message}")

            try:
                filename, protocol = message.split()

                if filename not in [FILE_A, FILE_B]:
                    udp_socket.sendto(b"ERRO: Arquivo inexistente.", client_addr)
                    continue

                if protocol.upper() != "TCP":
                    udp_socket.sendto(
                        "ERRO: Protocolo não suportado.".encode("utf-8"), client_addr
                    )
                    continue

                # tcp porta
                tcp_port = TCP_START

                # enviar porta
                udp_socket.sendto(str(tcp_port).encode(), client_addr)

                # thread para tcp conexao
                threading.Thread(
                    target=handle_tcp_connection, args=(tcp_port, filename), daemon=True
                ).start()

            except ValueError:
                udp_socket.sendto(
                    b"ERRO: Formato da mensagem invalido. Use: <arquivo> TCP",
                    client_addr,
                )


# iniciar srevidor
if __name__ == "__main__":
    # signal.signal(signal.SIGINT, signal_handler)
    start_udp_server()
    print("[SERVER] Servidor principal finalizado.")
