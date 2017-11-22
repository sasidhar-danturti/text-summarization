gcloud auth activate-service-account --key-file Sasidhar-Project1-015d5a46e21e.json
gsutil cp data/vocab gs://sasidhar-project1-mlengine/data/vocab_data

cd /home/sasidhar_danturti/textsum/

DATA_PATH=gs://sasidhar-project1-mlengine/data/data
VOCAB_PATH=gs://sasidhar-project1.mlengine/data/vocab_data/vocab
TRAIN_PATH=gs://sasidhar-project1-mlengine/data/train
LOG_ROOT=gs://sasidhar-project1-mlengine/data/log_root
JOB_NAME=$1
OUTPUT_PATH=gs://sasidhar-project1-mlengine/data/$JOB_NAME
REGION=us-central1

gcloud ml-engine jobs submit training $JOB_NAME \
	--job-dir $OUTPUT_PATH \
	--runtime-version 1.2 \
    	--module-name trainer.seq2seq_attention\
	--package-path trainer/ \
        --region $REGION \
	--scale-tier STANDARD_1 \
        -- \
    	--data_path $DATA_PATH \
        --vocab_path $VOCAB_PATH \
	--train_dir $TRAIN_PATH \
	--log_root $LOG_ROOT
    	--mode train \

