document.getElementById("search_btn").addEventListener('click', async function(e) {
    e.preventDefault();
    const search_form = document.getElementById("search_form");
    const form_data = new FormData(search_form);
    const daReq = new URLSearchParams(form_data).toString();
    try {
        const response = await fetch('/search?' + daReq, {
            method: 'GET'
        });

        if (!response.ok) throw new Error('Request failed');
        const data = await response.json();
        corpos_root = document.getElementById("allDaCorposInDaArea");
        corpos_root.innerHTML = '';
        corpos_root.appendChild(mkCorposLst(data));

        try {
            const amount = await fetch('/amount', {
                method: 'GET'
            });
            //2 awits cause first get the headers in async and the other get the body, it's so cursed....
            const count = await amount.json();
            document.getElementById("amount").textContent = ("FOUND : " + count.count || "FOUND : 0");

        } catch (error) {
            console.error('Fetch error:', error);
            console.log('Error at amount : ' + error.message);
        }

    } catch (error) {
        console.error('Fetch error:', error);
        console.log('Error at data : ' + error.message);
    }
})

//results_lst_root the ol i use as root element

function mkCorposLst(data) {
    console.log(data);
    const fragment = document.createDocumentFragment();

    data.forEach(corpo => {
        const li = document.createElement('li');
        const res_div = document.createElement('div');
        res_div.className = "result";
        li.appendChild(res_div);

        const name = document.createElement('p');
        name.className = "company_name";
        name.textContent = 'COMPANY NAME : ' + (corpo.denominationUniteLegale || 'no name for that corpo, fuck INSEE');
        res_div.appendChild(name);

        const res_div_flx = document.createElement('div');
        res_div_flx.className = "result-flx";
        res_div.appendChild(res_div_flx);

        const res_div_lft = document.createElement('div');
        res_div_lft.className = "result-left";
        res_div_flx.appendChild(res_div_lft);

        const acctivity = document.createElement('p');
        acctivity.className = "result_field";
        acctivity.textContent = 'acctivity : ' + corpo.acctivity;
        res_div_lft.appendChild(acctivity);
        //////////

        const naf25 = document.createElement('p');
        naf25.className = "result_field";
        naf25.textContent = 'NAF25 : ' + corpo.activitePrincipaleNAF25Etablissement;
        res_div_lft.appendChild(naf25);

        const naf_old = document.createElement('p');
        naf_old.className = "result_field";
        naf_old.textContent = 'NAF OLD : ' + corpo.activitePrincipaleEtablissement;
        res_div_lft.appendChild(naf_old);

        const slavesAmount = document.createElement('p');
        slavesAmount.className = "result_field";
        slavesAmount.textContent = 'number of emplyes : ' + corpo.trancheEffectifsEtablissement;
        res_div_lft.appendChild(slavesAmount);

        const postal_code = document.createElement('p');
        postal_code.className = "result_field";
        postal_code.textContent = 'POSTAL CODE : ' + corpo.codePostalEtablissement;
        res_div_lft.appendChild(postal_code);

        const comune_code = document.createElement('p');
        comune_code.className = "result_field";
        comune_code.textContent = 'CUMUNE CODE : ' + corpo.codeCommuneEtablissement;
        res_div_lft.appendChild(comune_code);

        ///right side & right part div
        const res_div_right = document.createElement('div');
        res_div_right.className = "result-right";
        res_div_flx.appendChild(res_div_right);

        const is_active = document.createElement('p');
        is_active.className = "result_field";
        is_active.textContent = 'IS ACTIVE : ' + (corpo.etatAdministratifEtablissement == 'A' ? 'YES' : 'NO');
        res_div_right.appendChild(is_active);

        const creatorInfo = document.createElement('p');
        creatorInfo.className = "result_field";
        creatorInfo.textContent = "creator Fname : " + (corpo.prenom1UniteLegale == "None" ? "N/A" : corpo.prenom1UniteLegale);
        creatorInfo.textContent += " Lname : " + (corpo.nomUniteLegale == "None" ? "N/A" : corpo.nomUniteLegale);
        res_div_right.appendChild(creatorInfo);


        const is_hq = document.createElement('p');
        is_hq.className = "result_field";
        is_hq.textContent = 'IS HQ : ' + corpo.etablissementSiege;
        res_div_right.appendChild(is_hq);

        const siren = document.createElement('p');
        siren.className = "result_field";
        siren.textContent = 'SIREN :  ' + corpo.siren;
        res_div_right.appendChild(siren);

        const siret = document.createElement('p');
        siret.className = "result_field";
        siret.textContent = 'SIRET :  ' + corpo.siret;
        res_div_right.appendChild(siret);

        const cords = document.createElement('a');
        cords.className = "result_field";
        cords.href = "https://www.google.com/maps?q=" + corpo.lng + ',' + corpo.lat;
        cords.target = "_blank";
        cords.textContent = '' + corpo.lat + ',' + corpo.lng;
        res_div_right.appendChild(cords);

        fragment.appendChild(li);
    });
    return fragment;
}