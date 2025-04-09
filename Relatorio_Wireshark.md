
# Relatório de Análise de Tráfego com Wireshark

## Objetivo
O objetivo deste projeto é realizar a captura e análise do tráfego de rede gerado por um protocolo FTCP, bem como identificar e estudar pacotes dos protocolos DHCP e DNS usando a ferramenta Wireshark.

## Ferramentas Utilizadas
- **Wireshark** (interface gráfica) para captura e análise dos pacotes
- **Sistema Operacional**: Windows
- **Cliente e Servidor FTCP** rodando na mesma máquina

## Etapas Realizadas

### 1. Instalação do Wireshark
- Download realizado pelo site oficial: https://www.wireshark.org/
- Instalação com Npcap incluído para possibilitar a captura de pacotes

### 2. Execução do Cenário FTCP
- Iniciado o servidor FTCP local
- Cliente FTCP executado para solicitar o arquivo `a.txt` via TCP
- Trânsito de pacotes registrado usando o Wireshark
- Interface utilizada para captura: **Loopback** (por estarem na mesma máquina)

### 3. Captura do Tráfego
- A captura foi feita utilizando a interface gráfica do Wireshark
- A gravação foi salva no formato `.pcapng`
- Durante a execução do cliente, a transferência foi observada na interface


### 5. Análise DNS
- Filtro utilizado: `dns`
- Observadas requisições DNS ("Standard Query") e respostas ("Standard Query Response")
- Exemplos analisados:
  - Identificação de pacotes UDP na porta 53

### 6. Análise do Tráfego FTCP com TCP

#### 6.1 Handshake TCP
- **Descrição**: Mostra o início da conexão TCP entre cliente e servidor FTCP.
- **Screenshot**: `imagens/handshake_tcp.png`
- **Pacotes esperados**:
  - SYN (cliente → servidor)
  - SYN-ACK (servidor → cliente)
  - ACK (cliente → servidor)

#### 6.2 Comando `get`
- **Descrição**: Pacote onde o cliente envia o comando `get a.txt` para o servidor.
- **Screenshot**: `imagens/comando_get.png`

#### 6.3 Dados do Arquivo
- **Descrição**: Vários pacotes contendo os dados do arquivo `a.txt` enviados pelo servidor ao cliente.
- **Screenshot**: `imagens/dados_arquivo.png`

#### 6.4 Comando `ftcp_ack`
- **Descrição**: Pacote onde o cliente envia um ACK confirmando o recebimento dos dados.
- **Screenshot**: `imagens/ftcp_ack.png`
- **Explicação**:
  - O protocolo TCP garante entrega confiável através dos **números de sequência (Sequence Number)** e **números de confirmação (Acknowledgment Number)**.
  - Cada byte de dados transmitido tem um número de sequência.
  - O ACK enviado pelo cliente informa qual o próximo byte esperado.
  - Isso garante que, caso um pacote seja perdido, ele será retransmitido, assegurando a entrega completa e correta dos dados.

## Capturas de Tela
As imagens estão localizadas na pasta `imagens/` e ilustram:
- Pacotes DHCP e seus detalhes
- Consultas DNS e respostas
- Tráfego FTCP (cliente e servidor)

## Conclusão
A análise permitiu visualizar claramente os pacotes trocados no protocolo FTCP customizado, assim como o funcionamento dos protocolos DHCP e DNS na rede. O uso do Wireshark se mostrou eficiente para inspeção e compreensão do comportamento da rede.

---
**Autor:** Ivan Gomes De Alcantara Junior

**Data:** 09/10/2025

**Observação:** O arquivo `.pcapng` da captura está disponível neste repositório.
