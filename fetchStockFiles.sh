#!/bin/env sh

#get fresh links here : https://www.data.gouv.fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret
stockEtablisementURL="https://static.data.gouv.fr/resources/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/20260901-090503/stock-stocketablissement-parquet.parquet"
stockUniteLegalURL="https://static.data.gouv.fr/resources/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/20260901-084858/stock-stockunitelegale-parquet.parquet"

#get fresh link here : https://www.data.gouv.fr/datasets/geolocalisation-des-etablissements-du-repertoire-sirene-pour-les-etudes-statistiques
geodataURL="https://static.data.gouv.fr/resources/geolocalisation-des-etablissements-du-repertoire-sirene-pour-les-etudes-statistiques/20260821-081708/geoloc-geolocalisationetablissement-sirene-pour-etudes-statistiques-parquet.parquet"


echo -e "\033[34m ▄▀▄▄▄▄   ▄▀▀▀▀▄   ▄▀▀▄▀▀▀▄  ▄▀▀▄▀▀▀▄  ▄▀▀▀▀▄       ▄▀▀▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▀█▄▄▄▄  ▄▀▀▄ █  ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄ \033[0m"
sleep 0.1
echo -e "\033[34m█ █    ▌ █      █ █   █   █ █   █   █ █      █     █ █   ▐ ▐  ▄▀   ▐ ▐  ▄▀   ▐ █  █ ▄▀ ▐  ▄▀   ▐ █   █   █ \033[0m"
sleep 0.2
echo "▐ █      █      █ ▐  █▀▀█▀  ▐  █▀▀▀▀  █      █        ▀▄     █▄▄▄▄▄    █▄▄▄▄▄  ▐  █▀▄    █▄▄▄▄▄  ▐  █▀▀█▀  "
sleep 0.1
echo "  █      ▀▄    ▄▀  ▄▀    █     █      ▀▄    ▄▀     ▀▄   █    █    ▌    █    ▌    █   █   █    ▌   ▄▀    █  "
sleep 0.2
echo -e "\033[31m ▄▀▄▄▄▄▀   ▀▀▀▀   █     █    ▄▀         ▀▀▀▀        █▀▀▀    ▄▀▄▄▄▄    ▄▀▄▄▄▄   ▄▀   █   ▄▀▄▄▄▄   █     █   \033[0m"
sleep 0.1
echo -e "\033[31m█     ▐           ▐     ▐   █                       ▐       █    ▐    █    ▐   █    ▐   █    ▐   ▐     ▐   \033[0m"
sleep 0.2
echo -e "\033[31m▐                           ▐                               ▐         ▐        ▐        ▐                  \033[0m"
sleep 0.2
echo -e "                                                                                              by mickdevil"
sleep 0.2

echo -e "\n\n"
echo "curling stockFiles from insee"

echo "stock etablisements :"
[ -f ./stockFiles/stock-stocketablissement-parquet.parquet ] && echo "stock etablisements is present" || curl $stockEtablisementURL  -o ./stockFiles/stock-stocketablissement-parquet.parquet
echo "stock unité legal :"
[ -f ./stockFiles/stock-stockunitelegale-parquet.parquet ] && echo "stock unité legal is present" || curl $stockUniteLegalURL  -o ./stockFiles/stock-stockunitelegale-parquet.parquet
echo "geodata stock :"
[ -f ./stockFiles/geoloc-geolocalisationetablissement-sirene-pour-etudes-statistiques-parquet.parquet ] && echo "geodata is present" || curl $geodataURL  -o ./stockFiles/geoloc-geolocalisationetablissement-sirene-pour-etudes-statistiques-parquet.parquet

#echo -e "\n\n"
#echo "runing the thing in docker in "
#echo "3"
#sleep 0.3
#echo "2"
#sleep 0.3
#echo "1"
#sleep 0.3
#echo "GO!!"







