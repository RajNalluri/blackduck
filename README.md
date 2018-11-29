# blackduck

Steps followed
1. Download Blackduck zip report. It contains source.csv and security.csv files
2. The security.csv file contain non-CVSSv3 scores. So first get the "new_security.csv" file.
3. Use this "new_security.csv" file and join it with source.csv file to get the ssclub.csv

Step 2 details:
1. First create a file with all cve's and their CVSSv2 and CVSSv3 scores:
	a) Download all the zipped files for all years from NVD feeds
	   Script to do this : "downloadZips()" function from "create_cve_scores_file.py" 
	   Inputs to the script: NONE.
	   Ouptut: This script creates a new "downloads" directory(as mentioned in the function), downloads the zip feeds for all years (as mentioned in the function) into the "downloads" directory.

	b) Extract the jsons from the zips:
	   Script to do this: "extractjsons()" function from "create_cve_scores_file.py"
	   Inputs to the script: The script looks for the "downloads" directory. The "downloads" directory should be in the same folder as that of the "create_cve_scores_file.py" file.
	   Ouptput: The scripts creates "jsons" directory in "downloads" directory and extracts all json files from zips into this "jsons" directory"
	   
	c) Create a csv file with all CVE's from all json files, those CVE's v2 scores and v3 scores.
	   Script to do this: "create_mapping_file()" function from "create_cve_scores_file.py"
	   Inputs: The script looks for json files in "downloads/jsons" directory. Club all CVE's in those jsons into "final_mapping.csv" csv file. This csv file contains information about all cve's, their v2 and v3 scores.
	   
	d) Create a "new_security.csv" file by making use of "security.csv" file and "final_mapping.csv" file.
	   Script to do this: "finalscore.py" 
	   Inputs: The following files should be present in the directory along with "finalscore.py":
			i) "final_mapping.csv" (input file with all cve's, their v2 and v3 scores. This file is obtained from above step i.e., step (c) )
			ii) "security.csv" (input security.csv file from blackduck report)
			iii) "input_to_finalscore.txt"
			iv) "list_bd_cves.txt"
			v) "new_security_file.txt". All the three .txt files are inputs to "sqlite"
	
