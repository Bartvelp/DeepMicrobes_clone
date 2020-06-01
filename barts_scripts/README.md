PATH=/home/WUR/grosm002/DeepMicrobes_clones/pipelines:$PATH
PATH=/home/WUR/grosm002/DeepMicrobes_clone/scripts:$PATH
PATH=/home/WUR/grosm002/DeepMicrobes_clone:$PATH



seq2tfrec_onehot.py --input_seq=combined_train_small_short.fa --output_tfrec=combined_train_small_short.tfrec --is_train=True


DeepMicrobes.py --input_tfrec=combined_train_small_short.tfrec --model_name=seq2species --model_dir=seq2species_new_weights_small_short --train_epochs=1 --encode_method=one_hot --num_classes=100 --max_len=400


"""
# OLD
# Run order
python split_16srrna_fasta.py ../bacteria_16s_rrna_all.fa ../bacteria_16s/
python label_split_16s_rrna.py ../bacteria_16s ../label_file.tsv
fna_label.py -m ../label_file.tsv -o ../bacteria_16s_labelled/
cat ../bacteria_16s_labelled/* > ../combined_train_labelled.fa
### seq2tfrec_onehot.py --input_seq=../combined_train_labelled.fa --output_tfrec=../combined_train.tfrec --is_train=True
"""