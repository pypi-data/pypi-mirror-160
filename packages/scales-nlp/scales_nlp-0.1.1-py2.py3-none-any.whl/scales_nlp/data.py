import requests 
import pandas as pd
from scales_nlp.utils import config

def from_docket_viewer(label_name, host_url=config['DOCKET_VIEWER_HOST'], api_key=config['DOCKET_VIEWER_API_KEY']):
    url = host_url + 'train-api'
    args = {'label': label_name, 'api_key': api_key}
    r = requests.post(url, data=args)
    if r.status_code != 200:
        raise Exception(r.text)
    return pd.DataFrame(r.json())
 
