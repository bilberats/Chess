import pygame as pg
import sys,os,time

sqsize = 80
topleft = (30,30)
haverook = False

def cango_vect(pos,positions,x,y,color,moves):
    i = 1
    cango = []
    while (pos[0]+i*x,pos[1]+i*y) not in positions[color] and 0<=pos[0]+i*x<=7 and 0<=pos[1]+i*y<=7 and i <= moves:
        if (pos[0]+i*x,pos[1]+i*y) in positions[not color]:
            cango += [(pos[0]+i*x,pos[1]+i*y)]
            return cango
        cango += [(pos[0]+i*x,pos[1]+i*y)]
        i+=1
    return cango

class Timer():
    def __init__(self,duration,increment,pos):
        self.timeleft = duration
        self.duration = duration
        self.increment = increment
        self.tempsecoule = 0
        self.pause = True
        self.timesup = False
        self.pos = pos
        self.firstmove = True

    def actualiser(self,timestart,time):
        if not self.pause:
            if self.timeleft > 0.0:
                diference_temps = time-timestart
                self.timeleft = self.duration - diference_temps - self.tempsecoule
            else:
                self.timesup = True

    def stop(self):
        if not self.firstmove:
            self.timeleft += self.increment
        self.pause = True
        self.tempsecoule = self.duration - self.timeleft
        self.firstmove = False

    def start(self):
        self.pause = False
    
    def display(self,screen):
        ds = int(self.timeleft*10)
        s,ds = divmod(ds,10)
        m,s = divmod(s,60)
        ds = int(ds)
        s = int(s)
        m = int(m)
        color = (255,255,255)
        if self.timesup:
            ds,s,m = (0,0,0)
        if self.timeleft < 20:
            color = (255,100,100)
        temps = f'{m:02d}:{s:02d}.{ds:d}'
        pg.draw.rect(screen,(170,170,170),pg.Rect(self.pos,(150,50)))
        font = pg.font.SysFont(None, 50)
        img = font.render(temps, True, color)
        screen.blit(img, (self.pos[0]+10, self.pos[1]+10))

    def reset(self,duration,increment):
        self.timeleft = duration
        self.duration = duration
        self.increment = increment
        self.tempsecoule = 0
        self.pause = True
        self.timesup = False
        self.firstmove = True

class Textinput():
    def __init__(self,pos,seconds,content):
        self.pos = pos
        self.seconds = seconds
        self.content = str(content)
        self.clicked = False
        self.rect = pg.Rect(self.pos,(35,30))
    def input(self,t):
        if t in ["0","1","2","3","4","5","6","7","8","9"] and len(self.content) < 2:
            self.content += str(t)
    def remove(self):
        self.content = self.content[:-1]
    def dis(self,screen):
        color = (120,120,200)
        if self.clicked:
            color = (200,120,120)
        pg.draw.rect(screen,color,self.rect,2)
        font = pg.font.SysFont(None, 30)
        img = font.render(str(self.content), True, (255,255,255))
        screen.blit(img,(self.pos[0]+5, self.pos[1]+5))
    def value(self):
        return int(self.content)*self.seconds

