import os, pandas, csv, re
import math

from biothings import config
logging = config.logger

def load_annotations(data_folder):
    infile = os.path.join(data_folder,"var_drug_ann.tsv")
    assert os.path.exists(infile)
    dat = pandas.read_csv(infile,sep="\t",squeeze=True,quoting=csv.QUOTE_NONE).to_dict(orient='records')
    results = {}
    for rec in dat:

        if not rec["Gene"] or pandas.isna(rec["Gene"]):
            logging.warning("No gene information for annotation ID '%s'", rec["Annotation ID"])
            continue
        _id = re.match(".* \((.*?)\)",rec["Gene"]).groups()[0]
        results.setdefault(_id,[]).append(rec)
        
    for _id,docs in results.items():
        doc = {"_id": _id, "annotations" : docs}
        yield doc
