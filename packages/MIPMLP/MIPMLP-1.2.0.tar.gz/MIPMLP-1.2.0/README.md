

## Preprocessing for 16S values.
The input file for the preprocessing should contain detailed unnormalized OTU/Feature values as a biom table, the appropriate taxonomy as a tsv file,
and a possible tag file, with the class of each sample.
The tag file is not used for the preprocessing, but is used to provide some statistics on the relation between the features and the class.
You can also run the preprocessing without a tag file.  
### input                                                               
Here is an example of how the input OTU file should look like : ([file example](https://mip-mlp.math.biu.ac.il/download-example-files))

<img src="https://drive.google.com/uc?export=view&id=18s12Zxc4nOHjk0vr8YG8YQGDU0D8g7wp" alt="drawing" width="400" height="450"/>

### Parameters to the preprocessing
Now you will have to select the parameters for the preprocessing.
1. The taxonomy level used - taxonomy sensitive dimension reduction by grouping the bacteria at
 a given taxonomy level. All features with a given representation at a given taxonomy
 level will be grouped and merged using three different methods: Average, Sum or Merge (using PCA then followed by normalization).
2. Normalization - after the grouping process, you can apply two different normalization methods. the first one is the log (10 base)scale. in this method <br/>
x → log10(x + ɛ),where ɛ is a minimal value to prevent log of zero values. <br/>
The second methos is to normalize each bacteria through its relative frequency.<br/>
> If you chose the Log normalization, you now have four standardization <br/>possibilities:<br/>
> a) No standardization<br/>
> b) Z-score each sample<br/>
> c) Z-score each bacteria<br/>
> d) Z-score each sample, and Z-score each bacteria (in this order)<br/>
When performing relative normalization, we either dont standardize the results
or performe only a standardization on the bacteria.<br/>
3. Dimension reduction - after the grouping, normalization and standardization you can choose from two Dimension reduction method: PCA or ICA. If you chose to apply a Dimension reduction method, you will also have to decide the number of dimensions you want to leave.


### How to use
use MIPMLP.preprocess(input_df)
####parameters:
taxonomy_level 4-7 , default is 7<br/>
taxnomy_group : sub PCA, mean, sum, default is mean<br/>
epsilon: 0-1<br/>
z_scoring: row, col, both, No, default is No<br/>
pca: (0, 'PCA') second element always PCA. first is 0/1<br/>
normalization: log, relative, default is log<br/>
norm_after_rel: No, relative, default is No<br/>

### output
The output is the processed file.

<img src="https://drive.google.com/uc?export=view&id=1UPdJfUs_ZhuWFaHmTGP26gD3i2NFQCq6" alt="drawing" width="400" height="400"/>