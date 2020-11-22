
#!/usr/bin/env bash

scripts/rdfcsv.py -i ontologies/rdf.ttl -f ttl -o data/rdf.csv
scripts/rdfcsv.py -i ontologies/rdfs.ttl -f ttl -o data/rdfs.csv
scripts/rdfcsv.py -i ontologies/owl.ttl -f ttl -o data/owl.csv
scripts/rdfcsv.py -i ontologies/foaf.rdf -f xml -o data/foaf.csv
