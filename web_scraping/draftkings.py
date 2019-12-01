import pandas as pd
from time import sleep
from random import randint

f = open('teams.txt', 'w+')

class DNA:
    def __init__(self, iter, child=False, genes=None):
        self.team_excluded = ['David Johnson', 'Evan Engram', 'Darren Waller']
        self.flex_excluded = []
        self.TEAM = {}
        self.iterations = iter
        self.init_search_gene = []
        self.optimize_pos_gene = []
        self.optimize_search_gene = []
        self.fitness = 0
        self.sal_weight = 2
        self.pt_weight = 1
        self.chance_start = 0
        self.chance_end = 0

        self.initial_search = ['pts', 'value', 'sal']
        self.optimize_search = ['pts', 'value']
        self.optimize_pos = ['QB1', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE1', 'DST', 'FLEX']
        self.optimize_dicts = [QB, RB, RB, WR, WR, WR, TE, DST, FLEX]


        if not child:
            for i in range(6):
                self.init_search_gene.append(randint(0, 1))

            for i in range(self.iterations):
                self.optimize_pos_gene.append(randint(0, 8))
                self.optimize_search_gene.append(randint(0, 1))

            self.genes = {'initial_search': self.init_search_gene, 'optpos': self.optimize_pos_gene, 'optsearch': self.optimize_search_gene}
        
        else:
            self.genes = genes

    def printGenes(self):
        pos = ['QB', 'RB', 'WR', 'TE', 'DST', 'FLEX']
        count = 0
        for k, v in self.genes.items():
            if count == 0:
                print("Initial Team: ")
                for c, i in enumerate(v):
                    print('{} for {}'.format(pos[c], self.initial_search[i]))

            elif count == 1:
                print("\nOptimization: ")
                for c, i in enumerate(v):
                    print('{} optimization for {}'.format(self.optimize_pos[i], self.optimize_search[self.genes['optsearch'][c]]))
                break
            count += 1



    def calcFitness(self, gen):
        self.TEAM, self.team_excluded, self.flex_excluded = makeTeam(self.initial_search[self.genes['initial_search'][0]], self.initial_search[self.genes['initial_search'][1]], self.initial_search[self.genes['initial_search'][2]], self.initial_search[self.genes['initial_search'][3]], self.initial_search[self.genes['initial_search'][4]], self.initial_search[self.genes['initial_search'][5]], self.team_excluded, self.flex_excluded)
        
        for i in range(self.iterations):
            self.TEAM, self.team_excluded, self.flex_excluded = optimize(self.TEAM, self.optimize_dicts[self.genes['optpos'][i]], self.optimize_pos[self.genes['optpos'][i]], self.optimize_search[self.genes['optsearch'][i]], self.team_excluded, self.flex_excluded)

        sal, pts = calcStats(self.TEAM)
        self.fitness = (pts * self.pt_weight) * ((1/(sal/50000)) * self.sal_weight)
        self.fitness -= (abs(sal-50000))/100

        if sal > 50000:
            self.fitness -= 15

        else:
            self.fitness += 10

        return self.fitness

    def mutate(self, mrate):
        if randint(0, 100) < mrate * 100:
            r = ['initial_search', 'optpos', 'optsearch']
            rindex = r[randint(0, 2)]
            self.genes[rindex][randint(0, len(self.genes[rindex])-1)] = randint(0, 1)


    
class Population:
    def __init__(self, iter, popmax, mutation_rate):
        self.popnum = popmax
        self.mrate = mutation_rate
        self.iterations = iter
        self.total_fitness = 0
        self.maxfit = 0
        self.generation = 1
        self.pool = []

        self.population = []

        for i in range(self.popnum):
            self.population.append(DNA(self.iterations))

    def calcFitness(self):
        self.maxfit = 0
        minfit = 99999999
        worst = None
        totalfit = 0
        self.best = None

        for dna in self.population:
            fts = dna.calcFitness(self.generation)
            totalfit += fts
            if fts > self.maxfit:
                self.maxfit = fts
                self.best = dna

            if fts < minfit:
                worst = dna
                minfit = fts

        print('Generation: {}'.format(self.generation))

        if evenmorestats:
            print('\nAverage Fitness: {}'.format(totalfit/len(self.population)))

        sal, pts = calcStats(self.best.TEAM)
        if bestteams:
            if sal <= 50000 and pts > 161.5:
                f.write("\nBest Team for Generation {}(Fitness: {}): ".format(self.generation, self.maxfit))
                print("\nBest Team for Generation {}(Fitness: {}): \n".format(self.generation, self.maxfit))
                printTeam(self.best.TEAM)
                print()
                f.write('\n')
                if extrastats:
                    self.best.printGenes()
        else:
            f.write("\nBest Team for Generation {}(Fitness: {}): ".format(self.generation, self.maxfit))
            print("\nBest Team for Generation {}(Fitness: {}): \n".format(self.generation, self.maxfit))
            printTeam(self.best.TEAM)
            print()
            f.write('\n')
            if extrastats:
                self.best.printGenes()

        if evenmorestats:
            print("\nWorst Team for Generation {}(Fitness: {}): ".format(self.generation, minfit))
            printTeam(worst.TEAM)
            worst.printGenes()
        


    def select(self):
        self.pool = []
        for dna in self.population:
            for i in range(int((dna.fitness/self.maxfit)*100)):
                self.pool.append(dna)

    def reproduce(self):
        new_population = []
        new_population.append(self.best)

        for i in range(self.popnum-1):
            new_genes = {'initial_search': [], 'optpos': [], 'optsearch': []}
            p1 = self.pool[randint(0, len(self.pool))-1]
            p2 = self.pool[randint(0, len(self.pool))-1]

            i_s_mid = int(len(p1.genes['initial_search'])/2)
            new_genes['initial_search'].extend(p1.genes['initial_search'][:i_s_mid])
            new_genes['initial_search'].extend(p2.genes['initial_search'][i_s_mid:])

            o_p_mid = int(len(p1.genes['optpos'])/2)
            new_genes['optpos'].extend(p1.genes['optpos'][:o_p_mid])
            new_genes['optpos'].extend(p2.genes['optpos'][:o_p_mid])

            o_s_mid = int(len(p1.genes['optsearch'])/2)
            new_genes['optsearch'].extend(p1.genes['optsearch'][:o_s_mid])
            new_genes['optsearch'].extend(p2.genes['optsearch'][:o_s_mid])

            child = DNA(self.iterations, child=True, genes=new_genes)
            child.mutate(self.mrate)
            new_population.append(child)

        self.population = new_population
        self.generation += 1



def calcStats(dictionary):
    tsal = 0
    tpts = 0
    for k, v in dictionary.items():
        tsal += v['stats']['sal']
        tpts += v['stats']['pts']

    return tsal, tpts

def printTeam(dictionary):
    tsal = 0
    tpts = 0
    for k, v in dictionary.items():
        f.write('{} - {}: Points - {}, Sal - {}, Value - {}\n'.format(k, v['name'], v['stats']['pts'], v['stats']['sal'], v['stats']['value']))
        print('{} - {}: Points - {}, Sal - {}, Value - {}'.format(k, v['name'], v['stats']['pts'], v['stats']['sal'], v['stats']['value']))
        tsal += v['stats']['sal']
        tpts += v['stats']['pts']

    f.write('Total Points: {}\n'.format(tpts))
    f.write('Total Salary: {}\n'.format(tsal))

    print('Total Points: {}'.format(tpts))
    print('Total Salary: {}'.format(tsal))

    return tsal

sals = pd.read_csv('DKSalaries.csv')
print(sals.head())

search = 'pts'

slp = False
prt = False
extrastats = True
evenmorestats = False
bestteams = True

QB = {}
RB = {}
WR = {}
DST = {}
TE = {}

flex_excluded = []
team_excluded = ['Evan Engram']

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

iteration = 0


for index, row in sals.iterrows():
    execute_string = row['Position'] + '["' + row['Name'] + "\"] = {'sal': " + str(row['Salary']) +", 'pts': " + str(row['AvgPointsPerGame']) + ", 'value': " + str(row['AvgPointsPerGame']/row['Salary'] * 1000)+ "}"
    exec(execute_string)

FLEX = {**TE, **RB, **WR}

# print(QB)
# print(RB)
# print(WR)
# print(DST)
# print(TE)


def makeTeam(qbsearch, rbsearch, wrsearch, dstsearch, tesearch, flexsearch, texlcuded, fexcluded):
    global iteration, lastsal
    team_excluded = texlcuded
    flex_excluded = fexcluded
    TEAM = {}

    temp = []
    for k, v in QB.items():
        if k not in team_excluded:
            temp.append(v[qbsearch])

    temp.sort()

    for k, v in QB.items():
        if v[qbsearch] == temp[-1]:
            TEAM['QB1'] = {'stats' : v, 'name': k}
            break


    temp = []
    for k, v in RB.items():
        if k not in team_excluded:
            temp.append(v[rbsearch])

    temp.sort()
    breakct = 0
    for k, v in RB.items():
        if v[rbsearch] == temp[-1]:
            breakct += 1
            flex_excluded.append(k)
            TEAM['RB1'] = {'stats' : v, 'name': k}

        if v[rbsearch] == temp[-2]:
            breakct += 1
            TEAM['RB2'] = {'stats' : v, 'name': k}
            flex_excluded.append(k)
            
        
        if breakct >= rb_count:
            break


    temp = []
    for k, v in WR.items():
        if k not in team_excluded:
            temp.append(v[wrsearch])

    temp.sort()

    breakct = 0
    for k, v in WR.items():
        if v[wrsearch] == temp[-1]:
            breakct += 1
            flex_excluded.append(k)
            TEAM['WR1'] = {'stats' : v, 'name': k}

        if v[wrsearch] == temp[-2]:
            breakct += 1
            flex_excluded.append(k)
            TEAM['WR2'] = {'stats' : v, 'name': k}

        if v[wrsearch] == temp[-3]:
            breakct += 1
            flex_excluded.append(k)
            TEAM['WR3'] = {'stats' : v, 'name': k}

        if breakct >= wr_count:
            break

    temp = []
    for k, v in TE.items():
        if k not in team_excluded:
            temp.append(v[tesearch])

    temp.sort()

    for k, v in TE.items():
        if v[tesearch] == temp[-1]:
            TEAM['TE1'] = {'stats' : v, 'name': k}
            flex_excluded.append(k)
            break

    temp = []
    for k, v in DST.items():
        if k not in team_excluded:
            temp.append(v[dstsearch])

    temp.sort()

    for k, v in DST.items():
        if v[dstsearch] == temp[-1]:
            TEAM['DST'] = {'stats' : v, 'name': k}
            break


    temp = []
    for k, v in FLEX.items():
        if not k in flex_excluded:
            if k not in team_excluded:
                temp.append(v[flexsearch])

    temp.sort()

    for k, v in FLEX.items():
        if v[flexsearch] == temp[-1]:
            TEAM['FLEX'] = {'stats' : v, 'name': k}
            flex_excluded.append(k)
            break

    iteration = 1

    for k, v in TEAM.items():
        team_excluded.append(v['name'])

    if prt:
        print('ITERATION {}: '.format(iteration))
        printTeam(TEAM)
    lastsal, pts = calcStats(TEAM)

    return TEAM, team_excluded, flex_excluded


def optimize(starting_dict, pos_dict, pos_name, stat, teamexcluded, flexexcluded):
    global iteration, lastsal
    TEAM = starting_dict
    temp = []
    team_excluded = teamexcluded
    flex_excluded = flexexcluded

    for k, v in pos_dict.items():
        if not k in team_excluded and not v['sal'] > TEAM[pos_name]['stats']['sal']:
            temp.append(v[stat])

    temp.sort()
    try:
        for k, v in pos_dict.items():
            if v[stat] == temp[-1]:
                lastplayer = TEAM[pos_name]
                tname = k
                TEAM[pos_name] = {'stats': v, 'name': k}

        iteration += 1
        # print('\nITERATION {}: {} Optimization'.format(iteration, pos_name))
        # sal = printTeam(TEAM)
        sal, pts = calcStats(TEAM)

        if lastsal < sal:
            if prt:
                print('REVERTED CHANGES')
            TEAM[pos_name] = lastplayer
            # print('\nITERATION {}: {} Optimization'.format(iteration, pos_name))
            # sal = printTeam(TEAM)
            sal, pts = calcStats(TEAM)


        else:
            team_excluded.append(tname)
            try:
                team_excluded.remove(lastplayer['name'])
            except:
                pass

            if 'WR' in pos_name or 'RB' in pos_name or 'TE' in pos_name:
                try:    
                    flex_excluded.append(tname)
                    flex_excluded.remove(lastplayer['name'])
                except:
                    pass
        lastsal = sal
    except:
        pass


    return TEAM, team_excluded, flex_excluded


initial_search = ['pts', 'value', 'sal']
optimize_search = ['pts', 'value']
optimize_pos = ['QB1', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE1', 'DST', 'FLEX']
optimize_dicts = [QB, RB, RB, WR, WR, WR, TE, DST, FLEX]


# TEAM = makeTeam(search, search, search, search, search, search)


# TEAM = optimize(TEAM, WR, 'WR3', 'value')
# TEAM = optimize(TEAM, DST, 'DST', 'pts')
# TEAM = optimize(TEAM, RB, 'RB1', 'value')
# TEAM = optimize(TEAM, QB, 'QB1', 'value')
# TEAM = optimize(TEAM, TE, 'TE1', 'pts')
# TEAM = optimize(TEAM, FLEX, 'FLEX', 'pts')
# TEAM = optimize(TEAM, WR, 'WR2', 'value')
# TEAM = optimize(TEAM, RB, 'RB2', 'pts')
# TEAM = optimize(TEAM, WR, 'WR1', 'value')

generations = 100
genetic_algorithm = Population(4, 250, 0.03)

for i in range(generations):
    genetic_algorithm.calcFitness()
    genetic_algorithm.select()
    genetic_algorithm.reproduce()

genetic_algorithm = Population(4, 100, 0.05)

for i in range(generations):
    genetic_algorithm.calcFitness()
    genetic_algorithm.select()
    genetic_algorithm.reproduce()

genetic_algorithm = Population(4, 100, 0.05)

for i in range(generations):
    genetic_algorithm.calcFitness()
    genetic_algorithm.select()
    genetic_algorithm.reproduce()

f.close()
