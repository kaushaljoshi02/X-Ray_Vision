The following steps has to be followed to setup the project on your system.
Python version 3.10.11 will be recommended for best compatibility and to run the project without any compatibility issues. 
A good internet connection is required to set-up the project on your system.
	
	Firstly, we will download the dataset into the project folder in which it will download, extract and arrange the dataset for the training of the model.

Step-1- Start the terminal

Step-2- 	Type python dataset_setup.py and press Enter
	This will start downloading the dataset and arrange them into folder for training. After the Dataset Successfully Downloaded.

Step-3- Now the model has to be trained 
		Type python training.py and press Enter
	This will start the model training. It will take around 30-40 minutes to train depending upon the system. 

Step-4- Now the requirements for the system has to be installed on the system
		Firstly, type cd backend and press Enter
		Now type pip install -r requirements.txt and press Enter
	This will install all the dependencies required for the project.

Step-5- Now activation of the virtual environment has to be done
		Open new terminal window and type venv/scripts/activate and press Enter 
	This will activate the virtual environment of the system to run the project

Step-6- After this type cd backend and press Enter
		Then type python app.py and press Enter 
	This will give you the local host code. To run the localhost CTRL+click on localhost code. A web-browser window will be opened for the 	analysis work and now you can start your work 	into it.