class Piecesclass():
    def __init__(self,color,pos,damtourfou,sqsize,topleft):
        self.sqsize = sqsize
        self.xtop = topleft[0]
        self.ytop = topleft[1]

        self.startingpos = pos
        self.color = color
        self.pos = pos
        self.alive = True
        self.canopen = True
        self.damtourfou = damtourfou

        self.roi = False

        self.pion = False
        self.cavalier = False
        self.dame = False
        self.tour = False
        self.canrook = True
        self.fou = False
        if self.damtourfou == 0:
            self.pion = True
        elif self.damtourfou == 1:
            self.dame = True
        elif self.damtourfou == 2:
            self.tour = True
        elif self.damtourfou == 3:
            self.fou = True
        else:
            self.cavalier = True

        self.rect = pg.Rect((self.xtop + self.pos[0]*self.sqsize,self.ytop + self.pos[1]*self.sqsize),(self.sqsize,self.sqsize))
        self.pionb = pg.image.load(os.path.join('images','pionb.png')).convert_alpha()
        self.pionb = pg.transform.smoothscale(self.pionb,(self.sqsize,self.sqsize))
        self.pionb.set_colorkey((230,230,230))
        self.pionn = pg.image.load(os.path.join('images','pionn.png')).convert_alpha()
        self.pionn = pg.transform.smoothscale(self.pionn,(self.sqsize,self.sqsize))
        self.pionn.set_colorkey((230,230,230))
        self.dameb = pg.image.load(os.path.join('images','dameb.png')).convert_alpha()
        self.dameb = pg.transform.smoothscale(self.dameb,(self.sqsize,self.sqsize))
        self.dameb.set_colorkey((230,230,230))
        self.damen = pg.image.load(os.path.join('images','damen.png')).convert_alpha()
        self.damen = pg.transform.smoothscale(self.damen,(self.sqsize,self.sqsize))
        self.damen.set_colorkey((230,230,230))
        self.tourb = pg.image.load(os.path.join('images','tourb.png')).convert_alpha()
        self.tourb = pg.transform.smoothscale(self.tourb,(self.sqsize,self.sqsize))
        self.tourb.set_colorkey((230,230,230))
        self.tourn = pg.image.load(os.path.join('images','tourn.png')).convert_alpha()
        self.tourn = pg.transform.smoothscale(self.tourn,(self.sqsize,self.sqsize))
        self.tourn.set_colorkey((230,230,230))
        self.foub = pg.image.load(os.path.join('images','foub.png')).convert_alpha()
        self.foub = pg.transform.smoothscale(self.foub,(self.sqsize,self.sqsize))
        self.foub.set_colorkey((230,230,230))
        self.foun = pg.image.load(os.path.join('images','foun.png')).convert_alpha()
        self.foun = pg.transform.smoothscale(self.foun,(self.sqsize,self.sqsize))
        self.foun.set_colorkey((230,230,230))
        self.cavalierb = pg.image.load(os.path.join('images','cavb.png')).convert_alpha()
        self.cavalierb = pg.transform.smoothscale(self.cavalierb,(self.sqsize,self.sqsize))
        self.cavalierb.set_colorkey((230,230,230))
        self.cavaliern = pg.image.load(os.path.join('images','cavn.png')).convert_alpha()
        self.cavaliern = pg.transform.smoothscale(self.cavaliern,(self.sqsize,self.sqsize))
        self.cavaliern.set_colorkey((230,230,230))

    def dis(self,screen):
        if self.color:
            if self.pion:
                screen.blit(self.pionb,(self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize))
            elif self.dame:
                screen.blit(self.dameb,(self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize))
            elif self.tour:
                screen.blit(self.tourb,(self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize))
            elif self.fou:
                screen.blit(self.foub,(self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize))
            else:
                screen.blit(self.cavalierb,(self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize))
        else:
            if self.pion:
                screen.blit(self.pionn,(self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize))
            elif self.dame:
                screen.blit(self.damen,(self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize))
            elif self.tour:
                screen.blit(self.tourn,(self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize))
            elif self.fou:
                screen.blit(self.foun,(self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize))
            else:
                screen.blit(self.cavaliern,(self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize))
    
    def move(self,w,rook):
        pospassant = (-1,-1)
        self.canrook = False
        self.canopen = False
        if self.pos[1]-w[1] in [2,-2] and self.pion:
            pospassant = (w[0],w[1]-1+(2*self.color))
        self.pos = w
        self.rect = pg.Rect((self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize),(self.sqsize,self.sqsize))

        return pospassant
    
    def wcango(self, positions, pospassant,rook):
        cango = []
        
        if self.tour or self.dame:
            cango += cango_vect(self.pos,positions,1,0,self.color,8)      #horizontal droite
            cango += cango_vect(self.pos,positions,-1,0,self.color,8)     #horizontal gauche
            cango += cango_vect(self.pos,positions,0,1,self.color,8)      #vertical bas
            cango += cango_vect(self.pos,positions,0,-1,self.color,8)     #vertical haut

        if self.dame or self.fou:
            cango += cango_vect(self.pos,positions,1,1,self.color,8)      #y = x droite
            cango += cango_vect(self.pos,positions,-1,-1,self.color,8)    #y = x gauche
            cango += cango_vect(self.pos,positions,-1,1,self.color,8)     #y = -x gauche
            cango += cango_vect(self.pos,positions,1,-1,self.color,8)     #y = -x droite

        if self.cavalier:
            #partie droite
            cango += cango_vect(self.pos,positions,1,2,self.color,1)      #bas droite
            cango += cango_vect(self.pos,positions,2,1,self.color,1)      #droite bas
            cango += cango_vect(self.pos,positions,2,-1,self.color,1)     #droite haut
            cango += cango_vect(self.pos,positions,1,-2,self.color,1)     #haut droite
            #partie gauche
            cango += cango_vect(self.pos,positions,-1,-2,self.color,1)    #haut gauche
            cango += cango_vect(self.pos,positions,-2,-1,self.color,1)    #gauche haut
            cango += cango_vect(self.pos,positions,-2,1,self.color,1)     #gauche bas
            cango += cango_vect(self.pos,positions,-1,2,self.color,1)     #bas gauche

        
        if self.pion:
            if self.color:
                positions[0].append(pospassant)
                if (self.pos[0]+1,self.pos[1]-1) in positions[0]:
                    cango += [(self.pos[0]+1,self.pos[1]-1)]
                if (self.pos[0]-1,self.pos[1]-1) in positions[0]:
                    cango += [(self.pos[0]-1,self.pos[1]-1)]
                if not((self.pos[0],self.pos[1]-1) in (positions[0]+positions[1])) :
                    if self.canopen and not((self.pos[0],self.pos[1]-2) in (positions[0]+positions[1])):
                        cango += [(self.pos[0],self.pos[1]-2)]
                        cango += [(self.pos[0],self.pos[1]-1)]
                    else:
                        cango += [(self.pos[0],self.pos[1]-1)]
                positions[0].remove(pospassant)

            else:
                positions[1].append(pospassant)
                if (self.pos[0]+1,self.pos[1]+1) in positions[1]:
                    cango += [(self.pos[0]+1,self.pos[1]+1)]
                if (self.pos[0]-1,self.pos[1]+1) in positions[1]:
                    cango += [(self.pos[0]-1,self.pos[1]+1)]
                if not((self.pos[0],self.pos[1]+1) in (positions[1]+positions[0])):
                    if self.canopen and not((self.pos[0],self.pos[1]+2) in (positions[1]+positions[0])) :
                        cango += [(self.pos[0],self.pos[1]+2)]
                        cango += [(self.pos[0],self.pos[1]+1)]
                    else:
                        cango += [(self.pos[0],self.pos[1]+1)]
                positions[1].remove(pospassant)
        return cango

    def promotion(self,move):
        if move[1] in [0,7]:
            self.pion = False
            self.dame = True

    def reset(self):
        self.pos = self.startingpos
        self.alive = True
        self.canopen = True

        self.roi = False

        self.pion = False
        self.cavalier = False
        self.dame = False
        self.tour = False
        self.canrook = True
        self.fou = False
        if self.damtourfou == 0:
            self.pion = True
        elif self.damtourfou == 1:
            self.dame = True
        elif self.damtourfou == 2:
            self.tour = True
        elif self.damtourfou == 3:
            self.fou = True
        else:
            self.cavalier = True
        self.rect = pg.Rect((self.xtop + self.pos[0]*self.sqsize,self.ytop + self.pos[1]*self.sqsize),(self.sqsize,self.sqsize))


