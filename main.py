import requests
import hashlib

DIDI_URLS = [
    "http://wifi.didi.ir/login",
    "http://zne.didi.ir/login",
]

USERNAME = "test"
PASSWORD = "test"

def octal_to_hexadecimal(octal):
    result = ""
    octnum = int(octal)
    chk = 0
    i = 0
    decnum = 0
    while octnum!=0:
        rem = octnum%10
        if rem>7:
            chk = 1
            break
        decnum = decnum + (rem * (8 ** i))
        i = i+1
        octnum = int(octnum/10)

    if chk == 0:
        i = 0
        hexdecnum = []
        while decnum != 0:
            rem = decnum % 16
            if rem < 10:
                rem = rem + 48
            else:
                rem = rem + 55
            rem = chr(rem)
            hexdecnum.insert(i, rem)
            i = i + 1
            decnum = int(decnum / 16)

        i = i - 1
        while i >= 0:
            result += str(hexdecnum[i])
            i = i - 1
        return result

    else:
        print("\nInvalid Input!")


def octal_to_str(octal_str):
    str_converted = ""
    for octal_char in filter(None,octal_str.split("\\")):
        letter = chr(int(octal_char, 8))
        if letter.isprintable():
            str_converted += letter
        else:
            str_converted += r"\x" + octal_to_hexadecimal(octal_char)

    return str_converted


def createPassword(password, startHex, endHex):
    return octal_to_str(startHex) + password + octal_to_str(endHex)


def dectoOct(decimal):
    octal = 0
    ctr = 0
    temp = decimal
    while (temp > 0):
        octal += ((temp % 8) * (10 ** ctr))  # Stacking remainders
        temp = int(temp / 8)  # updating dividend
        ctr += 1
    return octal


def stringToOctal(string):
    result = ""
    for character in list(string):
        result += "\\"+ str(dectoOct(ord(character)))
    return result


def start():
    pageHtml = ""
    sendDataUrl = ""
    for URL in DIDI_URLS:
        try:
            r = requests.get(url=URL)
            pageHtml = r.text
            sendDataUrl = URL
        except:
            pass

    startSearchString = "hexMD5("
    endSearchString = ");"

    startStringIndex = pageHtml.find(startSearchString)

    if startStringIndex > 0 and len(pageHtml) > 0:
        endStringIndex = pageHtml.find(endSearchString, startStringIndex + len(startSearchString))

        passwordAllOctal = pageHtml[startStringIndex + len(startSearchString):endStringIndex].replace(
            '+ document.login.password.value +', stringToOctal(PASSWORD)).replace("'", "").replace(" ", "")

        hashedPassword = hashlib.md5(bytes([int(i, 8) for i in passwordAllOctal.split("\\")[1:]]))

        print(hashedPassword.hexdigest())

        result = requests.post(sendDataUrl, {
            'popup': True,
            'dst': "",
            "username": USERNAME,
            "password": hashedPassword.hexdigest()
        })

        print(result.text)

    else:
        print("not connected to wifi")
        return False


if __name__ == '__main__':
    start()
