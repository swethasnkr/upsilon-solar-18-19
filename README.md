# upsilon-solar-18-19
import time
class Solarcell(object):
  def __init__(self, material, bandgap, inducedV, valence, cost):
    self.material = material #string that is the name of the material
    self.bandgap = bandgap #in electron volts (eV)
    self.valence = valence #valence electron energy (we can use this for the physics of the photons hitting the electrons)
    self.cost = cost
    self.inducedV = inducedV

class Particle(object):
    def __init__(self, material, bandgap, valence, posx, posy, initial_energy):
        self.material = material #string that is the name of the material
        self.bandgap = bandgap
        self.valence = valence #valence electron energy (we can use this for the physics of the photons hitting the 
        self.posx = posx #posx and posy describe the top left corner of the particle
        self.posy = posy
        self.initial_energy = initial_energy

    def setpos(self, x, y):
        self.posx = x
        self.posy = y

    def getvel(self):
        return self.vel

class Conditions:
  def __init__(self, temp, sunnydays, humidity, intensity):
    self.temp = temp
    self.sunnydays = sunnydays
    self.hum = humidity
    self.elev = elevation
    self.inten = intensity

material = "silicon"
bandgap = 1.1
inducedV = 1
valence = 1
cost = 100
vel = 0
h = 6.626 * 10 ** -34 #planck's constant
f = 8 * 10 ** 14 #frequency of ultraviolet light
initial_energy = h * f #of the photon

# we'll make the individual particles as 1 x 1 blocks for now, to keep things simple-ish
# to visualize what I've done:  I have a row of atoms represented by 1 x 1 cubes
# with top left corners at (posx,posy). They are stationary. As y'all fiddle with the code
# and expand upon it, think about assumptions we can make to make our lives easy (ex:  perfectly
# elastic collisions), which should help simplify creating photons and having them hit the material atoms

silicon = Solarcell(material, bandgap, inducedV, valence, cost)
siliconparts = []
for i in range(1,11):
    posx = i
    posy = 1
    newpart = Particle(material, bandgap, valence, posx, posy, vel)
    siliconparts.append(newpart)

for part in siliconparts:
    print(part.posx , part.posy)
    
    
#----------------photon code below---------------------

import pygame, math, sys, random

#variables
backgroundcolor = (0,0,0)
width, height = 1400, 900
globalGravity = 1000
FPS = 500
totalParticles = 100
particleTrail = False
maxVelocity = 1

#setup
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Photon Simulation')
screen.fill(backgroundcolor)
mainClock = pygame.time.Clock()

#classes and functions
class Particle:
    def __init__(self, x, y, size, e, gravity = globalGravity): 
        self.x = x
        self.y = y
        self.size = size
        self.e = e
        self.velocity = 0
        self.maxVelocity = math.sqrt(2*gravity*(height-y-size))
        self.gravity = gravity
            
    def render(self):
        pygame.draw.circle(screen, (255,255,0), (round(self.x), round(self.y)), self.size)
    
    def delete(self):
        pygame.draw.circle(screen, (0,0,0), (round(self.x), round(self.y)), self.size)


def terminate():
    pygame.quit()
    sys.exit()
   
def createParticles():
    particleList = []    
    for n in range(1,1+totalParticles):
        particle = Particle(int(width/(1+totalParticles) * (n)), random.randint(10,300), 1, random.randint(98,100)/100, 500)
        particleList.append(particle)
    for particle in particleList:
        particle.render()
    return particleList


#begin
particleList = createParticles()

#running loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == ord('r'): #reset
                screen.fill(backgroundcolor)
                particleList = createParticles()    
    for particle in particleList:
        if particle.maxVelocity > maxVelocity:
            maxVelocity = particle.maxVelocity
        if not particleTrail:
            particle.delete()
        if particle.y < height - (particle.size):
            particle.velocity += (1/FPS) * particle.gravity            
        else:
            particle.y = height - particle.size
            particle.velocity = -1 * particle.velocity * particle.e
        particle.y += particle.velocity * (1/FPS)
        particle.x += 0.1
        particle.render()
    pygame.display.update()
    mainClock.tick(FPS)
    



