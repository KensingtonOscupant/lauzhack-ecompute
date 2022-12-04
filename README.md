![ecom_banner2](https://user-images.githubusercontent.com/99140162/205484526-ac8a0950-da0b-4499-90a4-2b73b8d833d2.png)

# ECOmpute - compute during green time 🌿

A green energy scheduler for compute-intensive tasks that reduces your carbon footprint 👣

## Table of Contents

[I. Inspiration](#i-Inspiration)  
[II. What it does](#ii-What-it-does)  
[III. How we built it](#iii-How-we-built-it)   
[IV. Challenges we ran into](#iv-Challenges-we-ran-into)  
[V. Accomplishments that we are proud of](#v-Accomplishments-that-we-are-proud-of)  
[VI. What we learned](#vi-What-we-learned)  
[VII. What is next for ECOmpute?](#vii-What-is-next-for-ECOmpute)  


## I. Inspiration 💭
Almost every day, green energy goes to waste because of poor resource management. In times where climate change accelerates faster than ever, it is crucial to cut down on unnecessary energy consumption. Computing is a major factor here. 

## II. What it does 🔧

Our project allows users to schedule compute-intensive, and therefore energy-intensive, tasks in the cloud. It does this by predicting times at which most green energy is available, reducing carbon emissions particularly by leveraging times at which green energy is generated but not used. Our app is built around the concept of maximizing "green time" - the time in which the percentage of renewable energy used for the compute task is above a high threshold, ideally using only sustainable means of generation.

![dashboard_eco](https://user-images.githubusercontent.com/99140162/205486572-f32cd993-53be-4da4-83cf-0982cd98be5b.jpeg)  
*Our dashboard*

## III. How we built it 🏗️
We combined different data sources to get up-to-date information about the weather and the status of the power grid. We combined these sources to (1) get insights into the workings of the power grid and (2) to estimate when the power grid is overloaded and can't handle the amount of produced power. This is very often the case for renewable power plants due to their heterogenous production nature: 

→ Solar panels ☀️  
→ Wind turbines 🌬️

To predict this, we trained a support vector machine. Our predictions take one week of previous data to predict the upcoming three days. The model has an accuracy of ~88.9%.

![event_plot](https://user-images.githubusercontent.com/99140162/205484918-87c48ab6-5969-45fd-ad93-99f01de45239.png)  
*Time series plot of our model*

We built a web app around it that allows the end user to schedule his jobs, e.g. training a resource-intensive machine learning model in the cloud. It provides insights into how much green energy is generated generally, when energy is overproduced and when the jobs requested have been scheduled.

## IV. Challenges we ran into ⚡
Limitations of our frontend framework Streamlit. We had to work around regarding the display of interactive plots with the Plotly. To contribute to the open-source community, we documented the issue and submitted a bug fix.

## V. Accomplishments that we are proud of 🙌
Building a functioning scheduler.

## VI. What we learned 📚
The energy overproduction generated by wind in Western Europe is sometimes impressively large!

## VII. What is next for ECOmpute 🔮
Further improving the accuracy of our models and integration with Docker to execute jobs.
