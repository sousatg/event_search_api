# Fetch Events From Provider

In the context of extracting the events from a provider, facing the need to handle xml responses containing thousands of events with hundreds of zones each I decided to use a Task Queue with a scheduled cronjob to tigger the task against fetching the events on each request or using a Read-Through Cache to achive the desired latency of the search endpoint and the resilience of our service even when the provider is down accepting the downside of some possile inconsistencies between the provider and the data we have persisted.


## Considered Options

### Task Queue With Scheduled Task
Good, Isolation between reads and writes. Both can be scaled according to individual needs, when we need to execute tasks we can scale the number of workers according to our needs
Good, search api becomes isolated and just needs to handle I/O operations to the database
Good, fault taulerant (we can perform retries if the initial fetch fails) and if the task queue stops working it will not compromised the functionality of the search API
Good, ensures the reliability from the search API
Good, extraction and processing of the data before being requested by the user (warming)
Bad, week consistency (depending on the frequence the tasks are executed) betweent he data in our database and the data from the provider
Bad, adds more components to manage in our system

### Read-Through Cache
Good, possibility to use etags to ensure we get the most up to date information
Bad, when data is requested for the first time, it will alwats result in a cache miss and incurs the extra penalty of loading data.

## Links
[Caching Strategies and How to Choose the Right One](https://codeahoy.com/2017/08/11/caching-strategies-and-how-to-choose-the-right-one/)
