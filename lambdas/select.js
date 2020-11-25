// -- BEGIN BOILERPLATE
const select = async ({ filter, take, offset, ckg, svcRef, ontoKind }) => {
  const filterPrefix = ontoKind[0].toLowerCase() + ontoKind.slice(1);
  const fn = `${filterPrefix}Filter`;

  // Generate the query template
  const query = `query ${fn}($filters: [FieldFilterInput!]!, $take: Int, $offset: Int) {${fn}(filters: $filters, take: $take, offset: $offset) {id subject predicate object language datatype}}`;

  // Generate the filters based on what is present in the simplified input filter
  const filters = Object.keys(filter).reduce((acc, key) => {
    const value = filter[key];
    if (value)
      acc.push({
        fieldName: key,
        op: "==",
        value: { STRING: filter[key] },
      });
    return acc;
  }, []);

  const args = {
    svcRef,
    query,
    variables: { filters, take, offset },
  };

  const res = await ckg(args);
  return res[fn];
};
// --- END BOILERPLATE

// Specialize boilerplate
input.ckg = input.__requestCkg;
input.svcRef = input.__ownerSvcRef;
input.ontoKind = "RDFGraph";

return select(input);
