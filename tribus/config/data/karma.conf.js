module.exports = function(config){
    config.set({
        basePath: '../../../..',
        files: [
            'tribus/data/static/js/full/*.js',
            'tribus/testing/js/*.js',
        ],
        autoWatch : false,
        frameworks: ['jasmine'],
        browsers : ['Chrome'],
        plugins : [
            'karma-junit-reporter',
            'karma-chrome-launcher',
            'karma-firefox-launcher',
            'karma-phantomjs-launcher',
            'karma-jasmine'
            ],
    });
};