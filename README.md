# TDA.Python
Part of TDA Thesis

Program aims at clustering words by creating levenshtein distance smilimarity matrix between each of then and then running Affinity propagation algorithm (http://scikit-learn.org/stable/modules/generated/sklearn.cluster.AffinityPropagation.html). 
Duplicates are removed and word before processing are simplified to its stem version by means of porter2 algorithm (http://snowball.tartarus.org/algorithms/english/stemmer.html).

In console/ package you can find af_cluster.py script that can be executed as command  line program. 

## Reguirements

pip install --user numpy scipy distance stemming sklearn   
Anaconda or WinPython installation is advised 

## Usage

### Input
Takes file with words. Format is simple, word per line.

### Params 
-i <input_file_path>  
-o <output_file_path>  
-s <True|False> - compute silhouette coefficient  
-a <"auto"|"dynamic"|signed_integer> -affinity_preference_factor  
    auto - will be set to the median of the input similarities.  
    dynamic - minimum similarity value  
    signed_integer - any signed integer. Greater values result in fewer clusters.  

### Output 
Produces csv file with following columns: <lowercase(orginal_word)>, <stem(orginal_word)>, <group_label>

