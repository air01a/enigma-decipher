DEBUG = False

class Rotor:
#	_rotorI      = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
	_rotorI      = [4, 10, 12, 5, 11, 6, 3, 16, 21, 25, 13, 19, 14, 22, 24, 7, 23, 20, 18, 15, 0, 8, 1, 17, 2, 9]
#	_rotorII     = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
	_rotorII      = [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4]
#	_rotorIII    = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
	_rotorIII    = [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14]
#	_rotorIV     = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
	_rotorIV     = [4, 18, 14, 21, 15, 25, 9, 0, 24, 16, 20, 8, 17, 7, 23, 11, 13, 5, 19, 6, 10, 3, 2, 12, 22, 1]
#	_rotorV      = "VZBRGITYUPSDNHLXAWMJQOFECK"
	_rotorV      = [21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10]
#	_rotorVI     = "JPGVOUMFYQBENHZRDKASXLICTW"
	_rotorVI     = [13, 25, 9, 7, 6, 17, 2, 23, 12, 24, 18, 22, 1, 14, 20, 5, 0, 8, 21, 11, 15, 4, 10, 16, 3, 19]
#	_rotorVII    = "NZJHGRCXMYSWBOUFAIVLPEKQDT"
	_rotorVII    = [13, 25, 9, 7, 6, 17, 2, 23, 12, 24, 18, 22, 1, 14, 20, 5, 0, 8, 21, 11, 15, 4, 10, 16, 3, 19]
	_alphabet    = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	
	_rotorNotches = [[17],[5],[22],[10],[26],[25,12],[25,12]]

	
	def __init__(self):
		self._rotor=[]
		self._index=0
		self._rotors=[self._rotorI,self._rotorII,self._rotorIII,self._rotorIV,self._rotorV,self._rotorVI,self._rotorVII]
		self._base=0
		self._debug=True
		self._ringSetting=0
	
	def getIndex(self):
		return (self._index+self._base) % 26
	
	def selectRotor(self,rot):
		self._rotor  = self._rotors[rot]
		self._notche = self._rotorNotches[rot]
		
	def setInitRotor(self,pos):
		self._index = pos
			
	def moveRotor(self):
		self._index += 1
		ret = False
		if self._index in self._notche:
			ret = True
		self._index %= 26
		
		return ret
	
	def setRingSettings(self,pos):
		self._ringSetting = pos
	
	def _printStep(self,beg,fin,corrected):
		if DEBUG:
			print "RA[%c -> %c => %c]" % (chr(beg+ord('A')),chr(fin+ord('A')),chr(corrected+ord('A'))),
		
	def translate(self,ind):
		ret = self._rotor[(ind+self._index-self._ringSetting)%26]
		corrected = (ret-self._index+self._ringSetting)%26
		self._printStep(ind,ret,corrected)
		return corrected
		
	def translateR(self,ind):
		ret = self._rotor.index((ind+self._index-self._ringSetting)%26)
		corrected = (ret-self._index+self._ringSetting)%26
		self._printStep(ind,ret,corrected)
		return corrected
		
class Reflector:
	#_reflectorA = "EJMZALYXVBWFCRQUONTSPIKHGD"
	_reflectorA = [4, 9, 12, 25, 0, 11, 24, 23, 21, 1, 22, 5, 2, 17, 16, 20, 14, 13, 19, 18, 15, 8, 10, 7, 6, 3]
	#_reflectorB = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
	_reflectorB = [24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19]
	#_reflectorC = "FVPJIAOYEDRZXWGCTKUQSBNMHL"
	_reflectorC = [5, 21, 15, 9, 8, 0, 14, 24, 4, 3, 17, 25, 23, 22, 6, 2, 19, 10, 20, 16, 18, 1, 13, 12, 7, 11]
	_alphabet  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	
	def __init__(self):
		self._reflector=None
	
	def set(self,ref):
		if ref==0:
			self._reflector = self._reflectorA
		elif ref==1:
			self._reflector = self._reflectorB	
		else:
			self._reflector = self._reflectorC
	
	def _printStep(self,beg,fin):
		if DEBUG:
			print "REF[%c -> %c]" % (chr(beg+ord('A')),chr(fin+ord('A'))),
	
	def translate(self,ind):
		ct = self._reflector[ind]
		self._printStep(ind,ct)
		return ct

class Rotors:		
	def __init__(self):
		self._rotor1 = Rotor()
		self._rotor2 = Rotor()
		self._rotor3 = Rotor()
		self._doubleStep = False
		
	def setRotors(self,rotors,pos,ringsettings):		
		self._rotor1.selectRotor(rotors[0]-1)
		self._rotor1.setInitRotor(pos[0]-1)
		self._rotor1.setRingSettings(ringsettings[0]-1)
		self._rotor2.selectRotor(rotors[1]-1)
		self._rotor2.setInitRotor(pos[1]-1)
		self._rotor2.setRingSettings(ringsettings[1]-1)
		self._rotor3.selectRotor(rotors[2]-1)
		self._rotor3.setInitRotor(pos[2]-1)
		self._rotor3.setRingSettings(ringsettings[2]-1)
		
	def translateA(self,char):
		if self._doubleStep:
				self._rotor1.moveRotor()
				self._rotor2.moveRotor()
				self._doubleStep=False
		
		
		if (self._rotor3.moveRotor()==True) : 
			if (self._rotor2.moveRotor()==True):
				self._doubleStep = True
				
		if DEBUG:
			print "\nRotors (%i,%i,%i)" % (self._rotor1.getIndex(),self._rotor2.getIndex(),self._rotor3.getIndex())
		ct = self._rotor1.translate(self._rotor2.translate(self._rotor3.translate(char)))
		return ct
	
	def translateB(self,char):
		ct = self._rotor3.translateR(self._rotor2.translateR(self._rotor1.translateR(char)))
		
		return ct

		
class Enigma:
	_alphabet  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

	def __init__(self):
		self._rotors = Rotors()
		self._reflector = Reflector()
		self._subst = None

	def setRotors(self,rotors,pos,ringSettings):
		self._rotors.setRotors(rotors,pos,ringSettings)
		
	def setReflector(self,ref):
		self._reflector.set(ref)
	

	def subst(self,subst):
		self._subst = subst

	def _substitute(self,ct):
		if self._subst != None:
                        if ct in self._subst.keys():
                                return self._subst[ct]
                        elif ct in self._subst.values():
                                for c in self._subst.keys():
                                        if self._subst[c] == ct:
                                                return c
		return ct

	def translate(self,char):


		ct = char.upper()
		if not ct in self._alphabet:
			return ''


		ct = self._substitute(ct)
		ct = ord(ct) - ord('A')
		ct = self._reflector.translate((self._rotors.translateA(ct)))
		ct = self._rotors.translateB(ct)
		ct = chr(ct+ord('A'))
		ct = self._substitute(ct)		
		return ct
	

	
	def translateText(self,text):
		ret = ""
		for c in text:
			ret+=self.translate(c)
		return ret
		
		
if __name__ == "__main__":
	enigma = Enigma()
	enigma.setRotors([1,2,3],[12,13,14],[1,1,8])
	enigma.subst({'A':'B','D':'E'})
	enigma.setReflector(1)
	te="Texte a chiffrer"
	print enigma.translateText(te)



