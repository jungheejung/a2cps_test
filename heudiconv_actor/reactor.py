from reactors.utils import Reactor, agaveutils
import copy
import sys
import json


def check_metadata_file(r, file_uri):
    ag = r.client
    manifestUrl = file_uri
    if manifestUrl is None:
        try:
            manifestUrl = context.file_uri
        except Exception as e:
            print("No file_uri specified")
            exit(1)
    (agaveStorageSystem, dirPath, manifestFileName) = \
        agaveutils.from_agave_uri(uri=manifestUrl)
    # get the manifest and start parsing it
    manifestPath = dirPath + "/" + manifestFileName
    try:
        mani_file = agaveutils.agave_download_file(
                    agaveClient=ag,
                    agaveAbsolutePath=manifestPath,
                    systemId=agaveStorageSystem,
                    localFilename=manifestFileName
                    )
    except Exception as e:
        r.on_failure("failed to get manifest {}".format(manifestUrl), e)

    if mani_file is None:
        r.on_failure("failed to get manifest {}".format(manifestUrl), e)

    try:
        manifest = json.load(open(manifestFileName))
    except Exception as e:
        r.on_failure("failed to load manifest {}".format(manifestUrl), e)

    if 'cuff' in manifest['SeriesDescription']:
        job_def = copy.copy(r.settings.cuff)
        r.logger.info("Setting parameters for cuff image")
    if 'rest' in manifest['SeriesDescription']:
        job_def = copy.copy(r.settings.rest)
        r.logger.info("Setting parameters for rest image")
    else:
        print("No cuff/rest specification found for: ", manifest['SeriesDescription'])
        job_def = copy.copy(r.settings.rest)
    return job_def


def submit_fmriprep(r,participant_label, job_def):
    # Create agave client from reactor object
    ag = r.client
    # copy our job.json from config.yml
    parameters = job_def["parameters"]
    # Define the input for the job as the file that
    # was sent in the notificaton message
    parameters["PARTICIPANT_LABEL"] = participant_label
    job_def.parameters = parameters
    #job_def.archiveSystem = system

    # Submit the job in a try/except block
    try:
        # Submit the job and get the job ID
        #job_id = ag.jobs.submit(body=job_def)['id']
        #print(job_id)
        print(json.dumps(job_def, indent=4))
    except Exception as e:
        print(json.dumps(job_def, indent=4))
        print("Error submitting job: {}".format(e))
        print(e.response.content)
        return
    return


def main():
    """Main function"""
    # create the reactor object
    r = Reactor()
    r.logger.info("Hello this is actor {}".format(r.uid))
    # pull in reactor context
    context = r.context
    #print(context)
    # get the message that was sent to the actor
    message = context.message_dict
    print(message)
    # check the file_uri from the message
    file_uri = message['file_uri']
    # depending on the file_uri, set fmriprp parameters for a rest or cuff fmri
    job_def = check_metadata_file(r, file_uri)
    # pull in the participant_label
    participant_label = message['participant_label']
    # use submit function to submit job to fmriprep
    submit_fmriprep(r,participant_label,job_def)



if __name__ == '__main__':
    main()
