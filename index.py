
import tornado.ioloop
import tornado.web
import tornado.websocket
import aiml # AIML para tratamento de 
import json
from nltk.tokenize import TweetTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from wit import Wit
port = 8888

client = Wit('LNJEET2BYVHREQ5VNTZUSWKBWJTAJZFN')
k = aiml.Kernel()
k.learn('std-startup.xml')
k.respond('load aiml b')
sessao = 123
tk = TweetTokenizer()
utk = TreebankWordDetokenizer()
stopwords = ['!',',',':',';','.','?','a','tokeniza','deu','esta','está','quero','eu','uma','um','de','qual','me','so','e','é','o','em','do','sao','os','as','alfred']

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

"""
{
    "message":"OI!",
    "id":"123",
    "timestamp": "14:23",
    "user":"Joselito"
}
"""
class bot(tornado.web.RequestHandler):
    def get(self):
        self.render("demo/index.html")

class getJs1(tornado.web.RequestHandler):
    def get(self):
        self.render("demo/dist/index.js")

class getJs2(tornado.web.RequestHandler):
    def get(self):
        self.render("demo/Core/live2dcubismcore.min.js")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
        

    def post(self):#entrada de dados, reconhecimento do usuário, e designação de funções para as mensagens
        data = json.loads(self.request.body)#leitura do corpo da request
        response = ""
        
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
                response = ''
                #data2 = client.message(message["message"])
                for tags in message.keys():
                    if tags == "message" and message[tags] != '': # aqui fazemos o tratamento das respostas
                        tokens = tk.tokenize(message[tags])
                        k.setPredicate("n",message['user'],message['id'])
                        filter = [w.lower() for w in tokens if w.lower() not in stopwords] # retirar stop words
                        print(tokens)
                        print(utk.detokenize(filter))
                        response = json.loads('{"message":"'+k.respond(utk.detokenize(filter),message['id'])+'","user":"Alfred"}')

                    if tags == "message" and message[tags] == 'sair':
                        response = json.loads('{"message":"'+"Minha missão aqui foi concluida!, ADEUS!"+'","user":"Alfred"}')
                        client.write_message(response)
                        exit()
                #response = json.loads('{"message":"'+k.respond(message["message"])+'","user":"Pewee"}')
                client.write_message(response)

    def on_close(self):
        self.connections.remove(self)
    


def make_app():
    return tornado.web.Application([(r"/",MainHandler),(r"/websocket",SimpleWebSocket),(r"/dist/index.js",getJs1),(r"/Core/live2dcubismcore.min.js",getJs2),(r"/bot",bot)])

print("Running port "+str(port))
app = make_app() #constroi a aplicação
app.listen(port) #abre a porta para conexao
tornado.ioloop.IOLoop.current().start() #deixa em looping