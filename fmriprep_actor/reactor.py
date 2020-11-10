from reactors.utils import Reactor, agaveutils
import copy
import sys
import json


def submit_fmriprep(r,participant_label):
    # Create agave client from reactor object
    ag = r.client
    # copy our job.json from config.yml
    job_def = copy.copy(r.settings.fmriprep)
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
    # get the file name from the message that was sent to the actor
    message = context.message_dict
    print(message)
    # pull in the participant_label
    participant_label = message['participant_label']
    # use submit function to submit job to fmriprep
    submit_fmriprep(r,participant_label)



if __name__ == '__main__':
    main()
