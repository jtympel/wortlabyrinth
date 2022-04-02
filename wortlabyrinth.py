#-----------------------------------------------------------------------------
# ------------------------------------------------------- wortlabyrinth.py m n
# ------------------------------------------------------- erstellt: 01.02.2022
#-----------------------------------------------------------------------------
# Beschreibung: Ein Programm zum Erstellen von Wortlabyrinthen. Der Lösungsweg
# wird entlang eines Lösungssatzes gezeichnet. Das Labyrinth
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # unterdrücke die pygame-Nachricht in der Konsole
import pygame
import random
import string # nötig für Buchstaben
string.ascii_letters # 'abcde....ABCDE...'
import sys
sys.setrecursionlimit(4000) # höhere Rekursionstiefe für komplexere Labyrinthe (>20x20)

m = int(sys.argv[1]) # Anzahl der ZEILEN
n = int(sys.argv[2]) # Anzahl der SPALTEN

if n < 3 or m < 3: # Fehlerbehandlung für zu kleine Matrix
	print('Error: n and m Dimensionen müssen mindestens 2x2 sein!')
	sys.exit()
if n > 40 or m > 40:  # Fehlerbehandlung für zu große Matrix
	print('Error: n and m Dimensionen dürfen nicht größer als 40 sein!')
	sys.exit()

satz = input('Gib deinen Lösungssatz ein:')
if len(satz) < n + m:
	print('FEHLER: Lösungssatz ist zu kurz für die gewünschte Labyrinthgröße.')
	sys.exit()

# Input String formatieren
satz = satz.upper() # alle Buchstaben in Grossbuchstaben
satz = ''.join(filter(str.isalnum, satz)) # Sonderzeichen entfernen
satz = ''.join([i for i in satz if not i.isdigit()]) # Zahlen entfernen
print('formatierter Lösungssatz:',satz, '| Buchstabenzahl:',len(satz))

BREITE = n * 50  # Bildschirmgröße in Pixel (angepasst auf Labyrinth-Maße)
HÖHE = m * 50
# BREITE = 1000  # Bildschirmgröße in Pixel (vordefinierte Maße)
# HÖHE = 1000

SPALTEN = n
ZEILEN = m
ZE_BH = BREITE // SPALTEN # Zellengröße (Breite-Höhe)

delta_linien = {'l':[(0,0),(0,ZE_BH)], 'r':[(ZE_BH,0),(ZE_BH,ZE_BH)], 'o':[(0,0),(ZE_BH,0)], 'u': [(0,ZE_BH),(ZE_BH,ZE_BH)]} # Wandpositionen (Linien)
delta_nachbarn = {'l':(-ZE_BH,0), 'r':(ZE_BH,0), 'o':(0,-ZE_BH), 'u':(0,ZE_BH)} # l = links, r = rechts, o = oben, u = unten
richtung_invers = {'l':'r', 'r':'l', 'o':'u', 'u':'o'} # gegenüberliegende Seiten

pygame.init() # Anfangsbildschirm initialisieren
screen = pygame.display.set_mode([BREITE,HÖHE])
farbe_hintergrund = pygame.Color('White')
farbe_linie = pygame.Color('Black')
# farbe_weg = pygame.Color('Green') # momentan nicht in Verwendung

def raster_erstellen():
	for i in range(SPALTEN*ZEILEN):
		pos = i % SPALTEN * ZE_BH, i // SPALTEN * ZE_BH
		raster[pos] = {b for b in 'lrou'} # 4 Zellwände an einer Raster-Position (set comprehension)

def add_pos(pos1,pos2):
	return pos1[0] + pos2[0], pos1[1] + pos2[1]

def zeichne_zelle(pos,wände):
	for wand in wände:
		delta_von, delta_bis = delta_linien[wand]
		von = add_pos(pos,delta_von)
		bis = add_pos(pos,delta_bis)
		pygame.draw.line(screen,farbe_linie,von,bis,4) # strichstärke 4

