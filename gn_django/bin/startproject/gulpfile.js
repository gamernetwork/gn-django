require('es6-promise').polyfill();

var gulp = require('gulp');
var path = require('path');
var less = require('gulp-less');
var autoprefixer = require('gulp-autoprefixer');
var minify = require('gulp-minify-css');
var util = require('gulp-util');

gulp.task('compile', function () {
  var l = less({});
  l.on('error',function(e){
    console.log(e);
    l.end();
  });
  return val = gulp.src([
      './static/less/*.less',
      '!./static/less/modules/**',
      '!./static/less/helpers/**'
    ])
    .pipe(l)
    .pipe(minify())
    .pipe(autoprefixer({
      browsers: ['last 10 versions']
    }))
    .pipe(gulp.dest('./static/css'))
  ;
});

gulp.task('watch', function () {
  gulp.watch('./static/less/*.less', ['compile']);
});
