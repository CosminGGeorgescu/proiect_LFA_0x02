import sys
f=open(sys.argv[1], 'r')
states=[]
alphabet=[]
S=0
F=[]
transitions={}
delta_transitions={}
while line:=f.readline():   #cat timp mai sunt linii de citit
    if "Sigma" in line:    #daca pe linie e Sigma atunci incepe citirea alfabetului
        while "End" not in (line:=f.readline()):
            alphabet.append(line.split('letter')[1].split('\n')[0])
    elif "States" in line:    #daca pe linie e States atunci incepe citirea starilor
        while "End" not in (line:=f.readline()):
            if ("S" in line) and ("F" in line):    #trateaza cazul cand pe linie e si S si F
                S=line.split('state')[1].split(' ,S ,F')[0]
                F.append(S)
                states.append(S)
            elif "S" in line:   #trateaza cazul cand starea e cea initiala
                S=line.split('state')[1].split(' ,S')[0]
                states.append(S)
            elif "F" in line:   #trateaza cazul cand starea e finala
                F.append(line.split('state')[1].split(' ,F')[0])
                states.append(F[len(F)-1])
            else:
                states.append(line.split('state')[1].split('\n')[0])
    elif "Transitions" in line:   #daca pe linie e Transitions, incepe citirea tranzitiilor de la linia urmatoare
        while "End" not in (line:=f.readline()):    #citim pana dam de End pe linie
            line=line.split(' ,')
            t=[]
            t.append(line[0].split('state')[1])
            t.append(line[1].split('letter')[1])
            t.append(line[2].split('state')[1].split('\n')[0])
            if (t[0], t[2]) in transitions:
                transitions[(t[0], t[2])].append(t[1])    
            else:
                transitions[(t[0], t[2])]=[t[1]]    #pentru formatul din pdf, t[0] si t[2] sunt stari, iar t[1] e litera din alfabet
            delta_transitions[(t[0], t[1])]=t[2]
print(states)
for state1 in states:
    k=True
    for (state2, transition) in delta_transitions:
        if (state1==delta_transitions[(state2, transition)] and state2!=delta_transitions[(state2, transition)]) or state1==S:
            k=False
            break
    if k:
        states.pop(states.index(state1)) 
#in punctul asta am scapat de stari unreacheable
markup=[[0  if states[i] not in F else 1 for i in range(len(states))] if states[j] not in F else [1 if states[i]!=states[j] else 0 for i in range(len(states))] for j in range(len(states))]
print(states)
while 1:
    k=True
    for i in range(len(markup)):
        for j in range(len(markup[i])):
            for letter in alphabet:
                if markup[i][j]==0 and markup[states.index(delta_transitions[(states[i], letter)])][states.index(delta_transitions[(states[j], letter)])]==1:
                    markup[i][j]=1
                    k=False
                    break
    if k:
        break
distinguishable=states.copy()
for i in range(1, len(markup)):
    for j in range(i):
        if markup[i][j]==0:
            if states[i] in distinguishable:
                distinguishable.pop(distinguishable.index(states[i]))
            if states[j] in distinguishable:
                distinguishable.pop(distinguishable.index(states[j]))
            distinguishable.append([states[i], states[j]])
while 1:
    k=True
    for i in range(len(distinguishable)):
        a=set(distinguishable[i])
        for j in range(i+1, len(distinguishable)):
            b=set(distinguishable[j])
            if len(a&b)!=0:
                distinguishable.pop(i)
                distinguishable.pop(j-1)
                distinguishable.append(list(a|b))
                k=False
                break
        if not k:
            break
    if k:
        break
print(distinguishable)
print("Sigma:")
for letter in alphabet:
    print("\tletter", letter, sep='')
print("End")
print("States:")
b=set(S)
c=set(F)
for i in range(len(distinguishable)):
    print("\tstateq", i, sep='', end='')
    a=set(distinguishable[i])
    if len(a&b)!=0:
        print(" ,S", end='')
    if len(a&c)!=0:
        print(" ,F", end='')
    print()
print("End")
print("Transitions:")
for i in range(len(distinguishable)):
    if len(distinguishable[i])>1:
        for letter in alphabet:
            print("\tstateq",i," ,letter", letter, " ,stateq", sep='', end='') #delta_transitions[(distinguishable[i][0], letter)]
            for j in range(len(distinguishable)):
                if (len(distinguishable[j])>1) and (delta_transitions[(distinguishable[i][0], letter)] in distinguishable[j]):
                    print(j)
                    break
                elif (len(distinguishable[j])==1):
                    if delta_transitions[(distinguishable[i][0], letter)]==distinguishable[j]:
                        print(j)
                        break
    else:
        for letter in alphabet:
            print("\tstateq",i," ,letter", letter, " ,stateq", sep='', end='') #delta_transitions[(distinguishable[i], letter)]
            for j in range(len(distinguishable)):
                if (len(distinguishable[j])>1) and (delta_transitions[(distinguishable[i], letter)] in distinguishable[j]):
                    print(j)
                    break
                elif (len(distinguishable[j])==1):
                    if delta_transitions[(distinguishable[i], letter)]==distinguishable[j]:
                        print(j)
                        break