# Best Papers Awards
Web repository of best papers awards.

## Deployment of the web application

### Requirements
- [Python 3.10+](https://www.python.org/)
- [MongoDB](https://www.mongodb.com/)

### Download and install
1. Install [Python 3.10+](https://www.python.org/)
2. Install [MongoDB](https://www.mongodb.com/)
3. Clone this repository and enter into the main directory:

    `git clone https://github.com/jmhorcas/bestpapersawards`

    `cd bestpapersawards` 
4. Create a virtual environment: 
   
   `python -m venv env`
5. Activate the environment: 
   
   In Linux: `source env/bin/activate`

   In Windows: `.\env\Scripts\Activate`
   
6. Install the dependencies: 
   
   `pip install -r requirements.txt`

   
### Execution
1. Launch MongoDB with the associated database:
      
   In Windows: `"C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe" --dbpath="<path_to_db>"`

   where `<path_to_db>` is the path to the directory where the MongoDB database resides.

2. Run the server locally:

   `python  app.py`

Access to the web service in the localhost:

http://127.0.0.1:5000
