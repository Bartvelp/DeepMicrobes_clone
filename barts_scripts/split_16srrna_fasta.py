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
  current_species = ''
  for line in fh:
    line = line.strip()
    if line.startswith('>'):  # it's a header line
      line_parts = line.split()
      current_species = line_parts[1] + ' ' + line_parts[2]
      # Add current species to dict if it doesn't exist
      if not current_species in fasta_dict:
        fasta_dict[current_species] = ['']
      else:
        # add a new entry for this species
        fasta_dict[current_species].append('')
    else:  # Sequence line
      fasta_dict[current_species][-1] += line
  return fasta_dict

def save_fasta(species, sequence, fh):
  fh.write('>{}\n'.format(species))
  fh.write(sequence + '\n')
  fh.close()

if __name__ == "__main__":
  input_fn = argv[1]
  output_dir = argv[2]
  print("Input refseq: {} output dir: {}".format(input_fn, output_dir))
  fasta_dict = parse_fasta(open(input_fn))
  for species in fasta_dict:
    output_fn = output_dir + re.sub('\W+', '_', species) + '.fa'
    output_fh = open(output_fn, 'w')
    sequences = fasta_dict[species]
    save_fasta(species, sequences[0], output_fh)
