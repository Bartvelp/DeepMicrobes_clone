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


def generate_all_options(fasta_dict, window_length, keep_every_nd=1, num_entries=0):
  """Generates all possible sequence options for every entry in a fasta_dict.
  Calculates according to a moving window of size window_length, like:
  'BAAAC' -> '[BAAA]C' + 'B[AAAC] -> ['BAAA', 'AAAC']
  
  Args:
    fasta_dict: A sequence dict from parse_fasta
    window_length: int, size of the moving window
    keep_every_nd: int; Keep every nd sequence like sequences[0::nd]
    num_entries: Maximal number of entries, 0 if all
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
    # check if we added any windows, otherwise delete entry
    if len(all_sequence_dict[header]) == 0:
      del all_sequence_dict[header]
    elif keep_every_nd is not 1:
      all_sequence_dict[header] = all_sequence_dict[header][0::keep_every_nd]
  if num_entries > 0:
    # Select the "first" n keys
    kept_headers = list(all_sequence_dict.keys())[0:num_entries]
    # Create a new dict with those keys
    all_sequence_dict = {header: all_sequence_dict[header] for header in kept_headers}
  return all_sequence_dict


def print_fasta_stats(fasta_dict):
  """Prints some statistics of a sequence dictionary.

  Args:
    fasta_dict: dictionary of structure {'name': ['seq1', 'seq2'], etc. }

  Side Effect:
    Prints to standard out.
  """
  all_seqs = [seq for sublist in fasta_dict.values() for seq in sublist]
  seq_lens = [len(seq) for seq in all_seqs]
  num_seqs = len(all_seqs)
  max_len = max(seq_lens)
  min_len = min(seq_lens)
  print('NUM ENTRIES: ', len(fasta_dict.keys()))
  print('NUM SEQS TOTAL: ', num_seqs)
  print('MAX LEN: ', max_len)
  print('MIN LEN: ', min_len)
  


if __name__ == "__main__":
  input_fn = argv[1]
  output_fn = argv[2]
  max_len = int(argv[3])
  num_entries = int(argv[4]) # Number of classes to keep, 0 for all
  keep_every_nd = int(argv[5]) # 1 keeps all, 2 throws away half, 3 2/3ds etc. 1/nd
  print("Input refseq: {} output labbeled fasta: {}".format(input_fn, output_fn))

  fasta_dict = parse_fasta(open(input_fn))
  print('FASTA stats orig')
  print_fasta_stats(fasta_dict)
  all_options_dict = generate_all_options(fasta_dict, max_len, keep_every_nd, num_entries)
  print('FASTA stats new all options')
  print_fasta_stats(all_options_dict)

  label_fasta(all_options_dict, open(output_fn, 'w'))
  print('--num_classes={} --max_len={}'.format(len(all_options_dict.keys()), max_len))
  print('Done')
