import requests
import json
import os 

if not os.path.exists('data'): 
    os.makedirs('data')

BASE_URL = "https://sirekap-obj-data.kpu.go.id"
PPWP_URL = BASE_URL + "/wilayah/pemilu/ppwp"
HHCW_PPWP_URL = BASE_URL + "/pemilu/hhcw/ppwp"

provinsi = requests.get(f'{PPWP_URL}/0.json').json()
with open('data/provinsi.json', 'w', encoding='utf-8') as f:
    json.dump(provinsi, f, ensure_ascii=False, indent=4)
if not os.path.exists('data/provinsi'): 
    os.makedirs('data/provinsi')

for provinsi_ in provinsi:
    kotakab = requests.get(f'{PPWP_URL}/{provinsi_["kode"]}.json').json()
    with open(f'data/provinsi/{provinsi_["kode"]}.json', 'w', encoding='utf-8') as f:
        json.dump(kotakab, f, ensure_ascii=False, indent=4)
    if not os.path.exists(f'data/provinsi/{provinsi_["kode"]}'): 
        os.makedirs(f'data/provinsi/{provinsi_["kode"]}')
    for kotakab_ in kotakab:
        kecamatan = requests.get(f'{PPWP_URL}/{provinsi_["kode"]}/{kotakab_["kode"]}.json').json()
        with open(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}.json', 'w', encoding='utf-8') as f:
            json.dump(kecamatan, f, ensure_ascii=False, indent=4)
        if not os.path.exists(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}'): 
            os.makedirs(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}')
        for kecamatan_ in kecamatan:
            desakel = requests.get(f'{PPWP_URL}/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}.json').json()
            with open(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}.json', 'w', encoding='utf-8') as f:
                json.dump(desakel, f, ensure_ascii=False, indent=4)
            if not os.path.exists(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}'):
                os.makedirs(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}')
            for desakel_ in desakel:
                tps = requests.get(f'{PPWP_URL}/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}/{desakel_["kode"]}.json').json()
                with open(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}/{desakel_["kode"]}.json', 'w', encoding='utf-8') as f:
                    json.dump(tps, f, ensure_ascii=False, indent=4)
                if not os.path.exists(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}/{desakel_["kode"]}'): 
                    os.makedirs(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}/{desakel_["kode"]}')
                for tps_ in tps:
                    chasil = requests.get(f'{HHCW_PPWP_URL}/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}/{desakel_["kode"]}/{tps_["kode"]}.json').json()
                    with open(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}/{desakel_["kode"]}/{tps_["kode"]}.json', 'w', encoding='utf-8') as f:
                        json.dump(chasil, f, ensure_ascii=False, indent=4)
