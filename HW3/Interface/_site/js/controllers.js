/*
 * Calaca - Search UI for Elasticsearch
 * https://github.com/romansanchez/Calaca
 * http://romansanchez.me
 * @rooomansanchez
 * 
 * v1.2.0
 * MIT License
 */

/* Calaca Controller
 *
 * On change in search box, search() will be called, and results are bind to scope as results[]
 *
*/
Calaca.filter('highlight', function($sce) {
    return function(text, phrase) {      
      if (phrase) text = text.replace(new RegExp('('+phrase+')', 'gi'),
        '<span style="background:#ed4877;color:white">$1</span>')
      return $sce.trustAsHtml(text)
    }
  })
Calaca.filter('limitWords', function($sce) {
    return function(text, wordLimit) {      
      var length = text.length;
      return length > wordLimit ? text.substr(0, wordLimit - 1) : text;
    }
  })
Calaca.controller('calacaCtrl', ['calacaService', '$scope', '$location', function(results, $scope, $location){

        //Init empty array
        $scope.results = [];

        //Init offset
        $scope.offset = 0;

        // Search Mode : either 'normal' or 'morelikethis'
        $scope.searchMode = 'normal'

        var paginationTriggered;
        var maxResultsSize = CALACA_CONFIGS.size;
        var searchTimeout;

        $scope.delayedSearch = function(mode) {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                $scope.search(mode, $scope.loadResults)
            }, CALACA_CONFIGS.search_delay);
        }

        //On search, reinitialize array, then perform search and load results
        $scope.search = function(m, loadfunc){            
            $scope.results = [];
            $scope.offset = m == 0 ? 0 : $scope.offset;//Clear offset if new query
            $scope.loading = m == 0 ? false : true;//Reset loading flag if new query

            if(m == -1 && paginationTriggered) {
                if ($scope.offset - maxResultsSize >= 0 ) $scope.offset -= maxResultsSize;
            }     
            if(m == 1 && paginationTriggered) {
                $scope.offset += maxResultsSize;
            }
            $scope.paginationLowerBound = $scope.offset + 1;
            $scope.paginationUpperBound = ($scope.offset == 0) ? maxResultsSize : $scope.offset + maxResultsSize;
            // $scope.loadResults(m);
            loadfunc()
        };

        $scope.morelikethis = function(q, mode) {            
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                $scope.search(mode, $scope.loadMoreLikeThis)
            }, CALACA_CONFIGS.search_delay);
        }

        $scope.images = function(q, mode) {            
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                $scope.search(mode, $scope.loadImages)
            }, CALACA_CONFIGS.search_delay);
        }

        $scope.loadImages = function(m) {
            $scope.searchMode = 'images'
            results.image($scope.query, m, $scope.offset).then(function(a) {

                //Load results
                var i = 0;
                for(;i < a.hits.length; i++){
                    var html = a.hits[i].HTML
                    images = extractImages(html)
                    if (images.length > 3) {
                        a.hits[i].images = images
                        $scope.results.push(a.hits[i]);
                    }
                }

                //Set time took
                $scope.timeTook = a.timeTook;

                //Set total number of hits that matched query
                $scope.hits = a.hitsCount;

                //Pluralization
                $scope.resultsLabel = ($scope.hits != 1) ? "results" : "result";

                //Check if pagination is triggered
                paginationTriggered = $scope.hits > maxResultsSize ? true : false;

                //Set loading flag if pagination has been triggered
                if(paginationTriggered) {
                    $scope.loading = true;
                }
            });
        }

        $scope.loadMoreLikeThis = function(m) {
            $scope.searchMode = 'morelikethis'
            results.moreLikeThis($scope.query, m, $scope.offset).then(function(a) {

                //Load results
                var i = 0;
                for(;i < a.hits.length; i++){
                    $scope.results.push(a.hits[i]);
                }

                //Set time took
                $scope.timeTook = a.timeTook;

                //Set total number of hits that matched query
                $scope.hits = a.hitsCount;

                //Pluralization
                $scope.resultsLabel = ($scope.hits != 1) ? "results" : "result";

                //Check if pagination is triggered
                paginationTriggered = $scope.hits > maxResultsSize ? true : false;

                //Set loading flag if pagination has been triggered
                if(paginationTriggered) {
                    $scope.loading = true;
                }
            });
        }

        $scope.paginatesearch = function(m) {
            if ($scope.searchMode == 'normal') {
                $scope.search(m, $scope.loadResults)
            }
            else if ($scope.searchMode == 'morelikethis') {
                $scope.search(m, $scope.loadMoreLikeThis)
            }
            else {
                $scope.search(m, $scope.loadImages)
            }
        }
        //Load search results into array
        $scope.loadResults = function(m) {
            $scope.searchMode = 'normal'
            results.search($scope.query, m, $scope.offset).then(function(a) {

                //Load results
                var i = 0;
                for(;i < a.hits.length; i++){
                    $scope.results.push(a.hits[i]);
                }

                //Set time took
                $scope.timeTook = a.timeTook;

                //Set total number of hits that matched query
                $scope.hits = a.hitsCount;

                //Pluralization
                $scope.resultsLabel = ($scope.hits != 1) ? "results" : "result";

                //Check if pagination is triggered
                paginationTriggered = $scope.hits > maxResultsSize ? true : false;

                //Set loading flag if pagination has been triggered
                if(paginationTriggered) {
                    $scope.loading = true;
                }
            });
        };

        $scope.paginationEnabled = function() {
            return paginationTriggered ? true : false;
        };

        function extractImages(html) {
            var temp = document.createElement( 'div' );
            temp.innerHTML = html;
            var images = temp.getElementsByTagName( 'img' );
            img_srcs = []
            for(i = 0; i < images.length; i++) {
                src = images[i].src 
                if (src.startsWith('http'))
                    img_srcs.push(src)
            }
            return img_srcs
        }

    }]
);