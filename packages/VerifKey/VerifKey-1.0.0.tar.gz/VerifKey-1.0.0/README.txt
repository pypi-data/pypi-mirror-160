How to use ?

1. Import it to your programm using :
	import VerifKey
You can use this code to convert "verifkey" to "verifKey" :
	verifkey = VerifKey
Or :
	import VerifKey as verifkey

2. Generate a key list :
To generate a key list, you can write your own programm or use verifkey to generate a list (printed with print() and writed into "keys.txt") :
Default specs :
	Key lenght : 20 chars
	Charset : a-z A-Z 0-9
Use this command to generate a list :
	VerifKey.keyGenerator(amountOfKeysYouWant)
replace amountOfKeyYouWant by a digit (not into a string !)

3. Upload the key list. You can upload it on PasteBin, this module is compatible with every service who allow raw text.

4.If you use PasteBin, save only the "pastecode" and write this command to convert it to a link :
	link = VerifKey.getPB(pastecode)
Replace pastecode by a string and into it insert your pastecode.
NOTE : The keys are encrypted with SHA512 !

5. Get user input key :
For basics programms, you can use input() :
	key = input("Write your key here -> ")

6. Verify the key :
Use : 
	validity = VerifKey.verify(link, userkey)
Replace :
- link by your link or your pastebin generated link.
- userkey by the user's key.

7. You will got into the returned variable an boolean value :
- True : the key is correct
- False : the key is wrong


EXAMPLE PROGRAM :

import VerifKey as verifkey
pb = verifkey.getPB("mypastecodehere")
userKey = input("To use this programm, you need a product key.\nInsert it here --> ")
verify = False
while not verify:
	verify = verifkey.verify(pb, userKey)
	userKey = input("Wrong key ! Retry here --> ")
print("Correct key ! Welcome !")
#your programm
exit()
