import pandas as pd
from time import sleep


def printTeam(dictionary):
    global team_excluded
    tsal = 0
    tpts = 0
    for k, v in dictionary.items():
        print('{} - {}: Points - {}, Sal - {}, Value - {}'.format(k, v['name'], v['stats']['pts'], v['stats']['sal'], v['stats']['value']))
        tsal += v['stats']['sal']
        tpts += v['stats']['pts']

    print('Total Points: {}'.format(tpts))
    print('Total Salary: {}'.format(tsal))

    return tsal

sals = pd.read_csv('DKSalaries.csv')
print(sals.head())

search = 'pts'

slp = True

QB = {}
RB = {}
WR = {}
DST = {}
TE = {}

flex_excluded = []
team_excluded = []

TEAM = {}

totalpts = 0
totalsly = 0

breakct = 0

qb_count = 1
rb_count = 2
wr_count = 3
te_count = 1
flex_count = 1
dst_count = 1


for index, row in sals.iterrows():
    execute_string = row['Position'] + '["' + row['Name'] + "\"] = {'sal': " + str(row['Salary']) +", 'pts': " + str(row['AvgPointsPerGame']) + ", 'value': " + str(row['AvgPointsPerGame']/row['Salary'] * 1000)+ "}"
    exec(execute_string)

FLEX = {**TE, **RB, **WR}

# print(QB)
# print(RB)
# print(WR)
# print(DST)
# print(TE)

temp = []
for k, v in QB.items():
    temp.append(v[search])

temp.sort()

for k, v in QB.items():
    if v[search] == temp[-1]:
        totalpts += v['pts']
        totalsly += v['sal']
        TEAM['QB1'] = {'stats' : v, 'name': k}
        break


temp = []
for k, v in RB.items():
    temp.append(v[search])

temp.sort()
breakct = 0
for k, v in RB.items():
    if v[search] == temp[-1]:
        totalpts += v['pts']
        totalsly += v['sal']
        breakct += 1
        flex_excluded.append(k)
        TEAM['RB1'] = {'stats' : v, 'name': k}

    if v[search] == temp[-2]:
        totalpts += v['pts']
        totalsly += v['sal']
        breakct += 1
        TEAM['RB2'] = {'stats' : v, 'name': k}
        flex_excluded.append(k)
        
    
    if breakct >= rb_count:
        break


temp = []
for k, v in WR.items():
    temp.append(v[search])

temp.sort()

breakct = 0
for k, v in WR.items():
    if v[search] == temp[-1]:
        totalpts += v['pts']
        totalsly += v['sal']
        breakct += 1
        flex_excluded.append(k)
        TEAM['WR1'] = {'stats' : v, 'name': k}

    if v[search] == temp[-2]:
        totalpts += v['pts']
        totalsly += v['sal']
        breakct += 1
        flex_excluded.append(k)
        TEAM['WR2'] = {'stats' : v, 'name': k}

    if v[search] == temp[-3]:
        totalpts += v['pts']
        totalsly += v['sal']
        breakct += 1
        flex_excluded.append(k)
        TEAM['WR3'] = {'stats' : v, 'name': k}

    if breakct >= wr_count:
        break

temp = []
for k, v in TE.items():
    temp.append(v[search])

temp.sort()

for k, v in TE.items():
    if v[search] == temp[-1]:
        totalpts += v['pts']
        totalsly += v['sal']
        TEAM['TE1'] = {'stats' : v, 'name': k}
        flex_excluded.append(k)
        break

temp = []
for k, v in DST.items():
    temp.append(v[search])

temp.sort()

for k, v in DST.items():
    if v[search] == temp[-1]:
        totalpts += v['pts']
        totalsly += v['sal']
        TEAM['DST'] = {'stats' : v, 'name': k}
        break


temp = []
for k, v in FLEX.items():
    if not k in flex_excluded:
        temp.append(v['value'])

temp.sort()

for k, v in FLEX.items():
    if v['value'] == temp[-1]:
        totalpts += v['pts']
        totalsly += v['sal']
        TEAM['FLEX'] = {'stats' : v, 'name': k}
        flex_excluded.append(k)
        break

iteration = 1

