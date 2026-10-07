import pygame
from time import sleep
dim = 70
ris_x , ris_y = 9*dim , 9*dim

rosso  = (255,  0,  0)
verde  = (0  ,255,  0)
blu    = (0  ,  0,255)
giallo = (255,255,  0)
bianco = (255,255,255)
nero   = (  0,  0,  0)

c_nera   = pygame.image.load('n.png')
c_bianca = pygame.image.load('b.png')
c_salva  = pygame.image.load('s.png')

c_nera   = pygame.transform.scale(c_nera  ,(dim,dim))
c_bianca = pygame.transform.scale(c_bianca,(dim,dim))
c_salva  = pygame.transform.scale(c_salva ,(dim,dim))

#pezzi bianchi

re = pygame.image.load('re.png')
re = pygame.transform.scale(re,(dim,dim))

ped_b = pygame.image.load('ped_b.png')
ped_b = pygame.transform.scale(ped_b,(dim,dim))

pezzi_bianchi      = [re]
stato_bianchi      = ['v']
posizione_bianchi  = [(4,4),(2,4),(3,4),(5,4),(6,4),(4,2),(4,3),(4,5),(4,6)]

for i in range(0,8):
	pezzi_bianchi.append(ped_b)
	stato_bianchi.append('v')

#pezzi neri

ped_n = pygame.image.load('ped_n.png')
ped_n = pygame.transform.scale(ped_n,(dim,dim))

pezzi_neri     = []
stato_neri     = []
posizione_neri = [(3,0),(4,0),(5,0),(4,1),(3,8),(4,8),(5,8),(4,7),(8,3),(8,4),(8,5),(7,4),(0,3),(0,4),(0,5),(1,4)]

for i in range(0,16):
	pezzi_neri.append(ped_n)
	stato_neri.append('v')


#posizione dei pezzi
pygame.init()

#icona
pygame.display.set_icon(pygame.image.load('icona.png'))
#titolo
pygame.display.set_caption('Tablut')
schermo = pygame.display.set_mode((ris_x,ris_y))

pygame.mixer.init()
valhalla = pygame.mixer.Sound('valhalla.wav')
#valhalla.play() #-> aggiungere (-1) per ripetere all'infinito

#Musica cattiva a caso
#sottofondo =

tocco = 0
muovi_bianco = 0
muovi_nero   = 0
legale_bianco = True
legale_nero   = True
turno = 'n'
cimitero = (-1, -1)
print("Turno nero")

def cattura_angoli(pos, lista, stato):
	if pos == (0 , 2):
		for pos in lista:
			if pos==(0 , 1):
				stato[lista.index(pos)] = 'm'
	if pos == (0 , 6):
		for pos in lista:
			if pos==(0 , 7):
				stato[lista.index(pos)] = 'm'
	if pos == (2 , 0):
		for pos in lista:
			if pos==(1 , 0):
				stato[lista.index(pos)] = 'm'
	if pos == (2 , 8):
		for pos in lista:
			if pos==(1 , 8):
				stato[lista.index(pos)] = 'm'
	if pos == (6 , 0):
		for pos in lista:
			if pos==(7 , 0):
				stato[lista.index(pos)] = 'm'
	if pos == (6 , 8):
		for pos in lista:
			if pos==(7 , 8):
				stato[lista.index(pos)] = 'm'
	if pos == (8 , 2):
		for pos in lista:
			if pos==(8 , 1):
				stato[lista.index(pos)] = 'm'
	if pos == (8 , 6):
		for pos in lista:
			if pos==(8 , 7):
				stato[lista.index(pos)] = 'm'
	if posizione_bianchi[0] != (4,4):
		if pos == (4,2):
			for pos in lista:
				if pos == (4,3):
					stato[lista.index(pos)] = 'm'
		if pos == (2,4):
			for pos in lista:
				if pos == (3,4):
					stato[lista.index(pos)] = 'm'
		if pos == (6,4):
			for pos in lista:
				if pos == (5,4):
					stato[lista.index(pos)] = 'm'
		if pos == (4,6):
			for pos in lista:
				if pos == (4,5):
					stato[lista.index(pos)] = 'm'
	return  stato

