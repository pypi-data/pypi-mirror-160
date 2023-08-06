import string
import random
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
def generate_random_password(length):
	random.shuffle(characters)
	password = []
	for i in range(length):
		password.append(random.choice(characters))
	random.shuffle(password)
	print("".join(password))

def generate_random_string(length):
    res = ''.join(random.choices(string.ascii_letters, k=length))
    print("The generated random string : " + str(res))