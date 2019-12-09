Logging Data
============

Storing historical data, while a critical piece of a comprehensive controls system, is not inherently part of dripline itself.
Services are generally designed to be self contained and largely stateless; but they can very naturally produce data to be ingested and stored elsewhere.

Logging System General Principles
---------------------------------
When logging data in dripline, there is a deliberate separate of the logic which produces the data to be logged, from the act of actually saving it (typically to some sort of database).
This is achieved by sending messages on the `alerts` exchange.
Each message's routing key indicates the general type of the data (first word in the routing key) and the specific name for the data (second word in the routing key, often the same as the name of the endpoint sending the data).
For objects one would consider a "sensor" to store scalar values at a regular interval, the existing `Entity` class can be used and takes care of internal timing, as well as providing some logic for non-uniform sampling.
Other common patterns would be:
  * a service which produces an alert message as part of the logic resulting from a received command
  * a service which consumes alert messages and produces new alerts messages based on them (logging derived values or converting raw alerts to a log-system compatible form)

Design Benefits
---------------
The principles presented here has several benefits, keeping them in mind while putting together a specific system can make life easier as new features are required.
1. Separate out the logging process means that it is easy to have multiple consumers in parallel without them impacting each other
  1. This allows testing new databases, database version upgrades, etc., without disrupting the working/production system.
  2. This allows other services to listen for and respond to new values without needing to interact with the database.
2. Have a few, but specialized, database-injection services.
  1. Often these are isolated to the type of data they consume (since this may impact where/how they inject the data).
  2. This service is a place for potential scaling (either database ingestion rate or message processing rate).
