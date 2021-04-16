import swiftclient
import json
import pandas as pd
import gzip
from io import BytesIO, TextIOWrapper
import os

from project.server.main.logger import get_logger

logger = get_logger(__name__)

user = "{}:{}".format(os.getenv("OS_TENANT_NAME"), os.getenv("OS_USERNAME"))
key = os.getenv("OS_PASSWORD")
project_id = os.getenv("OS_TENANT_ID")
project_name = os.getenv("OS_PROJECT_NAME")

#user="6077430106264076:5uVjF2KJJUxg"
#key="gm3vRWbfpmutxR5vSf6WCZyZU48UupnF"
#project_id="32c5d10cb0fe4519b957064a111717e3"
#project_name="Alvitur"

conn = swiftclient.Connection(
    authurl='https://auth.cloud.ovh.net/v3',
    user=user,
    key=key,
    os_options={
            'user_domain_name': 'Default',
            'project_domain_name': 'Default',
            'project_id':project_id,
            'project_name': project_name,
            'region_name':'GRA'},
    auth_version='3'
    )

def exists_in_storage(container, filename):
    try:
        conn.head_object(container, filename)
        return True
    except:
        return False
    
def get_objects(container, path):
    try:
        df = pd.read_json(BytesIO(conn.get_object(container, path)[1]), compression='gzip')
    except:
        df = pd.DataFrame([])
    return df.to_dict("records")
    
def set_objects(all_objects, container, path):
    logger.debug(f"setting object {container} {path}",end=':', flush=True)
    if isinstance(all_objects, list):
        all_notices_content = pd.DataFrame(all_objects)
    else:
        all_notices_content = all_objects
    gz_buffer = BytesIO()
    with gzip.GzipFile(mode='w', fileobj=gz_buffer) as gz_file:
        all_notices_content.to_json(TextIOWrapper(gz_file, 'utf8'), orient='records')
    conn.put_object(container, path, contents=gz_buffer.getvalue())
    logger.debug(f"done",end=':', flush=True)
    return


def delete_folder(cont_name, folder):
    cont = conn.get_container(cont_name)
    for n in [e['name'] for e in cont[1] if folder in e['name']]:
        logger.debug(n)
        conn.delete_object(cont_name, n)
