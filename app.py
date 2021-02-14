from flask import Flask, render_template, request, url_for, redirect
from data import get_conso_fil_reg, get_region, get_gaz_region, get_elec_region, get_data, get_data_region_fil
import pandas as pd 
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefgh'

#Erwan
@app.route('/', methods = ['GET', 'POST'])
def index():
    regions = get_region()
    data_map = get_gaz_region()
    data_map2 = get_elec_region()
    if request.method == 'POST':
        select = request.form.get('region')
        data = get_conso_fil_reg(select)
        data_map = get_gaz_region()
        data_map2 = get_elec_region()        
        return render_template('index.html', data=data, regions=regions, select=select, data_map=data_map, data_map2=data_map2)
    return render_template('index.html', regions=regions, data_map=data_map, data_map2=data_map2)

#Julien
@app.route('/regions',methods=['POST','GET'])
def regions():

    domaines, regions = get_data()

    if request.method == 'POST':
        data = get_data_region_fil(request.form['region'], request.form['energie'], request.form['domaine'])
        infos = [request.form['region'], request.form['energie'], request.form['domaine']]
        return render_template('regions.html',data=data,domaines=domaines,regions=regions,condition=True,info=infos)

    return render_template('regions.html',domaines=domaines,regions=regions,condition=False)


#Pereg
@app.route('/edit', methods=['GET', 'POST'])
def get_id():
    if request.method == 'POST':
        dico = request.form.to_dict()
        data = requests.get('http://api-energy.herokuapp.com/api/energie/?' + f'filiere={dico["filiere"]}&commune={dico["commune"]}&operateur={dico["operateur"]}&iris={dico["iris"]}&secteur={dico["secteur"]}').json()
        _id = data['data'][0]['recordid']
        data = data['data'][0]['fields']
        return render_template('edit_item.html', id=_id, data=data)

    return render_template('edit.html')


@app.route('/edit/<_id>/delete', methods=['GET'])
def delete(_id):
    code, = requests.delete('http://api-energy.herokuapp.com/api/energie/' + str(_id))
    
    return redirect(url_for('get_id'))


@app.route('/edit/<_id>/update', methods=['GET', 'POST'])
def update(_id):
    if request.method == 'POST':
        conso = request.form.get('conso')
        operateur = request.form.get('operateur')
        filiere = request.form.get('filiere')
        secteur = request.form.get('secteur')

        requests.put('http://api-energy.herokuapp.com/api/energie/' + str(_id) + f'?conso={conso}&operateur={operateur}&filiere={filiere}&secteur={secteur}')

    return redirect(url_for('get_id'))
