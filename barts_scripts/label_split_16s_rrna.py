import os
from sys import argv

if __name__ == "__main__":
  input_dir = argv[1]
  output_fn = argv[2]
  print("Input dir: {} output label file: {}".format(input_dir, output_fn))
  output_fh = open(output_fn, 'w')

  all_fns = sorted([os.path.abspath(input_dir + '/' +f) for f in os.listdir(input_dir) if f.endswith('.fa')])
  for i in range(len(all_fns)):
    output_fh.write('{}\t{}\n'.format(all_fns[i], i))
  output_fh.close()
  print('done')