########################################################################
#             Trabalho 01 - Servidor Web Multithread                   #  
#                                                                      #
#   Author: Marcos Vinicius Souza Rodrigues                            # 
#   Matricula: 11711ECP008                                             #
#                                                                      #
#   Descrição: Servidor Web capaz de receber multipĺas requisições     #
#              ao mesmo tempo e responde-las enviando-a o              #
#              solicitado                                              #
#                                                                      #
#   Data: 12/07/2022                                                   #
########################################################################


import socket
import threading
import logging


def get_ip():
    """
        Metodo criado com a finalidade de buscar o IP da maquina host 
    """
    conn= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.getsockname()[0]
    cursor =  conn.getsockname()[0]
    conn.close()
    return cursor


IP = get_ip() # IP host
PORT = 6789   # Porta que vai ser escutada
ADDR = (IP, PORT)
FORMAT = "utf-8"

def process_request(conn, addr):
    """
            O Metodo analisa a requisição que foi recebida e envia para o cliente a pagina 
        ou recurso solicitado caso ele esteja disponivel
    """
    
    logging.info(f"[NEW CONNECTION FROM ]: {addr[0]} connected.")
    
    while True:
        msg = conn.recv(1024).decode(FORMAT)
        msg = msg.split(" ")
        if(msg[0] == 'GET'):
            file =msg[1].split(" ")
            if(file[0] == "/"):
                with open("index.html", "r") as contend:
                    response = contend.read()
                    http_response = """HTTP/1.1 200 OK\r\n\r\n""" + str(response)
            else: 
                try:
                    with open(file[0][1:], "r") as contend:
                        response = contend.read()
                        http_response = """HTTP/1.1 200 OK\r\n\r\n""" + str(response)
                except:
                    with open("not_found.html","r") as contend:
                        response = contend.read()
                        http_response = """HTTP/1.1 404 Not Found\r\n\r\n""" + str(response)
        else:
            logging.warning(f"{msg[0]} - Method Refused - ")
            with open("bad_request.html","r") as contend:
                response = contend.read()
                http_response = """HTTP/1.1 400 Bad Request\r\n\r\n""" + str(contend)

        try:
            conn.send(http_response.encode("utf-8"))
            conn.close()
            break
            
        except Exception as e:
            logging.info(f"! Disconecting ...")
            logging.warning(f"INTERNAL SERVER ERROR : {e}")
            conn.close()
            break
    
def web_server():
    """
        O metodo Cria uma conexão socket e fica ecutando a porta informada,
        quando chega uma requisiçao ela é enviada a outra funcao que consegue trata-la 
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(1)
    
    logging.info(f"[LISTENING] Server is listening on {IP}:{PORT}")
    
    while True:
        try:
            conn,addr = server.accept()
            thread = threading.Thread(target=process_request, args=(conn,addr))
            thread.start()
            
            logging.info(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1 }")
            
        except KeyboardInterrupt:
            server.close()
    
    
if __name__ == "__main__":
    
    #Formata os logs do servidor 
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s :--: %(message)s :--: %(asctime)s',
        )
    
    # Chama a função principal
    web_server()