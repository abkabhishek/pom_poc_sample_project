# pom_poc_sample_project
Sample project of pom poc in python

prerequisite:

 - python3.x
 - virtualenv
 - put chromdriver in "usr/local/bin" on MacOS, For windows, chromedriver is already placed in "Files/drivers/win/chromedriver"

To setup and run the test follow these steps:

1. clone the project
2. create virtual environemnt install requirements using following command (MacOS):
  
    cd <projectroot>
    pythont3 -m virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
  
3. Run tests
   cd AutoTest
   pytest -s Tests/Test_sample.py -v
    
    
Test Data is available in Hotel.json in TestData folder. Currently the test will run two times as per two json object in test data file.
