# BGPRouting_ASRelationship

This is the github repository for our final FCN project "Finding Relationships between ASes using the AS Route information".

To setup this project you need to follow the instructions below:           
  * Fast Run  
      1. Make sure you have installed python 2.7 on your computer
      2. Download the repository and run the two separate files "relationship\_finder.py" and "relationship\_finder\_tier1.py" using the command "python <filename>.py"
      3. The output for relationship\_finder.py gives you the information before adding Tier1 ASes and the output for relationship\_finder\_tier1.py gives you the information after that. Below you can see some of these informations:
          1. Number of ASes that we had and Number of trace routes between them
          2. The accuracy of finding p2p relationship
          3. The accuracy of finding p2c relationship
          4. The confusion matrix for p2p and p2c Relationships

  * Adding your own trace routes
      1. Go to "https://atlas.ripe.net"
      2. Click on "Measurements, Maps, and Tools" on the left side bar and go to "Measurements"
      3. Now choose the filters you want to apply to your search of trace routes.
      4. You can download any of those files provided by this filter from RIPE Atlas.
      5. Put the downloaded files in <project folder>/data/probes
      6. Run "process\_atlas\_json\_file.py" by these three input arguments "data/probes" "data/GeoIPASNum.dat" "data/output". 
         The first is the folder that contains all your Atlas files. The second is the address to the dat file that parses these files and returns the ASes. The third is our output file to write the trace routes in. 
      7. Now you can go back to the "Fast Run" and go through the steps to get your final results.
