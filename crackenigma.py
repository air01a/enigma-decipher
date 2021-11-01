from enigma import Enigma
import collections
import multiprocessing
import random, string
import json
import os

REFLECTOR = 1
cipher=""

MINIOC = 0.0393
PROCESS = multiprocessing.cpu_count()
CHUNKSIZE = int(26 / PROCESS)
REST = 26 % PROCESS
LOCK = multiprocessing.Lock()
FILENAME = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))


def IOC(cipher_flat):
	N            = len(cipher_flat)
	freqs        = collections.Counter( cipher_flat )
	alphabet     =  map(chr, range( ord('A'), ord('Z')+1))
	freqsum      = 0.0

	for letter in alphabet:
		freqsum += freqs[ letter ] * ( freqs[ letter ] - 1 )

	IC = freqsum / ( N*(N-1) )
	return IC


def computeRotorsSettings(enigma,rotors,init,start,end):

        for a in range(start,end):
                for b in xrange(1,27):
                        for c in xrange(1,27):
                                settings=[a,b,c]
                                enigma.setRotors(rotors,init,settings)
                                ioc=IOC(enigma.translateText(cipher))
                                if ioc>MINIOC:
                                        print "Ioc :" + str(ioc),
                                        print rotors,
                                        print init
					print enigma.translateText(cipher)
                                        LOCK.acquire()
                                        output = open(FILENAME+"_phase2", "a")
                                        output.write(json.dumps([ioc,rotors,init])+"\n")
                                        output.close()
                                        LOCK.release()



def computeRotors(enigma,rotors,start,end):
	for a in range(start,end):
		for b in xrange(1,27):
			for c in xrange(1,27):
				init=[a,b,c]
				enigma.setRotors(rotors,init,[1,1,1])	
				ioc=IOC(enigma.translateText(cipher))
				if ioc>MINIOC:
					print "Ioc :" + str(ioc),
					print rotors,
					print init
					LOCK.acquire()
					output = open(FILENAME, "a")
					output.write(json.dumps([ioc,rotors,init])+"\n")
					output.close()
					LOCK.release()
	
	
	
	
enigmas = []

print "-----------------------------------------------"
print "Temporary File Name : %s" % FILENAME
print ""
print "Min IOC for detection : %s" % str(MINIOC)
print "Process : %i" % PROCESS
print "Text length : %i" % len(cipher)
print "Reflector : %c" % ("abc"[REFLECTOR])
print "-----------------------------------------------"
print ""

chunk= [ CHUNKSIZE for x in range(0,PROCESS) ]
for i in range(0,PROCESS):
        enigmas.append(Enigma())
        enigmas[i].setReflector(REFLECTOR)

for i in range(0,REST):
        chunk[i]+=1

rotorSwap=0
for i in xrange(1,6):
	print "Next rotor swap (%i)" % rotorSwap
	for j in xrange(1,6):
			if i!=j:
				for k in xrange(1,6):
					if k!=j and k!=i:
						rotors=[i,j,k]
						procs = []
						start=1
						for prc in range(0,PROCESS):
							proc = multiprocessing.Process(target=computeRotors, args=(enigmas[prc],rotors,start,start + chunk[prc]))
							start+=chunk[prc]
							procs.append(proc)
							proc.start()
								
						for proc in procs:
							proc.join()
						rotorSwap+=1

print "-----------------------------------------------"		
print "Finding rotors settings"
print "-----------------------------------------------"

output = open(FILENAME, "rt")
result = []
for line in output:
        result.append(json.loads(line.rstrip()))
output.close()

result.sort(reverse=True)


for res in result:
        ioc = res[0]
        rotors = res[1]
        init = res[2]

        print "-- Testing",
        print rotors,
        print " ",
        print init

        procs = []
        start=1
        for prc in range(0,PROCESS):
                proc = multiprocessing.Process(target=computeRotorsSettings, args=(enigmas[prc],rotors,init,start,start + chunk[prc]))
                start+=chunk[prc]
                procs.append(proc)
                proc.start()

        for proc in procs:
                proc.join()
                rotorSwap+=1

