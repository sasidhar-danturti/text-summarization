echo '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
#echo $2
filepath=$(realpath trainer)
echo $filepath
cd $filepath
#gcloud config set project sample-app-testing-186113
DATA_PATH=gs://sample-app-testing-186113.appspot.com/data
TRAIN_PATH=gs://sample-app-testing-186113.appspot.com/train
LOG_ROOT=gs://sample-app-testing-186113.appspot.com/log_root
VOCAB_PATH=gs://sample-app-testing-186113.appspot.com/vocab/vocab
JOB_NAME=$1
OUTPUT_PATH=gs://sasidhar-project1-mlengine/$JOB_NAME
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
