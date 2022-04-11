from agents.agent import Agent
import random
#from agent import Agent

class MinMax2Agent(Agent):
    def __init__(self):
        #inicializa as variaveis pra expandir a arvore assim que o jogo e o jogador forem configurados
        self.game = None
        self.player = None
        print("init")

    def set_game(self, game):
        self.game = game
        self.board = game.get_initial_board()
        #cria a arvore se ja tem jogador
        if self.player:
            self.createTree()
    
    def set_player(self, player):
        self.player = player
        self.opponent = self.player*-1
        #cria a arvore se ja tem jogo
        if self.game:
            self.createTree()
        
    #TODO deduplicate nodes (e.g. -xo -> oxo == ox- -> oxo)
    def createTree(self):
        print("create tree")
        #agente começa
        if self.player == Agent.PLAYER_1:
            self.state = MinMaxNode(self.board, self.getScore(self.board), 'max', None)
        #outro começa
        else:
            self.state = MinMaxNode(self.board, self.getScore(self.board), 'min', None)
        expandList = [self.state]
        #expand entire tree
        while expandList != []:
            #proximo nodo
            curNode = expandList.pop(0)
            if curNode.type == 'max':
                player = self.player
            else:
                player = self.opponent
            #expande o nodo atual
            for move in self.game.moves(curNode.board, player):
                #inicializa o proximo nodo a partir de uma jogada possivel
                if curNode.type == 'max':
                    nextType = 'min'
                else:
                    nextType = 'max'
                nextBoard = self.game.apply(move, curNode.board)
                nextNode = MinMaxNode(nextBoard, self.getScore(nextBoard), nextType, move)
                #adiciona o nodo ao nodo superior
                curNode.addNode(nextNode)
                #adiciona a lista de expansão se o jogo não acabou
                if not self.game.is_terminal_state(nextBoard):
                    expandList += [nextNode]
        print("update tree values")
        self.state.updateValues()
    #retorna o score relativo ao jogador
    def getScore(self, board):
        winner = self.game.get_winner(board)
        return winner*self.player 

    def select_action(self, game, context, max_second=0, max_iterations=0, max_depth=4):
        print("select")
        #atualiza o estado interno. considera que passou no maximo um movimento
        print(context)
        if self.state != context:
            for node in self.state.next:
                if node.board == context:
                    print(node.board)
                    self.state = node
                    break  
        print(self.state.board)
                #sem verificação de erro, só morre 
        #cria uma lista dos proximos nodos com maior valor
        max = []
        for node in self.state.next:
            #nodo atual tem o score maximo
            if node.score == self.state.score:
                max += [node]
        #escolhe uma ação otima aleatória
        self.state = random.choice(max)
        print(self.state.__dict__)
        input()
        return self.state.move
        
    def get_name(self):
        return "Minmax 2 Agent"
        
class MinMaxNode():
    def __init__(self, board, score, type, lastMove):
        self.board = board 
        self.score = score
        self.type = type
        self.move = lastMove
        self.next = []
            
    def addNodes(self, nodeList):
        for n in nodeList:
            self.next += [n]
    def addNode(self, node):
        self.next += [node]
        
    #recursivamente atualiza os valores dos próximos nodos e retorna o valor resultante (min ou max)
    def updateValues(self):
        #nodo terminal
        if self.next == []:
            return self.score 
        if self.type == 'max':
            self.score = max(self.getNextValues())
        else: #type == min
            self.score = min(self.getNextValues())
        return self.score     
        
    #sem tail recursion kk vai dar pau em jogo grande
    def getNextValues(self):
        values = []
        for n in self.next:
            values += [n.updateValues()]
        return values