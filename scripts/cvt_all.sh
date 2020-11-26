
#!/usr/bin/env bash

# scripts/rdfcsv.py -i ontologies/rdf.ttl -f ttl -o data/rdf.csv
# scripts/rdfcsv.py -i ontologies/rdfs.ttl -f ttl -o data/rdfs.csv
# scripts/rdfcsv.py -i ontologies/owl.ttl -f ttl -o data/owl.csv
# scripts/rdfcsv.py -i ontologies/foaf.rdf -f xml -o data/foaf.csv
# scripts/rdfcsv.py -i ontologies/skos.rdf -f xml -o data/skos.csv
# scripts/rdfcsv.py -i ontologies/time.ttl -f ttl -o data/time.csv
# scripts/rdfcsv.py -i ontologies/time-gregorian.ttl -f ttl -o data/time-gregorian.csv
scripts/rdfcsv.py -i ontologies/dublin_core_abstract_model.ttl -f ttl -o data/dublin_abstract_model.csv
scripts/rdfcsv.py -i ontologies/dublin_core_elements.ttl -f ttl -o data/dublin_core_elements.csv
scripts/rdfcsv.py -i ontologies/dublin_core_terms.ttl -f ttl -o data/dublin_core_terms.csv
scripts/rdfcsv.py -i ontologies/dublin_core_type.ttl -f ttl -o data/dublin_core_type.csv
