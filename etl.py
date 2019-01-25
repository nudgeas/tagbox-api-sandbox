from config import tagbox
from logs.logger import log

import requests
import json
import jwt


verbose = True
test = True
log('etl start')



# Extract data from Tagbox

tagbox_doc_endpoint = tagbox.document_endpoint
tagbox_tag_endpoint = tagbox.geotag_endpoint
#tagbox_params = {'doc_id': tagbox.test_doc_id}
#tagbox_params = tagbox.test_docs
tagbox_params = {}
tagbox_secret = tagbox.secret
jwt_algorithm = 'HS256'
jwt_headers = {'kid': tagbox.key}

tagbox_token = jwt.encode(
    tagbox_params,
    tagbox_secret,
    jwt_algorithm,
    jwt_headers
).decode()

tagbox_headers = {
    'Authorization': 'Bearer {}'.format(tagbox_token)
}

if verbose:
    print('Tagbox request:\n{}\n'.format('\n'.join([
        tagbox_tag_endpoint, 
        str(tagbox_params),
        str(jwt_headers),
        str(tagbox_headers)]))
    )

tagbox_tag_request = requests.get(
    tagbox_tag_endpoint,
    params=tagbox_params,
    headers=tagbox_headers
)
tagbox_tag_results = tagbox_tag_request.text
tagbox_tags = json.loads(tagbox_tag_results)

log('{} tagbox tag results'.format(len(tagbox_tags)))
if verbose:
    print('Tagbox tags:\t{}'.format(len(tagbox_tags)))
    #print('Tags: {}'.format(tagbox_tags))

unique_tagbox_docs = {}
for tag in tagbox_tags:
    if tag['created_at'] > '2019-01-22 19':
        unique_tagbox_docs[tag['postId']] = {} 

for document_id in unique_tagbox_docs.keys():
    doc_params = {'document_id': document_id}
    doc_request_token = jwt.encode(
        doc_params,
        tagbox_secret,
        jwt_algorithm,
        jwt_headers
    ).decode()
    doc_headers = {
        'Authorization': 'Bearer {}'.format(doc_request_token)
    }
    tagbox_doc_request = requests.get(
        tagbox_doc_endpoint, 
        params=doc_params, 
        headers=doc_headers
    )
    doc_result = tagbox_doc_request.text
    #print(doc_result)
    doc = json.loads(doc_result)
    print('document request results {}'.format(len(doc)))
    unique_tagbox_docs[document_id] = doc[0]

log('{} tagbox doc results'.format(len(unique_tagbox_docs)))
#if verbose:
#    print('Tagbox docs: {}'.format(len(unique_tagbox_docs)))
#    for doc_id, doc in unique_tagbox_docs.items():
#print('\n{}\n{}\n{}'.format(doc_id, doc['url'][:20], doc['title'][:20]))



