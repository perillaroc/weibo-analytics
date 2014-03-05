module.exports = function(grunt){
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        copy:{
            main:{
                files:[
                    {
                        expand: true,
                        cwd: 'bower_components/bootstrap/dist/',
                        src: ['**'],
                        dest:'static/'
                    },
                    {
                        expand: true,
                        cwd: 'bower_components/bootstrap-datepicker/',
                        src: ['css/**','js/*','js/locals/bootstrap-datepicker.zh-CN.js'],
                        dest:'static/'
                    },
                    {
                        expand: true,
                        cwd: 'bower_components/require-js/',
                        src: ['css/**','js/*','js/locals/bootstrap-datepicker.zh-CN.js'],
                        dest:'static/'
                    }
                ]
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.registerTask('default', ['copy']);
}