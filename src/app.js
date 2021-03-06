
(function() {
    'use strict';

    angular.module('jobListings', [])
        .controller('JobsController', JobsController)
        .directive('jobsSource', jobsSource)
        .directive('terminalClipboard', terminalClipboard)
        .filter('excludeFilter', excludeFilter)
        .service('DataService', DataService);

    JobsController.$inject = ['$scope', 'DataService'];

    function JobsController($scope, DataService) {

        var _this = this;

        // Get List of Sources from sources.json
        var promise = DataService.getSources();

        promise.then(function(response) {
            // Store in local variable
            _this.sources = response.data.sources;

            // For each source, retrieve results.
            angular.forEach(_this.sources, function(value, key) {
                var promise = DataService.getJobResults(value.file);
                promise.then(function(response) {
                    // Append list of results to JSON Object
                    _this.sources[key]["results"] = response.data;
                    console.log("_this.sources", _this.sources);
                });
            });

        });

        $scope.saveMyJson = function(key, i) {
            //<button class="btn btn-default" ng-click="saveMyJson(idKey, result.id)">
            $scope.documentwriterTemplate = DataService.getSources();

            $scope.savedJSON = angular.toJson(_this.sources[key]["results"][i - 1], true);

            var blob = new Blob([$scope.savedJSON], {
                type: "application/json;charset=utf-8;"
            });
            var downloadLink = document.createElement('a');
            downloadLink.setAttribute('download', 'downloadJSON.json');
            downloadLink.setAttribute('href', window.URL.createObjectURL(blob));

            document.body.appendChild(downloadLink);
            downloadLink.click();
        };

        $scope.loadterminalScript = function(inputID) {
            var clipboard, terminalGetRepo, terminalLinuxSetup;
            console.log("inputID", inputID);

            if(inputID === "clipboard0"){
                $('#'+inputID).val("cd; cd github/scrapy-scrape-viewer/scrapyvirtualenv/jobsups; source upsjobsDemoShell.sh");
            }
            if(inputID === "clipboard1"){
                $('#'+inputID).val("cd; cd github/scrapy-scrape-viewer/scrapyvirtualenv/stackoverflow; source stackoverflowDemoShell.sh");
                //scrapyvirtualenv/expresspros/expressprosDemoShell.sh
            }
            if(inputID === "clipboard2"){
                $('#'+inputID).val("cd; cd github/scrapy-scrape-viewer/scrapyvirtualenv/expresspros; source expressprosDemoShell.sh");
            }
            if(inputID === "clipboard3"){
                $('#'+inputID).val("cd; cd github/scrapy-scrape-viewer/scrapyvirtualenv/targetedjobfairs");
            }

            clipboard = new Clipboard('.clipboardJS');
            clipboard.on('success', function(e) {
                console.log(e);
            });
            clipboard.on('error', function(e) {
                console.log(e);
            });
        };
    }

    function jobsSource() {
        return {
            restrict: 'E',
            templateUrl: 'src/jobs-source.directive.html'
        };
    }

    function terminalClipboard() {
        return {
            restrict: 'E',
            templateUrl: 'src/terminal-clipboard.directive.html'
        };
    }

    function excludeFilter() {
        return function(input, exclude) {
            var output = [];
            angular.forEach(input, function(result) {
                if (exclude && result.title !== null) {
                    if (!result.title.toLowerCase().includes(exclude)) {
                        output.push(result);
                    }
                } else output.push(result);
            });
            return output;
        }
    }

    DataService.$inject = ['$http'];

    function DataService($http) {
        var _this = this;

        _this.getSources = function() {
            /*
            # Note:
                * Chrome Error: Cross origin requests are only supported for protocol schemes: http, data, chrome, chrome-extension, https.
            # Resolve Error:
                * Use Firefox
                * Use localhost server
                * Add --allow-file-access-from-files after Chrome`s shortcut target, and open new browse instance using this shortcut
                * https://stackoverflow.com/questions/27742070/angularjs-error-cross-origin-requests-are-only-supported-for-protocol-schemes
            */
            var response = $http({
                method: 'GET',
                url: ('sources.json'),
            });
            return response
        };

        _this.getJobResults = function(file) {
            var response = $http({
                method: 'GET',
                url: (file),
            });
            return response;
        };
    }


})();
