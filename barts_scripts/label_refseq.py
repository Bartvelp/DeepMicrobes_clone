from sys import argv
import re


def parse_fasta(fh):
  """Parses a RefSeq fasta file.
  Fasta headers are expected to be like:
  >NR_165790.1 Tardibacter chloracetimidivorans strain JJ-A5 16S ribosomal RNA, partial sequence

  Args:
    fh: filehandle to the fasta file

  Returns:
    A fasta_dict like {'name': ['seq1', 'seq2'], etc. }
  """
  fasta_dict = {}
  current_header = ''
  for line in fh:
    line = line.strip()
    if line.startswith('>'):  # it's a header line
      current_header = line[1:]
      # Add current species to dict if it doesn't exist
      if not current_header in fasta_dict:
        fasta_dict[current_header] = ['']
      else:
        # add a new entry for this species
        fasta_dict[current_header].append('')
    else:  # Sequence line
      fasta_dict[current_header][-1] += line
  return fasta_dict

def label_fasta(fasta_dict, output_fh):
  i = 0
  for header in fasta_dict:
    new_header = '>label|{}|{}\n'.format(i, header)

    sequences = fasta_dict[header]
    for sequence in sequences:
      output_fh.write(new_header)
      output_fh.write(sequence + '\n')
    i += 1


def generate_all_options(fasta_dict, window_length):
  """Generates all possible sequence options for every entry in a fasta_dict.
  Calculates according to a moving window of size window_length, like:
  'BAAAC' -> '[BAAA]C' + 'B[AAAC] -> ['BAAA', 'AAAC']
  
  Args:
    fasta_dict: A sequence dict from parse_fasta
    window_length: int, size of the moving window
  Returns:
    A fasta_dict but with all possible options
  """
  all_sequence_dict = {}
  for header in fasta_dict:
    all_sequence_dict[header] = []
    for sequence in fasta_dict[header]:
      seq_length = len(sequence)
      if seq_length < window_length:  # can't get window
        continue
      num_windows = seq_length - window_length + 1
      for win_start in range(num_windows):
        win_end = win_start + window_length
        window = sequence[win_start:win_end]
        all_sequence_dict[header].append(window)
  return all_sequence_dict

if __name__ == "__main__":
  input_fn = argv[1]
  output_fn = argv[2]
  max_len = int(argv[3])
  print("Input refseq: {} output labbeled fasta: {}".format(input_fn, output_fn))
  fasta_dict = parse_fasta(open(input_fn))
  all_options_dict = generate_all_options(fasta_dict, max_len)
  label_fasta(fasta_dict, open(output_fn, 'w'))
  print('--num_classes={} --max_len={}', len(fasta_dict.keys), max_len)
  print('Done')
