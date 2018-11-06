# upsilon-solar-18-19

class solarcell:
  def __init__(self, material, bandgap, inducedV, valence, cost):
    self.material = material #string that is the name of the material
    self.bandgap = bandgap
    self.valence = valence #valence electron energy (we can use this for the physics of the photons hitting the electrons)
    self.cost = cost
  
class conditions:
  def __init__(self, temp, sunnydays, humidity, intensity):
    self.temp = temp
    self.sunnydays = sunnydays
    self.hum = humidity
    self.elev = elevation
    self.inten = intensity
