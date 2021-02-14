import requests
import pandas as pd


#Erwan
def get_region():
    lst_reg_name = []
    lst_reg = {'Corse': 94 , 'Bretagne': 53, 'Pays de la Loire': 52, 'Provence-Alpes-Côte d\'Azur': 93, 'Occitanie': 76, 'Nouvelle-Aquitaine': 75, 'Bourgogne-Franche-Comté': 27, 'Centre-Val de Loire': 24, 'Île-de-France': 11, 'Hauts-de-France': 32, 'Auvergne-Rhône-Alpes': 84, 'Grand Est': 44, 'Normandie': 28, 'La Réunion': 4, 'Mayotte' :6, 'Guyane': 3, 'Martinique': 2, 'Guadeloupe': 1}
    for region in lst_reg.keys():
        lst_reg_name.append(region)
    return lst_reg_name

def get_conso_fil_reg(reg:str):

    try:
        data_gaz = requests.get(f'https://api-energy.herokuapp.com/api/energie?&filiere=Gaz&region={reg}&conso=true').json()
        data_gaz = data_gaz['data']['conso']
    except:
        data_gaz = 0
    print(data_gaz)
    try:
        data_elec = requests.get(f'https://api-energy.herokuapp.com/api/energie?&filiere=Electricité&region={reg}&conso=true').json()
        data_elec = data_elec['data']['conso']
    except:
        data_elec = 0
    print(data_elec)

    total_conso = data_gaz + data_elec
    pourcent_gaz = (data_gaz / total_conso) * 100
    pourcent_elec = (data_elec / total_conso) * 100
    data = [{'name' : 'Gaz', 'y' : pourcent_gaz, 'sliced' : 'true'}, {'name': 'Electricité' , 'y' : pourcent_elec, 'sliced' : 'true'}]
    return data

def get_gaz_region():
    data_gaz_region = requests.get('https://api-energy.herokuapp.com/api/energie/regions?&filiere=Gaz').json()
    lst_reg = {'Corse' : 'fr-cor', 'Bretagne': 'fr-bre', 'Pays de la Loire':'fr-pdl', 'Provence-Alpes-Côte d\'Azur':'fr-pac', 'Occitanie':'fr-occ', 'Nouvelle-Aquitaine':'fr-naq', 'Bourgogne-Franche-Comté':'fr-bfc', 'Centre-Val de Loire':'fr-cvl', 'Île-de-France':'fr-idf' , 'Hauts-de-France':'fr-hdf', 'Auvergne-Rhône-Alpes':'fr-ara', 'Grand Est':'fr-ges', 'Normandie':'fr-nor', 'La Réunion':'fr-lre', 'Mayotte':'fr-may', 'Guyane':'fr-gf', 'Martinique':'fr-mq', 'Guadeloupe':'fr-gua'}
    data = data_gaz_region['data']
    lst = []
    for item in data.items():
        lst_int = []
        lst_int.append(lst_reg[item[0]])
        lst_int.append(item[1])
        lst.append(lst_int)
    return lst

def get_elec_region():
    data_gaz_region = requests.get('https://api-energy.herokuapp.com/api/energie/regions?&filiere=Electricité').json()
    lst_reg = {'Corse' : 'fr-cor', 'Bretagne': 'fr-bre', 'Pays de la Loire':'fr-pdl', 'Provence-Alpes-Côte d\'Azur':'fr-pac', 'Occitanie':'fr-occ', 'Nouvelle-Aquitaine':'fr-naq', 'Bourgogne-Franche-Comté':'fr-bfc', 'Centre-Val de Loire':'fr-cvl', 'Île-de-France':'fr-idf' , 'Hauts-de-France':'fr-hdf', 'Auvergne-Rhône-Alpes':'fr-ara', 'Grand Est':'fr-ges', 'Normandie':'fr-nor', 'La Réunion':'fr-lre', 'Mayotte':'fr-may', 'Guyane':'fr-gf', 'Martinique':'fr-mq', 'Guadeloupe':'fr-gua'}
    data = data_gaz_region['data']
    lst = []
    for item in data.items():
        lst_int = []
        lst_int.append(lst_reg[item[0]])
        lst_int.append(item[1])
        lst.append(lst_int)
    return lst

#Julien
def get_data():
    domains = requests.get(f'https://api-energy.herokuapp.com/api/energie/data/domains').json()
    regions = requests.get(f'https://api-energy.herokuapp.com/api/energie/data/regions').json()
    return domains, regions


def get_data_region_fil(reg, fil, domaine):
    data = requests.get(f'https://api-energy.herokuapp.com/api/energie?region={reg}&filiere={fil}&details=true').json()
    
    data = pd.json_normalize(data['data'])
    data = data.groupby(['fields.libelle_departement','fields.libelle_grand_secteur']).sum()
    infos = []
    for info in data.index.tolist():
        infos.append(info)

 
    allDataList = []
    for i in range(len(infos)):
        donnee = {}
        row = data.iloc[i].values
        donnee['region'] = infos[i][0]
        donnee['domaine'] = infos[i][1]
        donnee['pdl'] = row[2]
        donnee['conso'] = row[5]
        allDataList.append(donnee)

    data = pd.json_normalize(allDataList)
    value = data[data['domaine'] == domaine].values.tolist()
    dep = []
    val = []
    valeur = []
    for v in value:
        dep.append(v[0])
        val.append(v[3])
    valeur = [dep, val]
    return valeur