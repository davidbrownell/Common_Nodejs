// ----------------------------------------------------------------------
// |
// |  gulpfile.js
// |
// |  David Brownell <db@DavidBrownell.com>
// |      2020-03-14 10:52:46
// |
// ----------------------------------------------------------------------
// |
// |  Copyright David Brownell 2020
// |  Distributed under the Boost Software License, Version 1.0. See
// |  accompanying file LICENSE_1_0.txt or copy at
// |  http://www.boost.org/LICENSE_1_0.txt.
// |
// ----------------------------------------------------------------------

// This file is based on the "Gulp 4 Starter Kit" by JR Cologne <kontakt@jr-cologne.de>,
// which is licensed under the MIT license and available at
// https://github.com/jr-cologne/gulp-starter-kit.

const browserSync                           = require("browser-sync").create(),
      del                                   = require("del"),
      gulp                                  = require("gulp"),
      path                                  = require("path"),
      yargs                                 = require("yargs"),

      autoprefixer                          = require("gulp-autoprefixer"),
      dependents                            = require("gulp-dependents"),
      concat                                = require("gulp-concat"),
      cond                                  = require("gulp-cond"),
      imagemin                              = require("gulp-imagemin"),
      less                                  = require("gulp-less"),
      minifyCss                             = require("gulp-clean-css"),
      plumber                               = require("gulp-plumber"),
      rename                                = require("gulp-rename"),
      sass                                  = require("gulp-sass"),
      sourcemaps                            = require("gulp-sourcemaps"),
      typescript                            = require("gulp-typescript"),
      uglify                                = require("gulp-uglify"),

      server_port                           = 3000,

      src_folder                            = "./src/",
      dist_folder                           = "./dist/"
      ;

if (yargs.argv.release)
    process.env.NODE_ENV = 'release';

let RELEASE = process.env.NODE_ENV === 'release';

// Update the file's dirname member to remove the given
// prefix if it exists.
function RemovePathPrefix(file, prefix) {
    let dirname_parts = file.dirname.split(path.sep);

    if(dirname_parts[0] === prefix) {
        dirname_parts.shift();
        file.dirname = dirname_parts.join(path.sep);
    }
}

gulp.task("clean", () => del([dist_folder]));

gulp.task(
    "html",
    () => {
        return gulp.src(
            [ src_folder + "**/*.html" ],
            {
                base: src_folder,
                since: gulp.lastRun("html")
            }
        )
        .pipe(gulp.dest(dist_folder))
        .pipe(browserSync.stream())
        ;
    }
);

gulp.task(
    "less",
    () => {
        return gulp.src(
            [ src_folder + "**/!(_)*.less" ],
            {
                base: src_folder,
                since: gulp.lastRun("less"),
            }
        )
        .pipe(sourcemaps.init())
          .pipe(plumber())
          .pipe(dependents())
          .pipe(less())
          .pipe(autoprefixer())
          .pipe(minifyCss())
        .pipe(cond(!RELEASE, sourcemaps.write(".")))
        .pipe(rename((file) => RemovePathPrefix(file, "less")))
        .pipe(gulp.dest(dist_folder + "css"))
        .pipe(browserSync.stream())
        ;
    }
);

gulp.task(
    "sass",
    () => {
        return gulp.src(
            [ src_folder + "**/*.sass", src_folder + "**/*.scss" ],
            {
                base: src_folder,
                since: gulp.lastRun("sass")
            }
        )
        .pipe(sourcemaps.init())
          .pipe(plumber())
          .pipe(dependents())
          .pipe(sass())
          .pipe(autoprefixer())
          .pipe(minifyCss())
        .pipe(cond(!RELEASE, sourcemaps.write(".")))
        .pipe(rename((file) => RemovePathPrefix(file, "sass")))
        .pipe(gulp.dest(dist_folder + "css"))
        .pipe(browserSync.stream())
        ;
    }
);

gulp.task(
    "images",
    () => {
        return gulp.src(
            [ src_folder + "**/*.{png,jpg,jpeg,gif,svg,ico}" ],
            {
                base: src_folder,
                since: gulp.lastRun("images")
            }
        )
        .pipe(plumber())
        .pipe(imagemin())
        .pipe(rename((file) => RemovePathPrefix(file, "images")))
        .pipe(gulp.dest(dist_folder + "images"))
        .pipe(browserSync.stream())
        ;
    }
);

gulp.task(
    "typescript",
    () => {
        return gulp.src(
            [ src_folder + "**/!(_)*.{ts,tsx}" ],
            {
                base: src_folder,
                since: gulp.lastRun("typescript")
            }
        )
        .pipe(sourcemaps.init())
          .pipe(plumber())
          .pipe(typescript("tsconfig.json"))
          .pipe(concat("all.js"))
          .pipe(cond(RELEASE, uglify()))
        .pipe(cond(!RELEASE, sourcemaps.write(".")))
        .pipe(rename((file) => RemovePathPrefix(file, "typescript")))
        .pipe(gulp.dest(dist_folder + "js"))
        .pipe(browserSync.stream())
        ;
    }
);

gulp.task(
    "build",
    gulp.parallel(
        "html",
        "images",
        "less",
        "sass",
        "typescript"
    )
);

gulp.task(
    "rebuild",
    gulp.series(
        "clean",
        "build"
    )
);

gulp.task(
    "serve",
    () => {
        return browserSync.init({
                server: {
                    baseDir: [ "dist" ]
                },
                port: server_port,
                open: true
            }
        );
    }
);

gulp.task(
    "watch",
    () => {
        gulp.watch(
            [ src_folder + "**/*.*" ],
            {
                events: "all"
            },
            gulp.task("build")
        );
    }
);

gulp.task(
    "default",
    gulp.series(
        "rebuild",
        gulp.parallel(
            "serve",
            "watch"
        )
    )
);
