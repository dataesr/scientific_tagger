import time
import datetime
from project.server.main.pf_classifier import pf_classify
from project.server.main.bso_classifier import bso_classify
from project.server.main.asjc_classifier import asjc_classify
from project.server.main.sdg_classifier import sdg_classify

def create_task_classify(arg):
    classification = {}
    classification_type = arg.get('type', 'bso')
    publications = arg.get('publications', [])
    if len(publications) > 10000:
        classification['message'] = "More than 10.000 publications have been submitted. Only the first 10.000 are treated. Please split your request."
        publications = publications[0:10000]

    if "pf" in classification_type:
        publications = pf_classify(publications)
    
    if "bso" in classification_type:
        details = arg.get('details', False)
        publications = bso_classify(publications, details)
    
    if "asjc" in classification_type:
        publications = asjc_classify(publications)
    
    if "sdg" in classification_type:
        publications = sdg_classify(publications)
    
    classification['publications'] = publications
    
    return classification
