
<!-- PROJECT LOGO -->
<br />
<div align="center">
    <h3 align="center">The Crypto Clairvoyant</h3>

  <p align="center">
    A cryptocurrency price forecast web application   
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

This Web application takes advantage of Facebook's Open Source AI module Prophet in order to make forecasts about crypto prices' evolution. Select a coin-pair and a time frame and let it do its magic. The app plots both the actual and predicted values on the first graph from the top. To the right, we have some metrics like median forecasted price and median change in percentage.

## Demo
For more information take a look at the Demo video down below

### Built With

This project is mainly developed in Python. I used Streamlit as a front-end framework due to its Data Science oriented platform. Also, Plotly and Pandas were used for dataframes manipulation and graph plotting.

* [Python]
* [Streamlit]
* [FBProphet]
* [Pandas Dataframes]
* [Plotly]



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

Everything we need is in the Python Package Index (PyPi).
1. Install virtualenv
  ```sh
  pip install virtualenv
  ```
  
2. Create virtual environment
  ```sh
  virtualenv crypto_predictor_venv
  
  ```
3. Activate virtualenv & Install dependencies
  ```sh
  source crypto_predictor_venv/bin/activate
  pip install -r requirements.txt
  ```


<!-- USAGE EXAMPLES -->
## Usage

After installing all the dependencies all we need to do is start the Streamlit server. It will handle both internal and external traffic and port-forwarding in order for your site to be accesible from outside your local network.
  ```sh
  streamlit run crypto_clairvoyant.py
  ```

For any questions regarding Streamlit please refer to their documentation at https://docs.streamlit.io/


<!-- MARKDOWN LINKS & IMAGES -->
[demo-video]: assets/demo-video.mp4
