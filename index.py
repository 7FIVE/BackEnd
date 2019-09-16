
import tornado.ioloop
import tornado.web
import tornado.websocket
import aiml # AIML para tratamento de 
import json
from wit import Wit

client = Wit('LNJEET2BYVHREQ5VNTZUSWKBWJTAJZFN')
k = aiml.Kernel()
k.learn('std-startup.xml')
k.respond('load aiml b')

"""
Exemplo de requisição post ele tem que receber:

{
    "message": "onde encontro mentoria?",
    "user":"me",
    "event":"chat (chat, funcao),evento",
    "tempoativo":"25",
    "click": "",
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
        if filter != '':
            response = json.loads('{"resposta":"'+k.respond("funcao "+filter)+'","user":"Pewee"}')
        else:
            response = json.loads('{"resposta":"'+k.respond(data["message"])+'","user":"Pewee"}')
        self.write(response)


class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    connections = set()
    
    def open(self):
        self.connections.add(self)

    def on_message(self,message): #usar para mensagens gerais
        
        [client.write_message(message) for client in self.connections] #tratar a entrada lá
        

    def on_close(self):
        self.connections.remove(self)
    


def make_app():
    return tornado.web.Application([(r"/",MainHandler),(r"/websocket",SimpleWebSocket)])

app = make_app() #constroi a aplicação
app.listen(8888) #abre a porta para conexao
tornado.ioloop.IOLoop.current().start() #deixa em looping