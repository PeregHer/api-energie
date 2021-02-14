from fastapi import FastAPI, HTTPException
import uvicorn
from connexion import Connexion

api = FastAPI(redoc_url=None)

@api.get("/api/energie", tags=["Energy"])
async def get_data(filiere: str=None, region: str=None, departement: str=None, commune: str=None, operateur: str=None, id: str=None, iris: str=None, secteur: str=None, conso: bool=False, details: bool=False):
    if conso:
        conso = Connexion.get_data(filiere=filiere, region=region, departement=departement, commune=commune, operateur=operateur, iris=iris, secteur=secteur, id=id, conso=conso, details=details)
        return {'data': conso}

    data = list(Connexion.get_data(filiere=filiere, region=region, departement=departement, commune=commune, operateur=operateur, iris=iris, secteur=secteur, id=id, conso=conso, details=details))
    return {'data': data}

@api.get("/api/energie/regions", tags=["Energy"])
async def get_regions(filiere: str=None):
    data = Connexion.get_regions(filiere=filiere)
    return {'data': data}

@api.delete("/api/energie/{id}", tags=["Energy"])
async def delete_data(id: str):        
    Connexion.delete_data(id)

@api.put("/api/energie/{_id}", tags=["Energy"])
async def update_data(_id: str, conso: float, filiere: str, secteur: str, operateur: str):        
    data = {'fields.conso': conso, 'fields.filiere': filiere, 'fields.libelle_grand_secteur': secteur, 'fields.operateur': operateur}
    Connexion.update_data(_id, data)
    return {'message': 'check'}


@api.get("/api/energie/data/domains")
async def get_data_domain():
    domains = list(Connexion.find_distinct_domains())
    return domains

@api.get("/api/energie/data/regions")
async def get_data_region():
    regions = list(Connexion.find_distinct_regions())
    return regions