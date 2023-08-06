# Elastic CSV Loader

This command line utility loads csv file into an elasticsearch index, using a provided yaml config file.

`load-csv` considerations:

- CSV files MUST include a header with field names
- Header field names will be used as elastic index fields
- A `@timestamp` and `date`  fields will be added to all indexed docs
  - A `date` logic date could be forced through command parameter.
- Depending on `elastic_index.data_format.parent_data_object` value, all original csv header fields
  will be arranged under a `data` parent object.

Indexed data will use the same field names that

`download-index` considerations:

- If csv file is an existing file the download process will **append** data including headers
- You have to rename or delete previous csv file if you want to start fresh.

## Install

### Dependencies

- `Python` 3.8 or higher
- `pip` package manager

```shell
pip install --upgrade elasticcsv
```

## Run

### Elastic Connection Config

Connection configuration is based in a YAML text file (`connection.yaml`) that must be present in
command directory.

Sample `connection.yaml`


```yaml
elastic_connection:
  proxies:
    http: "http://user:pass@proxy.url:8080"
    https: "http://user:pass@proxy.url:8080"
  user: myuser
  password: mypassword
  node: my.elastic.node
  port: 9200
elastic_index:
  data_format:
    parent_data_object: true
```

### Run command

```text
❯ python elasticcsv/csv2es.py load-csv --help
Usage: csv2es.py load-csv [OPTIONS]

  Loads csv to elastic index

Options:
  --csv PATH               CSV File  [required]
  --csv_offset INT         CSV File offset
  --sep TEXT               CSV field sepator  [required]
  --index TEXT             Elastic Index  [required]
  --csv-date-format TEXT   date format for *_date columns as for ex:
                           '%Y-%m-%d'
  --logic_date [%Y-%m-%d]  Date reference for interfaces
  -d, --delete-if-exists   Flag for deleting index before running load
  --help                   Show this message and exit.

```
> Python date formats references: [String Format Time](https://www.geeksforgeeks.org/how-to-format-date-using-strftime-in-python/)

```text
❯ python elasticcsv/csv2es.py download-index --help
Usage: csv2es.py download-index [OPTIONS]

  Download index to csv file

Options:
  --csv PATH              CSV File  [required]
  --sep TEXT              CSV field sepator  [required]
  --index TEXT            Elastic Index  [required]
  -d, --delete-if-exists  Flag for deleting csv file before download
  --help                  Show this message and exit.

```
Example:

```text
csv2es load-csv --csv ./pathtomyfile/file.csv --index myindex --sep ";"

csv2es download-index --csv ./pathtomyfile/file.csv --index myindex --sep ";" -d
```
