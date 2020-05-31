# seq2tfrec_onehot.py --input_seq=../bacteria_16s_labelled/label_Zavarzinella_formosa.fa --output_tfrec=../bacteria_16s_tfrecs/test.onehot.tfrec --is_train=True --s
# Import relevant function
import sys
from sys import argv
import os

scripts_path = '/home/bart/DeepMicrobes/scripts/'  # CHANGEME
sys.path.append(scripts_path)
from seq2tfrec_onehot import convert_advance_file


if __name__ == "__main__":
  input_dir = argv[1]
  output_dir = argv[2]
  print("Input labelled fasta dir: {} output dir tf records: {}".format(input_dir, output_dir))

  all_fns = sorted([os.path.abspath(input_dir + '/' +f) for f in os.listdir(input_dir) if f.endswith('.fa')])
  for fasta_fn in all_fns:
    species_name = fasta_fn.split('label_')[-1][:-3]
    if species_name.startswith('_'):
      species_name = species_name[1:]
    tfrec_fn = os.path.abspath(output_dir + '/train_combined') + '.tfrec'
    convert_advance_file(fasta_fn, tfrec_fn, 'fasta')
  print('done')
