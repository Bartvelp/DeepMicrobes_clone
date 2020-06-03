PATH=/home/WUR/grosm002/DeepMicrobes_clones/pipelines:$PATH
PATH=/home/WUR/grosm002/DeepMicrobes_clone/scripts:$PATH
PATH=/home/WUR/grosm002/DeepMicrobes_clone:$PATH
conda activate py2tf1

# To generate a dataset
python barts_scripts/label_refseq.py bacteria_16s_rrna_all.fa bacteria_16s_rrna_maxlen_500_num_entries_1000.fa 500 1000 10

# Convert dataset to the binary format 
seq2tfrec_onehot.py --input_seq=bacteria_16s_rrna_maxlen_500_num_entries_1000.fa --output_tfrec=bacteria_16s_rrna_maxlen_500_num_entries_1000.tfrec --is_train=True

# To train
DeepMicrobes.py \
--input_tfrec=bacteria_16s_rrna_maxlen_500_num_entries_1000.tfrec \
--model_name=seq2species \
--model_dir=seq2species_new_weights_500max_100_entries \
--train_epochs=10 \
--batch_size=1024 \
--encode_method=one_hot \
--num_classes=1000 \
--max_len=500

# To use prediction
DeepMicrobes.py \
--batch_size=1 \
--model_name=seq2species \
--model_dir=seq2species_new_weights_500max_200entries \
--encode_method=one_hot \
--translate=False \
--num_classes=200 \
--max_len=500 \
--pred_out=output.txt \
--running_mode=predict_paired_class \
--input_tfrec tbd.tfrec

DeepMicrobes.py --input_tfrec=bacteria_16s_rrna_maxlen_500_num_entries_1000.tfrec --model_name=seq2species --model_dir=seq2species_new_weights_500max_100_entries --train_epochs=10 --encode_method=one_hot --num_classes=1000 --max_len=500
