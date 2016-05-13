# BGPRouting_ASRelationship

This is the github repository for our final FCN project "Finding Relationships between ASes using the AS Route information".

To setup this project you need to follow the instructions:
1. Fast Run
  1.1. Make sure you have installed python 2.7 on your computer
  1.2. Download the repository and run the two separate files "relationship_finder.py" and "relationship_finder_tier1.py" using the command "python <filename>.py"
  1.3. The output for relationship_finder.py gives you the information before adding Tier1 ASes and the output for relationship_finder_tier1.py gives you the information after that. Below you can see some of these informations:
    1.3.1. Number of ASes that we had and Number of trace routes between them
    1.3.2. The accuracy of finding p2p relationship
    1.3.3. The accuracy of finding p2c relationship
    1.3.4. The confusion matrix for p2p and p2c Relationships

2. Adding your own trace routes
2.1. Go to "https://atlas.ripe.net"
2.2. Click on "Measurements, Maps, and Tools" on the left side bar and go to "Measurements"
2.3. Now choose the filters you want to apply to your search of trace routes.
2.4. You can download any of those files provided by this filter from RIPE Atlas.
2.5. Put the downloaded files in <project folder>/data/probes
2.6. Run "process_atlas_json_file.py" by these three input arguments "data/probes" "data/GeoIPASNum.dat" "data/output"
The first is the folder that contains all your Atlas files. The second is the address to the dat file that parses these files and returns the ASes. The third is our output file to write the trace routes in. 
2.7. Now you can go to the Fast Run and go through the steps to get your final results.