class Roi():
    def __init__(self,color,pos,sqsize,topleft):
        self.sqsize = sqsize
        self.xtop = topleft[0]
        self.ytop = topleft[1]

        self.color = color
        self.startingpos = pos
        self.pos = pos
        self.alive = True
        self.canrook = True
        self.enechec = False

        self.roi = True
        self.pion = False

        self.rect = pg.Rect((self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize),(self.sqsize,self.sqsize))
        self.roib = pg.image.load(os.path.join('images','roib.png')).convert_alpha()
        self.roib = pg.transform.smoothscale(self.roib,(self.sqsize,self.sqsize))
        self.roib.set_colorkey((230,230,230))
        self.roin = pg.image.load(os.path.join('images','roin.png')).convert_alpha()
        self.roin = pg.transform.smoothscale(self.roin,(self.sqsize,self.sqsize))
        self.roin.set_colorkey((230,230,230))
        self.echecfond = pg.image.load(os.path.join('images','echec.png')).convert_alpha()
        self.echecfond = pg.transform.smoothscale(self.echecfond,(self.sqsize,self.sqsize))
        self.echecfond.set_colorkey((230,230,230))

    def dis(self,screen):
        if self.enechec:
            screen.blit(self.echecfond,(self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize))
        if self.color:
            screen.blit(self.roib,(self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize))
        else:
            screen.blit(self.roin,(self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize))

    def move(self,w,rook):
        dis = self.pos[0]-w[0]
        if self.roi and (dis > 1 or dis < -1):
            global haverook
            haverook = True
            if w[0] == 2:
                if self.color:
                    rook[1][0].move((3,7),rook)
                else:
                    rook[0][0].move((3,0),rook)
            else:
                if self.color:
                    rook[1][1].move((5,7),rook)
                else:
                    rook[0][1].move((5,0),rook)
            
        self.pos = w
        self.rect = pg.Rect((self.xtop+self.pos[0]*self.sqsize,self.ytop+self.pos[1]*self.sqsize),(self.sqsize,self.sqsize))
        self.canrook = False

        return (-1,-1)
        
    def wcango(self,positions,pospassant,rook):
        cango = []
        #déplacement non diagonal
        cango += cango_vect(self.pos,positions,1,0,self.color,1)     #droite
        cango += cango_vect(self.pos,positions,-1,0,self.color,1)    #gauche
        cango += cango_vect(self.pos,positions,0,1,self.color,1)     #bas
        cango += cango_vect(self.pos,positions,0,-1,self.color,1)    #haut

        #deplacement diagonal
        cango += cango_vect(self.pos,positions,1,1,self.color,1)     #bas droit
        cango += cango_vect(self.pos,positions,-1,1,self.color,1)    #bas gauche
        cango += cango_vect(self.pos,positions,-1,-1,self.color,1)   #haut gauche
        cango += cango_vect(self.pos,positions,1,-1,self.color,1)    #haut droit
        
        #ROOK
        toura = rook[self.color][0]
        tourh = rook[self.color][1]

        if self.canrook and not(self.enechec):

            if len(cango_vect(self.pos,positions,1,0,self.color,4)) == 2 and tourh.canrook:
                cango += [(6,self.pos[1])]

            if len(cango_vect(self.pos,positions,-1,0,self.color,4)) == 3 and toura.canrook:
                cango += [(2,self.pos[1])]
        return cango
    
    def reset(self):
        self.pos = self.startingpos
        self.alive = True
        self.canrook = True
        self.enechec = False

        self.roi = True
        self.pion = False
        self.rect = pg.Rect((self.xtop + self.pos[0]*self.sqsize,self.ytop + self.pos[1]*self.sqsize),(self.sqsize,self.sqsize))


