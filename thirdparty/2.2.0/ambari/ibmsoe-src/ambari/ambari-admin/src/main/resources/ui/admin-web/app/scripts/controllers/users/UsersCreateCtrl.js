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
'use strict';

angular.module('ambariAdminConsole')
.controller('UsersCreateCtrl',['$scope', '$routeParams', 'User', '$location', 'uiAlert', function($scope, $routeParams, User, $location, uiAlert) {
  $scope.user = {
    active: true
  };

  $scope.createUser = function() {
    $scope.form.submitted = true;
    if ($scope.form.$valid){
      User.create({
        'Users/user_name': $scope.user.user_name,
        'Users/password': $scope.user.password,
        'Users/active': !!$scope.user.active,
        'Users/admin': !!$scope.user.admin
      }).then(function() {
        uiAlert.success('Created user ' + $scope.user.user_name);
        $location.path('/users');
      }).catch(function(data) {;
        data = data.data;
        uiAlert.danger(data.status, data.message);
      });
    }
  };
}]);