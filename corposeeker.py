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


AMOUNT_FOUND = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods = ['POST', 'GET'])
def td():
    global AMOUNT_FOUND
    if request.method == 'GET' :
        sql_query = "\
        SELECT \
        e.siren, \
        e.siret, \
        u.prenom1UniteLegale, \
        u.nomUniteLegale, \
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
        is_hq = request.args.get('is_hq') #chekbox true or none //done
        ignore_hq = request.args.get('ignore_hq') #chekbox true or none
        ignore_date = request.args.get('ignore_date') #chekbox true or none
        ignore_size = request.args.get('ignore_size') #chekbox true or none
        ignore_comune = request.args.get('ignore_comune') #chekbox true or none
        #there is guarantie you get it
        status = request.args.get('status') #A for active, F for dead //done
        date_creation_from = request.args.get('date_creation_from') #the data when they started hustle //done
        trancheEffectifs = request.args.get('trancheEffectifs') #how many slaves they have //done
        postal_code = request.args.get('postal_code') #where they are 
        comune_code = request.args.get('comune_code') #where exactly they are //done
        main_acctivity = request.args.get('main_acctivity') #what they do
        
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
            AMOUNT_FOUND = len(corpos)
        return render_template('results.json', corpos=corpos)

@app.route('/amount', methods = ['GET'])
def get_amount():
    return "{\"count\" : " + f"{AMOUNT_FOUND}" + "}"
    
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static', filename)

def main() :
    app.run(debug=True)





if __name__ == "__main__" :
    main()