def echec(pieces,roipos,kingcolor,positions,rook,goeate):
    color = not kingcolor
    eate = goeate in positions[not kingcolor]
    if eate:
        positions[not kingcolor].remove(goeate)
    for piece in pieces:
        if piece.alive:
            if piece.color == color:
                if piece.pos != goeate:
                    cango = piece.wcango(positions,(-1,-1),rook)
                    if roipos in cango:
                        if eate:
                            positions[not kingcolor] += [goeate]
                        return True
    if eate:
        positions[not kingcolor] += [goeate]
    return False

def wcangoechec(pieces,roipos,kingcolor,piece,positions,pospassant,rook):
    cangoechec = []
    roipostemp = roipos
    for move in piece.wcango(positions,pospassant,rook):
        can = True

        positions[piece.color].remove(piece.pos)
        positions[piece.color] += [move]
        if piece.roi:
            dis = roipos[0]-move[0]
            if dis > 1 or dis < -1:
                pospassage = (int(roipos[0]-(dis)/2),roipos[1])
                if  pospassage in cangoechec:
                    roipostemp = move
                else:
                    can = False

            else:
                roipostemp = move
        if not(echec(pieces,roipostemp,kingcolor,positions,rook,move)) and can:
            cangoechec += [move]
        positions[piece.color].remove(move)
        positions[piece.color] += [piece.pos]
    return cangoechec

