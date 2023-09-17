# British Premier League Streamlit Docker Project

Hello and welcome to my British Premier League project. In order to use this project please clone this repo and within the folder where cloning was done please put the following csv file:

https://www.kaggle.com/datasets/quadeer15sh/premier-league-standings-11-seasons-20102021?resource=download

When this is done, just run the following commands on the terminal in order to access the app:

```
docker build -t streamlit .
docker run -p 8501:8501 streamlit.
```

After this, paste the following URL into your browser of choice:

http://0.0.0.0:8501

Happy visualizations!

