# Implementação de um chat multi-thread

Sistemas Distribuídos 2023/02 - Unilasalle Canoas

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



Protocol

- @LOGAR <username>
- @ORDENAR
- @SAIR
- @UPLOAD <filename>
- @DOWNLOAD <filename>