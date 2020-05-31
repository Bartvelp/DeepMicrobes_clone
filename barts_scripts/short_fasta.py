from sys import argv
import re


def parse_fasta(fh):
  """Parses a RefSeq fasta file.
  Fasta headers are expected to be like:
  >NR_165790.1 Tardibacter chloracetimidivorans strain JJ-A5 16S ribosomal RNA, partial sequence

  Args:
    fh: filehandle to the fasta file

  Returns:
    A seq_dict like {'name': ['seq1', 'seq2'], etc. }
  """
  fasta_dict = {}
  current_header = ''
  for line in fh:
    line = line.strip()
    if line.startswith('>'):  # it's a header line
      current_header = line
      # Add current species to dict if it doesn't exist
      if not current_header in fasta_dict:
        fasta_dict[current_header] = ['']
      else:
        # add a new entry for this species
        fasta_dict[current_header].append('')
    else:  # Sequence line
      fasta_dict[current_header][-1] += line
  return fasta_dict


if __name__ == "__main__":
  input_fn = argv[1]
  output_fn = argv[2]
  SEQ_LENGTH = 400
  print("Input fasta: {} output fasta: {}".format(input_fn, output_fn))
  fasta_dict = parse_fasta(open(input_fn))
  output_fh = open(output_fn, 'w')

  for header in fasta_dict:
    output_fh.write(header + '\n')
    output_fh.write(fasta_dict[header][0][:SEQ_LENGTH] + '\n')

  output_fh.close()
  print('Done')