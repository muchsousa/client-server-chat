# Implementação de um chat multi-thread

Sistemas Distribuídos 2023/02 - Unilasalle Canoas

- Bruno Much - @muchsousa
- Melissa Gheller - @MelissaGheller

## Objetivos
Experimentar o desenvolvimento de sistemas multi-thread e compreender os problemas de comunicação entre processos numa arquitetura distribuida.

## Tarefas

Dado o código base para uma implementação de um programa de chat na linguagem Python, alterar o programa de forma que:

- Seja possível utilizar o chat por múltiplos usuários simultaneamente;
    - As mensagens são impressas no formato ":: MENSAGEM" (10%);
    - Os seguintes comandos são permitidos:
         - @ORDENAR: mostra as últimas 15 mensagens, ordenadas pelo horário de envio (5%);
         - @SAIR: faz "logout" do cliente (5%);
         - @UPLOAD : faz upload de um arquivo para o servidor (10%);
         - @DOWNLOAD : faz download de um arquivo do servidor (10%);
- Tanto o programa cliente como o programa servidor utilizem múltiplas threads (40%);
- O programa servidor é um sistema distribuído (10%);
- O sistema está bem documentado em relação a sua arquitetura (10%);

# Descrição  

Chat simples abordando o uso de sockets e threads na arquitetura cliente-servidor. 
Para a comunicação entre cliente e servidor utilizamos o formato TLV (tag-length-value) para a codificação das informações.

### Referências
- https://docs.python.org/3/library/threading.html
- https://docs.python.org/3/library/socket.html
- https://en.wikipedia.org/wiki/Type%E2%80%93length%E2%80%93value
- https://chrisyeh96.github.io/2020/03/28/terminal-colors.html