def mat(pieces,roipos,kingcolor,positions,pospassant,rook):
    for piece in pieces:
        if piece.alive:
            if piece.color == kingcolor:
                if wcangoechec(pieces,roipos,kingcolor,piece,positions,pospassant,rook) != []:
                    return False
    return True



def draw_rect_alpha(surface, color, rect):
    shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
    pg.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def draw_circle_alpha(surface, color, center, radius):
    target_rect = pg.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
    pg.draw.circle(shape_surf, color, (radius, radius), radius,7)
    surface.blit(shape_surf, target_rect)

width = topleft[0]*2 + sqsize*8 + 420
height = topleft[1]*2 +sqsize*8

screen = pg.display.set_mode((width,height))
sqpos = []
colorcase = (20,20,20)
for x in range(1,8,2):
    for y in range(8):
        sqpos += [(x*sqsize-(y%2)*sqsize,y*sqsize)]
def damier():
    screen.fill((230,230,230))
    fondamier = pg.Rect(topleft,(sqsize*8,sqsize*8))
    pg.draw.rect(screen,(210,210,210),fondamier)
    for i in sqpos:
        pg.draw.rect(screen,colorcase,pg.Rect((topleft[0]+i[0],topleft[1]+i[1]),(sqsize,sqsize)))
    font = pg.font.SysFont(None,20)
    
    for i in range(8,0,-1):
        if i%2 == 0:
            color = colorcase
        else:
            color = (210,210,210)
        img = font.render(str(i), True, color)
        posy = (sqsize*8)-(sqsize*i)
        screen.blit(img,(topleft[0]+4,topleft[1]+4+posy))
    lettres = ["a","b","c","d","e","f","g","h"]
    for i in range(8):
        if (i+1)%2 == 0:
            color = colorcase
        else:
            color = (210,210,210)
        img = font.render(lettres[i], True, color)
        posy = (sqsize*7) + sqsize - 15
        posx = (sqsize*i) + sqsize - 10
        screen.blit(img,(topleft[0]+posx,topleft[1]+posy))

def dispieces(pieces,screen):
    for i in pieces:
        if i.alive:
            i.dis(screen)

cangoimg = pg.image.load(os.path.join('images','cango.png')).convert_alpha()
cangoimg = pg.transform.smoothscale(cangoimg,(sqsize,sqsize))
cangoimg.set_colorkey((230,230,230))

caneatimg = pg.image.load(os.path.join('images','caneat.png')).convert_alpha()
caneatimg = pg.transform.smoothscale(caneatimg,(sqsize,sqsize))
caneatimg.set_colorkey((230,230,230))

def discango(wcango,positions,color,screen,pospassant):
    positions[not color].append(pospassant)
    for i in wcango:
        if i in positions[not color]:
            screen.blit(caneatimg,(topleft[0]+i[0]*sqsize,topleft[1]+i[1]*sqsize))
        else:
            screen.blit(cangoimg,(topleft[0]+i[0]*sqsize,topleft[1]+i[1]*sqsize))
    positions[not color].remove(pospassant)

def dislastmove(historique):
    if len(historique) >= 1:
        gohere = historique[0]
        fromhere = historique[1]
        colormove = (190,190,100,127)
        rect1 = pg.Rect((topleft[0]+fromhere[0]*sqsize,topleft[1]+fromhere[1]*sqsize),(sqsize,sqsize))
        rect2 = pg.Rect((topleft[0]+gohere[0]*sqsize,topleft[1]+gohere[1]*sqsize),(sqsize,sqsize))
        draw_rect_alpha(screen,colormove,rect1)
        draw_rect_alpha(screen,colormove,rect2)
        