in_esecuzione = True
while in_esecuzione:
	#Handling input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			in_esecuzione = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if turno == 'b':
				#PER IL BIANCO
				#vittoria nera
				vittoria_nero = 0
				#definisco il re che se no è troppo lunga
				re = posizione_bianchi[0]
				#se è su un lato
				if (re[0] == 0) or (re[0] == 8) or (re[1] == 0) or (re[1] == 8):
					vittoria_nero += 1
				#se è vicino ad una casella casella nera
				if (re[0]==0 and (re[1] == dim or re[1] == 7)) or (re[0]==8 and (re[1] == dim or re[1] == 7)):
					vittoria_nero += 1
				if (re[1]==0 and (re[0] == dim or re[0] == 7)) or (re[1]==8 and (re[0] == dim or re[0] == 7)):
					vittoria_nero += 1
				for pos_nero in posizione_neri:
					if re[0] == pos_nero[0] and ((re[1] == pos_nero[1] - 1) or (re[1] == pos_nero[1] + 1)):
						vittoria_nero += 1
					if re[1] == pos_nero[1] and ((re[0] == pos_nero[0] - 1) or (re[0] == pos_nero[0] + 1)):
						vittoria_nero += 1
				if vittoria_nero == 4:
					print("Vittoria nera")
					valhalla.play()
					turno = 'f'

				if tocco == 0:
					punt_0 = pygame.mouse.get_pos()
				#controllo abbia preso un pezzo valido
				#devo aggiungere il turno poi
					punt_0 = ((punt_0[0]//dim)) , ((punt_0[1]//dim))
					for pos_bianco in posizione_bianchi:
						if pos_bianco == punt_0:
							#trovo la posizione dell'oggetto toccato
							muovi_bianco = posizione_bianchi.index(pos_bianco)
							tocco = 1
							break
				if tocco == 1:
					punt_1 = pygame.mouse.get_pos()
					punt_1 = ((punt_1[0]//dim)) , ((punt_1[1]//dim))
					#non su un altro pezzo bianco
					for pos_bianco in posizione_bianchi:
						if pos_bianco == punt_1:
							legale_bianco = False
							punt_0 = punt_1
							muovi_bianco = posizione_bianchi.index(pos_bianco)
					#non su un pezzo nero
					for pos_nero in posizione_neri:
						if pos_nero == punt_1:
							legale_bianco = False
					#non negli angoli
					if ((punt_1==(0,0) or punt_1==(0,8) or punt_1==(8,0) or punt_1==(8,8) or punt_1==(4,4)) and muovi_bianco != 0):
						legale_bianco = False
					#non in diagonale
					if not (((punt_0[0] != punt_1[0]) and (punt_0[1] == punt_1[1])) or ((punt_0[1] != punt_1[1]) and (punt_0[0] == punt_1[0]))):
						legale_bianco = False
						#non trapassare
						#va bene non ho idea di come farlo
					#############################
						#non trapassare nero
					var_0 = 0
					var_1 = 1
					if punt_0[0] == punt_1[0]:
						var_0 = 0
						var_1 = 1
					else:
						var_0 = 1
						var_1 = 0
					#non trapasso i bianchi
					for pos_bianco in posizione_bianchi:
						#se sono sulla stessa riga o colonna
						if pos_bianco[var_0] == punt_0[var_0]:
							if punt_0[var_1] > punt_1[var_1]:
								if pos_bianco[var_1] > punt_1[var_1] and pos_bianco[var_1] < punt_0[var_1]:
									legale_bianco = False
							if punt_0[var_1] < punt_1[var_1]:
								if pos_bianco[var_1] < punt_1[var_1] and pos_bianco[var_1] > punt_0[var_1]:
									legale_bianco = False
					#non trapasso i pezzi_neri
					#non rinomino per velocità
					for pos_bianco in posizione_neri:
						#se sono sulla stessa riga o colonna
						if pos_bianco[var_0] == punt_0[var_0]:
							if punt_0[var_1] > punt_1[var_1]:
								if pos_bianco[var_1] > punt_1[var_1] and pos_bianco[var_1] < punt_0[var_1]:
									legale_bianco = False
							if punt_0[var_1] < punt_1[var_1]:
								if pos_bianco[var_1] < punt_1[var_1] and pos_bianco[var_1] > punt_0[var_1]:
									legale_bianco = False
					#se lo spostamento è legale sposto e mangio
					if legale_bianco:
							posizione_bianchi[muovi_bianco] = punt_1
							tocco = 0
							turno = 'n'
							print("Turno nero")
							#escludo il re che non può mangiare
							stato_neri = cattura_angoli(punt_1,posizione_neri,stato_neri)
							for pos_bianco in posizione_bianchi[1:]:
								#se sulla colonna giù di due
								if pos_bianco[0] == punt_1[0] and pos_bianco[1] + 2 == punt_1[1]:
									for pos_nero in posizione_neri:
										if pos_nero[0] == punt_1[0] and pos_nero[1] + 1 == punt_1[1]:
											stato_neri[posizione_neri.index(pos_nero)] = 'm'
											posizione_neri[posizione_neri.index(pos_nero)] = cimitero
								#se sulla colonna su di due
								if pos_bianco[0] == punt_1[0] and pos_bianco[1] - 2 == punt_1[1]:
									for pos_nero in posizione_neri:
										if pos_nero[0] == punt_1[0] and pos_nero[1] - 1 == punt_1[1]:
											stato_neri[posizione_neri.index(pos_nero)] = 'm'
											posizione_neri[posizione_neri.index(pos_nero)] = cimitero
								#se sulla riga a destra di due
								if pos_bianco[1] == punt_1[1] and pos_bianco[0] + 2 == punt_1[0]:
									for pos_nero in posizione_neri:
										if pos_nero[1] == punt_1[1] and pos_nero[0] + 1 == punt_1[0]:
											stato_neri[posizione_neri.index(pos_nero)] = 'm'
											posizione_neri[posizione_neri.index(pos_nero)] = cimitero
								#se sulla riga a sinistra di due
								if pos_bianco[1] == punt_1[1] and pos_bianco[0] - 2 == punt_1[0]:
									for pos_nero in posizione_neri:
										if pos_nero[1] == punt_1[1] and pos_nero[0] - 1 == punt_1[0]:
											stato_neri[posizione_neri.index(pos_nero)] = 'm'
											posizione_neri[posizione_neri.index(pos_nero)] = cimitero
				legale_bianco = True #se era falso lo riporto a vero
			#PER IL NERO
			if turno == 'n':
				#PER IL NERO
				#vittoria bianca
				re = posizione_bianchi[0]
				if ((re==(0,0) or re==(0,8) or re==(8,0) or re==(8,8)) and muovi_bianco == 0):
					print("Vittoria bianca")
					valhalla.play()
					turno = 'f'
				if tocco == 0:
					punt_0 = pygame.mouse.get_pos()
				#controllo abbia preso un pezzo valido
					punt_0 = ((punt_0[0]//dim)) , ((punt_0[1]//dim))
					for pos_nero in posizione_neri:
						if pos_nero == punt_0:
							#trovo la posizione dell'oggetto toccato
							muovi_nero = posizione_neri.index(pos_nero)
							tocco = 1
							break
				if tocco == 1:
					punt_1 = pygame.mouse.get_pos()
					punt_1 = ((punt_1[0]//dim)) , ((punt_1[1]//dim))
					#non su un altro pezzo nero
					for pos_nero in posizione_neri:
						if pos_nero == punt_1:
							legale_nero = False
							punt_0 = punt_1
							muovi_nero = posizione_neri.index(pos_nero)
					#non su un pezzo bianco
					for pos_bianco in posizione_bianchi:
						if pos_bianco == punt_1:
							legale_nero = False
					#non negli angoli
					if ((punt_1==(0,0) or punt_1==(0,8) or punt_1==(8,0) or punt_1==(8,8) or punt_1==(4,4))):
						legale_nero = False
					#non in diagonale
					if not (((punt_0[0] != punt_1[0]) and (punt_0[1] == punt_1[1])) or ((punt_0[1] != punt_1[1]) and (punt_0[0] == punt_1[0]))):
						legale_nero = False
						#non trapassare nero
					var_0 = 0
					var_1 = 1
					if punt_0[0] == punt_1[0]:
						var_0 = 0
						var_1 = 1
					else:
						var_0 = 1
						var_1 = 0
					#non trapasso i bianchi
					for pos_bianco in posizione_bianchi:
						#se sono sulla stessa riga o colonna
						if pos_bianco[var_0] == punt_0[var_0]:
							if punt_0[var_1] > punt_1[var_1]:
								if pos_bianco[var_1] > punt_1[var_1] and pos_bianco[var_1] < punt_0[var_1]:
									legale_nero = False
							if punt_0[var_1] < punt_1[var_1]:
								if pos_bianco[var_1] < punt_1[var_1] and pos_bianco[var_1] > punt_0[var_1]:
									legale_nero = False
					#non trapasso i pezzi_neri
					#non rinomino per velocità
					for pos_nero in posizione_neri:
						#se sono sulla stessa riga o colonna
						if pos_nero[var_0] == punt_0[var_0]:
							if punt_0[var_1] > punt_1[var_1]:
								if pos_nero[var_1] > punt_1[var_1] and pos_nero[var_1] < punt_0[var_1]:
									legale_nero = False
							if punt_0[var_1] < punt_1[var_1]:
								if pos_nero[var_1] < punt_1[var_1] and pos_nero[var_1] > punt_0[var_1]:
									legale_nero = False
					#se lo spostamento è legale sposto e mangio
					if legale_nero:
							posizione_neri[muovi_nero] = punt_1
							tocco = 0
							turno = 'b'
							print("Turno bianco")
							stato_bianchi = cattura_angoli(punt_1,posizione_bianchi[1:],stato_bianchi)
							stato_bianchi[0] = 'v'
							for pos_bianco in posizione_neri:
							  #se sulla colonna giù di due
							  if pos_bianco[0] == punt_1[0] and pos_bianco[1] + 2 == punt_1[1]:
							    for pos_nero in posizione_bianchi:
							      if pos_nero[0] == punt_1[0] and pos_nero[1] + 1 == punt_1[1] and posizione_bianchi.index(pos_nero) != 0:
							        stato_bianchi[posizione_bianchi.index(pos_nero)] = 'm'
							        posizione_bianchi[posizione_bianchi.index(pos_nero)] = cimitero
							  #se sulla colonna su di due
							  if pos_bianco[0] == punt_1[0] and pos_bianco[1] - 2 == punt_1[1]:
							    for pos_nero in posizione_bianchi:
							      if pos_nero[0] == punt_1[0] and pos_nero[1] - 1 == punt_1[1] and posizione_bianchi.index(pos_nero) != 0:
							        stato_bianchi[posizione_bianchi.index(pos_nero)] = 'm'
							        posizione_bianchi[posizione_bianchi.index(pos_nero)] = cimitero
							  #se sulla riga a destra di due
							  if pos_bianco[1] == punt_1[1] and pos_bianco[0] + 2 == punt_1[0]:
							    for pos_nero in posizione_bianchi:
							      if pos_nero[1] == punt_1[1] and pos_nero[0] + 1 == punt_1[0] and posizione_bianchi.index(pos_nero) != 0:
							        stato_bianchi[posizione_bianchi.index(pos_nero)] = 'm'
							        posizione_bianchi[posizione_bianchi.index(pos_nero)] = cimitero
							  #se sulla riga a sinistra di due
							  if pos_bianco[1] == punt_1[1] and pos_bianco[0] - 2 == punt_1[0]:
							    for pos_nero in posizione_bianchi:
							      if pos_nero[1] == punt_1[1] and pos_nero[0] - 1 == punt_1[0] and posizione_bianchi.index(pos_nero) != 0:
							        stato_bianchi[posizione_bianchi.index(pos_nero)] = 'm'
							        posizione_bianchi[posizione_bianchi.index(pos_nero)] = cimitero
				legale_nero = True #se era falso lo riporto a vero

	schermo.fill(nero)

	for i in range(0,9):
			for k in range(0,9):
				if ((i==0 or i==8) and k==0) or ((i==0 or i==8) and k==8) or (k==4 and i==4):
					schermo.blit(c_salva ,(i*dim,k*dim))
				elif (i+k)%2==0:
					schermo.blit(c_nera  ,(i*dim,k*dim))
				else:
					schermo.blit(c_bianca,(i*dim,k*dim))

	for i in range(len(pezzi_bianchi)):
		if stato_bianchi[i] == 'v':
			schermo.blit(pezzi_bianchi[i],(posizione_bianchi[i][0]*dim,posizione_bianchi[i][1]*dim))
	for i in range(len(pezzi_neri)):
		if stato_neri[i] == 'v':
			schermo.blit(pezzi_neri[i]   ,(   posizione_neri[i][0]*dim,   posizione_neri[i][1]*dim))

	pygame.display.update()
