# CS235 Flix - part 3
![main layout](/screenshots/main_layout.png)

### New Features:
* Integrated with a SQLite database to allow data persistence

### Requirements for this project:
1. PyCharm
2. Python 3

### Instruction for downloading the CS235 Project:
* Please download the CS235 GitHub Repository to a local drive by clicking the green "code" button and select "Download" ZIP
* Extract the ZIP File
* Right click the CS235FlixSkeleton-part-2-master folder and select "Open Folder as PyCharm Community Edition Project" **OR** simply launch PyCharm and select this folder via the open folder option.
* There will be no Python interpreter initially so we need to create a virtual environment and add a python interpreter

### Instruction for setting up Python interpreter and a virtual environment
* Single click the <No interpreter> button located on the bottom right hand corner:
    
    ![No interpreter](/screenshots/no_interpreter.png)
* Select the "Add interpreter" button: 

    ![Add Interpreter](/screenshots/add_interpreter.png)
* While making sure "Virtual Environment" is selected at the menu on the left, select "New environment" to create a new virtual environment and select Python3.7 as your base interpreter. Click "OK" to proceed.

    ![Set up virtual environment](/screenshots/setup_venv.png)

* Double click the wsgi.py script to open the script. PyCharm should prompt you to install any non-installed modules:

    ![Download dependency modules](/screenshots/install_dependency.png)

* Click "**install requirements**" to install all required modules to run CS235 Flix
* Make sure all packages are selected:

    ![Select all packages](/screenshots/select_packages.png)

* Once all packages are installed, you are ready to run and test CS235 Flix

### Running PyTest
* Running Pytest from in terminal:
    * In the PyCharm Terminal, run: <code>python -m pytest</code> or <code>python3 -m pytest</code> depending on your setup.
You should see the following outcome:

    ![Results of running pytest in Terminal](/screenshots/running_pytest.png)

* Running Pytest in PyCharm: 
    * Comment out line 17 and line 18 and uncomment line 13 and line 14 <code>Tests/conftest.py</code>
    * Comment out line 6 and uncomment line 7 in <code>Tests/Unit/test_domain_model/test_movie_file_csv_reader.py</code>
    * Right click the <code>Tests</code> folder and select "Run 'pytest' in 'Tests'"
    * Result of running Pytest in PyCharm:
    
    ![Results of running pytest in PyCharm](/screenshots/running_pytest_in_pycharm.png)

### Running CS235 Flix
* In the PyCharm Terminal, execute <code>flask run</code> command. 

    ![flask run](/screenshots/running_flask_run.png)

* If the terminal does not recognize <code>flask</code> as an internal command, simply double click wsgi.py and right click to run the script

    ![running wsgi.py](/screenshots/run_wsgi_py.png)

You will see a link, either http://127.0.0.1:5000/ or  http://localhost:5000/ appear in the terminal. Single click this link will launch CS235 Flix in your default browser.


# Important Note to Markers
The home page will take a short while to load (10 seconds for me) due to it is extracting movie cover images from an external API, IMDb Py API. This is normal as it takes time for the API to return data.
This same issue will occur when doing an integration testing for the home route.

All other functions of the Web Application have minimal loading time.

If one would like to disable to the API, please go to <code>CS235FlixSkeleton-part-2/CS235Flix/home/home.py</code> and **comment out line 23 and line 24.**
This will stop the Web app from using the IMDb API and the long loading problem will disappear.

My apology to any inconvenience this may cause and I highly appreciate your understanding.


