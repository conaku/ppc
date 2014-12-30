/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.ambari.view.slider;

import org.apache.ambari.view.slider.rest.client.Metric;
import org.codehaus.jackson.annotate.JsonIgnore;
import org.codehaus.jackson.annotate.JsonIgnoreProperties;

import java.util.List;
import java.util.Map;

@JsonIgnoreProperties({ "jmxMetrics", "gangliaMetrics" })
public class SliderAppType {
  private String id;
  private String typeName;
  private String typeVersion;
  private String typeDescription;
  private Map<String, String> typeConfigs;
  private List<SliderAppTypeComponent> typeComponents;
  private String typePackageFileName;
  @JsonIgnore
  private Map<String, Map<String, Map<String, Metric>>> jmxMetrics;
  @JsonIgnore
  private Map<String, Map<String, Map<String, Metric>>> gangliaMetrics;

  @JsonIgnore
  public Map<String, Map<String, Map<String, Metric>>> getJmxMetrics() {
    return jmxMetrics;
  }

  public void setJmxMetrics(Map<String, Map<String, Map<String, Metric>>> jmxMetrics) {
    this.jmxMetrics = jmxMetrics;
  }

  @JsonIgnore
  public Map<String, Map<String, Map<String, Metric>>> getGangliaMetrics() {
    return gangliaMetrics;
  }

  public void setGangliaMetrics(Map<String, Map<String, Map<String, Metric>>> gangliaMetrics) {
    this.gangliaMetrics = gangliaMetrics;
  }

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public String getTypeName() {
    return typeName;
  }

  public void setTypeName(String name) {
    this.typeName = name;
  }

  public String getTypeDescription() {
    return typeDescription;
  }

  public void setTypeDescription(String description) {
    this.typeDescription = description;
  }

  public Map<String, String> getTypeConfigs() {
    return typeConfigs;
  }

  public void setTypeConfigs(Map<String, String> configs) {
    this.typeConfigs = configs;
  }

  public List<SliderAppTypeComponent> getTypeComponents() {
    return typeComponents;
  }

  public void setTypeComponents(List<SliderAppTypeComponent> components) {
    this.typeComponents = components;
  }

  public String getTypeVersion() {
    return typeVersion;
  }

  public void setTypeVersion(String version) {
    this.typeVersion = version;
  }

  public String getTypePackageFileName() {
    return typePackageFileName;
  }

  public void setTypePackageFileName(String typePackageFileName) {
    this.typePackageFileName = typePackageFileName;
  }

}
