import json
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware

from schemas import ChatbotSchema
from search_chatbot_lab_assistant import chatbot


async def e_com_chatbot(request) -> json:
    schema = await request.json()
    # calling the backend model
    model_response = chatbot(schema.get('query'))
    return JSONResponse({'response': model_response})


app = Starlette(debug=False, routes=[
    Route('/chatbot', e_com_chatbot, methods=['POST']),
])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],  # Add OPTIONS here
    allow_headers=["*"],
)

'''
- Since Holistic provides the flexibility to write SQL SELECT statements for creating Transform Models. we can leverage 
various SQL optimisation techniques such as proper indexing, optimising join operations, 
using appropriate WHERE clauses,and avoiding unnecessary calculations or sub-queries to improve query performance.

- We can leverage the materialised views provided by Holistic for frequently accessed Transform Models to pre-compute 
and store the results.
    Need to consider below factors while working on materialised views -
    - Refresh Frequency
    - Incremental Refresh
    - Indexing and Partitioning
    - Query Complexity
    - Refresh Triggers

- Query caching - we can configure appropriate caching strategies based on the frequency of data updates and the 
requirements of the reporting or dash-boarding workflows.
- Query scheduling and automation (Need to check how we can do this in Holistic)
'''

'''
Questions related to Holistic

1 - How does Holistic optimize query performance, especially for large datasets or complex transformations?
2 - How does Holistic leverage materialized views for frequently accessed Transform Models, and what strategies are 
used to optimize their performance?
3 - Need to know more about refresh mechanisms for materialized views and the impact on query response time?
4 - What monitoring tools and capabilities does Holistic provide to track query performance, identify bottlenecks, 
and optimize resource utilization?
5 - Are they using asynchronous processing?
'''

'''
Materialised view concepts and suggestions:-

When working with materialized views, especially with large datasets, it's essential to consider several factors to 
ensure efficient performance and optimal resource utilization. Below are some key considerations:

Storage Requirements:
Materialized views store pre-computed query results, which can consume significant storage space, especially for large 
datasets. We need to evaluate the storage requirements of materialized views and ensure that we have sufficient storage 
capacity available in database system.

Refresh Frequency:
We have to determine the appropriate refresh frequency for materialized views based on the volatility of the underlying 
data and the requirements of reporting and analysis workflows. Frequent refreshes ensure that the materialized views 
remain up-to-date but may increase the overhead on the database server.

Incremental Refresh:
Implement incremental refresh strategies for materialized views to optimize refresh operations, especially for large 
datasets. Instead of recomputing the entire result set, only update the materialized view with changes since the last 
refresh. This reduces the computational overhead and minimizes the impact on database performance.

Indexing and Partitioning:
Have to consider indexing and partitioning strategies to optimize query performance on materialized views, 
especially for large datasets. Identify the columns frequently used in queries and create appropriate indexes to 
accelerate query execution. Partitioning materialized views based on relevant criteria can also improve 
query performance by distributing data across multiple partitions.

Query Complexity:
Evaluating the complexity of the underlying queries used to populate materialized views. Complex queries may result in 
longer refresh times and increased resource utilization during refresh operations. Simplifying and optimising queries 
where possible to minimize the computational overhead.

Resource Management:
Monitor resource usage, including CPU, memory, and disk I/O, during materialized view refresh operations. Ensure that 
the database server has sufficient resources available to handle concurrent refresh operations without impacting 
the performance of other database activities.

Refresh Triggers:
Implementing refresh triggers or schedules based on off-peak hours or low-traffic periods to minimize the impact 
on database performance during refresh operations, especially for large materialized views.

Performance Testing:
Conducting performance testing and benchmarking of materialized views to evaluate their impact on query performance and 
resource utilization, especially with large datasets. Identifying any performance bottlenecks or scalability issues and 
fine-tune configurations accordingly.
'''
