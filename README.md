nohup python3 -u scrape.py {prov} {kotakab} {kecamatan} {desakel} {tps} > output.log 2> error.log & echo $! > process_id.txt