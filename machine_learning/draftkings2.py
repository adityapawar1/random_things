import pandas as pd
from time import sleep
from random import randint

class DNA:
    def __init__(self, child=False, genes=None):
        self.team_included = {} # {'RB1' : 'Leonard Fournette', 'QB1' : 'Patrick Mahomes'}
        self.TEAM = {}
        self.fitness = 0
        self.sal_weight = 1
        self.pt_weight = 2

        if not child:
            self.genes = []

            for i in range(9):
                if i == 0:
                    gene = randint(0, len(QB) - 1)
                elif i <= 2:
                    gene = randint(0, len(RB) - 1)
                elif i <= 5:
                    gene = randint(0, len(WR) - 1)
                elif i == 6:
                    gene = randint(0, len(TE) - 1)
                elif i == 7:
                    gene = randint(0, len(DST) - 1)
                else:
                    gene = randint(0, len(FLEX) - 1)

                self.genes.append(gene)
        
        else:
            self.genes = genes
        
        self.TEAM = makeTeam(self.genes)

        for k, v in self.team_included.items():
            if 'RB' in k:
                self.TEAM[k] = {'name' : v, 'stats' : RB[v]}
            elif 'QB' in k:
                self.TEAM[k] = {'name' : v, 'stats' : QB[v]}
            elif 'WR' in k:
                self.TEAM[k] = {'name' : v, 'stats' : WR[v]}
            elif 'FLEX' in k:
                self.TEAM[k] = {'name' : v, 'stats' : FLEX[v]}
            elif 'TE' in k:
                self.TEAM[k] = {'name' : v, 'stats' : TE[v]}
            elif 'DST' in k:
                self.TEAM[k] = {'name' : v, 'stats' : DST[v]}




    def printGenes(self):
        printTeam(self.TEAM)

    def calcFitness(self, gen):
        sal, pts = calcStats(self.TEAM)
        self.fitness = pts * self.pt_weight + (sal / 1000) * self.sal_weight

        if sal == 50000:
            sal_target_bonus = 40
        elif abs(50000-sal) <= 100:
            sal_target_bonus = 30
        elif abs(50000-sal) <= 500:
            sal_target_bonus = 15
        elif abs(50000-sal) <= 1000:
            sal_target_bonus = 5
        elif abs(50000-sal) <= 1500:
            sal_target_bonus = 0
        else:
            sal_target_bonus = -15
        
        self.fitness += sal_target_bonus * self.sal_weight

        if sal > 50000:
            self.fitness -= 15

        else:
            self.fitness += 20


        return self.fitness

    def mutate(self, mrate):
        if randint(0, 100) < mrate * 100:
            mutate_gene = randint(0, len(self.genes) - 1)
            temp = [len(QB) - 1, len(RB) - 1, len(RB) - 1, len(WR) - 1, len(WR) - 1, len(WR) - 1, len(TE) - 1, len(DST) - 1, len(FLEX) - 1]
            self.genes[mutate_gene] = randint(0, temp[mutate_gene])

    
