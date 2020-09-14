import argparse
from principalmapper.analysis import find_risks
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
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', default='default')
    parser.add_argument('--format', default='text', choices=['text', 'json'])
    
    #parsed_args = parser.parse_args(["None"])
    parsed_args = parser.parse_args()
    session = botocore_tools.get_session(parsed_args.profile)
    graph_obj = graph_actions.create_new_graph(session, checker_map.keys())
    
    dateNow = datetime.now()
    unique_outputFile = "output_" + dateNow.strftime("%H-%M-%S-%f")
    s3ObjectName = unique_outputFile + '.svg'


    filePath = LOCAL_STORAGE_PATH + s3ObjectName
    graph_writer.handle_request(graph_obj,filePath,'svg')
    print(filePath)
    uploaded = s3util.upload_to_s3(filePath,bucketName,s3ObjectName)
    return uploaded

if __name__ == '__main__':
    lambda_handler(None, None)

