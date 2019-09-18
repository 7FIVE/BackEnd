
import tornado.ioloop
import tornado.web
import tornado.websocket
import aiml # AIML para tratamento de 
import json
from wit import Wit
port = 8888

client = Wit('LNJEET2BYVHREQ5VNTZUSWKBWJTAJZFN')
k = aiml.Kernel()
k.learn('std-startup.xml')
k.respond('load aiml b')

"""
Exemplo de requisição post ele tem que receber:

{
    "message": "onde encontro mentoria?",
    "user":"me",
    "event":"chat,evento",
    "parametro":"25", Talvez mudar ele
    "acao": "",
    "id": ""
}
"""

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):#entrada de dados, reconhecimento do usuário, e designação de funções para as mensagens
        data = json.loads(self.request.body)#leitura do corpo da request
        response = ""
        data2 = client.message(data["message"])
        filter = str(data2["entities"])
        filter = filter.split(":")
        filter = filter[0].replace("{","")
        filter = filter.replace(":","")
        
        if data["event"] == "chat":
            if filter != "":
                response = json.loads('{"resposta":"'+k.respond("funcao "+filter)+'","user":"Pewee"}')
            else:
                response = json.loads('{"resposta":"'+k.respond(data["message"])+'","user":"Pewee"}')
        else:
            if data["event"] == "event":
                if data["acao"] == "?" and data["parametro"] != "":
                    response = json.loads('{"resposta":"Evento Solicitado" ,"user":"Pewee"}')
                if data["acao"] == "inicial" and data["parametro"] != "":
                    response = json.loads('{"resposta":"Evento Solicitado","user":"Pewee"}')
                if data["acao"] == "tempo" and data["parametro"] != "":
                    response = json.loads('{"resposta":"Evento Solicitado","user":"Pewee"}')
        self.write(response)


class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    connections = set()
    connection = []
    
    
    def open(self):
        self.connections.add(self)

    def on_message(self,message): #usar para mensagens gerais
        # print(self.get)
        for client in self.connections:
            if client.get == self.get:
                client.write_message(message)
                message = json.loads(message)
                data = json.loads('{"message":"'+k.respond(message["message"])+'","user":"Pewee"}')
                client.write_message(data)

        # [client.write_message(message) for client in self.connections]

    def on_close(self):
        self.connections.remove(self)
    


def make_app():
    return tornado.web.Application([(r"/",MainHandler),(r"/websocket",SimpleWebSocket)])

print("Running port "+str(port))
app = make_app() #constroi a aplicação
app.listen(port) #abre a porta para conexao
tornado.ioloop.IOLoop.current().start() #deixa em looping