class Population:
    def __init__(self, popmax, mutation_rate):
        self.GOAT = None
        self.GOAT_gen = {'fitness': 0, 'generation' : 0}
        self.GOATs_gen = None
        self.popnum = popmax
        self.mrate = mutation_rate
        self.total_fitness = 0
        self.maxfit = 0
        self.generation = 1
        self.pool = []
        self.best_qb = {}
        self.best_rb = {}
        self.best_wr = {}
        self.best_te = {}
        self.best_dst = {}

        self.population = []

        for i in range(self.popnum):
            self.population.append(DNA())

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

        try:
            self.best_qb[self.best.TEAM['QB1']['name']] += 1
        except:
            self.best_qb[self.best.TEAM['QB1']['name']] = 1

        try:
            self.best_rb[self.best.TEAM['RB1']['name']] += 1
        except:
            self.best_rb[self.best.TEAM['RB1']['name']] = 1

        try:
            self.best_rb[self.best.TEAM['RB2']['name']] += 1
        except:
            self.best_rb[self.best.TEAM['RB2']['name']] = 1

        try:
            self.best_wr[self.best.TEAM['WR1']['name']] += 1
        except:
            self.best_wr[self.best.TEAM['WR1']['name']] = 1

        try:
            self.best_wr[self.best.TEAM['WR2']['name']] += 1
        except:
            self.best_wr[self.best.TEAM['WR2']['name']] = 1

        try:
            self.best_wr[self.best.TEAM['WR3']['name']] += 1
        except:
            self.best_wr[self.best.TEAM['WR3']['name']] = 1

        try:
            self.best_te[self.best.TEAM['TE1']['name']] += 1
        except:
            self.best_te[self.best.TEAM['TE1']['name']] = 1

        try:
            self.best_dst[self.best.TEAM['DST1']['name']] += 1
        except:
            self.best_dst[self.best.TEAM['DST1']['name']] = 1

        if self.GOAT == None:
            self.GOAT = self.best
            self.GOATs_gen = 1
        elif self.best.fitness > self.GOAT.fitness:
            self.GOAT = self.best
            self.GOATs_gen = self.generation

        if totalfit/len(self.population) > self.GOAT_gen['fitness']:
            self.GOAT_gen['generation'] = self.generation
            self.GOAT_gen['fitness'] = totalfit/len(self.population)
        
        print('Generation: {}'.format(self.generation))

        if avrteam_stats_console:
            print('\nAverage Fitness: {}'.format(totalfit/len(self.population)))

        if bestteams_console:
            if write_to_file:
                f.write("\nBest Team for Generation {}(Fitness: {}): ".format(self.generation, self.maxfit))
            print("\nBest Team for Generation {}(Fitness: {}): \n".format(self.generation, self.maxfit))
            self.best.printGenes()


        if worstteam_stats_console:
            print("\nWorst Team for Generation {}(Fitness: {}): ".format(self.generation, minfit))
            worst.printGenes()

        global generations

        if best_player_stats_console and self.generation >= generations:

            print()
            print('Best QB - {} ({}% in best teams)'.format(findHighestKey(self.best_qb)[0], int(findHighestKey(self.best_qb)[1]/generations * 100)))
            print()
            print('Best RB - {} ({}% in best teams)'.format(findHighestKey(self.best_rb)[0], int(findHighestKey(self.best_rb)[1]/generations * 100)))
            print()
            print('Best WR - {} ({}% in best teams)'.format(findHighestKey(self.best_wr)[0], int(findHighestKey(self.best_wr)[1]/generations * 100)))
            print()
            print('Best TE - {} ({}% in best teams)'.format(findHighestKey(self.best_te)[0], int(findHighestKey(self.best_te)[1]/generations * 100)))
            print()
            print('Best DST - {} ({}% in best teams)'.format(findHighestKey(self.best_dst)[0], int(findHighestKey(self.best_dst)[1]/generations * 100)))


        if session_stats_console:
            if self.generation >= generations:
                print()
                print('Best Generation: Gen - {}, AvrFitness - {}'.format(self.GOAT_gen['generation'], self.GOAT_gen['fitness']))
                print()
                print('Best Team: Gen - {}, Fitness - {}'.format(self.GOATs_gen, self.GOAT.fitness))
                print()
                self.GOAT.printGenes()


    def select(self):
        self.pool = []
        for dna in self.population:
            for i in range(int((dna.fitness/self.maxfit)*100)):
                self.pool.append(dna)

    def reproduce(self):
        new_population = []
        # new_population.append(self.best)

        for i in range(self.popnum-1):
            new_genes = []
            p1 = self.pool[randint(0, len(self.pool))-1]
            p2 = self.pool[randint(0, len(self.pool))-1]

            for i in range(9):
                if i % 2 == 0:
                    new_genes.append(p1.genes[i])
                else:
                    new_genes.append(p2.genes[i])

            child = DNA(child=True, genes=new_genes)
            child.mutate(self.mrate)
            new_population.append(child)

        self.population = new_population
        self.generation += 1

