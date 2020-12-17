# Import Agave runtime extensions
. _lib/extend-runtime.sh

# Allow CONTAINER_IMAGE over-ride via local file
if [ -z "${CONTAINER_IMAGE}" ]
then
    if [ -f "./_lib/CONTAINER_IMAGE" ]; then
        CONTAINER_IMAGE=$(cat ./_lib/CONTAINER_IMAGE)
    fi
    if [ -z "${CONTAINER_IMAGE}" ]; then
        echo "CONTAINER_IMAGE was not set via the app or CONTAINER_IMAGE file"
        CONTAINER_IMAGE="jurrutia/ubuntu17"
    fi
fi

# BUG Input Directory ${BIDS_DIRECTORY} not defined
# using some bash tricks to get if from the participant label
DIR=*/*-${PARTICIPANT_LABEL}
DIR=$(echo ${DIR} | cut -d "/" -f1)
echo Input is ${DIR}

mkdir -p  ${OUTPUT_DIR}
PYTHONPATH=""

# Usage: container_exec IMAGE COMMAND OPTIONS
#   Example: docker run centos:7 uname -a
#            container_exec centos:7 uname -a

# Echo command to std out
echo container_exec ${CONTAINER_IMAGE} \
                  heudiconv \
                 --dicom_dir_template ${DICOM_DIR_TEMPLATE} | --files ${FILES} \
                 ${LIST_OF_SUBJECTS} \
                 ${CONVERTER} \
                 --outdir ${OUTDIR} \
                 ${LOCATOR} ${CONV_OUTDIR} ${ANON_CMD} \
                 --heuristic ${HEURISTIC} \
                 ${SESSION_FOR_LONGITUDINAL} ${BIDS} ${OVERWRITE} \
                 ${DATALAD} ${DCMCONFIG}


container_exec ${CONTAINER_IMAGE} \
heudiconv \
--dicom_dir_template ${DICOM_DIR_TEMPLATE} | --files ${FILES} \
${LIST_OF_SUBJECTS} \
${CONVERTER} \
--outdir ${OUTDIR} \
${LOCATOR} ${CONV_OUTDIR} ${ANON_CMD} \
--heuristic ${HEURISTIC} \
${SESSION_FOR_LONGITUDINAL} ${BIDS} ${OVERWRITE} \
${DATALAD} ${DCMCONFIG} 

rm -rf ${DIR}




"parameters": [

{
  "id": "LIST_OF_SUBJECTS",
  "value": {
    "default": "outputs",
    "description": "list of subjects - required for dicom template. If not provided, DICOMS would first be “sorted” and subject IDs deduced by the heuristic",
    "type": "string",
    "visible": true,
    "required": true
  }
},
{
  "id": "CONVERTER",
  "details": {
    "description": "",
    "argument": "--converter ",
    "showArgument": true,
  },
  "value": {
    "default": "dcm2niix",
    "type": "enumeration",
    "enumValues": ["dcm2niix", "none"],
    "visible": true,
    "required": false
  }
},
{
  "id": "OUTDIR",
  "value": {
    "default": "outputs",
    "description": "output directory for conversion setup (for further customization and future reference. This directory will refer to non-anonymized subject IDs",
    "type": "string",
    "visible": true,
    "required": true
  }
},




{
  "id": "ANON_CMD",
  "details": {
    "argument": "--anon-cmd ",
    "showArgument": true,
    "description": "command to run to convert subject IDs used for DICOMs to anonymized IDs. Such command must take a single argument and return a single anonymized ID. Also see –conv-outdir"
  },
  "value": {
    "default": 0,
    "description": "command to run to convert subject IDs used for DICOMs to anonymized IDs. Such command must take a single argument and return a single anonymized ID. Also see –conv-outdir",
    "type": "flag",
    "visible": true,
    "required": false
  }
},




{
  "id": "HEURISTIC",
  "value": {
    "default": "heuristic file (python)",
    "description": "Name of a known heuristic or path to the Pythonscript containing heuristic",
    "type": "string",
    "visible": true,
    "required": true
  }
},

{
  "id": "SESSION_FOR_LONGITUDINAL",
  "details": {
    "argument": "--ses ",
    "showArgument": true,
    "description": "session for longitudinal study_sessions, default is none"
  },
  "value": {
    "default": 0,
    "type": "flag",
    "visible": true,
    "required": false
  }
},

{
  "id": "BIDS",
  "details": {
    "argument": "--bids ",
    "showArgument": true,
    "description": "flag for output into BIDS structure"
  },
  "value": {
    "default": 0,
    "type": "flag",
    "visible": true,
    "required": false
  }
},

{
  "id": "OVERWRITE",
  "details": {
    "argument": "--overwrite ",
    "showArgument": true,
    "description": "flag to allow overwriting existing converted files"
  },
  "value": {
    "default": 0,
    "type": "flag",
    "visible": true,
    "required": false
  }
},
{
  "id": "DATALAD",
  "details": {
    "argument": "--datalad ",
    "showArgument": true,
    "description": "Store the entire collection as DataLad dataset(s). Small files will be committed directly to git, while large to annex. New version (6) of annex repositories will be used in a “thin” mode so it would look to mortals as just any other regular directory (i.e. no symlinks to under .git/annex). For now just for BIDS mode."
  },
  "value": {
    "default": 0,
    "type": "flag",
    "visible": true,
    "required": false
  }
},



{
  "id": "DCMCONFIG",
  "value": {
    "default": "outputs",
    "description": "JSON file for additional dcm2niix configuration",
    "type": "string",
    "visible": true,
    "required": true
  }
}]
