# Integrate mesos masters and agents with New Relic Infrastructure

This is a simple "custom integration" build according to the [New Relic Infrastructure SDK](https://docs.newrelic.com/docs/integrations/integrations-sdk), that grabs the [Observability Metrics](http://mesos.apache.org/documentation/latest/monitoring/) from Apache Mesos. It has only been tested in the context of [DC/OS 1.10](https://docs.mesosphere.com/1.10/monitoring/performance-monitoring/), and thus may reflect assumptions that are only true in that scenario.

![](https://raw.githubusercontent.com/cfpb/mesos-nr-infrastructure/master/screenshot.png)


## Dependencies

This has been tested on RHEL 7 with Python 2.7, but *may* work in other environments. The python `requests` library must be installed.

## Installation

- 'mesos-nr.py' should be copied to /var/db/newrelic-infra/custom-integrations/mesos-nr
- 'mesos-nr-definition.yml' should be copied to /var/db/newrelic-infra/custom-integrations/mesos-nr-definition.yml
- the approprite sample configuration (master or agent) should be copied to /etc/newrelic-infra/integrations.d/mesos-nr-config.yml, and edited to reflect a working set of mesos credentials, and your desired [labels](https://docs.newrelic.com/docs/integrations/integrations-sdk/file-specifications/integration-configuration-file-specifications)
- restart the newrleic-infra service. On RHEL 7, that looks like `systemctl restart newrelic-infra`


## Usage

If you're up and running, you should be able to see MesosMasterMetrics (or MesosAgentMetrics) in New Relic Insights. Most master metrics are only reported on the current elected leader.

No data? [try turning on logging and verbose mode and seeing if there are any errors](https://docs.newrelic.com/docs/infrastructure/new-relic-infrastructure/configuration/configure-infrastructure-agent).

## Known issues

- this currently only grabs metrics-- we haven't yet explored how to best take advantage of 'inventory' or 'events' in New Relic Infrastructure.

## Getting help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker.

## Getting involved

Pull requests welcome! See [CONTRIBUTING](CONTRIBUTING.md) for more.


----

## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)


----

## Credits and references

I learned quite a bit by looking at [DataDog's mesos integrations](https://github.com/DataDog/integrations-core/tree/master/mesos_master/datadog_checks)
