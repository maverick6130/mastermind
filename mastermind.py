from z3 import *

def z3min(x,y):
    return If(x <= y, x, y)

class Player:
    def __init__(self):
        self.n = 0
        self.k = 0
        self.v = []
        self.solver = Optimize()
        self.lq = []
        self.turns = 0
        self.retry = 0
    def initialize(self,n,k):
        self.n = n
        self.k = k
        self.v = [ [ Bool("v_{}_{}".format(i,j)) for j in range(n) ] for i in range(k) ]
        self.solver = Optimize()
        for i in range(k):
            self.solver.add( PbEq( [ (self.v[i][j], 1) for j in range(n) ], 1 ) )
    def move(self):
        self.solver.check()
        model = self.solver.model()
        query = [ [ is_true(model[self.v[i][j]]) for j in range(self.n) ].index(True) for i in range(self.k) ]
        self.lq = query
        self.turns = self.turns + 1
        if self.retry < 3 and self.turns >= self.n+self.k:
            self.retry = self.retry + 1
            self.initialize(self.n, self.k)
            self.turns = 0
        return query
    def receiverw(self,red,white):
        self.solver.add_soft( PbEq( [ (self.v[i][self.lq[i]],1) for i in range(self.k) ], red ), 1 )
        self.solver.add_soft( Sum([ z3min( self.lq.count(j), Sum( [ If( self.v[i][j], 1, 0 ) for i in range(self.k) ] ) ) for j in range(self.n) ]) == red + white, 1 )

player = Player()

def initialize(n,k):
    player.initialize(n,k)

def get_second_player_move():
    return player.move()

def put_first_player_response( red, white ):
    player.receiverw(red, white)