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

Storage Backends
----------------
You can use any storage backend that you prefer.
Most of our existing systems make use postgreSQL, but a service which receives alert messages could put data into whatever system you want (text files, no-SQL database, other SQL database, etc.).

Design Benefits and Concepts
----------------------------

The principles presented here has several benefits, keeping them in mind while putting together a specific system can make life easier as new features are required.
1. Separate out the logging process means that it is easy to have multiple consumers in parallel without them impacting each other
  1. This allows testing new databases, database version upgrades, etc., without disrupting the working/production system.
  2. This allows other services to listen for and respond to new values without needing to interact with the database.
2. Have a few, but specialized, database-injection services.
  1. Often these are isolated to the type of data they consume (since this may impact where/how they inject the data).
  2. This service is a place for potential scaling (either database ingestion rate or message processing rate).
3. Sensors should be logged individually (that is, there should be independent records for each sensor for each time, so that that data is able to be fully consumed independently).
4. Database storage should distinguish between storage of newly measured values, and derived values from existing measurements. The latter can be useful to log, but are different in nature.
5. At least under SQL, the storage design should be driven by how one can "naturally" store the data, with enough context for building relations that exist.
   It is almost always a bad idea to design based on how the data will be consumed later (databases provide sophisticated query systems precisely for this purpose).
