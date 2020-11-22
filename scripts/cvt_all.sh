
#!/usr/bin/env bash

./rdfcsv.py -i ontologies/rdf.ttl -f ttl -o data/rdf.csv
./rdfcsv.py -i ontologies/rdfs.ttl -f ttl -o data/rdfs.csv
./rdfcsv.py -i ontologies/owl.ttl -f ttl -o data/owl.csv
