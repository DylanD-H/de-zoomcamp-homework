## **Question 1: dlt Version**

1. **Install dlt**:

```
!pip install dlt[duckdb]
```

2. **Check** the version:

```
!dlt --version
```


**Answer**:  
```
dlt 1.6.1
```

## **Question 2: Define & Run the Pipeline (NYC Taxi API)**

```py
import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator


@dlt.resource(name="rides") 
def ny_taxi():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        paginator=PageNumberPaginator(
            base_page=1,
            total_path=None
        )
    )

    for page in client.paginate("data_engineering_zoomcamp_api"): 
        yield page 


pipeline = dlt.pipeline(
    pipeline_name="ny_taxi_pipeline",
    destination="duckdb",
    dataset_name="ny_taxi_data"
)
```
How many tables were created?

**Answer:**

* 4


## **Question 3: Explore the loaded data**

Inspect the table `rides`:

```py
df = pipeline.dataset(dataset_type="default").rides.df()
df
```
What is the total number of records extracted?

**Answer:**
* 10000

## **Question 4: Trip Duration Analysis**

Run the SQL query below to:

* Calculate the average trip duration in minutes.

```py
with pipeline.sql_client() as client:
    res = client.execute_sql(
            """
            SELECT
            AVG(date_diff('minute', trip_pickup_date_time, trip_dropoff_date_time))
            FROM rides;
            """
        )
    # Prints column values of the first row
    print(res)
```
What is the average trip duration?

**Answer:**

* 12.3049