def nachbarn_ermitteln(pos):
	nachb = []
	for richtung, delta in delta_nachbarn.items():
		neue_pos = add_pos(pos,delta)
		if neue_pos not in raster: continue # schnappt sich die nächste Richtung
		nachb.append((richtung,neue_pos))
	random.shuffle(nachb)
	return nachb

def labyrinth_erstellen(pos_aktuell,richtung_von):
	besucht.add(pos_aktuell)
	raster[pos_aktuell].remove(richtung_von)
	nachb = nachbarn_ermitteln(pos_aktuell)
	for richtung_nach, pos_neu in nachb:
		if pos_neu in besucht: continue
		raster[pos_aktuell].remove(richtung_nach)
		labyrinth_erstellen(pos_neu, richtung_invers[richtung_nach]) # lösche die Wand aus der neuen Zelle in die ich reingehe

def mögliche_richtungen(pos):
	richtungen = []
	for richtung,delta in delta_nachbarn.items():
		neue_pos = add_pos(pos,delta)
		if neue_pos not in raster: continue
		if richtung in raster[pos]: continue
		richtungen.append(neue_pos)
	return richtungen

def labyrinth_lösen(pos_aktuell):
	besucht.append(pos_aktuell)
	if pos_aktuell == ziel:
		# print('aktuelle position ist das Ziel!',pos_aktuell,'Ziel:',ziel)
		return True
	for pos_neu in mögliche_richtungen(pos_aktuell):
		if pos_neu in besucht: continue
		if labyrinth_lösen(pos_neu):
			weg.append(pos_neu)
			# print('Weg nimmt zu:',weg) # überprüfen der Lösungs-Wegpukte
			return True

ziel = ((SPALTEN-1)*ZE_BH,(ZEILEN-1)*ZE_BH) # Koordinaten der Zielzelle
solution = False
iteration = 0

while solution == False:
	iteration += 1
	if iteration > 2000: # definiertes Limit für Anzahl an zufällig generierten Labyrinthen 
		print('Keine Lösung nach 2000 Iterationen gefunden!')
		sys.exit()
	raster = {}
	raster_erstellen()	
	weg = []
	besucht = set()
	labyrinth_erstellen((0,0),'l')
	besucht = []
	labyrinth_lösen((0,0))
	weg.append((0,0)) # Startposition hinzufügen
	if len(satz) == len(weg):
		solution = not solution # boolean auf 'True' setzen um 'while' Loop zu beenden
		print('Lösung nach',iteration,'Iterationen gefunden!')

screen.fill(farbe_hintergrund)
for pos,wände in raster.items():
	zeichne_zelle(pos,wände)
pygame.display.flip()
pygame.image.save(screen,'lab_1.png') # Screenshot 1 mit dem leeren Labyrinth

schrift = pygame.font.SysFont('Arial',40)
invers_satz = satz[::-1] # Inverse des Lösungssatzes

i = 0
while i < len(invers_satz):
	buchstabe = schrift.render(invers_satz[i], 1, (0,0,1), None) # Attribute: 'string', antialias, color, ?
	x,y = weg[i]
	x = x + ZE_BH // 3.5 # Buchstaben in mittlere Position innerhalb einer Zelle schieben
	screen.blit(buchstabe,(x,y)) # Buchstabe zeichnen
	pygame.display.flip()
	i += 1
pygame.image.save(screen,'lab_2.png') # Screenshot 2 mit dem Lösungsweg

for pos in raster.items(): # Zufällige Buchstaben in alle Felder setzen, die nicht Teil der Lösung sind
	if pos[0] not in weg:
		buchstabe = schrift.render(random.choice(string.ascii_letters).upper(), 1, (0,0,1), None) # Attribute: 'string', antialias, color, ?
		x,y = pos[0]
		x = x + ZE_BH // 3.5 # Buchstaben in mittlere Position innerhalb einer Zelle schieben
		screen.blit(buchstabe,(x,y)) # Buchstabe zeichnen
		pygame.display.flip()
pygame.image.save(screen,'lab_3.png') # Screenshot 3 mit dem kompletten Labyrinth

pygame.quit()