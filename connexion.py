import pymongo

class Connexion:
    @classmethod
    # Se connecter à Atlas
    def connect(cls):
        cls.user = 'Stephane'
        cls.password = 'isenbrest'
        return pymongo.MongoClient(f"mongodb+srv://{cls.user}:{cls.password}@bel-cluster.1cbyc.mongodb.net/?retryWrites=true&w=majority")
    
    @classmethod
    # Se connecter à la base de données
    def open_connexion(cls):
        cls.client = cls.connect()
        cls.collection = cls.client.conso.data

    @classmethod
    # Se déconnecter de la base de données
    def close_connexion(cls):
        cls.client.close()

    @classmethod
    def match(cls, kwargs):
        match_vars = {'region': 'fields.libelle_region', 'departement': 'fields.libelle_departement',
        'filiere': 'fields.filiere', 'commune': 'fields.libelle_commune', 'operateur': 'fields.operateur',
        'id': 'recordid', 'iris': 'fields.libelle_iris', 'secteur': 'fields.libelle_grand_secteur'}
        match = {}
        
        for key, value in kwargs.items():
            if value != None and value != True and value != False:
                match[match_vars[key]] = value

        return match

    @classmethod
    def kwargs_conso(cls, kwargs, conso):
        copy = kwargs.copy()
        for k, v in copy.items():
            if v == None or v == False or v == True:
                kwargs.pop(k)
        
        kwargs.update({'conso': conso})
        return kwargs

    @classmethod
    def get_data(cls, **kwargs):
        match = cls.match(kwargs)

        if kwargs['details']:
            _filter = {'_id': 0}
        else:
            _filter = {'_id': 0, 'fields.operateur': 1, 'fields.libelle_commune': 1, 'fields.filiere': 1, 'fields.conso': 1,
            'recordid': 1, 'fields.libelle_iris': 1, 'fields.libelle_grand_secteur': 1, 'fields.libelle_region': 1}

        cls.open_connexion()
        data = cls.collection.find(match, _filter)
        
        if kwargs['conso'] == False:
            cls.close_connexion()
            return data
        else:
            count = cls.collection.aggregate([{'$match': match}, {'$group': {'_id': 1, 'count': {'$sum': '$fields.conso'}}}])
            cls.close_connexion()
            conso = list(count)[0]['count']
            return cls.kwargs_conso(kwargs, conso)

    @classmethod
    def get_regions(cls, filiere):
        cls.open_connexion()
        if filiere == None:
            match = {}
        else:
            match = {'fields.filiere': filiere}
        data = list(cls.collection.find(match, {'_id': 0, 'fields.libelle_region': 1, 'fields.conso': 1}))
        cls.close_connexion()
        
        dico = {}
        for item in data:
            dico[item['fields']['libelle_region']] = dico.get(item['fields']['libelle_region'], 0) + item['fields']['conso']
        return dico


    @classmethod
    def delete_data(cls, _id):
        print("Delete", _id)
        cls.open_connexion()
        cls.collection.delete_one({'recordid' : _id})
        cls.close_connexion()

    @classmethod
    def update_data(cls, _id, data):
        cls.open_connexion()
        cls.collection.update({'recordid': _id}, {'$set' : data})
        cls.close_connexion()


    #Méthodes page Julien

    @classmethod
    def find_distinct_regions(cls):
        cls.open_connexion()
        regions = list(cls.collection.distinct('fields.libelle_region'))
        cls.close_connexion()
        return regions
    
    @classmethod
    def find_distinct_domains(cls):
        cls.open_connexion()
        domains = list(cls.collection.distinct('fields.libelle_grand_secteur'))
        cls.close_connexion()
        return domains


print(Connexion.find_distinct_regions())