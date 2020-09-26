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
    
    '''
    unique_outputFile2 = "analysis_report_" + dateNow.strftime("%H-%M-%S-%f")
    s3ObjectName2 =  'analysis_report.json'
    filePath2 = LOCAL_STORAGE_PATH + s3ObjectName2
    print(filePath2)
    '''
    
    #analysis report section
    reportobj = find_risks.gen_report(graph_obj)
    reportdict = reportobj.as_dictionary()
    with open('/tmp/analysis_report.json', 'w') as outfile:  
        json.dump(reportdict, outfile)            
    s3ObjectName2 = 'analysis_report.json'
    filePath2 = LOCAL_STORAGE_PATH + s3ObjectName2
    print(filePath2)

    #s3 upload section
    uploaded = s3util.upload_to_s3(filePath,bucketName,s3ObjectName)
    uploaded2 = s3util.upload_to_s3(filePath2,bucketName,s3ObjectName2)

    return uploaded
    return uploaded2

if __name__ == '__main__':
    lambda_handler(None, None)

Analysis 
principalmapper.analysis.find_risks: 
function gen_findings_and_print: dumps findings in markdown(text)/JSON format to stdout. Wraps around gen_report, which can be used instead for custom formatting by pulling Report and Finding objects.

principalmapper.analysis.report: 
class Report: a simple object containing metadata about generated findings (account ID, date, version of PMapper). 
principalmapper.analysis.finding: 
class Finding: a simple object containing data about a risk to the AWS account. 
 