for k, v in TEAM.items():
    team_excluded.append(v['name'])

print('ITERATION {}: '.format(iteration))
lastsal = printTeam(TEAM)
print(TEAM)

if slp:
    sleep(0.5)

if totalsly > 50000:


    temp = []
    for k, v in WR.items():
        if not k in team_excluded:
            temp.append(v['value'])

    temp.sort()

    for k, v in WR.items():
        if v['value'] == temp[-1]:
            lastplayer = TEAM['WR3']
            tname = k
            TEAM['WR3'] = {'stats' : v, 'name': k}

    iteration += 1
    print('\nITERATION {}: WR3 Optimization'.format(iteration))
    sal = printTeam(TEAM)


    if lastsal < sal:
        print('REVERTED CHANGES')
        TEAM['WR3'] = lastplayer

    else:
        print(k)
        team_excluded.append(tname)
        team_excluded.remove(lastplayer['name'])
        flex_excluded.append(tname)
        flex_excluded.remove(lastplayer['name'])

    lastsal = sal

    if slp:
        sleep(0.5)

    temp = []
    for k, v in DST.items():
        if not k in team_excluded and not v['sal'] > TEAM['DST']['stats']['sal']:
            temp.append(v['pts'])

    temp.sort()

    for k, v in DST.items():
        if v['pts'] == temp[-1]:
            lastplayer = TEAM['DST']
            tname = k
            TEAM['DST'] = {'stats' : v, 'name': k}

    iteration += 1
    print('\nITERATION {}: DST Optimization'.format(iteration))
    sal = printTeam(TEAM)


    if lastsal < sal:
        print('REVERTED CHANGES')
        TEAM['DST'] = lastplayer
        print('\nITERATION {}: DST Optimization'.format(iteration))
        sal = printTeam(TEAM)

    else:
        team_excluded.append(tname)
        team_excluded.remove(lastplayer['name'])

    lastsal = sal

    if slp:
        sleep(0.5)

    temp = []
    for k, v in RB.items():
        if not k in team_excluded:
            temp.append(v['value'])

    temp.sort()

    for k, v in RB.items():
        if v['value'] == temp[-1]:
            lastplayer = TEAM['RB1']
            tname = k
            TEAM['RB1'] = {'stats' : v, 'name': k}

    iteration += 1
    print('\nITERATION {}: RB1 Optimization'.format(iteration))
    sal = printTeam(TEAM)

    if lastsal < sal:
        print('REVERTING CHANGES')
        TEAM['RB1'] = lastplayer
        print('\nITERATION {}: RB1 Optimization'.format(iteration))
        sal = printTeam(TEAM)

    else:
        team_excluded.append(tname)
        team_excluded.remove(lastplayer['name'])
        flex_excluded.append(tname)
        flex_excluded.remove(lastplayer['name'])

    lastsal = sal

    if slp:
        sleep(0.5)

    temp = []
    for k, v in QB.items():
        if not k in team_excluded:
            temp.append(v['value'])

    temp.sort()

    for k, v in QB.items():
        if v['value'] == temp[-1]:
            tname = k
            lastplayer = TEAM['QB1']
            TEAM['QB1'] = {'stats' : v, 'name': k}

    iteration += 1
    print('\nITERATION {}: QB Optimization'.format(iteration))
    sal = printTeam(TEAM)


    if lastsal < sal:
        print('REVERTED CHANGES')
        TEAM['QB1'] = lastplayer
        print('\nITERATION {}: QB Optimization'.format(iteration))
        sal = printTeam(TEAM)

    else:
        team_excluded.append(tname)
        team_excluded.remove(lastplayer['name'])

    lastsal = sal

    if slp:
        sleep(0.5)

    temp = []
    for k, v in TE.items():
        if not k in team_excluded:
            temp.append(v['value'])

    temp.sort()

    for k, v in TE.items():
        if v['value'] == temp[-1]:
            tname = k
            lastplayer = TEAM['TE1']
            TEAM['TE1'] = {'stats' : v, 'name': k}

    iteration += 1
    print('\nITERATION {}: TE1 Optimization'.format(iteration))
    sal = printTeam(TEAM)


    if lastsal < sal:
        print('REVERTING CHANGES')
        TEAM['TE1'] = lastplayer
        print('\nITERATION {}: TE1 Optimization'.format(iteration))
        sal = printTeam(TEAM)

    else:
        team_excluded.append(tname)
        team_excluded.remove(lastplayer['name'])
        flex_excluded.append(tname)
        flex_excluded.remove(lastplayer['name'])

    if slp:
        sleep(0.5)

    lastsal = sal

    temp = []
    
    for k, v in FLEX.items():
        if not k in team_excluded:
            temp.append(v['value'])

    temp.sort()
    

    for k, v in FLEX.items():
        if v['value'] == temp[-1]:
            tname = k
            lastplayer = TEAM['FLEX']
            TEAM['FLEX'] = {'stats' : v, 'name': k}

    iteration += 1
    print('\nITERATION {}: FLEX Optimization'.format(iteration))
    sal = printTeam(TEAM)

    if lastsal < sal:
        print('REVERTED CHANGES')
        TEAM['FLEX'] = lastplayer
        print('\nITERATION {}: FLEX Optimization'.format(iteration))
        sal = printTeam(TEAM)

    else:
        team_excluded.append(tname)
        team_excluded.remove(lastplayer['name'])
        flex_excluded.append(tname)
        flex_excluded.remove(lastplayer['name'])

    lastsal = sal
    
    if slp:
        sleep(0.5)

    temp = []
    for k, v in WR.items():
        if not k in team_excluded:
            temp.append(v['value'])

    temp.sort()

    for k, v in WR.items():
        if v['value'] == temp[-1]:
            lastplayer = TEAM['WR2']
            tname = k
            TEAM['WR2'] = {'stats' : v, 'name': k}

    iteration += 1
    print('\nITERATION {}: WR2 Optimization'.format(iteration))
    sal = printTeam(TEAM)

    if lastsal < sal:
        print('REVERTING CHANGES')
        TEAM['WR2'] = lastplayer
        print('\nITERATION {}: WR2 Optimization'.format(iteration))
        sal = printTeam(TEAM)

    else:
        team_excluded.append(tname)
        team_excluded.remove(lastplayer['name'])
        flex_excluded.append(tname)
        flex_excluded.remove(lastplayer['name'])

    lastsal = sal

    if slp:
        sleep(0.5)

    if not TEAM['RB2']['stats']['value'] > 3.1:
        temp = []
        for k, v in RB.items():
            if not k in team_excluded:
                temp.append(v['value'])

        temp.sort()

        for k, v in RB.items():
            if v['value'] == temp[-1]:
                tname = k
                lastplayer = TEAM['RB2']
                TEAM['RB2'] = {'stats' : v, 'name': k}

        iteration += 1
        print('\nITERATION {}: RB2 Optimization'.format(iteration))
        sal = printTeam(TEAM)


        if lastsal < sal:
            print('REVERTING CHANGES')
            TEAM['RB2'] = lastplayer
            print('\nITERATION {}: RB2 Optimization'.format(iteration))
            sal = printTeam(TEAM)

        else:
            team_excluded.append(tname)
            team_excluded.remove(lastplayer['name'])
            flex_excluded.append(tname)
            flex_excluded.remove(lastplayer['name'])


    lastsal = sal

    if slp:
        sleep(0.5)

    temp = []
    for k, v in WR.items():
        if not k in team_excluded:
            temp.append(v['value'])

    temp.sort()

    for k, v in WR.items():
        if v['value'] == temp[-1]:
            lastplayer = TEAM['WR1']
            tname = k
            TEAM['WR1'] = {'stats' : v, 'name': k}

    iteration += 1
    print('\nITERATION {}: WR1 Optimization'.format(iteration))
    sal = printTeam(TEAM)

    if lastsal < sal:
        print('REVERTING CHANGES')
        TEAM['WR1'] = lastplayer
        print('\nITERATION {}: WR1 Optimization'.format(iteration))
        sal = printTeam(TEAM)

    else:
        team_excluded.append(tname)
        team_excluded.remove(lastplayer['name'])
        flex_excluded.append(tname)
        flex_excluded.remove(lastplayer['name'])

    if slp:
        sleep(0.5)
