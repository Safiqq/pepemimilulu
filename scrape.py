from datetime import datetime
import requests
import json
import os
import sys

if not os.path.exists('data'): 
    os.makedirs('data')

is_continue = False
continue_from = {
    "provinsi": "",
    "kotakab": "",
    "kecamatan": "",
    "desakel": "",
    "tps": ""
}

if len(sys.argv) > 1:
    is_continue = True
    continue_from["provinsi"] = sys.argv[1]
    if len(sys.argv) > 2: continue_from["kotakab"] = sys.argv[2]
    if len(sys.argv) > 3: continue_from["kecamatan"] = sys.argv[3]
    if len(sys.argv) > 4: continue_from["desakel"] = sys.argv[4]
    if len(sys.argv) > 5: continue_from["tps"] = sys.argv[5]

BASE_URL = "https://sirekap-obj-data.kpu.go.id"
WILAYAH_URL = BASE_URL + "/wilayah"
PPWP_URL = WILAYAH_URL + "/pemilu/ppwp"
HHCW_PPWP_URL = BASE_URL + "/pemilu/hhcw/ppwp"

tpsbelumadachasil = set()

presiden = requests.get(f'{BASE_URL}/pemilu/ppwp.json').json()
with open('data/presiden.json', 'w', encoding='utf-8') as f:
    json.dump(presiden, f, ensure_ascii=False, indent=4)

provinsi = requests.get(f'{PPWP_URL}/0.json').json()
with open('data/provinsi.json', 'w', encoding='utf-8') as f:
    json.dump(provinsi, f, ensure_ascii=False, indent=4)
if not os.path.exists('data/provinsi'): 
    os.makedirs('data/provinsi')
if os.path.exists('data/tpsbelumadachasil.json'): 
    f = open('data/tpsbelumadachasil.json', 'r', encoding='utf-8')
    tpsbelumadachasil = set(json.loads(f.read()))
    f.close()

for provinsi_ in provinsi:
    if is_continue and continue_from["provinsi"] != provinsi_["kode"]: continue
    elif (continue_from["provinsi"] != provinsi_["kode"]) and (continue_from["kotakab"] == ""): is_continue = False

    kotakab = requests.get(f'{PPWP_URL}/{provinsi_["kode"]}.json').json()
    with open(f'data/provinsi/{provinsi_["kode"]}.json', 'w', encoding='utf-8') as f:
        json.dump(kotakab, f, ensure_ascii=False, indent=4)
    if not os.path.exists(f'data/provinsi/{provinsi_["kode"]}'): 
        os.makedirs(f'data/provinsi/{provinsi_["kode"]}')
    for kotakab_ in kotakab:
        if is_continue and continue_from["kotakab"] != kotakab_["kode"]: continue
        elif (continue_from["kotakab"] != kotakab_["kode"]) and (continue_from["kecamatan"] == ""): is_continue = False

        kecamatan = requests.get(f'{PPWP_URL}/{provinsi_["kode"]}/{kotakab_["kode"]}.json').json()
        with open(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}.json', 'w', encoding='utf-8') as f:
            json.dump(kecamatan, f, ensure_ascii=False, indent=4)
        if not os.path.exists(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}'): 
            os.makedirs(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}')
        for kecamatan_ in kecamatan:
            if is_continue and continue_from["kecamatan"] != kecamatan_["kode"]: continue
            elif (continue_from["kecamatan"] != kecamatan_["kode"]) and (continue_from["desakel"] == ""): is_continue = False

            desakel = requests.get(f'{PPWP_URL}/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}.json').json()
            with open(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}.json', 'w', encoding='utf-8') as f:
                json.dump(desakel, f, ensure_ascii=False, indent=4)
            if not os.path.exists(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}'):
                os.makedirs(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}')
            for desakel_ in desakel:
                if is_continue and continue_from["desakel"] != desakel_["kode"]: continue
                elif (continue_from["desakel"] != desakel_["kode"]) and (continue_from["tps"] == ""): is_continue = False

                tps = requests.get(f'{PPWP_URL}/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}/{desakel_["kode"]}.json').json()
                with open(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}/{desakel_["kode"]}.json', 'w', encoding='utf-8') as f:
                    json.dump(tps, f, ensure_ascii=False, indent=4)
                if not os.path.exists(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}/{desakel_["kode"]}'): 
                    os.makedirs(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}/{desakel_["kode"]}')
                for tps_ in tps:
                    if is_continue and continue_from["tps"] != tps_["kode"]: continue
                    else: is_continue = False

                    chasil = requests.get(f'{HHCW_PPWP_URL}/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}/{desakel_["kode"]}/{tps_["kode"]}.json').json()
                    print(f'({datetime.now()})', provinsi_["kode"], kotakab_["kode"], kecamatan_["kode"], desakel_["kode"], tps_["kode"])
                    with open(f'data/provinsi/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}/{desakel_["kode"]}/{tps_["kode"]}.json', 'w', encoding='utf-8') as f:
                        json.dump(chasil, f, ensure_ascii=False, indent=4)
                    if chasil["images"][1] == None:
                        with open('data/tpsbelumadachasil.json', 'w', encoding='utf-8') as f:
                            tpsbelumadachasil.add(f'{HHCW_PPWP_URL}/{provinsi_["kode"]}/{kotakab_["kode"]}/{kecamatan_["kode"]}/{desakel_["kode"]}/{tps_["kode"]}.json')
                            json.dump(list(tpsbelumadachasil), f, ensure_ascii=False, indent=4)