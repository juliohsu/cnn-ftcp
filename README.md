# Projeto: Protocolo de Transferência de Arquivos Personalizado – FTCP

Este repositório contém a implementação do projeto **FTCP (File Transfer Custom Protocol)**, um sistema cliente-servidor para transferência de arquivos utilizando os protocolos TCP e UDP de forma customizada, conforme especificado nas instruções.

## Equipe

* GUILHERME DANTAS BOIA DE ALBUQUERQUE - 122110002
* IVAN GOMES DE ALCANTARA JUNIOR - 123110305
* JOÃO MATHEUS PINTO VILLARIM COUTINHO DE ALMEIDA - 121110386
* JULIO HSU - 120110370

## Visão Geral do Projeto

O objetivo principal é desenvolver um cliente e um servidor que se comunicam através de um protocolo próprio (FTCP). A negociação inicial ocorre via UDP, onde o cliente requisita um arquivo (`a.txt` ou `b.txt`) e especifica o protocolo de transferência (obrigatoriamente TCP nesta versão). O servidor responde com a porta TCP designada para a transferência. Em seguida, o cliente estabelece uma conexão TCP nessa porta, solicita o arquivo, o recebe e confirma o recebimento antes de encerrar a conexão.

## Entregáveis

| Item # | Descrição                                      | Forma de Entrega                  |
| :----- | :--------------------------------------------- | :-------------------------------- |
| 1      | **Código Fonte** (Cliente e Servidor)          | [cliente](/client_ftcp.py) e [servidor](/server_ftcp.py)|
| 2      | **Arquivos de Teste** (`a.txt` e `b.txt`)      | [a.txt](/a.txt) e [b.txt](/b.txt) |
| 3      | **Arquivo de Configuração** (`config.ini`)     | [config.ini](/config.ini)         |
| 4      | **Arquivo de Captura de Tráfego** (`.pcapng`)  | [.pcapng](/dhcp.pcapng)           |
| 5      | **Relatório de Análise** (PDF ou Markdown)     | [relatório](https://docs.google.com/document/d/1pLhx4d6tvF1S86pzKTBOpHfOZeELoE1qyTE0ZACiETQ/edit?usp=sharing)                     |


## Documentação Importante

Consulte os seguintes arquivos neste repositório para obter detalhes completos sobre cada parte do projeto:

*   **[📄 Especificação do Protocolo FTCP](./protocolo.md):** Descreve em detalhes as etapas de negociação (UDP) e transferência (TCP), os formatos das mensagens e o fluxo de comunicação esperado entre cliente e servidor.
*   **[🦈 Tutorial de Análise com Wireshark](./wireshark_tutorial.md):** Contém um guia passo a passo sobre como usar o Wireshark para analisar o arquivo de captura (`.pcap`), incluindo exemplos com DHCP/DNS e instruções específicas para analisar o tráfego do seu protocolo FTCP.
*   **[📝 Instruções para o Relatório](./relatorio.md):** Apresenta a estrutura e o conteúdo esperado para o relatório final, focando na análise do protocolo e do tráfego de rede capturado.
*   **[🐍 Exemplo de servidor/cliente (Python)](./echo_server.py):** Um código de exemplo em Python demonstrando um servidor e cliente "echo" que opera simultaneamente em TCP e UDP. 

## Como Executar (Exemplo Básico)

1.  **Configuração:** Certifique-se de que o arquivo `config.ini` está presente na mesma pasta dos scripts e configurado corretamente com as portas desejadas e os caminhos para os arquivos `a.txt` e `b.txt`.
2.  **Iniciar o Servidor:**
    
    ```bash
    python servidor_ftcp.py
    ```
3.  **Executar o Cliente (em outro terminal):**
    ```bash
    python cliente_ftcp.py
    ```
