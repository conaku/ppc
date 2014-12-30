#!/usr/bin/env ambari-python-wrap
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import socket

class StackAdvisor(object):

  def recommendComponentLayout(self, services, hosts):
    """Returns Services object with hostnames array populated for components"""
    pass

  def validateComponentLayout(self, services, hosts):
    """Returns array of Validation objects about issues with hostnames components assigned to"""
    pass

  def recommendConfigurations(self, services, hosts):
    """Returns Services object with configurations object populated"""
    pass

  def validateConfigurations(self, services, hosts):
    """Returns array of Validation objects about issues with configuration values provided in services"""
    pass

class DefaultStackAdvisor(StackAdvisor):

  def recommendComponentLayout(self, services, hosts):
    """Returns Services object with hostnames array populated for components"""

    stackName = services["Versions"]["stack_name"]
    stackVersion = services["Versions"]["stack_version"]
    hostsList = [host["Hosts"]["host_name"] for host in hosts["items"]]
    servicesList = [service["StackServices"]["service_name"] for service in services["services"]]

    layoutRecommendations = self.provideLayout(services, hosts)

    recommendations = {
      "Versions": {"stack_name": stackName, "stack_version": stackVersion},
      "hosts": hostsList,
      "services": servicesList,
      "recommendations": layoutRecommendations
    }

    return recommendations

  def provideLayout(self, services, hosts):

    recommendations = {
      "blueprint": {
        "host_groups": [ ]
      },
      "blueprint_cluster_binding": {
        "host_groups": [ ]
      }
    }

    hostsList = [host["Hosts"]["host_name"] for host in hosts["items"]]

    hostsComponentsMap = {}
    for hostName in hostsList:
      if hostName not in hostsComponentsMap:
        hostsComponentsMap[hostName] = []

    #extend 'hostsComponentsMap' with MASTER components
    for service in services["services"]:
      masterComponents = [component for component in service["components"] if self.isMaster(component)]
      for component in masterComponents:
        componentName = component["StackServiceComponents"]["component_name"]

        if self.isAlreadyPopulated(component):
          hostsForComponent = component["StackServiceComponents"]["hostnames"]
        else:
          availableHosts = hostsList
          if len(hostsList) > 1 and self.isNotPreferableOnAmbariServerHost(component):
            availableHosts = [hostName for hostName in hostsList if not self.isLocalHost(hostName)]

          if self.isMasterWithMultipleInstances(component):
            hostsCount = self.defaultNoOfMasterHosts(component)
            if hostsCount > 1: # get first 'hostsCount' available hosts
              if len(availableHosts) < hostsCount:
                hostsCount = len(availableHosts)
              hostsForComponent = availableHosts[:hostsCount]
            else:
              hostsForComponent = [self.getHostForComponent(component, availableHosts, hostsComponentsMap)]
          else:
            hostsForComponent = [self.getHostForComponent(component, availableHosts, hostsComponentsMap)]

        #extend 'hostsComponentsMap' with 'hostsForComponent'
        for hostName in hostsForComponent:
          hostsComponentsMap[hostName].append( { "name":componentName } )

    #extend 'hostsComponentsMap' with Slave and Client Components
    componentsListList = [service["components"] for service in services["services"]]
    componentsList = [item for sublist in componentsListList for item in sublist]
    usedHostsListList = [component["StackServiceComponents"]["hostnames"] for component in componentsList if not self.isNotValuable(component)]
    utilizedHosts = [item for sublist in usedHostsListList for item in sublist]
    freeHosts = [hostName for hostName in hostsList if hostName not in utilizedHosts]

    for service in services["services"]:
      slaveClientComponents = [component for component in service["components"]
                               if self.isSlave(component) or self.isClient(component)]
      for component in slaveClientComponents:
        componentName = component["StackServiceComponents"]["component_name"]

        if self.isAlreadyPopulated(component):
          hostsForComponent = component["StackServiceComponents"]["hostnames"]
        elif component["StackServiceComponents"]["cardinality"] == "ALL":
          hostsForComponent = hostsList
        else:
          if len(freeHosts) == 0:
            hostsForComponent = hostsList[-1:]
          else: # len(freeHosts) >= 1
            hostsForComponent = freeHosts
            if self.isClient(component):
              hostsForComponent = freeHosts[0:1]

        #extend 'hostsComponentsMap' with 'hostsForComponent'
        for hostName in hostsForComponent:
          if hostName not in hostsComponentsMap:
            hostsComponentsMap[hostName] = []
          hostsComponentsMap[hostName].append( { "name": componentName } )

    #prepare 'host-group's from 'hostsComponentsMap'
    host_groups = recommendations["blueprint"]["host_groups"]
    bindings = recommendations["blueprint_cluster_binding"]["host_groups"]
    index = 0
    for key in hostsComponentsMap.keys():
      index += 1
      host_group_name = "host-group-{0}".format(index)
      host_groups.append( { "name": host_group_name, "components": hostsComponentsMap[key] } )
      bindings.append( { "name": host_group_name, "hosts": [{ "fqdn": socket.getfqdn(key) }] } )

    return recommendations
  pass

  def prepareValidationResponse(self, services, validationItems):
    """Returns array of Validation objects about issues with hostnames components assigned to"""
    stackName = services["Versions"]["stack_name"]
    stackVersion = services["Versions"]["stack_version"]

    validations = {
      "Versions": {"stack_name": stackName, "stack_version": stackVersion},
      "items": validationItems
    }

    return validations

  def validateComponentLayout(self, services, hosts):
    """Returns array of Validation objects about issues with hostnames components assigned to"""
    validationItems = self.getLayoutValidationItems(services, hosts)
    return self.prepareValidationResponse(services, validationItems)

  def validateConfigurations(self, services, hosts):
    """Returns array of Validation objects about issues with hostnames components assigned to"""
    validationItems = self.getConfigurationsValidationItems(services, hosts)
    return self.prepareValidationResponse(services, validationItems)

  def getLayoutValidationItems(self, services, hosts):
    return []

  def getClusterData(self, servicesList, hosts, components):
    pass

  def getConfigurationsValidationItems(self, services, hosts):
    return []

  def recommendConfigurations(self, services, hosts):
    stackName = services["Versions"]["stack_name"]
    stackVersion = services["Versions"]["stack_version"]
    hostsList = [host["Hosts"]["host_name"] for host in hosts["items"]]
    servicesList = [service["StackServices"]["service_name"] for service in services["services"]]
    components = [component["StackServiceComponents"]["component_name"]
                  for service in services["services"]
                  for component in service["components"]]

    clusterData = self.getClusterData(servicesList, hosts, components)

    recommendations = {
      "Versions": {"stack_name": stackName, "stack_version": stackVersion},
      "hosts": hostsList,
      "services": servicesList,
      "recommendations": {
        "blueprint": {
          "configurations": {},
          "host_groups": []
        },
        "blueprint_cluster_binding": {
          "host_groups": []
        }
      }
    }

    configurations = recommendations["recommendations"]["blueprint"]["configurations"]

    for service in servicesList:
      calculation = self.recommendServiceConfigurations(service)
      if calculation is not None:
        calculation(configurations, clusterData)

    return recommendations

  def recommendServiceConfigurations(self, service):
    return self.getServiceConfiguratorDict().get(service, None)

  def getServiceConfiguratorDict(self):
    return {}

  # Recommendation helper methods
  def isAlreadyPopulated(self, component):
    hostnames = self.getComponentAttribute(component, "hostnames")
    if hostnames is not None:
      return len(hostnames) > 0
    return False

  def isClient(self, component):
    return self.getComponentAttribute(component, "component_category") == 'CLIENT'

  def isSlave(self, component):
    return self.getComponentAttribute(component, "component_category") == 'SLAVE'

  def isMaster(self, component):
    return self.getComponentAttribute(component, "is_master")

  def getComponentAttribute(self, component, attribute):
    serviceComponent = component.get("StackServiceComponents", None)
    if serviceComponent is None:
      return None
    return serviceComponent.get(attribute, None)

  def isLocalHost(self, hostName):
    return socket.getfqdn(hostName) == socket.getfqdn()

  def isMasterWithMultipleInstances(self, component):
    componentName = self.getComponentName(component)
    masters = self.getMastersWithMultipleInstances()
    return componentName in masters

  def isNotValuable(self, component):
    componentName = self.getComponentName(component)
    service = self.getNotValuableComponents()
    return componentName in service

  def defaultNoOfMasterHosts(self, component):
    componentName = self.getComponentName(component)
    return self.cardinality(componentName)["min"]

  # Helper dictionaries
  def cardinality(self, componentName):
    return self.getCardinalitiesDict().get(componentName, {"min": 1, "max": 1})

  def getHostForComponent(self, component, hostsList, hostsComponentsMap):
    componentName = self.getComponentName(component)

    if len(hostsList) == 1:
      return hostsList[0]
    else:
      scheme = self.defineSelectionScheme(componentName)
      if scheme is not None:
        for key in scheme.keys():
          if isinstance(key, ( int, long )):
            if len(hostsList) < key:
              return hostsList[scheme[key]]
      return self.getLeastOccupiedHost(hostsList, hostsComponentsMap)

  def getLeastOccupiedHost(self, hostsList, hostComponentsMap):
    hostOccupations = dict((host, len(components)) for host, components in hostComponentsMap.iteritems() if host in hostsList)
    return min(hostOccupations, key=hostOccupations.get)

  def defineSelectionScheme(self, componentName):
    return self.selectionSchemes().get(componentName, None)

  def getComponentName(self, component):
    return self.getComponentAttribute(component, "component_name")

  def isNotPreferableOnAmbariServerHost(self, component):
    componentName = self.getComponentName(component)
    service = self.getNotPreferableOnServerComponents()
    return componentName in service

  def getMastersWithMultipleInstances(self):
    return []

  def getNotValuableComponents(self):
    return []

  def getNotPreferableOnServerComponents(self):
    return []

  def getCardinalitiesDict(self):
    return {}

  def selectionSchemes(self):
    return {}
