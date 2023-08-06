import requests
from retry import retry

from ebi_eva_common_pyutils.logger import logging_config as log_cfg


logger = log_cfg.get_logger(__name__)

eutils_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
esearch_url = eutils_url + 'esearch.fcgi'
esummary_url = eutils_url + 'esummary.fcgi'
efetch_url = eutils_url + 'efetch.fcgi'
ensembl_url = 'http://rest.ensembl.org/info/assembly'


@retry(tries=3, delay=2, backoff=1.2, jitter=(1, 3))
def get_ncbi_assembly_dicts_from_term(term, api_key=None):
    """Function to return NCBI assembly objects in the form of a list of dictionaries based on a search term."""
    payload = {'db': 'Assembly', 'term': '"{}"'.format(term), 'retmode': 'JSON'}
    if api_key:
        payload['api_key'] = api_key
    req = requests.get(esearch_url, params=payload)
    req.raise_for_status()
    data = req.json()
    assembly_dicts = []
    if data:
        assembly_id_list = data.get('esearchresult').get('idlist')
        payload = {'db': 'Assembly', 'id': ','.join(assembly_id_list), 'retmode': 'JSON'}
        if api_key:
            payload['api_key'] = api_key
        req = requests.get(esummary_url, params=payload)
        req.raise_for_status()
        summary_list = req.json()
        for assembly_id in summary_list.get('result', {}).get('uids', []):
            assembly_dicts.append(summary_list.get('result').get(assembly_id))
    return assembly_dicts


@retry(tries=3, delay=2, backoff=1.2, jitter=(1, 3))
def get_ncbi_taxonomy_dicts_from_term(term, api_key=None):
    """Function to return NCBI taxonomy objects in the form of a list of dictionaries based on a search term."""
    payload = {'db': 'Taxonomy', 'term': '"{}"'.format(term), 'retmode': 'JSON'}
    if api_key:
        payload['api_key'] = api_key
    req = requests.get(esearch_url, params=payload)
    req.raise_for_status()
    data = req.json()
    taxonomy_dicts = []
    if data:
        taxonomy_dicts = get_ncbi_taxonomy_dicts_from_ids(data.get('esearchresult').get('idlist'))
    return taxonomy_dicts


@retry(tries=3, delay=2, backoff=1.2, jitter=(1, 3))
def get_ncbi_taxonomy_dicts_from_ids(taxonomy_ids, api_key=None):
    """Function to return NCBI taxonomy objects in the form of a list of dictionaries
    based on a list of taxonomy ids."""
    taxonomy_dicts = []
    payload = {'db': 'Taxonomy', 'id': ','.join(taxonomy_ids), 'retmode': 'JSON'}
    if api_key:
        payload['api_key'] = api_key
    req = requests.get(esummary_url, params=payload)
    req.raise_for_status()
    summary_list = req.json()
    for taxonomy_id in summary_list.get('result', {}).get('uids', []):
        taxonomy_dicts.append(summary_list.get('result').get(taxonomy_id))
    return taxonomy_dicts
