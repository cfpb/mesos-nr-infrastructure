#!/usr/bin/env python2

import argparse
import json
import os
import requests
import socket


def authenticate(endpoint, username, password):
    response = requests.post(endpoint,
                             json={'uid': username, 'password': password},
                             verify=False)

    token = response.json()['token']
    session = requests.Session()
    session.headers.update({'Authorization': 'token=%s' % token})

    return session


def get_metrics(endpoint, session):

    response = session.get(endpoint,
                           verify=False)

    return response.json()


def rename_metric(metric_name):
    # dots instead of slashes, and prepend 'mesos.'
    return 'mesos.' + metric_name.replace('/', '.')


def format_metrics(metrics, role, whitelist=None):

    if whitelist:
        metrics = {rename_metric(k): v for k, v
                   in metrics.items() if k in whitelist}
    else:
        metrics = {rename_metric(k): v for k, v in metrics.items()}

    document = {"name": "org.apache.mesos",
                "protocol_version": "1",
                "integration_version": "1.0.0",
                "metrics": [metrics]
                }

    document['metrics'][0]['event_type'] = 'Mesos%sMetrics' % role.title()

    return document


if __name__ == '__main__':

    # defaults assume we are *on* the host we are checking metrics for
    # and spartan/mesos-DNS is sane (which allows 'leader.mesos' to resolve)
    default_auth_endpoint = 'https://leader.mesos/acs/api/v1/auth/login'

    parser = argparse.ArgumentParser(description='Retrieve mesos\
                                     /metrics/snapshot data, and format it for\
                                     New Relic Infructure')
    parser.add_argument("role")
    parser.add_argument("--metrics-endpoint")
    parser.add_argument("--auth-endpoint", default=default_auth_endpoint)

    username = os.environ['MESOS_USERNAME']
    password = os.environ['MESOS_PASSWORD']

    args = parser.parse_args()

    if not args.metrics_endpoint:
        if args.role.lower() == 'master':
            default_port = 5050
        else:
            default_port = 5051
        metrics_endpoint = 'https://%s:%s/metrics/snapshot' % (
            socket.gethostname(), default_port)

    session = authenticate(args.auth_endpoint, username, password)
    metrics = get_metrics(metrics_endpoint, session)

    if args.role.lower() == 'master' and not metrics['master/elected']:
        # borrowed this list from the datadog mesos integration
        # https://github.com/DataDog/integrations-core/tree/master/mesos_master
        whitelist = ('system/cpus_total',
                     'system/load_15min',
                     'system/load_1min',
                     'system/load_5min',
                     'system/mem_free_bytes',
                     'system/mem_total_bytes',
                     'master/elected',
                     'master/uptime_secs',
                     'registrar/log/recovered')
    else:
        whitelist = None

    document = format_metrics(metrics, args.role, whitelist=whitelist)

    print(json.dumps(document))
