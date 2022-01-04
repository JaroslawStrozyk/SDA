#!/opt/SD/env/bin/python3
import os
import sys
import subprocess



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_service():
    services = ["apache2", "postgresql", "sda"]
    outw = ("=" * 33) + '\n'
    outw = outw + ("| %16s | %10s |" % ( "Usługi", "Stan")) + '\n'
    outw = outw + ("=" * 33) + '\n'

    for se in services:
        output = subprocess.run(args=["systemctl","status", se], capture_output=True)
        output = output.stdout.decode(sys.stdout.encoding)
        result = output.find('Active: active')
        if result>=0:
           out = True
        else:
           out = False
        outw = outw + ("| %16s | %10s |" % ( se.upper(), str(out))) + '\n'
    outw = outw + ("-" * 33) + '\n'
    return outw


def konwert_li(lis):
    lista = lis.split('\n')
    i = 0
    for list in lista:
        if list=='':
           del lista[i]
        i += 1

    li = {}
    for r in lista:
        row   = r.split('==')
        klucz = row[0]
        wartosc = row[1]
        li[klucz] = wartosc
    return li


def test_modules():
    f = open(os.path.join(BASE_DIR, 'requirements.txt'), "r")
    da = f.read()
    f.close()
    lista = konwert_li(da)

    kom = subprocess.run(["which", "pip3"], capture_output=True)
    kom = kom.stdout.decode('utf-8').split('\n')[0]
    output = subprocess.run(args=[kom,"freeze"], capture_output=True)
    output = output.stdout.decode(sys.stdout.encoding)
    listaw = konwert_li(output)

    tst = subprocess.run(["which", "pip3"], capture_output=True)
    link = str(tst.stdout)

    out = ''
    if lista==listaw:
       out = out + ("=" * 82) + '\n'
       out = out + ("| %16s | %10s | %46s |" % ( "PIP3 moduły", str(True), link)) + '\n'
       out = out + ("=" * 82) + '\n'
    else:
       out = out + ("=" * 82) + '\n'
       out = out + ("| %16s | %10s | %46s |" % ( "PIP3 moduły", str(False), link))+'\n'
       out = out + ("=" * 82) + '\n'
       out = out + ("| %36s | %18s | %18s |" % ("MODUŁ", "JEST", "POWINNO BYĆ"))+'\n'
       out = out + ("=" * 82) + '\n'

       dt1 = len(lista)
       dt2 = len(listaw)
       if dt1 == dt2:
          for kl in lista:
              if lista[kl] != listaw[kl]:
                 out = out + ("| %36s | %18s | %18s |" % ( kl, listaw[kl], lista[kl]))+'\n'

       if dt1 < dt2:
          for kl in listaw:
              try:
                 l1 = lista[kl]
              except KeyError:
                 l1 = ''
              l2 = listaw[kl]
              if l1 != listaw[kl]:
                 out = out + ("| %36s | %18s | %18s |" % ( kl, listaw[kl], l1))+'\n'

       if dt1 > dt2:
          for kl in lista:
              try:
                 l2 = listaw[kl]
              except KeyError:
                 l2 = ''
              l1 = lista[kl]
              if l2 != lista[kl]:
                 out = out + ("| %36s | %18s | %18s |" % ( kl, l2, lista[kl]))+'\n'

       out = out + ("=" * 82) + '\n'

    return out





print(test_service())
print(test_modules())


