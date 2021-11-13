
import pandas as pd  
import numpy as np 
from itertools import combinations 

choice = input("Please, Select your Dataset for \n 1 Amazon.\n 2 bestbuy.\n 3 K_mart.\n 4 Nike.\n 5 Generic. \n ")
choice = int(choice)

if choice == 1:
    df =pd.read_csv('/Users/teja/Kulkarni_Teja_MidtermProj/amazon.csv')
    print(df)
elif choice == 2:
    df = pd.read_csv('/Users/teja/Kulkarni_Teja_MidtermProj/bestbuy.csv')
    print(df.head())
elif choice == 3:
    df = pd.read_csv('/Users/teja/Kulkarni_Teja_MidtermProj/kmart.csv')
    print(df)
elif choice == 4:
    df = pd.read_csv('/Users/teja/Kulkarni_Teja_MidtermProj/nike.csv')
    print(df)  
elif choice == 5:
    df = pd.read_csv('/Users/teja/Kulkarni_Teja_MidtermProj/generic.csv')
    print(df)  
else:
    print("Wrong Choice")

min_sup = input("Please, input your Min. Support \n")
min_sup = float(min_sup)
min_con = input("Please, input your Min. confidence \n")
min_con = float(min_con)

names = list(df.columns)
tid = df[names[0]] 
items = df[names[1]] 
uni_items = df[names[1]].unique()
uni_tid = df[names[0]].unique()

def build_transactions(uni_tid, tid, items):
    transactions = []
    for i in uni_tid:
        temp_list = []
        for j in range(0, len(tid)):
            if tid[j] == i:
                temp_list.append(items[j])
        transactions.append(temp_list)
    return(transactions)

transactions = build_transactions(uni_tid, tid, items)
num_trans = len(transactions)
def check_pattern(list1, list2):
    x = 0
    if(all(x in list2 for x in list1)):
        x = 1
    return x

def update_fre_items (a, b):
    f = []
    
    for i in a:
        for j in i:
            f.append(j)
    
    temp = []
    for i in b:
        if i  in f:
            temp.append(i)
    
    return temp

pat_size = 1 
fre_pat = [] 
#Number of pattrens
fre_pat_count = [] 
temp_fre_pat = [1] 
fre_items = list(uni_items) 
while (temp_fre_pat):

    # generate acceptable patterns
    pats = combinations(fre_items, pat_size)
    temp_fre_pat = [] # frequent patterns
    for f in list(pats):
        count = 0
        for t in transactions:
            count = count + check_pattern(f, t)
        if count >= min_sup * num_trans:
            temp_fre_pat.append(f)
            fre_pat_count.append(count)
    
    fre_pat = fre_pat + temp_fre_pat
    pat_size += 1 
    # update frequent items list for creating new patterns
    fre_items = update_fre_items(temp_fre_pat, fre_items)

print('frequent patterns   \n',fre_pat)

print('\nAssociation rules')

for i in fre_pat:

    if len(i) > 1:
        
        sub_groups = list(combinations(i, len(i) - 1))
        #print(sub_groups)
        for j in sub_groups:
            temp = []
            for k in j:
                temp.append(k)
            z = list(set(i).difference(set(temp)))
            confidence = fre_pat_count[fre_pat.index(i)] / fre_pat_count[fre_pat.index(j)]
            if confidence > min_con:
                print(j,' ---> ', z ,'   confidence = ',confidence)
