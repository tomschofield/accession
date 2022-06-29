"use strict";
var masonry_1 = require('./src/masonry');
var brick_1 = require('./src/brick');
var module_1 = require('./src/module');
exports.MasonryModule = module_1.MasonryModule;
var masonry_2 = require('./src/masonry');
exports.AngularMasonry = masonry_2.AngularMasonry;
var brick_2 = require('./src/brick');
exports.AngularMasonryBrick = brick_2.AngularMasonryBrick;
exports.MASONRY_DIRECTIVES = [
    masonry_1.AngularMasonry,
    brick_1.AngularMasonryBrick
];
//# sourceMappingURL=index.js.map