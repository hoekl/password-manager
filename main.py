import secrets
import string

def pw_gen(pw_length):
    password = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(pw_length)))
    return(password)

print(pw_gen(10))
