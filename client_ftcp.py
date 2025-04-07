import socket
import configparser

# configuracao
config = configparser.ConfigParser()
config.read("config.ini")

SERVER_IP = "127.0.0.1"
UDP_PORT = int(config["SERVER"]["udp_port"])


# udp solicitacao
def udp_solicitation(nome_arquivo):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        mensagem = f"{nome_arquivo} TCP"
        udp_socket.sendto(mensagem.encode("utf-8"), (SERVER_IP, UDP_PORT))

        try:
            udp_socket.settimeout(5)
            resposta, _ = udp_socket.recvfrom(1024)
            resposta = resposta.decode("utf-8")

            if resposta.startswith("ERRO"):
                print(f"[UDP] Erro do servidor: {resposta}")
                return None

            print(f"[UDP] Porta TCP recebida: {resposta}")
            return int(resposta)

        except socket.timeout:
            print("[UDP] Tempo de resposta esgotado.")
            return None


# receber resposta e baixar arquivo
def download_file(tcp_port, nome_arquivo):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        try:
            tcp_socket.connect((SERVER_IP, tcp_port))
            print(f"[TCP] Conectado ao servidor na porta {tcp_port}.")

            # dados
            dados = "".encode()
            parte = tcp_socket.recv(1024)
            print("checkar resposta do servidor")
            print(f"resposta dele -> {parte}...")
            if not parte:
                print("nao tem resposta para solicitacao enviada!")
            dados += parte

            # erro
            if dados.decode(errors="ignore").startswith("ERRO"):
                print(f"[TCP] {dados.decode('utf-8')}")
                return

            # arquivo digitado
            with open(f"recebido_{nome_arquivo}", "wb") as f:
                print("escrevendo arquivo")
                f.write(dados)
                print(f"[TCP] Arquivo salvo como 'recebido_{nome_arquivo}'.")

            tcp_socket.sendall("RECEBIDO".encode("utf-8"))
            print("[TCP] Confirmação enviada ao servidor.")

        except Exception as e:
            print(f"[TCP] Erro durante conexão: {e}")


# prompt do usuario
if __name__ == "__main__":
    while True:
        nome_arquivo = input(
            "Digite o nome do arquivo para baixar (a.txt ou b.txt): "
        ).strip()
        porta_tcp = udp_solicitation(nome_arquivo)
        if porta_tcp:
            download_file(porta_tcp, nome_arquivo)
