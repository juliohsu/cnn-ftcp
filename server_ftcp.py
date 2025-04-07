import socket
import configparser
import threading
import signal
import sys

# Configuração inicial do servidor
# Lê as configurações do arquivo config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Configurações do servidor
UDP_PORT = int(config["SERVER"]["udp_port"])
TCP_START = int(config["SERVER"]["tcp_port_range_start"])
TCP_END = int(config["SERVER"]["tcp_port_range_end"])
FILE_A = config["SERVER"]["file_a"]
FILE_B = config["SERVER"]["file_b"]

SERVER_IP = "0.0.0.0"  # Aceita conexões de qualquer IP

def find_available_port(start_port, end_port):
    """
    Procura uma porta TCP disponível no intervalo especificado.
    
    Args:
        start_port (int): Início do intervalo de portas
        end_port (int): Fim do intervalo de portas
    
    Returns:
        int ou None: Retorna a porta disponível ou None se nenhuma estiver livre
    """
    for port in range(start_port, end_port + 1):
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.bind((SERVER_IP, port))
            test_socket.close()
            return port
        except OSError:
            continue
    return None

def handle_tcp_connection(tcp_port, filename):
    """
    Gerencia uma conexão TCP para transferência de arquivo.
    Implementa a Etapa 2 do protocolo FTCP.
    
    Args:
        tcp_port (int): Porta TCP para escutar
        filename (str): Nome do arquivo a ser transferido
    """
    tcp_socket = None
    try:
        # Configuração do socket TCP
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((SERVER_IP, tcp_port))
        tcp_socket.listen(1)
        print(f"[TCP] Aguardando conexão na porta {tcp_port}...")

        # Aceita conexão do cliente
        conn, addr = tcp_socket.accept()
        with conn:
            print(f"[TCP] Conectado por {addr}")
            
            # Espera e valida o comando get
            command = conn.recv(1024).decode().strip()
            if not command.startswith("get,"):
                error_msg = "ERROR,Comando invalido. Use: get,<arquivo>"
                conn.sendall(error_msg.encode("utf-8"))
                return
            
            # Verifica se o arquivo solicitado corresponde ao negociado
            _, requested_file = command.split(",")
            if requested_file != filename:
                error_msg = "ERROR,Arquivo solicitado não corresponde ao negociado"
                conn.sendall(error_msg.encode("utf-8"))
                return
            
            try:
                # Lê e envia o arquivo em chunks
                with open(filename, "rb") as file:
                    data = file.read()
                    # Transferência em chunks de 1024 bytes para evitar sobrecarga
                    for i in range(0, len(data), 1024):
                        chunk = data[i:i + 1024]
                        conn.sendall(chunk)
                    print(f"[TCP] Arquivo '{filename}' enviado.")
            except FileNotFoundError:
                error_msg = "ERROR,Arquivo não encontrado"
                conn.sendall(error_msg.encode("utf-8"))
                return

            # Aguarda confirmação ftcp_ack do cliente
            confirmation = conn.recv(1024).decode().strip()
            if confirmation.startswith("ftcp_ack,"):
                print("[TCP] Cliente confirmou recebimento.\n")
            else:
                print("[TCP] Confirmação inválida ou não recebida.\n")
    finally:
        # Garante que o socket seja fechado mesmo em caso de erro
        if tcp_socket:
            tcp_socket.close()

def start_udp_server():
    """
    Inicia o servidor UDP para negociação inicial.
    Implementa a Etapa 1 do protocolo FTCP.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        # Configura o socket UDP
        udp_socket.bind((SERVER_IP, UDP_PORT))
        print(f"[UDP] Servidor escutando na porta {UDP_PORT}...")

        while True:
            # Espera por solicitações de clientes
            data, client_addr = udp_socket.recvfrom(1024)
            message = data.decode().strip()
            print(f"[UDP] Mensagem recebida: {message}")

            try:
                # Processa a mensagem REQUEST,TCP,filename
                command, protocol, filename = message.split(',')
                
                # Valida o comando
                if command != "REQUEST":
                    udp_socket.sendto(b"ERROR,Comando invalido", client_addr)
                    continue

                # Valida o arquivo
                if filename not in [FILE_A, FILE_B]:
                    udp_socket.sendto(b"ERROR,Arquivo inexistente", client_addr)
                    continue

                # Valida o protocolo
                if protocol.upper() != "TCP":
                    udp_socket.sendto(
                        "ERROR,Protocolo nao suportado".encode("utf-8"), client_addr
                    )
                    continue

                # Procura uma porta TCP disponível
                tcp_port = find_available_port(TCP_START, TCP_END)
                if tcp_port is None:
                    udp_socket.sendto(b"ERROR,Nenhuma porta TCP disponivel", client_addr)
                    continue

                # Inicia thread para conexão TCP
                thread = threading.Thread(
                    target=handle_tcp_connection, 
                    args=(tcp_port, filename), 
                    daemon=True
                )
                thread.start()

                # Envia resposta no formato do protocolo
                response = f"RESPONSE,TCP,{tcp_port},{filename}"
                udp_socket.sendto(response.encode(), client_addr)

            except ValueError:
                # Trata erro de formato da mensagem
                udp_socket.sendto(
                    b"ERROR,Formato da mensagem invalido. Use: REQUEST,TCP,<arquivo>",
                    client_addr,
                )

if __name__ == "__main__":
    try:
        start_udp_server()
    except KeyboardInterrupt:
        print("\n[SERVER] Servidor encerrado pelo usuário.")
    except Exception as e:
        print(f"\n[SERVER] Erro fatal: {e}")
    finally:
        print("[SERVER] Servidor finalizado.")
