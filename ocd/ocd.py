#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, redirect, request, \
    jsonify

import requests
import json
import os
# importo el cliente de kubernetes y los objetos de configuracion

from kubernetes import client, config

application = Flask(__name__)
application.secret_key = os.environ['FLASK_SECRET']
config.load_incluster_config()
v1 = client.CoreV1Api()
api_instance = client.AppsV1Api()
DEPLOYMENT_NAME = "nginx-ejemplo"
@application.route('/health')
def health():
    """
    healthckeck para readiness
    del pod
    """

    return 'OK'

@application.route('/<ns>/deployments', methods=['GET'])
def events(ns):
    #@application.route('/ddeployments', methods=['GET'])
    #def deployments():
    """
    Lista los DC en el proyecto actual
    """
    deployments = AppsV1instance.list_namespaced_deployment(namespace = ns)

    return jsonify(message = str(deployments))

@application.route('/<ns>/quota', methods=['GET'])
def quota(ns):
   
   quota = False
   quota = v1.list_namespaced_resource_quota(namespace = ns)
   return jsonify(message = str(quota))

#TODO conseguir una SA para poder hacer lo de abajo
@application.route('/<ns>/pods', methods=['GET'])
def pods(ns):
#@application.route('/pods', methods=['GET'])
#def pods():
    """
    Lista los pods en el proyecto actual
    """

    pods = False
    #seteo esto sino no existe namespace y la request falla, busco solo en mi proyecto actual con la SA deployer
    pods = v1.list_namespaced_pod(namespace = ns)

# testeando response JSON
  #  for i in pods.items:
   # i.metadata.name
   # i.metadata.namespace
   # i.status.pod_ip
   # i.status.host_ip

    data = [{
        'pod_namespace': i.metadata.namespace,
        'pod_name': i.metadata.name,
        'pod_ip': i.status.pod_ip,
        'node_ip': i.status.host_ip,
        } for i in pods.items]
    return jsonify(message = data)

#@application.route('/recursos/<ns>/<podname>', methods=['GET'])
#def resources(ns, podname):
#@application.route('/pods', methods=['GET'])
#def pods(): sarasa
# return jsonify(message = str(api_response.??))

@application.route('/createnginx')
def createnginx():
    # Configureate Pod template container
    container = client.V1Container(
        name="nginx",
        image="docker-registry.default.svc:5000/openshift/nginx:1.12",
        ports=[client.V1ContainerPort(container_port=8080)],
        resources=client.V1ResourceRequirements(
            requests={"cpu": "100m", "memory": "200Mi"},
            limits={"cpu": "500m", "memory": "500Mi"}
        )
    )
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=3,
        template=template,
        selector={'matchLabels': {'app': 'nginx'}})
    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec)
    
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace=os.environ['POD_NAMESPACE'])
    print("Deployment created. status='%s'" % str(api_response.status))
    return jsonify(message = str(api_response.status))

@application.route('/delnginx')
def delnginx():
    # Delete deployment
    api_response = api_instance.delete_namespaced_deployment(
        name=DEPLOYMENT_NAME,
        namespace=os.environ['POD_NAMESPACE'],
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Deployment deleted. status='%s'" % str(api_response.status))
    return jsonify(message = str(api_response.status))

@application.route('/')
def index():
    return render_template('index.html')
