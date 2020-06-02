PATH=/home/WUR/grosm002/DeepMicrobes_clones/pipelines:$PATH
PATH=/home/WUR/grosm002/DeepMicrobes_clone/scripts:$PATH
PATH=/home/WUR/grosm002/DeepMicrobes_clone:$PATH

conda activate py2tf1
python barts_scripts/label_refseq.py bacteria_16s_rrna_all.fa bacteria_16s_rrna_max_len_1400.fa 1400 2
python barts_scripts/label_refseq.py bacteria_16s_rrna_all.fa bacteria_16s_rrna_max_len_500_num_entries_200.fa 500 200 10

seq2tfrec_onehot.py --input_seq=combined_train_small_short.fa --output_tfrec=combined_train_small_short.tfrec --is_train=True
seq2tfrec_onehot.py --input_seq=bacteria_16s_rrna_max_len_1400.fa --output_tfrec=bacteria_16s_rrna_max_len_1400.tfrec --is_train=True

DeepMicrobes.py --input_tfrec=combined_train_small_short.tfrec --model_name=seq2species --model_dir=seq2species_new_weights_small_short --train_epochs=1 --encode_method=one_hot --num_classes=100 --max_len=400

DeepMicrobes.py --input_tfrec=bacteria_16s_rrna_max_len_500.tfrec --model_name=seq2species --model_dir=seq2species_new_weights_500bp --train_epochs=15 --encode_method=one_hot --num_classes=20456 --max_len=500


DeepMicrobes.py \
	--batch_size=1 --num_classes=20456 \
	--model_name=seq2species --encode_method=one_hot \
	--model_dir=seq2species_new_weights_500bp \
  --max_len=500 \
  --input_tfrec=ecoli_16s_500bp.tfrec \
	--cpus=1 \
	--translate=False \
	--pred_out=output.txt \
	--running_mode=predict_paired_class 
"""
# OLD
# Run order
python split_16srrna_fasta.py ../bacteria_16s_rrna_all.fa ../bacteria_16s/
python label_split_16s_rrna.py ../bacteria_16s ../label_file.tsv
fna_label.py -m ../label_file.tsv -o ../bacteria_16s_labelled/
cat ../bacteria_16s_labelled/* > ../combined_train_labelled.fa
### seq2tfrec_onehot.py --input_seq=../combined_train_labelled.fa --output_tfrec=../combined_train.tfrec --is_train=True
"""