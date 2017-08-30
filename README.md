# s3ant
Python script for backup data to Amazon S3 bucket like an ant

## Requirement:
* GPL Linux
* Python 2.6 or higher
* Boto3 library

## Usage:

### Set up configure

```bash
$ python /path/to/s3ant/main.py configure
```

### Execute backup

Delete expired backups and add new backup:

```bash
$ python /path/to/s3ant/main.py backup
```

Only add new backup without deleting expired backups:

```bash
$ python /path/to/s3ant/main.py backup --disable-delete
```

Dry-run only:

~~~
$ python /path/to/s3ant/main.py backup -n
~~~