var casper = require('casper').create(),
    image = casper.cli.args[0],
    url = casper.cli.args[1],
    delay = parseInt(casper.cli.args[6], 10),
    quality = parseInt(casper.cli.args[8], 10),
    target = casper.cli.args[3],
    full = casper.cli.args[4],
    viewport_args = casper.cli.args[2].split(','),
    crop_args = casper.cli.args[5].split(','),
    events_args = casper.cli.args[7].split('+'),
    thumb_args = casper.cli.args[9].split(','),
    viewport_width = parseInt(viewport_args[0], 10),
    viewport_height = parseInt(viewport_args[1], 10),
    crop_x = parseInt(crop_args[0], 10),
    crop_y = parseInt(crop_args[1], 10),
    crop_width = parseInt(crop_args[2], 10),
    crop_height = parseInt(crop_args[3], 10),
    formatOptions = undefined,
    clipOptions = undefined,
    events = {};


casper.start(url, function () {

    casper.viewport(viewport_width, viewport_height);

});


casper.wait(delay); // Give some time....


casper.then(function () {

    if (target === 'body' && !crop_args.length > 0) {

        if (full === 'false') {

            // No cropping arguments, but we have the 'full' keyword argument
            // set to false, so we crop capture height to viewport.

            clipOptions = {top: 0, left: 0, width: viewport_width, height: viewport_height};

            this.capture(image, clipOptions, formatOptions);

        } else {

            // No cropping arguments and full is true, so we just capture
            // everything.

            this.captureSelector(image, target, formatOptions);

        }

    } else if (target === 'body' && crop_args) {

        if (crop_args.length === 3) {

            // Passed x, y, and width args for cropping. We crop height to
            // viewport.

            clipOptions = {top: crop_x, left: crop_y, width: crop_width, height: viewport_height};

        } else if (crop_args.length === 4) {

            // Passed x, y, width and height arguments for cropping.

            clipOptions = {top: crop_x, left: crop_y, width: crop_width, height: crop_height};

        } else {

            // Passed x and y arguments for cropping. We crop width and height
            // to viewport.

            clipOptions = {top: crop_x, left: crop_y, width: viewport_width, height: viewport_height};

        }

        this.capture(image, clipOptions, formatOptions);

    } else {

        // Targeting a specific non-body selector. In such a case, the capture
        // is set to the rendered dimensions of the selector.

        this.captureSelector(image, target, formatOptions);

    }

});


casper.run();
