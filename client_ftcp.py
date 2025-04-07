import socket
import configparser
import time

# Configuração inicial do cliente
config = configparser.ConfigParser()
config.read("config.ini")

SERVER_IP = "127.0.0.1"  # Endereço do servidor (localhost)
UDP_PORT = int(config["SERVER"]["udp_port"])

def udp_solicitation(nome_arquivo):
    """
    Realiza a negociação inicial via UDP (Etapa 1).
    Envia uma solicitação de arquivo e recebe a porta TCP para transferência.
    
    Args:
        nome_arquivo (str): Nome do arquivo desejado (a.txt ou b.txt)
    
    Returns:
        int ou None: Número da porta TCP se sucesso, None se erro
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        # Envia solicitação no formato REQUEST,TCP,<arquivo>
        mensagem = f"REQUEST,TCP,{nome_arquivo}"
        udp_socket.sendto(mensagem.encode("utf-8"), (SERVER_IP, UDP_PORT))

        try:
            # Aguarda resposta com timeout de 5 segundos
            udp_socket.settimeout(5)
            resposta, _ = udp_socket.recvfrom(1024)
            resposta = resposta.decode("utf-8")

            # Trata mensagens de erro
            if resposta.startswith("ERROR"):
                print(f"[UDP] Erro do servidor: {resposta}")
                return None

            # Processa resposta RESPONSE,TCP,<porta>,<arquivo>
            parts = resposta.split(',')
            if len(parts) >= 3 and parts[0] == "RESPONSE":
                print(f"[UDP] Porta TCP recebida: {parts[2]}")
                return int(parts[2])
            else:
                print(f"[UDP] Resposta inválida do servidor")
                return None

        except socket.timeout:
            print("[UDP] Tempo de resposta esgotado.")
            return None

def download_file(tcp_port, nome_arquivo):
    """
    Realiza a transferência do arquivo via TCP (Etapa 2).
    Conecta na porta TCP, envia comando get e recebe o arquivo.
    
    Args:
        tcp_port (int): Porta TCP para conexão
        nome_arquivo (str): Nome do arquivo a ser baixado
    """
    time.sleep(0.1)  # Pequena pausa para garantir que o servidor está pronto
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        try:
            # Estabelece conexão TCP
            tcp_socket.connect((SERVER_IP, tcp_port))
            print(f"[TCP] Conectado ao servidor na porta {tcp_port}.")

            # Envia comando get,<arquivo>
            comando = f"get,{nome_arquivo}"
            tcp_socket.sendall(comando.encode("utf-8"))
            print(f"[TCP] Solicitando arquivo: {nome_arquivo}")

            # Recebe dados do arquivo
            dados = b""
            tcp_socket.settimeout(5)  # timeout de 5 segundos
            
            try:
                while True:
                    parte = tcp_socket.recv(1024)
                    
                    # Verifica fim da transmissão
                    if not parte:
                        break
                    
                    # Verifica mensagens de erro
                    if not dados and parte.startswith(b"ERROR"):
                        print(f"[TCP] Erro: {parte.decode('utf-8')}")
                        return
                    
                    dados += parte
                    
                    # Se recebeu menos que o buffer, é o último chunk
                    if len(parte) < 1024:
                        break
                        
            except socket.timeout:
                print("[TCP] Timeout ao receber dados")
                if not dados:
                    return

            # Verifica se recebeu dados
            if not dados:
                print("[TCP] Nenhum dado recebido do servidor")
                return

            # Salva o arquivo recebido
            with open(f"recebido_{nome_arquivo}", "wb") as f:
                f.write(dados)
                print(f"[TCP] Arquivo salvo como 'recebido_{nome_arquivo}'.")

            # Envia confirmação ftcp_ack
            tamanho_bytes = len(dados)
            confirmacao = f"ftcp_ack,{tamanho_bytes}"
            tcp_socket.sendall(confirmacao.encode("utf-8"))
            print(f"[TCP] Confirmação enviada: {tamanho_bytes} bytes recebidos")

        except Exception as e:
            print(f"[TCP] Erro durante conexão: {e}")
        finally:
            tcp_socket.settimeout(None)  # Restaura timeout padrão

if __name__ == "__main__":
    # Loop principal do cliente
    while True:
        try:
            # Solicita nome do arquivo ao usuário
            nome_arquivo = input(
                "\nDigite o nome do arquivo para baixar (a.txt ou b.txt): "
            ).strip()
            
            # Realiza negociação UDP e transferência TCP
            porta_tcp = udp_solicitation(nome_arquivo)
            if porta_tcp:
                download_file(porta_tcp, nome_arquivo)
        except KeyboardInterrupt:
            print("\nPrograma encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"Erro inesperado: {e}")
