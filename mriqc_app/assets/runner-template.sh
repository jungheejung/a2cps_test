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
               mriqc \
               ${DIR} \
               ${OUTPUT_DIR} \
               participant --participant-label ${PARTICIPANT_LABEL} \
               --n_procs 16 \
               --mem_gb 8 \
               --ica --fft-spikes-detector --correct-slice-timing

container_exec ${CONTAINER_IMAGE} \
               mriqc \
               ${DIR} \
               ${OUTPUT_DIR} \
               participant --participant-label ${PARTICIPANT_LABEL} \
               --n_procs 16 \
	             --mem_gb 8 \
               --ica --fft-spikes-detector --correct-slice-timing


rm -rf ${DIR}
