# Finbox (Tasty Search)

## Installation
Step - 1: clone repository

Step - 2: create a virtual machine and install required packages from requirements.txt and do the base setup.
* `$ cd finbox-test`
* `$ virtualenv -p python3 venv`
* `$ source venv/bin/activate`
* `$ pip install -r requirements.txt`
* `$ ./manage.py migrate`

Step - 2: Download sample data from (https://drive.google.com/file/d/0B8_VSW2-5XmpSTNlZXV4cVdLRUE/view)

Step - 3: Extract `finefoods.txt.gz` to any location you will find foods.txt

Step - 4: Load and index `foods.txt` in our system.
* I have created a custom django command that will load as well as create inverted index of the data from the txt file.
    * `$ ./manage.py upload_data <path-to-foods.txt-file>`
      * if you want to limit the no of documents upload then pass a limit argument
    * `$ ./manage.py upload_data <path-to-foods.txt-file> --limit 1000`
      * It will load only 1000 documents from the .txt file
    * NOTE: Run it only once, if you want to run it again. I would recommend you to first delete the database and then run the migration and then re-run it.

Step - 5: Now, run the server `$ ./manage.py runserver` and go to `http://127.0.0.1:8000`. Done, Happy Searching!

---------------------------------


