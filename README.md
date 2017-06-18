# s3ant
Python script for backup data to Amazon S3 bucket

## Require evironment:
* GPL Linux
* Python 2.6 or higher
* Boto3 library

## Usage:

### Set up configure

~~~
$ python /path/to/s3bk/main.py configure
~~~

### Execute backup

~~~
$ python /path/to/s3bk/main.py backup
~~~

Beside that, dry-run can be executed by adding flag `-n`:

~~~
$ python /path/to/s3bk/main.py backup -n
~~~