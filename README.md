# DataSciencePipeline
### Performed end to end data science pipeline tasks

#### Phase 1: Scrap and extract data from websites, store them in CSV files

Written 2 web crawlers (EasyScrape for IMDB and ScrapeOff for Rotten Tomatoes) to scrap data from IMDB and Rotten Tomatoes, then extract target data from the HTML files scrapped, and store them in 2 separate CSV files.

#### Phase 2: Data transformation, cleaning and visualisation

* Write codes to calculate the percentage of missing values, and propose solutions to fill up the missing values.

* Classify attribute types and analyse the values for each attribute (length, synonyms attribute values, misplaced of             values)

* Find anomalies among attribute values through data visualiation like density plot histogram or box plot.

* Write codes to transform 2 tables to have the same schema to prepare for blocking and entity matching.

#### Phase 3. Blocking on data to reduce the number of tuple pairs matched

*Note: Blocking is not the same as matching. The purpose of blocking is to get rid of as many tuples that are clearly not 
matched. For example, given table A and table B, each having 1000 tuples, we will not want to match 1 million tuples in the 
Cartesian Product. Blocking serves the purpose of reducing the number of pairs we have to consider.*
   
* Perform blocking using string matching techniques like equivalence, edit distance, overlap measure and Jaccard measure. 

* Successfully reduced 150192621 potential tuple pairs (Cartesian product) to 23331 potential tuple pairs, which is 0.016%      of the total size.

* Ensure that there's no false negative (leaking out positive data) by randomly sampling several tuples and checking them 
  against golden data.

#### Phase 4: Entity matching

* Creates golden data and fills up null values

* Find the best matcher among Decision Tree, Logistic Regression, Random Forest, Support Vector Machine and Naive Bayes         learning algorithm through 6 iterations of 4-fold cross validation and debugging.

* Achieves a precision and recall of 1.0 in our test set.

* Train the classifier on our training set and test set and perform entity matching on entire dataset.

#### Phase 5: Data Analysis
 * Perform matching on entire dataset and perform multiple linear regression and OLAP exploration to gain insights on the        data.
 * It's being found that:
   - The longer the duration of the film is, the more likey it will be rated with high score. In addtion, the more earnings        the film obtained, the more likely it will be rated with high scores.
   - Movie categories that are being rated highest are Musical & Performing Arts; Action & Adventure; Animation; Art House &      International; Special Interest; and Documentary,Kids & Family.
   - Furthermore, it was being found that people tend to love movie that are labelled with R (for violence, pervasive              language, some sexual content and drug use).
   - The most popular movies are usually in English, Mandarin, Japanese.
   

*Note: To run the Web Crawlers EasyScrape and ScapeOff, go to `phase_1/WebCrawlers/easyscape` or `phase_1/WebCrawlers/scrapeoff` and follows the README instructions there.*


   

   
