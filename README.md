# bioproject_elasticsearch
After the user query is processed the match phrase process is conducted using the Elasticsearch API, searching for a phrase match in all three fields of the project description – title, name and description. Scoring method is based on the Lucene’s Practical Scoring Function and returns the score, name, and title of the retrieved document. The archive ID is also returned and appended to the main link in order to return a set of links corresponding to the user query and re-directing to the project data source pages. That same query is then looked up in the thesaurus, and the same process is repeated for its sister pair. 

search_file.py contains index and search functions based on Elasticsearch, as well as a function to find sister query 
app.py processes user query and returns results
script.py contains script for transforming the original dataset to include only the following fields:
1.	Archive ID
2.	Project Description: Name
3.	Project Description: Title
4.	Project Description: Description
