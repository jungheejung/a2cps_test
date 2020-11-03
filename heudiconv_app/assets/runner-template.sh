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
                 --subjects ${LIST_OF_SUBJECTS} \
                 --converter {dcm2niix,none}] \
                 --outdir ${OUTDIR} \
                 --locator ${LOCATOR} --conv-outdir ${CONV_OUTDIR} \
                 --anon-cmd ${ANON_CMD} \
                 --heuristic ${HEURISTIC} --with-prov \
                 --ses ${SESSION_FOR_LONGITUDINAL} --bids --overwrite \
                 --datalad] --dbg \
                 --grouping {studyUID,accession_number} --minmeta \
                 --random-seed ${RANDOM_SEED} --dcmconfig ${DCMCONFIG} \


container_exec ${CONTAINER_IMAGE} \
heudiconv \
--dicom_dir_template ${DICOM_DIR_TEMPLATE} | --files ${FILES} \
--subjects ${LIST_OF_SUBJECTS} \
--converter {dcm2niix,none}] \
--outdir ${OUTDIR} \
--locator ${LOCATOR} --conv-outdir ${CONV_OUTDIR} \
--anon-cmd ${ANON_CMD} \
--heuristic ${HEURISTIC} --with-prov \
--ses ${SESSION_FOR_LONGITUDINAL} --bids --overwrite \
--datalad] --dbg \
--grouping {studyUID,accession_number} --minmeta \
--random-seed ${RANDOM_SEED} --dcmconfig ${DCMCONFIG} \


rm -rf ${DIR}
