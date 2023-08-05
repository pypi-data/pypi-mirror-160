def isprime(x):
    divisores= []
    for loop in range(2, x):
        if x%i ==0:
            return False
        i=i+1
    return True
#################################################################
#################################################################
def isamstrong(x):
    digitos = [int(d) for d in str(x)]
    intdigitos = [int(f) for f in digitos]
    pot = len(intdigitos)
    i = 0
    resultado = 0
    for i in range (pot):
        comprobacion = pow(intdigitos[i], pot)
        i=i+1
        resultado = resultado+comprobacion
    if resultado == x:
        return True
    else:
        return False
#################################################################
#################################################################
def ispair(x):
    if x%2 ==0:
        return True
    else:
        return False
#################################################################
#################################################################
def factorial(x):
    factorial = 1
    while x > 1:
        fac = x*x-1
        factorial= factorial*fac
        x = x-2
    return factorial
#################################################################
#################################################################
def tobinary(x):
    binary = 0
    i = 0
    while (x>0):
        digit = x%2
        x = int(x//2)
        binary = binary+digit*(10**i)
        i = i+1
    return binary
#################################################################
#################################################################
def tohexadecimal(x):
    hexadecimal = ''
    while x >0:
        rest = x%16
        x=x//16
        strrest = str(rest)
        if rest == 10:
            hexadecimal = hexadecimal+'A'
        elif rest == 11:
            hexadecimal = hexadecimal+'B'
        elif rest == 12:
            hexadecimal = hexadecimal+'C'
        elif rest == 13:
            hexadecimal = hexadecimal+'D'
        elif rest == 14:
            hexadecimal = hexadecimal+'E'
        elif rest == 15:
            hexadecimal = hexadecimal+'F'
        else:
            hexadecimal = hexadecimal+strrest
    hexadecimal = ''.join(reversed(hexadecimal))
    return hexadecimal
#################################################################
#################################################################
