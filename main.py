import random

def pw_gen(pw_length):
    char_choices = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']
    pw = random.choices(char_choices, k=pw_length)
    pw = ''.join(pw)
    return(pw)
pw_length = input("Specify the length of the password to generate: ")
print(pw_gen(int(pw_length)))

