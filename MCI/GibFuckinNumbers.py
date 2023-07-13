
import collections
import datetime, dateutil.tz
import glob
import os
import sys

def supernamefuereinesupermethode(rec):
    ieinTyp = {}
    Rrrrrrgebnis = []
    skellet = {}
    startTime = None
    endTime = None
    msTime = 0
    blocknr= 0
    spaltennummer = 0

    Schwelle = 0
    flag = 0 # 1 lesen, 0 blocked

    for line in rec.splitlines():
        if line.startswith('ts ') and startTime is None:
            startTime = datetime.datetime.strptime(line[3:]+'000', '%Y-%m-%dT%H:%M:%S.%f')
        elif line.startswith('f '):
            msTime = int(line[2:])
            endTime = startTime + datetime.timedelta(milliseconds=msTime)
            if msTime == 0 or msTime >= Schwelle: 
                Schwelle += 500
                blocknr += 1
                flag = 1
                skellet[blocknr] = {'time': endTime}
            else: flag = 0

        elif line.startswith('p '):
            teile = line.split(' ')
            brad = teile[1]
            if brad not in ieinTyp:
                ieinTyp[brad] = {'start: ': startTime}
            ieinTyp[brad]['ende: '] = endTime
    
        elif flag == 1:
            zeile = line.split(' ')
            if line.startswith('gro '):
                skellet[blocknr][spaltennummer] = {'gro': zeile[1:]}
                spaltennummer += 1
            if line.startswith('v '):
                skellet[blocknr][spaltennummer] = {'v': zeile[1:]}
                spaltennummer += 1
            if line.startswith('k '):
                skellet[blocknr][spaltennummer] = {'k': zeile[1:]}
                spaltennummer += 1

    for brad in ieinTyp:
        utcTime = ieinTyp[brad]['start: '].replace(tzinfo=dateutil.tz.gettz('UTC'))
        Rrrrrrgebnis.append(utcTime.astimezone(dateutil.tz.gettz('Europe/Berlin')))

    #print(brad, startTime, endTime)
    print(skellet)
    return Rrrrrrgebnis

if __name__ == '__main__':
    params = sys.argv[1:]
    for param in list(params):
        if '*' in param:
            def cut_cwd(path):
                if path.startswith(os.getcwd()):
                    path = path[len(os.getcwd()):]
                return path
            matches = sorted(list(map(cut_cwd, glob.glob(param))))
            params = params[:params.index(param)] + matches + params[params.index(param)+1:]

    menschenvorkamera = []
    for param in params:
        #print('Scanning', param, '...')
        with open(param, 'r') as fp:
            datei = fp.read()
        menschenvorkamera += supernamefuereinesupermethode(datei)

