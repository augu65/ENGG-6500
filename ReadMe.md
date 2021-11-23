Jonah Stegman 0969112

Requirements: 
-
- pandas
- numpy
- sklearn
- selenium
- matplotlib
- seaborn

Running the code:
-
To get the country codes for the dataset lookup.py must be run. The outputted file will be out2.csv
To get the page rank for the dataset pagerank.py must be run. The outputted file will be called out4.csv
Both of these scripts pull their data from malicious_phish.csv.

To extract features from either of these outputted files run feature_extraction.py. This will give you all of the 
extracted features that are found in the dataset.

To get raw statistics on the dataset run statistics.py (note: some of statistics.py functions require classification to be 
done).

To train and test the classifier run classifier.py (note: classifier.py also has visualization functions for the data.
additionally, it can give you an output of the fp and fn for the  dataset.)
fp and fn can be visualized using the statistics.py script.
