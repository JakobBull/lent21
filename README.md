
# EduMate


## General

Online learning has been hard, especially with the loneliness and uncertainty of a global pandemic. We are here to take some of the burden and inject some more joy into learning. Think of us as your online learning buddy!

## How to use this

EduMate can be run locally on your device! To do this please first generate you API keys for mathpix at https://mathpix.com/ocr. Clone into the repository by navigating to your target directory and running.

'git clone https://github.com/Jakob2000Cam/lent21.git'

Please insert your API key into 'mathpix.py'.

In order to run this locally please install dependencies. Run

'pip install -r requirements.txt'

Now you can launch the flask server by running 'main.py'

If you wish to retrain the model please use 'create_dataset.py', 'preprocess.py' and 'classifier.py'