**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

## Verify the monitoring installation

*DONE:* run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation

![Image: Kubectl get pods,svc Default namespace](https://github.com/EmekaMomodu/metrics-dashboard/blob/main/answer-img/kubectl-get-pods-svc-n-default.png "Pods and Services for Default namespace")
![Image: Kubectl get pods,svc Monitoring namespace](https://github.com/EmekaMomodu/metrics-dashboard/blob/main/answer-img/kubectl-get-pods-svc-n-moniroring.png "Pods and Services for Monitoring namespace")
![Image: Kubectl get pods,svc Observability namespace](https://github.com/EmekaMomodu/metrics-dashboard/blob/main/answer-img/kubectl-get-pods-svc-n-observability.png "Pods and Services for Observability namespace")

## Setup the Jaeger and Prometheus source
*DONE:* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.
![Grafana Home Page Image](https://github.com/EmekaMomodu/metrics-dashboard/blob/main/answer-img/grafana-home-page.png "Grafana Home Page")

## Create a Basic Dashboard
*DONE:* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.
![Grafana Dashboard Prometheus Datasource Image](https://github.com/EmekaMomodu/metrics-dashboard/blob/main/answer-img/sample-grafana-dashboard-with-prometheus-datasource.png "Grafana Dashboard with Prometheus Datasource")

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

4. For Network Capacity SLO; The metric to measure the SLI will be the average bandwidth of the network.

5. For traffic SLO; The metric to measure the SLI will be the number of requests processed successfully in a specific period of time.

## Create a Dashboard to measure our SLIs
*DONE:* Create a dashboard to measure the uptime of the frontend and backend services We will also want to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.
![Uptime, 40x, and 50x Errors of Frontend and Backend Services Image](https://github.com/EmekaMomodu/metrics-dashboard/blob/main/answer-img/uptime-40x-50x-errors.png "Uptime, 40x, and 50x Errors of Frontend and Backend Services")

## Tracing our Flask App
*DONE:*  We will create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here.

[Here is the python file](reference-app/backend/app.py) for the Jaeger span code.

![Jaeger Span measuring the processes of the Backend Service Image](https://github.com/EmekaMomodu/metrics-dashboard/blob/main/answer-img/Jaeger-Span-of-the-Backend-Service.png "Jaeger Span measuring the processes of the Backend Service")

## Jaeger in Dashboards
*DONE:* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.
![Jaeger Traces on Grafana Dashboard Image](https://github.com/EmekaMomodu/metrics-dashboard/blob/main/answer-img/jaeger-traces-on-grafana-dashboard.png "Jaeger Traces on Grafana Dashboard")

## Report Error
*DONE:* Using the template below, write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue.

TROUBLE TICKET

Name: Http Response 500 on backend-service endpoint /api

Date: December 11, 2021, 14:51:50 GMT+1

Subject: Http Error Response 500 on backend-service endpoint /api, failed to resolve

Affected Area:  File path: "./reference-app/backend/app.py", 
                error line:  89, 
                function: my_api

Severity: High

Description: class 'NameError' error  - name 'error' is not defined

![Error shown in jaeger trace Image](https://github.com/EmekaMomodu/metrics-dashboard/blob/main/answer-img/Error-shown-in-jaeger-trace.png "Error shown in jaeger trace")


## Creating SLIs and SLOs
*DONE:* We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name three SLIs that you would use to measure the success of this SLO.

1. Latency
2. Errors
3. Saturation

## Building KPIs for our plan
*DONE*: Now that we have our SLIs and SLOs, create KPIs to accurately measure these metrics. We will make a dashboard for this, but first write them down here.

### 2-3 KPIs per SLI

**Latency**
- request time (in ms) for successful requests
- request time (in ms) for failed requests

**Errors** : It is important to understand what kind of errors are happening in the application. This can be done with Jaeger Tracing.
- 500 errors - 500 errors are more severe: the application is unable to start or completely crashes during execution of a request.
- 400 errors - 404 errors are less severe but also need urgent attention.
- What percentage of overall requests result in 200 as opposed to 400 or 500 errors

**Saturation**
- % CPU usage allocated per service as configured in yaml for example
- % CPU usage available on host
- Total number of requests received over time. Are there spikes in usage?

### Example PromQL Queries for Some Metrics.

**Response types : Flask HTTP requests status 200, 500, 400**
- sum(flask_http_request_total{container=~"backend|frontend|trial",status=~"500|503"}) by (status,container)
- sum(flask_http_request_total{container=~"backend|frontend|trial",status=~"403|404"}) by (status,container)
- sum(flask_http_request_total{container=~"backend|frontend|trial",status=~"200"}) by (status,container)

**Failed responses per second**
- sum(rate(flask_http_request_duration_seconds_count{status!="200"}[30s]))

**Uptime : frontend, trial, backend**
- sum(up{container=~"frontend"}) by (pod)
- sum(up{container=~"trial"}) by (pod)
- sum(up{container=~"backend"}) by (pod)

**Pods health : Pods not ready**
- sum by (namespace) (kube_pod_status_ready{condition="false"})

**Pods health : Pod restarts by namespace**
- sum by (namespace)(changes(kube_pod_status_ready{condition="true"}[5m]))

**Average Response time (Latency)**
- rate(flask_http_request_duration_seconds_sum{status="200"}[1d])/rate(flask_http_request_duration_seconds_count{status="200"}[1d])


## Final Dashboard
*DONE*: Create a Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs. Include a screenshot of the dashboard here, and write a text description of what graphs are represented in the dashboard.
Panels listed are :
- Flask HTTP request total: Status 200
- Flask HTTP request exceptions
- 5xx Errors
- 4xx Errors
- Failed responses per second
- Uptime Frontend Service
- Uptime Backend Service
- Uptime Trial Service
- Pods not in ready state
- Pod restarts per namespace
- CPU Usage
- Latency: Average response time

![Final Dashboard 1 Image](https://github.com/EmekaMomodu/metrics-dashboard/blob/main/answer-img/Final-Dashboard-1.png "Final Dashboard 1")

![Final Dashboard 2 Image](https://github.com/EmekaMomodu/metrics-dashboard/blob/main/answer-img/Final-Dashboard-2.png "Final Dashboard 2")


