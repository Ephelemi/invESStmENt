
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
    endTime = None
    msTime = 0

    Schwelle = 0
    flag = 0 # 1 lesen, 0 blocked

    zähler = 0

    date = {}

    for line in rec.splitlines():
        if line.startswith('ts ') and startTime is None:
            startTime = datetime.datetime.strptime(line[3:]+'000', '%Y-%m-%dT%H:%M:%S.%f')
        elif line.startswith('f '):
            msTime = int(line[2:])
            endTime = startTime + datetime.timedelta(milliseconds=msTime)
            if msTime == 0 or msTime >= Schwelle: 
                zähler +=1
                Schwelle += 500
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
                skellet.append(zeile[1:])
            if line.startswith('v '):
                skellet.append(zeile[1:])
            if line.startswith('k '):
                skellet.append(zeile[1:])

    for brad in ieinTyp:
        utcTime = ieinTyp[brad]['start: '].replace(tzinfo=dateutil.tz.gettz('UTC'))
        Rrrrrrgebnis.append(utcTime.astimezone(dateutil.tz.gettz('Europe/Berlin')))

    #print(brad, startTime, endTime)
    #print(skellet)

    print(zähler)
    counter = 0
    list = []
    with open('dinge_2.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';')
        for row in skellet:
            if(counter==37):
                filewriter.writerow('\n')
                filewriter.writerow(list)
                list = []
                counter = 0
            list.append(row)
            counter += 1

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
    