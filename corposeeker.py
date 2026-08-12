#!/bin/env python3

import time
from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request
import duckdb
import pandas

#local modules
from dict_naf_code_to_name import naf_codes_dict
from trenche_efectif_codes import tecodes


"""
what i can get :

status value A or F for the is Active, the C is for legal unit, cause you cancel a legal unit and you CLOSE (ferme) a place 

is_hq chekbox true or nonne
ignore_hq chekbox true or nonne

date_creation_from is date
ignore_date chekbox true or none

trancheEffectifs values for the size
ignore_size chekbox true or nonne

codePostal is a number or empty string, if empty give error

codeCommune is a number or empty string, if empty give error

activitePrincipale is a string, can't be empty


"""

#SIRETS , corpo buildings, entrprise phisical incarnations
BUILDINGS = "./stockFiles/stock-stocketablissement-parquet.parquet" #will be refered as e
#SIRENs , entreprise, all that stuff
CORPOS = "./stockFiles/stock-stockunitelegale-parquet.parquet" #will be refered as u
#geolocalization of buildings
GEOLOC = "./stockFiles/geoloc-geolocalisationetablissement-sirene-pour-etudes-statistiques-parquet.parquet" #will be refered as g if will be at all

app = Flask(__name__)

buildingsdb = duckdb.read_parquet(BUILDINGS)
corposdb = duckdb.read_parquet(CORPOS)
geodb = duckdb.read_parquet(GEOLOC)


@app.route('/')
def index():
    return render_template('index.html', amount=0)

@app.route('/search', methods = ['POST', 'GET'])
def search():
    """
    should get : NAF25 NAF_old 
    
    """
    sql_query = "\
    SELECT \
    e.siren, \
    e.siret, \
    u.denominationUniteLegale, \
    e.etatAdministratifEtablissement, \
    e.etablissementSiege, \
    e.dateCreationEtablissement, \
    e.activitePrincipaleEtablissement, \
    e.activitePrincipaleNAF25Etablissement, \
    e.trancheEffectifsEtablissement, \
    e.codePostalEtablissement, \
    e.codeCommuneEtablissement, \
    g.y_latitude as lat, \
    g.x_longitude as lng \
    FROM buildingsdb AS e \
    JOIN corposdb AS u ON e.siren = u.siren \
    JOIN geodb as g ON e.siret = g.siret \
    WHERE \
    "
    
    #chekboxes, there is no guarantie u get them in the post
    is_hq = request.form.get('is_hq') #chekbox true or none //done
    ignore_hq = request.form.get('ignore_hq') #chekbox true or none
    ignore_date = request.form.get('ignore_date') #chekbox true or none
    ignore_size = request.form.get('ignore_size') #chekbox true or none
    ignore_comune = request.form.get('ignore_comune') #chekbox true or none
    #there is guarantie you get it
    status = request.form.get('status') #A for active, F for dead //done
    date_creation_from = request.form.get('date_creation_from') #the data when they started hustle //done
    trancheEffectifs = request.form.get('trancheEffectifs') #how many slaves they have //done
    postal_code = request.form.get('postal_code') #where they are 
    comune_code = request.form.get('comune_code') #where exactly they are //done
    main_acctivity = request.form.get('main_acctivity') #what they do

    #all posible ignores
    if not ignore_hq :
        if is_hq :
            sql_query += " e.etablissementSiege = true AND "
        else :
            sql_query += " e.etablissementSiege = false AND "
    if not ignore_date :
        sql_query += f" e.dateCreationEtablissement >= {date_creation_from} AND " 
    if not ignore_size :
        sql_query += f" e.trancheEffectifsEtablissement >= '{trancheEffectifs}' AND e.trancheEffectifsEtablissement != 'NN' AND"
    if not ignore_comune :
        sql_query += f" e.codeCommuneEtablissement LIKE '{comune_code}' AND "
    #guaranied stuff
    sql_query += f" e.etatAdministratifEtablissement = '{status}' AND "
    sql_query += f" e.codePostalEtablissement LIKE '{postal_code}' AND "
    sql_query += f" (e.activitePrincipaleEtablissement LIKE '{main_acctivity}' OR e.activitePrincipaleNAF25Etablissement LIKE '{main_acctivity}')"
    print(sql_query)
    corpos = duckdb.sql(sql_query).df().to_dict('records')
    if corpos :
        for corpo in corpos :
            try :
                corpo["trancheEffectifsEtablissement"] = tecodes[corpo["trancheEffectifsEtablissement"]]
            except :
                ...
            try :
                corpo["main_acctivity"] = naf_codes_dict[corpo["activitePrincipaleNAF25Etablissement"]]
            except :
                try :
                    corpo["main_acctivity"] = naf_codes_dict[corpo["activitePrincipaleEtablissement"]]
                except :
                    corpo["main_acctivity"] = "name not found, go google the NAF code bro"
        print(corpos[0])
    return render_template('index.html', amount=len(corpos), corpos=corpos)

        

    


@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static', filename)

def main() :
    app.run(debug=True)





if __name__ == "__main__" :
    main()
