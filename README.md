# jsonToTSInterface
Script to create a Typescript interface from a JSON or API response.

## Options

- `-f`, `--file`: Source JSON file
- `-u`, `--url`: API url
- `-o`, `--output`: Output file name
- `-h`, `--help`: List of available commands


## Usage:
### Get Typescript interface from API: -u, --url

```
    python ./jsonToTSinterface.py -u http://fakeapi.jsonparseronline.com/posts
```

### Get Typescript interface from a file: -file --file

```
    python ./jsonToTSinterface.py -f file-name.json
```

### Indicate output file: -o, --output

```
    python ./jsonToTSinterface.py -f file-name.json -o interface.ts
```