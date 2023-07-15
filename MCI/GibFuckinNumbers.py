
import collections
import datetime, dateutil.tz
import glob
import os
import sys
import csv

def supernamefuereinesupermethode(rec):
    ieinTyp = {}
    Rrrrrrgebnis = []
    skellet = []
    startTime = None
    csvName = ""
    endTime = None
    msTime = 0

    Schwelle = 0
    flag = 0 # 1 lesen, 0 blocked

    zähler = 0

    date = {}

    for line in rec.splitlines():
        if line.startswith('ts ') and startTime is None:
            startTime = datetime.datetime.strptime(line[3:]+'000', '%Y-%m-%dT%H:%M:%S.%f')
            csvName = line[3:].replace(":", "-") + ".csv"
        elif line.startswith('f '):
            msTime = int(line[2:])
            endTime = startTime + datetime.timedelta(milliseconds=msTime)
            if msTime == 0 or msTime >= Schwelle: 
                zähler +=1
                Schwelle += 250
                flag = 1
                date = {'time0': endTime}
                skellet.append(date)
                
            else: 
                flag = 0
                

        elif line.startswith('p '):
            teile = line.split(' ')
            brad = teile[1]
            if brad not in ieinTyp:
                ieinTyp[brad] = {'start: ': startTime}
            ieinTyp[brad]['ende: '] = endTime
    
        elif flag == 1:
            zeile = line.split(' ')
            if line.startswith('gro '):
                for val in zeile[1:]:
                    skellet.append(val)
                    #auffüllen mit 0 falls Werte fehlen
                    for i in range(4 - len(zeile[1:])):
                        skellet.append(0)
            if line.startswith('v '):
                for val in zeile[1:]:
                    skellet.append(val)
                    # auffüllen mit 0 falls Werte fehlen
                    for i in range(3 - len(zeile[1:])):
                        skellet.append(0)
            if line.startswith('k '):
                for val in zeile[2:]:
                    skellet.append(val)
                    # auffüllen mit 0 falls Werte fehlen
                    for i in range(3 - len(zeile[2:])):
                        skellet.append(0)

    for brad in ieinTyp:
        utcTime = ieinTyp[brad]['start: '].replace(tzinfo=dateutil.tz.gettz('UTC'))
        Rrrrrrgebnis.append(utcTime.astimezone(dateutil.tz.gettz('Europe/Berlin')))

    #print(brad, startTime, endTime)
    #print(skellet)

    print(zähler)
    list = []
    with open(csvName, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        
        filewriter.writerow(
            ['time', 'gro1', 'gro2', 'gro3', 'gro4', 'v1', 'v2', 'v3', 'k0x', 'k0y', 'k0z', 'k1x', 'k1y', 'k1z',
             'k2x', 'k2y', 'k2z', 'k3x', 'k3y', 'k3z', 'k4x', 'k4y', 'k4z', 'k5x', 'k5y', 'k5z', 'k6x', 'k6y', 'k6z',
             'k7x', 'k7y', 'k7z', 'k8x', 'k8y', 'k8z', 'k9x', 'k9y', 'k9z', 'k10x', 'k10y', 'k10z', 'k11x', 'k11y', 'k11z',
             'k12x', 'k12y', 'k12z', 'k13x', 'k13y', 'k13z', 'k14x', 'k14y', 'k14z', 'k15x', 'k15y', 'k15z', 'k16x', 'k16y', 'k6z',
             'k17x', 'k17y', 'k17z', 'k18x', 'k18y', 'k18z', 'k19x', 'k19y', 'k19z', 'k20x', 'k20y', 'k20z', 'k21x', 'k21y', 'k21z',
             'k22x', 'k22y', 'k22z', 'k23x', 'k23y', 'k23z', 'k24x', 'k24y', 'k24z', 'k25x', 'k25y', 'k25z', 'k26x', 'k26y', 'k26z',
             'k27x', 'k27y', 'k27z', 'k28x', 'k28y', 'k28z', 'k29x', 'k29y', 'k29z', 'k30x', 'k30y', 'k30z', 'k31x', 'k31y', 'k31z',
             'k32x', 'k32y', 'k32z', 'k33x', 'k33y', 'k33z'])
        
        for row in skellet:
            strrow = str(row)

            if 'datetime' in strrow and len(list) > 0:
                if len(list) == 110:
                    filewriter.writerow(list)
                list = []

            strrow = strrow.replace('{', '')
            strrow = strrow.replace("'", '')
            strrow = strrow.replace(':', '')
            strrow = strrow.replace('time0', '')
            strrow = strrow.replace('datetime.datetime(', '')
            strrow = strrow.replace(')', '')
            strrow = strrow.replace('}', '')

            list.append(strrow)

    return skellet


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
    