def findHighestKey(dictionary):
    best = ['', 0]
    for k, v in dictionary.items():
        if v > best[1]:
            best = [k, v]

    return best


def calcStats(team):
    tsal = 0
    tpts = 0
    for k, v in team.items():
        tsal += v['stats']['sal']
        tpts += v['stats']['pts']

    return tsal, tpts

def printTeam(team):
    tsal, tpts = calcStats(team)

    if write_to_file:
        f.write('Total Points: {}\n'.format(tpts))
        f.write('Total Salary: {}\n'.format(tsal))

    print('Total Points: {}'.format(tpts))
    print('Total Salary: {}'.format(tsal))

    for k, v in team.items():
        print('{} - {} (Points - {}, Salary - {})'.format(k, v['name'], v['stats']['pts'], v['stats']['sal']))


    return tsal

def makeTeam(genes):
    TEAM = {}
    TEAM['QB1'] = {'name' : QB_names[genes[0]], 'stats' : QB[QB_names[genes[0]]]}
    TEAM['RB1'] = {'name' : RB_names[genes[1]], 'stats' : RB[RB_names[genes[1]]]}
    TEAM['RB2'] = {'name' : RB_names[genes[2]], 'stats' : RB[RB_names[genes[2]]]}
    TEAM['WR1'] = {'name' : WR_names[genes[3]], 'stats' : WR[WR_names[genes[3]]]}
    TEAM['WR2'] = {'name' : WR_names[genes[4]], 'stats' : WR[WR_names[genes[4]]]}
    TEAM['WR3'] = {'name' : WR_names[genes[5]], 'stats' : WR[WR_names[genes[5]]]}
    TEAM['TE1'] = {'name' : TE_names[genes[6]], 'stats' : TE[TE_names[genes[6]]]}
    TEAM['DST1'] = {'name' : DST_names[genes[7]], 'stats' : DST[DST_names[genes[7]]]}
    TEAM['FLEX1'] = {'name' : FLEX_names[genes[8]], 'stats' : FLEX[FLEX_names[genes[8]]]}

    return TEAM

sals = pd.read_csv('DKSalaries.csv')

worstteam_stats_console = False
avrteam_stats_console = False
bestteams_console = False
write_to_file = False
session_stats_console = True
best_player_stats_console= True
team_excluded = ['David Johnson', 'Evan Engram', 'Darren Waller', 'Chris Thompson']
point_threshold = 1

QB = {}
RB = {}
WR = {}
DST = {}
TE = {}

QB_names = []
RB_names = []
WR_names = []
TE_names = []
FLEX_names = []
DST_names = []

if write_to_file:
    f = open('teams.txt', 'w+')

for index, row in sals.iterrows():
    if row['AvgPointsPerGame'] >= point_threshold and not row['Name'] in team_excluded:
        execute_string = row['Position'] + '["' + row['Name'].strip() + "\"] = {'sal': " + str(row['Salary']) +", 'pts': " + str(row['AvgPointsPerGame']) + ", 'value': " + str(row['AvgPointsPerGame']/row['Salary'] * 1000)+ "}"
        exec(execute_string)
        execute_string = row['Position'] + '_names.append("' + row['Name'].strip() + '")'
        exec(execute_string)

FLEX = {**TE, **RB, **WR}

FLEX_names.extend(TE_names)
FLEX_names.extend(RB_names)
FLEX_names.extend(WR_names)

generations = 1000
genetic_algorithm = Population(250, 0.03)

for i in range(generations):
    genetic_algorithm.calcFitness()
    genetic_algorithm.select()
    genetic_algorithm.reproduce()

generations = 1000
genetic_algorithm = Population(250, 0.05)

for i in range(generations):
    genetic_algorithm.calcFitness()
    genetic_algorithm.select()
    genetic_algorithm.reproduce()

generations = 1000
genetic_algorithm = Population(250, 0.1)

for i in range(generations):
    genetic_algorithm.calcFitness()
    genetic_algorithm.select()
    genetic_algorithm.reproduce()

if write_to_file:
    f.close()
