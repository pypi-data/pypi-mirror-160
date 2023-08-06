# Cassandra
## Cassandra's library for Marketing Mix Modeling

To best perform an mmm, you will need to perform these processes in order:
- Data Processing
- Data Analysis
- Trasformations
- Models
- Model Evaluation


##Deploy and install Cassandra
###Deploy
The first thing to do to deploy your library is to create the zip file to deploy in the dist folder, 
run this command and delete the previous version of the zip
```
python setup.py sdist
```

You can now release your new version. While executing the command, you will be asked for the username and password of your pypi account
```
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

###Install
If you haven't installed cassandra yet, run the following command
```
pip install cassandra-mmm
```

otherwise, update the library
```
pip install cassandra-mmm --upgrade
```