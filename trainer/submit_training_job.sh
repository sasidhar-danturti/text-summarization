gsutil cp data/vocab gs://text-summarization-webapp.appspot.com/data/vocab_data
cd /home/sasidhar_danturti/text-summarization-master


DATA_PATH=gs://text-summarization-webapp.appspot.com/data/data
TRAIN_PATH=gs://text-summarization-webapp.appspot.com/data/train
LOG_ROOT=gs://text-summarization-webapp.appspot.com/data/data/log_root
VOCAB_PATH=gs://text-summarization-webapp.appspot.com/data/vocab_data/vocab
MAX_RUN_STEPS=10
JOB_NAME=$1
FILES_TO_EXCLUDE=$2
OUTPUT_PATH=gs://text-summarization-webapp.appspot.com/jobs/$JOB_NAME
REGION=us-central1
gcloud ml-engine jobs submit training $JOB_NAME \
	--job-dir $OUTPUT_PATH \
	--runtime-version 1.2 \
    	--module-name trainer.seq2seq_attention\
	--package-path trainer/ \
        --region $REGION \
        -- \
    	--data_path $DATA_PATH \
        --exclude_files=$FILES_TO_EXCLUDE \
        --vocab_path $VOCAB_PATH \
	--train_dir $TRAIN_PATH \
	--log_root $LOG_ROOT \
    	--mode train \
        --max_run_steps $MAX_RUN_STEPS \
