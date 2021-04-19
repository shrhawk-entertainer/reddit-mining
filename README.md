# Reddit Crypto Mining

## Requirements:
1. This app required a MongoDB instance is running on the default host and port. Assuming you have [downloaded and installed](http://www.mongodb.org/display/DOCS/Getting+Started) MongoDB, you can start it like so
```shell
$ mongod
```
2. You will need your own Reddit account and API credentials for PRAW (used for mining reddit).Refer to this [guide](https://github.com/JosephLai241/URS/blob/master/docs/How%20to%20Get%20PRAW%20Credentials.md) to get your credentials, then update the environment variables located in .env.
3. The crypto symbols can be seen using mongo-db under collection named **crypto_symbols**


Before running the app assuming that **python 3.7.xx** is installed on development machine

1. Create virtual enviroment with python3.7.xx
```shell
$ python3.7 -m venv envname
```
2. Activate the virtual enviroment
```shell
$ source envname/bin/activate
```
3. Install requisite packages:
```shell
$ pip install -r requirements.txt
```
4. Run Reddit Scrapper:
```shell
$ python app.py
