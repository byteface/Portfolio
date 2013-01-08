#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Filnamn: data.py
## 2012-10-22 Per Jonsson & Linda Jansson
## IP1, Linköpings universitet
## Kurs: TDP003 (Anders Fröberg) ##

"""
-------------DATAMODUL-------------------------------------------
Datamodulen läser in projektdata från en fil kodad i json-format.
Innehållet i modulen föjer specifikationer från ett givet
"portfolio-API", som beskriver hur man ska behandla datan.

Samverkar med portfolioserver.py (presentationslagret)
----------------------------------------------------------------
"""

# MODULER
import json
import logging
import datetime

# VARIABLER
__package__ = None

#FUNKTIONER
def data_log(msg):
    """ Loggar anrop och lägger i loggfil, anger tidpunkt
        samt sträng med information om händelsetyp """

    # ändrar loggfilens datumstämpel i filnamnet
    date_tag = datetime.datetime.now().strftime("%Y-%b-%d")
    logging.basicConfig(filename='portfolio_{}.log'.format(date_tag),
                        level=logging.INFO,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    # ta emot meddelandesträng och logga
    logging.info(msg)

def load(filename): # = "data.json" under testningsfasen
    """ Funktionen läser in en UTF-8:kodad JSON file, lagrar den
        i variabeln data som en lista med dictionaries och returnerar
        sedan listan med alla projekt i.
        Vid fel i inläsning returnas None. """
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            data_log("data.load: Loading json file:" + filename )

    except Exception as e:
        error = "data.load: Error when loading from file: " + repr(e)
        data_log(error)
        return None
    return data

def get_project_count(db):
    """ Erhåller antalet projekt i listan (som ges av load())
        genom att returnera längden av den (antalet index)  """
    data_log("data.get_project_count(): Retrieving the number of projects in the database: " + str(len(db)) )
    return len(db)

def get_project(db, p_id):
    """
    Tar reda på ett specifikt projekt i den konverterade json-filen
    genom att ett projekt-ID-nummer (p_id) skickas till funktionen.
    Funktionen söker igenom listan av dictionaries som ges av load()
    Returnerar den dictionary där projekt-id:t återfinns, om inget
    projekt hittas returneras None
    """
    for dicts in db:
        if dicts[u'project_no'] == p_id:
            data_log("data.get_project(): Returning dict: " + str(p_id))
            return dicts
    data_log("data.get_project(): Returning None, couldn't find project no: " + str(p_id))
    return None

def get_techniques(db):
    """
    Går igenom listan med projekt(db) och returnerar en ny lista
    sorterad i alfabetisk ordning som anger alla tekniker som
    angetts i projektlistan
    """
    sorted_list = []

    for dicts in db:
        for element in dicts[u'techniques_used']:
            if not element in sorted_list: #sortera bort dubletter
                sorted_list.append(element)
    data_log("data.get_techniques: Returning sorted list of projects with techniques")
    return sorted(sorted_list)

def get_technique_stats(db):
    """
    Samlar och returnerar en dictionary med statistik för hur många gånger
    alla tekniker har använts samt i vilka projekt.
    Nyckeln i den returnerade dictionaryn anger tekniknamnet, sedan följer värdet
    som består av en lista med nya dictionaries för varje projekt där
    tekniken använts, (med nycklarna 'id':projektnummer och 'name': projektnamn).
    """
    techniques_list = get_techniques(db) # Tekniklistan som vi itererar genom
    technique_dict = {} # Dictionary som vi returner
    technique_dict_list=[] # temporär behållare till ovanstående

    for t in techniques_list:
        for dicts in db:
            if t in dicts[u'techniques_used']:
                technique_dict_list.append({u'id': dicts[u'project_no'],
                                            u'name': dicts[u'project_name']})
        technique_dict_list.reverse()
        technique_dict[t]=technique_dict_list
        technique_dict_list=[]

    data_log("data.get_technique_stats(): Returning dict with stats")
    return technique_dict

def search(db, sort_by=u'start_date',sort_order=u'desc',
           techniques=None,search=None,search_fields=None):
    """
    Sök-funktionen tar emot parametrar med sorteringskriterier
    som den matchar med projekt i listan som ges av load() -> db 

    Man kan välja:
    - sorteringsprioritering (startdatum, slutdatum, etc) -> sort_by
    - fallande eller stigande sortering (sort_order, 'asc' eller 'desc')
    - tekniklista (techniques) som sorterar ut med projekt med enbart dessa tekniker
      ... finns inga tekniker ignoreras den sorteringsmetoden
    - fritextsökning (search), är en sträng som skickas till funktionen
    search (string) - Free text search string.
    - sökfält (search_fields), en lista med kriterier såsom projektnummer, kursnamn, etc
      ... om inga sökfält anges söks alla fält igenom.
    
    Returnerar en lista med dictionaries med projekten som matchar sökkriterierna
    """

    matching_projects = db # Lista med projekt som returneras i slutet
    if techniques == "None": techniques = None
    if search == "": search = None

    ### TEKNIKER: Denna funktion anropas om man vill undvika att loopa
    #### igenom en dictionary utan angivna tekniker inuti
    def tech_check(dicts, techniques, db):
        for t in techniques:
            if not t in dicts[u'techniques_used']:
                return False
        return True

    ### SÖK ### (Om söksträng har angetts)
    if not search == None:

        matching_projects = [] # Återställ        
        search=search.lower() # gör allt till lowercase

        # Om search_fields är tom returneras inget
        if search_fields == []:
            return matching_projects

        # Om search_fields har fyllts med kriterier
        elif not search_fields == None:
            for dicts in db:
                # Kolla om vi ska hoppa över loopen
                if techniques == None or tech_check(dicts, techniques, db):
                    for field in search_fields:
                        s=unicode(dicts[field]) # Koda om matchande sträng
                        s=s.lower() # Kowercase
                        if search in s:
                            if not dicts in matching_projects: # Inga dubletter
                                matching_projects.append(dicts)

        # Om search_fields == None, sök igenom allt
        else:
            for dicts in db:
                if techniques == None or tech_check(dicts, techniques, db):
                    for element in dicts:
                        s=unicode(dicts[element])
                        s=s.lower()
                        if search in s:
                            if not dicts in matching_projects:
                                matching_projects.append(dicts)
                                # Om search är None, sök tekniker istället, och sortera
    elif not techniques == None :
        matching_projects = [] # Återställ
        for dicts in db:
            if tech_check(dicts, techniques, db) and not dicts in matching_projects:
                matching_projects.append(dicts)

    #### SORTERA
    sorting_list = []
    dict_no = 0

    # Leta efter matchande kriterier"
    for dicts in matching_projects:
        if sort_by in dicts:
            sorting_list.append([dicts[sort_by], matching_projects[dict_no]])
        dict_no+=1

    sorting_list.sort()
    if sort_order == u'desc': sorting_list.reverse() # Andra hållet om så önskas

    matching_projects = [] # Återställ
    for field in sorting_list:
        matching_projects.append(field[1])

    # Gör om strängen till utf-8 för att kunna skicka till loggen
    s = "";
    if not search == None:
        s = search.encode("utf-8")
    data_log("data.search(): Searching for: {} by {} in {} order".format(s, sort_by, sort_order) )

    ### RETURNERA LISTAN
    return matching_projects
