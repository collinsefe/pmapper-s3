import argparse
import json
from principalmapper.analysis import find_risks
from principalmapper.analysis import report
from principalmapper.analysis import finding
from principalmapper.graphing import graph_actions
from principalmapper.graphing.edge_identification import checker_map
from principalmapper.util import botocore_tools
from principalmapper.visualizing import graph_writer
import s3util
from datetime import datetime

LOCAL_STORAGE_PATH = "/tmp/"

def lambda_handler(event, context):

    bucketName = event['bucketname']
    bucketRegion = event['bucketregion']
    s3ObjectName = event['s3objectname']
    s3ObjectName2 = event['s3objectname2']

    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', default='default')
    parser.add_argument('--format', default='text', choices=['text', 'json'])
    
    parsed_args = parser.parse_args()
    session = botocore_tools.get_session(parsed_args.profile)
    graph_obj = graph_actions.create_new_graph(session, checker_map.keys())

    dateNow = datetime.now()

    #graph report section
    filePath = LOCAL_STORAGE_PATH + s3ObjectName
    graph_writer.handle_request(graph_obj,filePath,'svg')
    print(filePath)
    uploaded = s3util.upload_to_s3(filePath,bucketName,s3ObjectName)
    
    #analysis report section
    filePath2 = LOCAL_STORAGE_PATH + s3ObjectName2
    reportobj = find_risks.gen_report(graph_obj)
    reportdict = reportobj.as_dictionary()
    with open(filePath2, 'w') as outfile:  
        json.dump(reportdict, outfile)            
    print(filePath2)
    uploaded2 = s3util.upload_to_s3(filePath2,bucketName,s3ObjectName2)

    return uploaded
    return uploaded2

if __name__ == '__main__':
    lambda_handler(None, None)