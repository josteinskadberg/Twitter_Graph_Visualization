# Twitter_Graph_Visualization
An python Fask application that scrapes twitter hashtags with Selenium and render graph visualization with Bokeh and Networkx. The application crawls twitter and scrapes hashtags in a breath first search pattern. It then renders a graph with tags as nodes with edges to neighbour tags. 

before you run you will need to set up a virtual environment with virtualenv: 

pip install virtualenv

activate virtualenv: 
windows: 
./env/Scripts/activate.ps1 

Mac/OS 
source mypython/bin/activate

Then you will need to install the dependecies from requirements.txt 

pip install -r requirements.txt 

start application with 
python<3> app.py 

If you should whant to deploy the application change the SECRET_KEY parameter in instance/config.py to a proper key and gitignore the instance folder. (for example os.urandom(16))