def clickedpiece(piece,clicked):
    if clicked:
        color = (190,190,100,127)
        draw_rect_alpha(screen,color,piece.rect)


#pieces noirs
pna = Piecesclass(0,(0,1),0,sqsize,topleft)
pnb = Piecesclass(0,(1,1),0,sqsize,topleft)
pnc = Piecesclass(0,(2,1),0,sqsize,topleft)
pnd = Piecesclass(0,(3,1),0,sqsize,topleft)
pne = Piecesclass(0,(4,1),0,sqsize,topleft)
pnf = Piecesclass(0,(5,1),0,sqsize,topleft)
png = Piecesclass(0,(6,1),0,sqsize,topleft)
pnh = Piecesclass(0,(7,1),0,sqsize,topleft)

tourna = Piecesclass(0,(0,0),2,sqsize,topleft)
cavnb = Piecesclass(0,(1,0),4,sqsize,topleft)
founc = Piecesclass(0,(2,0),3,sqsize,topleft)
damen = Piecesclass(0,(3,0),1,sqsize,topleft)
roin = Roi(0,(4,0),sqsize,topleft)
founf = Piecesclass(0,(5,0),3,sqsize,topleft)
cavng = Piecesclass(0,(6,0),4,sqsize,topleft)
tournh = Piecesclass(0,(7,0),2,sqsize,topleft)

#pieces blanches
pa = Piecesclass(1,(0,6),0,sqsize,topleft)
pb = Piecesclass(1,(1,6),0,sqsize,topleft)
pc = Piecesclass(1,(2,6),0,sqsize,topleft)
pd = Piecesclass(1,(3,6),0,sqsize,topleft)
pe = Piecesclass(1,(4,6),0,sqsize,topleft)
pf = Piecesclass(1,(5,6),0,sqsize,topleft)
pge = Piecesclass(1,(6,6),0,sqsize,topleft)
ph = Piecesclass(1,(7,6),0,sqsize,topleft)

toura = Piecesclass(1,(0,7),2,sqsize,topleft)
cavb = Piecesclass(1,(1,7),4,sqsize,topleft)
fouc = Piecesclass(1,(2,7),3,sqsize,topleft)
dame = Piecesclass(1,(3,7),1,sqsize,topleft)
roi = Roi(1,(4,7),sqsize,topleft)
fouf = Piecesclass(1,(5,7),3,sqsize,topleft)
cavg = Piecesclass(1,(6,7),4,sqsize,topleft)
tourh = Piecesclass(1,(7,7),2,sqsize,topleft)


pieces = [pa,pb,pc,pd,pe,pf,pge,ph,toura,cavb,fouc,dame,roi,fouf,cavg,tourh,
pna,pnb,pnc,pnd,pne,pnf,png,pnh,tourna,cavnb,founc,damen,roin,founf,cavng,tournh]

rook = [[tourna,tournh],[toura,tourh]]
positions = [[],[]]

damiersidex = sqsize*8+topleft[0]

timern = Timer(60,1,(damiersidex,topleft[1]))
timerb = Timer(60,1,(damiersidex,sqsize*8+topleft[0]-50))

timers = [timern,timerb]

xin = damiersidex
yin = 350

minute_input = Textinput((xin+60,yin+65),60,10)
second_input = Textinput((xin+105,yin+65),1,0)

minute_input_in = Textinput((xin+60,yin+135),60,0)
second_input_in = Textinput((xin+105,yin+135),1,5)

text_inputs = [minute_input,second_input,minute_input_in,second_input_in]



def resetpieces():
    for piece in pieces:
        piece.reset()


def getpositions(pieces):
    positions = [[],[]]
    for i in pieces:
        if i.alive:
            if not i.color:
                positions[0] += [i.pos]
            else:
                positions[1] += [i.pos]
    return positions


