# sinai

Monitor application state, data integrity, or anything you want.

## Usage

To develop a monitoring application with sinai, you install it and import it like any other Python library. See `example.py`.

There are no required dependencies, but optional dependencies are required for the relevant features:

* `requests` to use API sources and stores, and the Slack store
* `pymongo` to use MongoDB sources and stores
* `boto3` to use the CloudWatch store

## Development

To develop sinai itself, check out the code from Github and use the following commands to create a development environment:

```bash
$ pipenv install --dev
$ pre-commit install
```

## What's it all about?

This is a library for developing monitoring applications. 

The idea is akin to Model-View-Controller (MVC) Frameworks that you find in web applications. Sinai provides useful base classes and you subclass them to build your own monitoring application.

Following the MVC analogy, sinai only provides one model called `Metric`.

The views come in two types. A `Source` provides data. A `Store` receives data.

A controller is called a `Rule`. A rule takes data from sources, does whatever calculations or transformations are required, then returns the metrics to be stored.

We describe those classes in more detail below.

## Base Classes

### Metric

A `Metric` records a piece of data that you want to capture, either from an external source or from performing calculations or aggregations on other metrics.

A metric has a few default fields. The precise semantic meaning of the values is specific to your application.

Your metric subclass needs a `name` to distinguish its instances from others. This is important when storing or serialising the metrics.

Your metric can have an optional `context` string you can use to group instances of that metric together. For example, if you wanted to group the metrics by region, the context values might be UK, EU, US, etc. If you are monitoring animals, your context values might be lion, crocodile, etc.

The `ref` field is available to store a piece of arbitrary string data. If your application monitors data integrity, it might be the external reference of a piece of incorrect data in the system under test. If you are tracking planets, it might be the name of the planet.

The `value` field is available to store a numerical value. Again, whatever that means is particular to your metric. E.g. the number of fish caught, or the refund owed to a customer.

The `checked` field is available to store a boolean value (True/False). Was the customer happy? Was the suspect read his rights? Have we taken relevant action? 

The `annotations` field is available to store textual data. A list of items bought, notes on the metric. Whatever you want.

You can add extra fields, but you have to deal with the serialisation and deserialisation of those yourself in your source and store classes. 

### Sources and Stores

Sinai provides several stores and sources, you will subclass them to make your own application specific ones.

Provided Sources:

* Source - the base class for all stores.

* ApiSource - Get data from an API endpoint

* MongoSource - Get data from MongoDB Collections

* MetricSource - Get Metrics from memory (for aggregation or further calculations) 

* MongoMetricSource - Get Metrics from MongoDB

Provided Stores:

* Store - the base class for all stores

* ApiStore - post data to an API endpoint

* MetricStore - base class for Metric Stores

* MemoryMetricStore - Store Metrics in memory (for aggregation or further calculations) 

* MongoMetricStore - Store Metrics in MongoDB

* Slack - Post metrics to a Slack channel

* CloudWatch - store metrics in AWS Cloudwatch

### Rules

`Rule` is the base class - you override the `sources` and `stores` attributes to tell your rule where to take data from and where to send your resulting metrics. Your subclass overrides the `evaluate` method to perform whatever calculations you require to populate your metric instances with data.

Sinai currently comes with one premade rule:

* MetricAggregationRule - aggregates stored metrics and produces a metric with the result. Supports count, sum, max, min, mean, mode and median.

### Monitor

The `Monitor` is the entry point to the application. A user invokes the monitor, using a command, or through a cron or AWS lambda or whatever. It connects to the sources, evaluates the rules, then stores the data. Your Monitor subclass overrides the `rules` attribute with the list of rule classes to run.
