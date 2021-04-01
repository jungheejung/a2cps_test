from reactors.utils import Reactor, agaveutils
import copy
import sys
import json
import os
import psycopg2
from datetime import datetime




def vbr_read(r):
    
    vbr_user = os.getenv("_vbr_user")
    vbr_host = os.getenv("_vbr_ip")
    vbr_pass = os.getenv("_vbr_pass")

    print(
        vbr_host,
        "a2cps",
        vbr_user,
        vbr_pass)

    conn = psycopg2.connect(
        host=vbr_host,
        database="a2cps",
        user=vbr_user,
        password=vbr_pass)
    cur = conn.cursor()
    cur.execute("SELECT * FROM data_event;")
    print(cur.fetchone())

    return

def open_connection():
    vbr_user = os.getenv("_vbr_user")
    vbr_host = os.getenv("_vbr_ip")
    vbr_pass = os.getenv("_vbr_pass")

    conn = psycopg2.connect(
        host=vbr_host,
        database="a2cps",
        user=vbr_user,
        password=vbr_pass)
    return conn

def insert_into_table(table, columns, data):
    conn = open_connection()
    cur = conn.cursor()
    # create a '%s' string for every data element, stupid postgres module
    number_of_data_s = ','.join(['%s' for data in data])
    SQL = "INSERT INTO {} ({}) VALUES ({});".format(table,columns,
                                                    number_of_data_s)
    #print(SQL)
    cur = conn.cursor()
    cur.execute(SQL, data)
    #print(cur.query)
    conn.commit()
    return

def get_key_for_table(key_column,table,query_column,query_value):
    conn = open_connection()
    cur = conn.cursor()
    SQL = "SELECT  {} FROM {} WHERE {}='{}';".format(key_column,table,
                                                    query_column,query_value)
    print(SQL)
    # alternatively for likes
    # SELECT  dataset_id FROM dataset WHERE description LIKE 'baseline visit for subject 1';
    # SQL = "SELECT  {} FROM {} WHERE {} LIKE '{}';".format(key_column,table,query_column,query_value)
    cur.execute(SQL)
    key_id = cur.fetchall()
    #print(key_id)
    if key_id == []:
        print("no value found for query: ", SQL)
        return
    if len(key_id) > 1:
        print("multiple mathes for query: ", SQL)
        return key_id
    else:
        # returns list, get first list element and
        # un-tuple-fy it with [0]
        return key_id[0][0]

def write_dataset_entry(data):
    columns = 'data_source,title,description,contained_in' 
    insert_into_table('dataset',columns,data)
    return

def check_and_write_datasets(subject_id):
    #subject_id = 'subject_1'
    subject_title = 'subject_' + subject_id
    subject_dataset_key = get_key_for_table('dataset_id', 'dataset', 'title', 
                                            subject_title)
    if subject_dataset_key is None:
        # make subject datasetkey
        # make visit dataset key
        print('creating subject dataset')
        data = (1,subject_title,"dataset for subject " + str(subject_id), 1)
        write_dataset_entry(data)
        subject_dataset_key = get_key_for_table('dataset_id', 'dataset', 
                                                'title', subject_title)
        
    baseline_visit_protocol_key = get_key_for_table('protocol_id','protocol','name','baseline_visit')

    baseline_query = 'baseline visit for {}'.format(' '.join(subject_title.split('_')))
    baseline_visit_dataset_key = get_key_for_table('dataset_id','dataset','description',baseline_query)
    if baseline_visit_dataset_key is None:
        # create baseline visit dataset entry
        print('creating baseline visit dataset') 
        data = (1,"event"+str(baseline_visit_protocol_key) +'_1',"baseline vist for subject " + str(subject_id), subject_dataset_key)
        write_dataset_entry(data)
        baseline_visit_dataset_key = get_key_for_table('dataset_id','dataset','description',baseline_query)
        
    image_protocol_key = get_key_for_table('protocol_id','protocol','name','image upload')

    return subject_dataset_key, baseline_visit_protocol_key, baseline_visit_dataset_key, image_protocol_key

def write_data_event(protocol_key,rank,subject_id,site_key,dataset_key):
    columns = "protocol,rank,event_ts,event_count,subject,performed_by,status,reason,dataset"
    data = (protocol_key,rank,datetime.now(),1,subject_id,site_key,None,None,dataset_key)
    insert_into_table('data_event',columns,data)
    return

def submit_file_job():
    job_def = copy.copy(r.settings.file_job)

def main():
    """Main function"""
    # create the reactor object
    r = Reactor()
    r.logger.info("Hello this is actor {}".format(r.uid))
    # pull in reactor context
    context = r.context
    print(context)
    # get the message that was sent to the actor
    message = context.message_dict
    # ex UI
    site = message['site']
    subject_id = message['subject_id']
    session = message['session']
    zipfile = message['zipfile']
    outdir = message['outdir']

    # check datasets table for subject and baseline visit entries
    # and write entries if they don't exist
    (subject_dataset_key, baseline_visit_protocol_key, 
    baseline_visit_dataset_key, image_protocol_key) = \
        check_and_write_datasets(subject_id)

    # upload event
    site_key = get_key_for_table('organization_id','organization','name',site)
    write_data_event(image_protocol_key,1,subject_id,site_key,baseline_visit_dataset_key)

    # submit file entry
    #submit_file_job(zipfile,)
 
    #vbr_read(r)


if __name__ == '__main__':
    main()