def disrejouer(screen,jouer):
    pos = (xin,yin)
    pg.draw.rect(screen,(170,170,170),pg.Rect(pos,(400,200)))
    font = pg.font.SysFont(None, 40)
    fontsmall = pg.font.SysFont(None, 35)
    white = (255,255,255)
    temps = font.render("Temps :", True, white)
    increment = font.render("Increment :", True, white)
    separation = font.render(":", True, white)
    jouertxt = font.render("JOUER", True, white)
    s = fontsmall.render("s", True, white)
    screen.blit(temps,(xin+30,yin+30))
    screen.blit(increment,(xin+30,yin+100))
    screen.blit(separation,(xin+95,yin+65))
    screen.blit(separation,(xin+95,yin+135))
    screen.blit(s,(xin+145,yin+70))
    screen.blit(s,(xin+145,yin+140))
    for t in text_inputs:
        t.dis(screen)
    pg.draw.rect(screen,(100,200,100),jouer)
    screen.blit(jouertxt,(xin+235,yin+88))

jouer = pg.Rect((xin+210,yin+70),(150,60))

def flip(pieces,screen,wcango,positions,piece,color,clicked,historique,pospassant):
    damier()
    clickedpiece(piece,clicked)
    dislastmove(historique)
    dispieces(pieces,screen)
    discango(wcango, positions, color, screen,pospassant)
    disrejouer(screen,jouer)
    pg.display.flip()

def flip_timers(screen,timestart):
    for t in timers:
        t.actualiser(timestart,time.time())
        t.display(screen)
    pg.display.flip()

def gagne_timer():
    if timerb.timesup:
        return (True,False)
    elif timern.timesup:
        return (True,True)
    else:
        return (False,False)

def afficher_victoire(text):
    font = pg.font.SysFont(None, 60)
    img = font.render(text, True, (50,50,50))
    screen.blit(img,(damiersidex+10,180))


haverook = False

