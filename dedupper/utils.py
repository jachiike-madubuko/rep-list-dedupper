#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 19 17:53:34 2018

@author: jachi
"""
import dedupper.threads
import os
from dedupper.models import progress, repContact, sfcontact, dedupTime, duplifyTime, uploadTime
import string
from time import perf_counter
from random import *
from range_key_dict import RangeKeyDict
from fuzzywuzzy import fuzz
from fuzzywuzzy import process #could be used to generate suggestions for unknown records
import numpy as np
from tablib import Dataset
import logging
import time
from django.db.models import Avg
from fuzzyset import FuzzySet
from operator import itemgetter
import json
import pandas as pd
from gc import collect
#find more on fuzzywuzzy at https://github.com/seatgeek/fuzzywuzzy


standard_sorting_range = RangeKeyDict({
    (97, 101): 'Duplicate',
    (95, 97): 'Manual Check',
    (0, 95): 'Undecided'
})
last_key_sorting_range = RangeKeyDict({
    (97, 101): 'Duplicate',
    (95, 97): 'Manual Check',
    (0, 95): 'New Record'
})
manual_sorting_range = RangeKeyDict({
    (95, 101): 'Manual Check',
    (0, 95): 'Undecided',
})
last_manual_sorting_range = RangeKeyDict({
    (95, 101): 'Manual Check',
    (0, 95): 'New Record'
})

waiting= True
keylist = list()
currKey=sort_alg=None
start=end=cnt=doneKeys=totalKeys=0

#TODO finish phone/eemail multi sf field mapping

#TODO add docstrings go to realpython.com/documenting-python-code/
#TODO update documentation go to dbader.org/blog/write-a-great-readme-for-your-github-project
#TODO django test cases realpython <--

def convert_csv(file):
    print('converting CSV: ', str(file))
    # print('utf-8')
    # pd_csv = pd.read_csv(file, encoding = "utf-8", delimiter=',')
    # print('iso8859_15')
    # pd_csv = pd.read_csv(file, encoding = "iso8859_15", delimiter=',')
    print('cp1252')
    pd_csv = pd.read_csv(file, encoding = "cp1252", delimiter=',')  #western european

    return list(pd_csv), pd_csv

def find_rep_dups(rep, keys, numthreads):
    global cnt
    dup_start=perf_counter()
    rep_key = rep.key(keys[:-1])
    if 'NULL' in rep_key:
        logging.debug("bad rep key")
        return 0
    search_party =  sfcontact.objects.none()
    # TODO test this one to many code
    '''
    for n,i in enumerate(key_parts):
        if 'Phone' in i:
            multi_key = True
            sf_keys = []
            for j in ['mobilePhone', 'homePhone', 'otherPhone', 'Phone']:
                vary_key = key_parts.copy()
                vary_key[n] = j
                addon = [i.key(vary_key[:-1]) for i in sf_list if "NULL" not in i.key(vary_key[:-1]) ]
                sf_keys.extend(addon)
        elif 'Email' in i:
            multi_key = True
            sf_keys = []
            for j in ['workEmail', 'personalEmail', 'otherEmail']:
                vary_key = key_parts.copy()
                vary_key[n] = j
                addon = [i.key(vary_key[:-1]) for i in sf_list if "NULL" not in i.key(vary_key[:-1]) ]
                sf_keys.extend(addon)
    if not multi_key:
        sf_keys = [i.key(key_parts[:-1]) for i in sf_list if "NULL" not in i.key(key_parts[:-1]) ] #only returns    
    '''

    for key in keys[:-1]:
        if 'Phone' in key:
            for type_of_phone in ['mobilePhone', 'homePhone', 'otherPhone', 'Phone']:
                kwargs = {f'{type_of_phone}__icontains': f'{rep.key([key])}'}
                # queryset of Sfcontacts that have a matching field with the rep
                search_party = search_party.union(sfcontact.objects.filter(**kwargs))
        if 'Email' in key:
            for type_of_email in ['workEmail', 'personalEmail', 'otherEmail']:
                kwargs = {f'{type_of_email}__icontains': f'{rep.key([key])}'}
                # queryset of Sfcontacts that have a matching field with the rep
                search_party = search_party.union(sfcontact.objects.filter(**kwargs))

        kwargs = { f'{key}__icontains' : f'{rep.key([key])}' }
        # queryset of Sfcontacts that have a matching field with the rep
        search_party = search_party.union(sfcontact.objects.filter(**kwargs))
    '''
    for n, i in enumerate(key):
    if 'Phone' in i:
        multi_key = True
        sf_keys = []
        for j in ['mobilePhone', 'homePhone', 'otherPhone', 'Phone']:
            vary_key = key_parts.copy()
            vary_key[n] = j
            addon = [i.key(vary_key[:-1]) for i in sf_list if "NULL" not in i.key(vary_key[:-1])]
            sf_keys.extend(addon)
    elif 'Email' in i:
        multi_key = True
        sf_keys = []
        for j in ['workEmail', 'personalEmail', 'otherEmail']:
            vary_key = key_parts.copy()
            vary_key[n] = j
            addon = [i.key(vary_key[:-1]) for i in sf_list if "NULL" not in i.key(vary_key[:-1])]
            sf_keys.extend(addon)
    '''
    sf_map = {i.key(keys[:-1]): i for i in search_party if "NULL" not in i.key(keys[:-1])}  # only returns
    sf_keys = sf_map.keys()

    closest = fuzzyset_alg(rep_key, sf_keys)
    if len(closest) == 0:
         logging.debug("no close matches")
         if currKey == keylist[-1]:
            string_key = '-'.join(currKey)
            rep.keySortedBy = string_key
            rep.type = sort(1)
            rep.save()
            return
         else:
            return
    for i in closest:
        i[0] = sf_map[i[0]] #replace key with sf contact record
    if len(closest) == 3  and closest[0][1] <= closest[-1][1] + 10 :
        rep.average = np.mean([closest[0][1], closest[1][1], closest[2][1]])
        rep.closest1 = closest[0][0]
        rep.closest2 = closest[1][0]
        rep.closest3 = closest[2][0]
        rep.closest1_contactID = closest[0][0].ContactID
        rep.closest2_contactID = closest[1][0].ContactID
        rep.closest3_contactID = closest[2][0].ContactID
    elif  len(closest) == 2 and closest[0][1] <= closest[-1][1] + 5:
        rep.average = np.mean([closest[0][1], closest[1][1]])
        rep.closest1 = closest[0][0]
        rep.closest2 = closest[1][0]
        rep.closest1_contactID = closest[0][0].ContactID
        rep.closest2_contactID = closest[1][0].ContactID
    else:
        rep.average = closest[0][1]
        rep.closest1 = closest[0][0]
        rep.closest1_contactID = closest[0][0].ContactID
    rep.type = sort(rep.average)

    if rep.type=='Duplicate' and rep.CRD != '' and  closest[0][0].CRD != '' and  int(rep.CRD) != int(closest[0][0].CRD.replace(".0","")) :
        rep.type = 'Manual Check'
    string_key = '-'.join(currKey)
    rep.keySortedBy = string_key
    rep.save()
    # logging.debug(f'{rep.firstName} sorted as {rep.type} with {rep.keySortedBy} key ')
    time = round(perf_counter()-dup_start, 2)

    dups = len(repContact.objects.filter(type='Duplicate'))
    news = len(repContact.objects.filter(type='New Record'))
    undies = len(repContact.objects.filter(type='Undecided'))
    avg = dedupTime.objects.aggregate(Avg('seconds'))['seconds__avg']
    if avg == None:
        avg = 0
    else:
        avg = round(avg, 2)
    dedupTime.objects.create(
                             seconds=time,
                             num_threads=numthreads,
                             avg=avg,
                             num_dup=dups,
                             num_new=news,
                             num_undie=undies,
                             current_key=currKey)
    cnt += 1
    del time, avg, dups, news, undies, string_key, sf_map, sf_keys, search_party, dup_start, rep_key

def finish(numThreads):
    global end, waiting
    c = collect()                   #garbage collection
    logging.debug(f'# of garbage collected = {c}')
    if currKey == keylist[-1]:
        for i in list(repContact.objects.filter(type='Undecided')):
            i.type = last_key_sorting_range[i.average]
            i.save()
        end = perf_counter()
        time = end - start
        duplifyTime.objects.create(num_threads=numThreads,
                                   seconds=round(time, 2)
                                   )
        os.system('say "The repp list has been duplified!"')
    waiting=False

def fuzzyset_alg(key, key_list):
    finder = FuzzySet()
    finder.add(key)
    candidates = list()
    for i in key_list:
        try:
            added = [i]
            matched = finder[i]
            added.extend(*matched)
            del added[-1]  #remove rep's key from list
            added[1] *= 100
            '''
            [0] the sf key
            [1] match percentage
            '''
            candidates.append(added)
        except:
            pass
    candidates.sort(key=lambda x: x[1], reverse=True)
    # print("###############################################\n candidates \n {}\n".format(candidates))
    top_candi = candidates[:10]
    finalist = [[i[0], fuzz.ratio(key, i[0])] for i in top_candi]
    finalist.sort(key=lambda x: x[1], reverse=True)
    del finder, candidates, top_candi
    if len(finalist) > 0:
        return finalist[:3]
    else:
        return []

def key_generator(partslist):
    global start, waiting, doneKeys, totalKeys, cnt, currKey, sort_alg, keylist
    start = perf_counter()
    totalKeys = len(partslist)
    keylist = partslist
    for key_parts in partslist:
        sort_alg = key_parts[-1]
        currKey = key_parts
        cnt=0
        print('starting key: {}'.format(key_parts))
        waiting = True
        multi_key = False
        string_key = '-'.join(currKey)
        rep_list = repContact.objects.filter(type='Undecided').exclude(keySortedBy=string_key)
        print('adding {} items to the Q'.format(len(rep_list)))
        dedupper.threads.updateQ([[rep, key_parts] for rep in rep_list])
        while waiting:
            pass
        doneKeys += 1

def load_csv2db(csv, header_map, resource, file_type='rep'):
    start = perf_counter()
    dataset = Dataset()
    pd_csv = csv
    # print(list(pd_csv))
    print(json.dumps(header_map, indent=4))
    try:
        pd_csv.rename(columns=header_map, inplace=True)
        pd_csv['id'] = np.nan
        dataset.csv = pd_csv.to_csv()
        resource.import_data(dataset, dry_run=False)
        print(list(pd_csv))
    except:
        print("lost the pandas csv")
    end = perf_counter()
    time = end - start
    if file_type == 'rep':
        uploadTime.objects.create(num_records = len(repContact.objects.all()), seconds=round(time, 2))
    else:
        uploadTime.objects.create(num_records = len(sfcontact.objects.all()),seconds=round(time, 2))

def make_keys(headers):
    keys = []
    rep_total = repContact.objects.all().count()
    sf_total = sfcontact.objects.all().count()
    phoneUniqueness = 0
    emailUniqueness = 0
    phoneTypes = ['Phone', 'homePhone', 'mobilePhone', 'otherPhone']
    emailTypes = ['workEmail', 'personalEmail', 'otherEmail']
    excluded = ['id', 'average', 'type', 'match_ID', 'closest1', 'closest2', 'closest3',
                'closest1_contactID', 'closest2_contactID', 'closest3_contactID', 'dupFlag', 'keySortedBy' ]

    for i in headers:
        if i not in excluded:
            kwargs = {
                '{}__{}'.format(i, 'exact'):''
            }
            rp_uniqueness = repContact.objects.order_by().values_list(i).distinct().count() / rep_total
            rp_utility = (len(repContact.objects.all()) - len(repContact.objects.filter(**kwargs))) /rep_total
            sf_uniqueness = sfcontact.objects.order_by().values_list(i).distinct().count() / sf_total
            sf_utility = (len(sfcontact.objects.all()) - len(sfcontact.objects.filter(**kwargs))) /sf_total
            score = (rp_uniqueness + rp_utility + sf_uniqueness + sf_utility)/4
            keys.append((i, int(rp_uniqueness * 100), int(rp_utility * 100), int(sf_uniqueness * 100), int(sf_utility * 100), score))
    keys.sort(key=itemgetter(5), reverse=True)
    return keys

def match_keys(key,key_list):
    for i in key_list:
        yield match_percentage(key, i)

def match_percentage(key1,key2):
    return fuzz.ratio(key1, key2)

def mutate(keys):
    mutant = keys.copy()
    num_mutating = randint(int(len(keys)/5),int(len(keys)*0.8))

    for i in range(num_mutating):
        j = randint(0,len(keys)-1)
        for i in range(randint(3,len(mutant[j])+3)):
            mutant[j]=mutant[j].replace(mutant[j][int(sample(range(len(mutant[j])-1), 1)[0])], choice(string.printable))
    return mutant

def set_sorting_algorithm(min_dup, min_uns):
    global standard_sorting_range, manual_sorting_range
    cnt=0
    standard_sorting_range = RangeKeyDict({
    (min_dup, 101): 'Manual Check',
    (0, min_dup): 'Undecided',
})

    manual_sorting_range = RangeKeyDict({
    (min_dup, 101): 'Manual Check',
    (min_uns, min_dup): 'Undecided',
    (0, min_uns): 'New Record'
})
    for rep in list(repContact.objects.all()):
        cnt+=1
        if rep.keySortedBy != '':
            keys = rep.keySortedBy.split('-')
            if keys == keylist[-1]:
                rep.type = last_key_sorting_range[rep.average]
            elif keys[-1] == 'true':
                rep.type = manual_sorting_range[rep.average]
            else:
                rep.type = standard_sorting_range[rep.average]
            rep.save()
        else:
            rep.type = standard_sorting_range[rep.average]
            rep.save()
            print('{}-{}'.format(rep.type, rep.average))

        if cnt%500 ==0:
            print('re-sort #{}'.format(cnt))

def sort(avg):
    if sort_alg == 'true' and currKey == keylist[-1]:
        return last_manual_sorting_range[avg]
    elif sort_alg == 'true':
        return manual_sorting_range[avg]
    elif currKey == keylist[-1]:
        return last_key_sorting_range[avg]
    else:
        return standard_sorting_range[avg]

def get_progress():
    return doneKeys, totalKeys, currKey, cnt
