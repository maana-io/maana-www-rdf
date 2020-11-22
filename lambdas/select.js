const select = async ({
  graphRef,
  filter,
  take,
  offset,
  __requestCkg: ckg,
}) => {
  // The graph being queried is dynamic
  const kindPrefix = graphRef.kind[0].toLowerCase() + graphRef.kind.slice(1);
  const fn = `${kindPrefix}Filter`;

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
    svcRef: graphRef.svc,
    query,
    variables: { filters, take, offset },
  };

  // throw new Error(JSON.stringify(args))

  const res = await ckg(args);
  return res[fn];
};

return select(input);
