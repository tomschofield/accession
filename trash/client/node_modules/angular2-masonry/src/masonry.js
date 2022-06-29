"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
// import * as masonry from 'masonry-layout';
var masonry = require('masonry-layout');
var AngularMasonry = (function () {
    function AngularMasonry(_element) {
        this._element = _element;
        this.useImagesLoaded = false;
        // Outputs
        this.layoutComplete = new core_1.EventEmitter();
        this.removeComplete = new core_1.EventEmitter();
    }
    AngularMasonry.prototype.ngOnInit = function () {
        ///TODO: How to load imagesloaded only if this.useImagesLoaded===true?
        // if (this.useImagesLoaded) {
        //     this._imagesLoaded = require('imagesloaded');
        // }
        var _this = this;
        // Create masonry options object
        if (!this.options)
            this.options = {};
        // Set default itemSelector
        if (!this.options.itemSelector) {
            this.options.itemSelector = '[masonry-brick], masonry-brick';
        }
        // Set element display to block
        if (this._element.nativeElement.tagName === 'MASONRY') {
            this._element.nativeElement.style.display = 'block';
        }
        // Initialize Masonry
        this._msnry = new masonry(this._element.nativeElement, this.options);
        // console.log('AngularMasonry:', 'Initialized');
        // Bind to events
        this._msnry.on('layoutComplete', function (items) {
            _this.layoutComplete.emit(items);
        });
        this._msnry.on('removeComplete', function (items) {
            _this.removeComplete.emit(items);
        });
    };
    AngularMasonry.prototype.ngOnDestroy = function () {
        if (this._msnry) {
            this._msnry.destroy();
        }
    };
    AngularMasonry.prototype.layout = function () {
        var _this = this;
        setTimeout(function () {
            _this._msnry.layout();
        });
        // console.log('AngularMasonry:', 'Layout');
    };
    // public add(element: HTMLElement, prepend: boolean = false) {
    AngularMasonry.prototype.add = function (element) {
        var _this = this;
        var isFirstItem = false;
        // Check if first item
        if (this._msnry.items.length === 0) {
            isFirstItem = true;
        }
        if (this.useImagesLoaded) {
            imagesLoaded(element, function (instance) {
                _this._element.nativeElement.appendChild(element);
                // Tell Masonry that a child element has been added
                _this._msnry.appended(element);
                // layout if first item
                if (isFirstItem)
                    _this.layout();
            });
            this._element.nativeElement.removeChild(element);
        }
        else {
            // Tell Masonry that a child element has been added
            this._msnry.appended(element);
            // layout if first item
            if (isFirstItem)
                this.layout();
        }
        // console.log('AngularMasonry:', 'Brick added');
    };
    AngularMasonry.prototype.remove = function (element) {
        // Tell Masonry that a child element has been removed
        this._msnry.remove(element);
        // Layout items
        this.layout();
        // console.log('AngularMasonry:', 'Brick removed');
    };
    __decorate([
        core_1.Input(), 
        __metadata('design:type', Object)
    ], AngularMasonry.prototype, "options", void 0);
    __decorate([
        core_1.Input(), 
        __metadata('design:type', Boolean)
    ], AngularMasonry.prototype, "useImagesLoaded", void 0);
    __decorate([
        core_1.Output(), 
        __metadata('design:type', core_1.EventEmitter)
    ], AngularMasonry.prototype, "layoutComplete", void 0);
    __decorate([
        core_1.Output(), 
        __metadata('design:type', core_1.EventEmitter)
    ], AngularMasonry.prototype, "removeComplete", void 0);
    AngularMasonry = __decorate([
        core_1.Component({
            selector: '[masonry], masonry',
            template: '<ng-content></ng-content>'
        }), 
        __metadata('design:paramtypes', [core_1.ElementRef])
    ], AngularMasonry);
    return AngularMasonry;
}());
exports.AngularMasonry = AngularMasonry;
//# sourceMappingURL=masonry.js.map