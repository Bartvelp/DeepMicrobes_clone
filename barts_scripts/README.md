# Run order
python split_16srrna_fasta.py ../bacteria_16s_rrna_all.fa ../bacteria_16s/
python label_split_16s_rrna.py ../bacteria_16s ../label_file.tsv
fna_label.py -m ../label_file.tsv -o ../bacteria_16s_labelled/
cat ../bacteria_16s_labelled/* > ../combined_train_labelled.fa
seq2tfrec_onehot.py --input_seq=../combined_train_labelled.fa --output_tfrec=../combined_train.tfrec --is_train=True