**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

## Verify the monitoring installation

*DONE:* run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation

![Kubectl get pods/svc Image](https://github.com/EmekaMomodu/metrics-dashboard/blob/main/answer-img/kubectl-get-pods-svc.png "Kubectl get pods/svc")

## Setup the Jaeger and Prometheus source
*DONE:* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.
![Grafana Home Page Image](https://github.com/EmekaMomodu/metrics-dashboard/blob/main/answer-img/grafana-home-page.png "Grafana Home Page")

## Create a Basic Dashboard
*DONE:* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.
![Grafana Dashboard Prometheus Datasource Image](https://github.com/EmekaMomodu/metrics-dashboard/blob/main/answer-img/grafana-dashboard-with-prometheus-datasource.png "Grafana Dashboard Prometheus Datasource")

## Describe SLO/SLI
*DONE:* Describe, in your own words, what the SLIs are, based on an SLO of *monthly uptime* and *request response time*.

For an SLO of  *monthly uptime*, more particularly the SLO would be;  "monthly uptime of 99.999%".
This implies that our service should be up and running 99.999% of time in a month.
The SLI would be the result from evaluating the time for which the service is in a healthy state, i.e. evaluate the error rates. 
This value gotten from the error rate is the SLI.

For an SLO of *request response time*, more particularly the SLO would be;  "request response time of less than 1000ms".
It means we expect each request response must be 1000ms or less. The SlI for this would be the measure of latency
of the request response time, whose value should be 1000ms or less.

## Creating SLI metrics.
*DONE:* It is important to know why we want to measure certain metrics for our customer. Describe in detail 5 metrics to measure these SLIs.

1. For Latency SLO; The metric to measure the SLI will be the time a request takes to complete, which could be done by 
tracing the time each request takes to complete and computing the average.

2. For uptime SLO; The metric to measure the SLI will be the number of error messages we are seeing in the period of time
i.e. the error rate, this value indicates if we reached the SLO.

3. For saturation SLO; The metric to measure the SLI will be the amount of memory consumed by the service, or
the amount of cpu utilisation of the service.

4. For Network Capacity SLO; The metric to measure the SLI will be the average bandwidth of the service network.

5. For traffic SLO; The metric to measure the SLI will be the number of requests processed successfully in a specific period of time.

## Create a Dashboard to measure our SLIs
*TODO:* Create a dashboard to measure the uptime of the frontend and backend services We will also want to measure to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.

## Tracing our Flask App
*TODO:*  We will create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here.

## Jaeger in Dashboards
*TODO:* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.

## Report Error
*TODO:* Using the template below, write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue.

TROUBLE TICKET

Name:

Date:

Subject:

Affected Area:

Severity:

Description:


## Creating SLIs and SLOs
*TODO:* We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name three SLIs that you would use to measure the success of this SLO.

## Building KPIs for our plan
*TODO*: Now that we have our SLIs and SLOs, create KPIs to accurately measure these metrics. We will make a dashboard for this, but first write them down here.

## Final Dashboard
*TODO*: Create a Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs. Include a screenshot of the dashboard here, and write a text description of what graphs are represented in the dashboard.  
