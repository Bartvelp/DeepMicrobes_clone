# Deepmicrobe for 16s rRNA
Runs fine on CPU for inferance + eval but training is faster on GPU. Installation instructions below in orig README.
# Current problem!
It seems like the accuracy [as can be seen in this graph](https://imgur.com/DZK5A4k) is reset everytime the model starts training and presumably during evaluation or inference. So maybe something to do with the checkpoints?
perhaps init_weights(), which sets the weights to zero, in models/seq2species.py is saved in the graph and thus the problem? Not really sure on how to verify this.
## Activate env
```bash
PATH=/home/WUR/grosm002/DeepMicrobes_clones/pipelines:$PATH
PATH=/home/WUR/grosm002/DeepMicrobes_clone/scripts:$PATH
PATH=/home/WUR/grosm002/DeepMicrobes_clone:$PATH
conda activate py2tf1
```

## To generate a dataset

```bash
python barts_scripts/label_refseq.py bacteria_16s_rrna_all.fa bacteria_16s_rrna_maxlen_500_num_entries_100.fa 500 100 10
```

## Convert dataset to the binary format 
```bash
seq2tfrec_onehot.py --input_seq=bacteria_16s_rrna_maxlen_500_num_entries_100.fa --output_tfrec=bacteria_16s_rrna_maxlen_500_num_entries_100.tfrec --is_train=True
```

## To train
```bash
DeepMicrobes.py \
--input_tfrec=bacteria_16s_rrna_maxlen_500_num_entries_100.tfrec \
--model_name=seq2species \
--model_dir=seq2species_new_weights_500max_100_entries \
--train_epochs=10 \
--encode_method=one_hot \
--num_classes=100 \
--max_len=500
```
## Eval

```bash
DeepMicrobes.py \
--model_name=seq2species \
--model_dir=seq2species_new_weights_500max_100_entries \
--encode_method=one_hot \
--translate=False \
--num_classes=100 \
--max_len=500 \
--running_mode=eval \
--input_tfrec=bacteria_16s_rrna_maxlen_500_num_entries_100.tfrec # Note that this also is the training file
```


## To use prediction
```bash
DeepMicrobes.py \
--model_name=seq2species \
--model_dir=seq2species_new_weights_500max_100_entries \
--encode_method=one_hot \
--translate=False \
--num_classes=100 \
--max_len=500 \
--pred_out=output.txt \
--running_mode=predict_paired_class \
--input_tfrec=bacteria_16s_rrna_maxlen_500_num_entries_100.tfrec
```

## Some stats about my created datasets
| Dataset | Number of species | Number of sequences | File size |
| :------------ | :------------- | :-------------- | :-------------- |
|Original| 20460 | 20460 | 30 MiB
|Small training| 100 | 9589 | 73 MiB
|Large Training| 20460 | 1964192 | 14.7 GiB

# DeepMicrobes original README

DeepMicrobes: taxonomic classification for metagenomics with deep learning <br>
Supplementary data for the paper is available at https://github.com/MicrobeLab/DeepMicrobes-data <br>
<b>IMPORTANT: The new DeepMicrobes (beta version) is available now. Please feel free to contact us if you have any suggestions or encounter any errors.</b>

## Usage

* [Getting start with DeepMicrobes](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/example.md)
* [How to install](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/install.md)
* [How to convert fastq/fasta sequences to TFRecord](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/tfrecord.md)
* [How to make predictions on a metagenome dataset](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/prediction.md)
* [How to generate taxonomic profiles](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/profile.md)
* [How to choose the confidence threshold](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/confidence.md)
* [How to train the DNN model of DeepMicrobes](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/train.md)
* [How to submit to GPUs](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/gpu.md)
* [Suggestions on training a custom model (for advanced users)](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/custom.md)



## Contact

Any issues with the DeepMicrobes framework can be filed with [GitHub issue tracker](https://github.com/MicrobeLab/DeepMicrobes/issues).
We are committed to maintain this repository to assist users and tackle errors. 

<b>Email</b>
* liangqx7@mail2.sysu.edu.cn (Qiaoxing Liang)



## Citation

Qiaoxing Liang, Paul W Bible, Yu Liu, Bin Zou, Lai Wei, [DeepMicrobes: taxonomic classification for metagenomics with deep learning](https://doi.org/10.1093/nargab/lqaa009), NAR Genomics and Bioinformatics, Volume 2, Issue 1, March 2020, lqaa009, https://doi.org/10.1093/nargab/lqaa009