def main(pieces,screen,pg):
    pg.mixer.pre_init(44100, -16, 1, 512)
    pg.mixer.init()
    pg.init()
    a_moveb = pg.mixer.Sound(os.path.join('audio','moveb.wav'))
    a_moven = pg.mixer.Sound(os.path.join('audio','moven.wav'))
    a_eat = pg.mixer.Sound(os.path.join('audio','eat.wav'))
    a_echec = pg.mixer.Sound(os.path.join('audio','echec.wav'))
    a_end = pg.mixer.Sound(os.path.join('audio','end.wav'))
    a_start = pg.mixer.Sound(os.path.join('audio','start.wav'))
    a_rook = pg.mixer.Sound(os.path.join('audio','rook.wav'))
    positions = getpositions(pieces)
    wcango = []
    pospassant = (-1,1)
    clicked = False
    color = True
    won = False
    textinput_clicked = False
    historique = []         #[position de depard, position d'arivée]
    timestart = time.time()
    text = ""
    partiefinie = False
    eat = False
    global haverook

    flip(pieces,screen,wcango,positions,False,color,clicked,historique,pospassant)
    enechecb = echec(pieces,roi.pos,roi.color,positions,rook,(-1,-1))
    enechec = echec(pieces,roin.pos,roin.color,positions,rook,(-1,-1))
    

    while True:
        flip_timers(screen,timestart)
        if not partiefinie:
            timesup,won = gagne_timer()
        if timesup:
            timerb.firstmove = True
            timern.firstmove = True
            timerb.stop()
            timern.stop()
            partiefinie = True
            pg.mixer.Sound.play(a_end)
            if won:
                text = "Les blancs gagnent"
            else:
                text = "Les noirs gagnent"
        afficher_victoire(text)
        timesup = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_BACKSPACE:
                    textinput.remove()
                elif textinput_clicked:
                    textinput.input(event.unicode)
                disrejouer(screen,jouer)

                
            if event.type == pg.MOUSEBUTTONDOWN:
                for move in wcango:
                    rect = pg.Rect((topleft[0]+move[0]*sqsize,topleft[1]+move[1]*sqsize),(sqsize,sqsize))
                    if rect.collidepoint(event.pos) and not partiefinie:
                        if piecesel.pion:
                            piecesel.promotion(move)
                        for i in pieces:
                            if i.alive and i.pos == move:
                                i.alive = False
                                eat = True
                                break
                            elif move == pospassant and i.pion and piecesel.pion:
                                if (i.pos[0],i.pos[1]) == (pospassant[0],pospassant[1]+1-(2*(not color))):
                                    i.alive = False
                                    eat = True
                                    break
                        
                        timers[color].stop()
                        if not timers[not color].firstmove:
                            timers[not color].start()
                        timestart = time.time()

                        historique = (piecesel.pos,move)
                        pospassant = piecesel.move(move,rook)
                        positions = getpositions(pieces)
                        enechec = echec(pieces,roin.pos,roin.color,positions,rook,(-1,-1))

                        if enechec:
                            print("echec")
                            roin.enechec = True
                            if mat(pieces,roin.pos,roin.color,positions,pospassant,rook):
                                print("echec et mat")
                                won = True
                                text = "Les blancs gagnent"
                                timerb.stop()
                                timern.stop()
                                partiefinie = True
                                pg.mixer.Sound.play(a_end)


                        enechecb = echec(pieces,roi.pos,roi.color,positions,rook,(-1,-1))
                        if enechecb:
                            roi.enechec = True
                            print("echec")
                            if enechecb and mat(pieces,roi.pos,roi.color,positions,pospassant,rook):
                                print("echec et mat")
                                won = False
                                text = "Les noirs gagnent"
                                timern.stop()
                                timerb.stop()
                                partiefinie = True
                                pg.mixer.Sound.play(a_end)

                        if not enechec and mat(pieces,roin.pos,roin.color,positions,pospassant,rook):
                                text = "Egalité"
                                partiefinie = True
                                pg.mixer.Sound.play(a_end)
                        if not enechecb and mat(pieces,roi.pos,roi.color,positions,pospassant,rook):
                                text = "Egalité"
                                partiefinie = True
                                pg.mixer.Sound.play(a_end)

                        if not enechec:
                            roin.enechec = False
                        if not enechecb:
                            roi.enechec = False
                        
                        if not partiefinie:
                            if enechecb or enechec:
                                pg.mixer.Sound.play(a_echec)
                                pg.mixer.music.stop()
                            elif eat:
                                pg.mixer.Sound.play(a_eat)
                                pg.mixer.music.stop()
                            elif haverook:
                                pg.mixer.Sound.play(a_rook)
                                pg.mixer.music.stop()
                            else:
                                if color:
                                    pg.mixer.Sound.play(a_moveb)
                                else:
                                    pg.mixer.Sound.play(a_moven)
                                pg.mixer.music.stop()
                        eat = False
                        haverook = False
                        color = not color
                        

                clicked = False
                for piece in pieces:
                    if piece.alive and piece.color == color:
                        if piece.rect.collidepoint(event.pos):

                            if color:
                                wcango = wcangoechec(pieces,roi.pos,roi.color,piece,positions,pospassant,rook)
                            else:
                                wcango = wcangoechec(pieces,roin.pos,roin.color,piece,positions,pospassant,rook)
                            clicked = True
                            piecesel = piece
                            flip(pieces,screen,wcango,positions,piece,piece.color,clicked,historique,pospassant)

                            break
                if not clicked:
                    wcango = []
                    flip(pieces,screen,wcango,positions,piece,piece.color,clicked,historique,pospassant)
                
                for t in text_inputs:
                    t.clicked = False
                textinput = None
                disrejouer(screen,jouer)
                textinput_clicked = False
                for t in text_inputs:
                    if t.rect.collidepoint(event.pos):
                        t.clicked = True
                        textinput = t
                        textinput_clicked = True
                        disrejouer(screen,jouer)
                if jouer.collidepoint(event.pos):
                    pg.mixer.Sound.play(a_start)
                    pg.mixer.music.stop()
                    resetpieces()
                    positions = getpositions(pieces)
                    historique = []
                    text = ""
                    color = True
                    partiefinie = False
                    duration = minute_input.value() + second_input.value()
                    increment = minute_input_in.value() + second_input_in.value()
                    pospassant = (-1,-1)
                    timern.reset(duration,increment)
                    timerb.reset(duration,increment)
                    flip(pieces,screen,wcango,positions,piece,color,clicked,historique,pospassant)
                







while __name__ == "__main__":
    main(pieces,screen,pg)