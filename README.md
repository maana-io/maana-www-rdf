# maana-www-rdf

Maana Q support for the Semantic Web and Linked Data

## Mapping to Kinds

```
rdfs:Class -> Kind
  rdfs:isDefinedBy -> Workspace/Service
  rdfs:label -> Kind name
  rdfs:comment -> Kind description
  rdfs:subClassOf -> embedded reference to superclass (Kind) instance

rdf:Property -> Kind field
  rdfs:isDefinedBy -> Workspace/Service
  rdfs:label -> Field name
  rdfs:comment -> Field description
  rdfs:domain -> Kind with field
  rdfs:range -> Field type
```
