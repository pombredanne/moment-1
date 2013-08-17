var casper = require('casper').create(),
    url = casper.cli.args[0],
    image = casper.cli.args[1],
    viewport = casper.cli.args[2].split(','),
    target = casper.cli.args[3];


casper.start(url, function () {

    casper.viewport(parseInt(viewport[0]), parseInt(viewport[1]));

});


casper.wait(500); // Give some time....


casper.then(function () {

    this.captureSelector(image, target);

});


casper.run();
