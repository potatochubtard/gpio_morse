from time import sleep
import RPi.GPIO as GPIO
import argparse

def setup(pin, mode=GPIO.BOARD):
    GPIO.setmode(mode)
    GPIO.setup(pin, GPIO.OUT)

def text2morse(word):
    data = []
    ddict = {".":0.3, "-":0.1}

    MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-'} 

    for encoding in word.upper():
        for symbol in MORSE_CODE_DICT[encoding]:
            data.append(ddict[symbol])
    
    return data

def transmitword(data, pin):
    for duration in data:
        GPIO.output(pin, GPIO.HIGH)
        sleep(duration)
        GPIO.output(pin, GPIO.LOW)
        sleep(0.01)

def main(text, pin, mode):
    setup(pin, mode)
    cipher = text.split(" ")
    for word in cipher:
        transmitword(text2morse(word), pin)
        sleep(0.03)
        
    GPIO.cleanup()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pin",  type=int, default=5)
    parser.add_argument("-d", "--data", type=str, required=True)
    parser.add_argument("-m", "--mode", type=int, choices={GPIO.BCM, GPIO.BOARD}, 
                        default=GPIO.BOARD)

    args = parser.parse_args()
    main(args.data, args.pin, args.mode)
