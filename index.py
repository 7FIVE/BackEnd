
import tornado.ioloop
import tornado.web
import tornado.websocket
import aiml # AIML para tratamento de 
import json
import os
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
        self.write("{'status get': 'connected'}")

    def post(self):
        self.write("{'status post': 'connected'}")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
        

    def post(self):#entrada de dados, reconhecimento do usuário, e designação de funções para as mensagens
        data = json.loads(self.request.body)#leitura do corpo da request
        response = ""
        #data2 = client.message(message["message"])
        for tags in data.keys():
            if tags == "message" and data[tags] != '': # aqui fazemos o tratamento das respostas
                tokens = tk.tokenize(data[tags])
                k.setPredicate("n",data['user'],data['id'])
                filter = [w.lower() for w in tokens if w.lower() not in stopwords] # retirar stop words
                print(tokens)
                print(utk.detokenize(filter))
                response = json.loads('{"message":"'+k.respond(utk.detokenize(filter),data['id'])+'","user":"Alfred"}')

            # if tags == "message" and data[tags] == 'sair' or data[tags] == 'exit':
            #     response = json.loads('{"message":"'+"Minha missão aqui foi concluida!, ADEUS!"+'","user":"Alfred"}')
            #     exit()
        self.write(response)


class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    connections = set()
    connection = []
    
    def check_origin(self, origin):
        return True
        
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

                    # if tags == "message" and message[tags] == 'sair':
                    #     response = json.loads('{"message":"'+"Minha missão aqui foi concluida!, ADEUS!"+'","user":"Alfred"}')
                    #     client.write_message(response)
                    #     exit()
                #response = json.loads('{"message":"'+k.respond(message["message"])+'","user":"Pewee"}')
                client.write_message(response)

    def on_close(self):
        self.connections.remove(self)
    


def make_app():
    return tornado.web.Application([(r"/",MainHandler),(r"/websocket",SimpleWebSocket),(r"/bot",bot)])




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app = make_app()
    print("Running port "+str(port))
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()
# if __name__ == "__main__":
#     app = make_app() #constroi a aplicação
#     app.listen(8888) #abre a porta para conexao
#     tornado.ioloop.IOLoop.current().start() #deixa em looping