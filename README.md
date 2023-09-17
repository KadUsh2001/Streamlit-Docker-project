# British Premier League Streamlit Docker Project

Hello and welcome to my British Premier League project. In order to use this project please clone this repo and within the folder where cloning was done please put the following [csv file](https://www.kaggle.com/datasets/quadeer15sh/premier-league-standings-11-seasons-20102021?resource=download)


## Installing requirements

In order to install the requirements please run the following command:

```
pip install -r requirements.txt
```

## Run the App

In order to run the app locally, and within the folder on which rhe repo was cloned, please run the following command:

```
streamlit run air_index.py
```


## Run the app on Docker
In order to run the app on docker,and within the folder on which the repo was cloned, please run the following commands on the terminal in order to access the app:

```
docker build -t streamlit .
docker run -p 8501:8501 streamlit
```

Happy visualizations!

