module.exports = function(grunt){
    grunt.initConfig({
        karma: {
            unit: {
                configFile: 'tribus/config/data/karma.conf.js',
                background: true,
            }
        },
        watch: {
            karma: {
                files: [
                    'tribus/data/static/js/full/*.js',
                    'tribus/testing/js/*.js',
                ],
                tasks: ['karma:unit:run']
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-karma');
    grunt.registerTask('devmode', ['karma:unit', 'watch']);
};