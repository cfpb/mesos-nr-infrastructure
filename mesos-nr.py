#!/usr/bin/env python2

import argparse
import json
import requests
import socket
import urlparse


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
    return 'mesos.' + metric_name.replace('/', '.')


def format_metrics(metrics, role, whitelist=None):

    if whitelist:
        metrics = {k: v for k, v in metrics.items() if k in whitelist}

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
    parser.add_argument("username")
    parser.add_argument("password")
    parser.add_argument("--metrics-endpoint") # we don't set a default here, since we need the role argument
    parser.add_argument("--auth-endpoint", default=default_auth_endpoint)

    args = parser.parse_args()
    
    if not args.metrics_endpoint:
        if args.role.lower() == 'master':
            default_port = 5050
        else:
            default_port = 5051
        metrics_endpoint = 'https://%s:{port}/metrics/snapshot' % (
            socket.gethostname(), default_port)

    session = authenticate(args.auth_endpoint, args.username, args.password)
    metrics = get_metrics(metrics_endpoint, session)

    document = format_metrics(metrics, args.role)

    print(json.dumps(document))
