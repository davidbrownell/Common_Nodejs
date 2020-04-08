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

const browserify                            = require("browserify"),
      browserSync                           = require("browser-sync").create(),
      del                                   = require("del"),
      glob                                  = require("glob"),
      gulp                                  = require("gulp"),
      path                                  = require("path"),
      through                               = require("through2"),
      yargs                                 = require("yargs"),

      autoprefixer                          = require("gulp-autoprefixer"),
      dependents                            = require("gulp-dependents"),
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

      buffer                                = require("vinyl-buffer"),
      source                                = require("vinyl-source-stream"),

      server_port                           = 3000,

      src_folder                            = "./src/",
      dist_folder                           = "./dist/",
      temp_folder                           = "./temp/"
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

gulp.task("clean", () => del([dist_folder, temp_folder]));

gulp.task(
    "html",
    () => {
        return gulp.src(
            [
                `${src_folder}**/*.html`,
                `!${src_folder}node_modules/**/*.*`
            ],
            {
                base: src_folder
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
            [
                `${src_folder}**/!(_)*.less`,
                `!${src_folder}node_modules/**/*.*`
            ],
            {
                base: src_folder
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
        .pipe(gulp.dest(`${dist_folder}css`))
        .pipe(browserSync.stream())
        ;
    }
);

gulp.task(
    "sass",
    () => {
        return gulp.src(
            [
                `${src_folder}**/*.sass`,
                `${src_folder}**/*.scss`,
                `!${src_folder}node_modules/**/*.*`
            ],
            {
                base: src_folder
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
        .pipe(gulp.dest(`${dist_folder}css`))
        .pipe(browserSync.stream())
        ;
    }
);

gulp.task(
    "images",
    () => {
        return gulp.src(
            [
                `${src_folder}**/*.{png,jpg,jpeg,gif,svg,ico}`,
                `!${src_folder}node_modules/**/*.*`
            ],
            {
                base: src_folder
            }
        )
        .pipe(plumber())
        .pipe(imagemin())
        .pipe(rename((file) => RemovePathPrefix(file, "images")))
        .pipe(gulp.dest(`${dist_folder}images`))
        .pipe(browserSync.stream())
        ;
    }
);

gulp.task(
    "typescript",
    () => {
        return gulp.src(
            [
                `${src_folder}**/!(_)*.{ts,tsx}`,
                `!${src_folder}node_modules/**/*.*`
            ],
            {
                base: src_folder
            }
        )
        .pipe(sourcemaps.init())
            .pipe(plumber())
            .pipe(typescript("src/tsconfig.json"))
        .pipe(cond(!RELEASE, sourcemaps.write(".")))
        .pipe(rename((file) => RemovePathPrefix(file, "typescript")))
        .pipe(gulp.dest(`${temp_folder}js`))
        ;
    }
);

gulp.task(
    "javascript",
    () => {
        return gulp.src(
            [
                `${src_folder}js/!(_)*.{js,jsx}`,
                `!${src_folder}node_modules/**/*.*`
            ],
            {
                base: src_folder
            }
        )
        .pipe(gulp.dest(`${temp_folder}js`))
        ;
    }
);

gulp.task(
    "browserify",
    () => {
        var bundledStream = through();

        bundledStream
            .pipe(source("app.js"))
            .pipe(buffer())
            .pipe(cond(RELEASE, uglify()))
            .pipe(gulp.dest(`${dist_folder}js`))
            .pipe(browserSync.stream())
            ;

        var b = browserify(
            {
                entries: glob.sync(`${temp_folder}js/**/*.{js,jsx}`),
                debug: !RELEASE,
                paths: [
                    "./src/node_modules"
                ],
                standalone: "app"
            });

        b.bundle().pipe(bundledStream);

        return bundledStream;
    }
);

gulp.task(
    "build",
    gulp.parallel(
        gulp.series(
            gulp.parallel(
                "javascript",
                "typescript"
            ),
            "browserify",
            () => del([temp_folder])
        ),
        "html",
        "images",
        "less",
        "sass"
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
            [
                `${src_folder}**/*.*`,
                `!${src_folder}node_modules/**/*.*`
            ],
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
