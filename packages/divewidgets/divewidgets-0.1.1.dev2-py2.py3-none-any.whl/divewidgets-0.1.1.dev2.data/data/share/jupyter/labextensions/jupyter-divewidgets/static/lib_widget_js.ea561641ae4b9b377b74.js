(self["webpackChunkjupyter_divewidgets"] = self["webpackChunkjupyter_divewidgets"] || []).push([["lib_widget_js"],{

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Chung Chan
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Chung Chan
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.DIVEWidgetView = exports.DIVEWidgetModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
// Codemirror
const codemirror_1 = __webpack_require__(/*! codemirror */ "webpack/sharing/consume/default/codemirror/codemirror");
// import {EditorView} from "codemirror"
// import {editorSetup} from "./editorsetup"
// import {keymap} from "@codemirror/view"
// import {defaultKeymap} from "@codemirror/commands"
const lang_javascript_1 = __webpack_require__(/*! @codemirror/lang-javascript */ "webpack/sharing/consume/default/@codemirror/lang-javascript/@codemirror/lang-javascript?559b");
const lang_html_1 = __webpack_require__(/*! @codemirror/lang-html */ "webpack/sharing/consume/default/@codemirror/lang-html/@codemirror/lang-html");
class DIVEWidgetModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: 'DIVEWidgetModel', _view_name: 'DIVEWidgetView', _model_module: version_1.MODULE_NAME, _model_module_version: version_1.MODULE_VERSION, _view_module: version_1.MODULE_NAME, _view_module_version: version_1.MODULE_VERSION, code: '// some code here', html: '<!-- some code here -->', height: 600, width: 600 });
    }
}
exports.DIVEWidgetModel = DIVEWidgetModel;
DIVEWidgetModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
class DIVEWidgetView extends base_1.DOMWidgetView {
    render() {
        this.codeTab = document.createElement('div');
        this.htmlTab = document.createElement('div');
        this.codeTab.innerHTML = "Code";
        this.htmlTab.innerHTML = "HTML";
        this.codeTab.classList.add("active-tab");
        this.tabContainer = document.createElement('div');
        this.tabContainer.className = "tab-container";
        this.codeTab.onclick = (() => {
            this.htmlTab.classList.remove("active-tab");
            this.codeTab.classList.add("active-tab");
            this.htmlContainer.style.display = "none";
            this.codeContainer.style.display = "block";
        }).bind(this);
        this.htmlTab.onclick = (() => {
            this.htmlTab.classList.add("active-tab");
            this.codeTab.classList.remove("active-tab");
            this.htmlContainer.style.display = "block";
            this.codeContainer.style.display = "none";
        }).bind(this);
        this.tabContainer.appendChild(this.codeTab);
        this.tabContainer.appendChild(this.htmlTab);
        this.codeContainer = document.createElement('div');
        this.codeContainer.className = "code-container";
        this.codeContainer.style.display = 'block';
        this.codeContainer.style.overflowX = 'auto';
        this.codeView = new codemirror_1.EditorView({
            extensions: [codemirror_1.basicSetup,
                // keymap.of([{
                //   key: "Ctrl-Enter", run: (() => {
                //     this.runCode()
                //     return true;
                //   }).bind(this)
                // }]),
                // keymap.of(defaultKeymap),
                lang_javascript_1.javascript()],
            parent: this.codeContainer
        });
        this.codeView.dispatch({ changes: { from: 0, insert: this.model.get('code') } });
        this.htmlContainer = document.createElement('div');
        this.htmlContainer.className = "html-container";
        this.htmlContainer.style.display = 'none';
        this.htmlContainer.style.overflowX = 'auto';
        this.htmlView = new codemirror_1.EditorView({
            extensions: [codemirror_1.basicSetup,
                lang_html_1.html()],
            parent: this.htmlContainer
        });
        this.htmlView.dispatch({ changes: { from: 0, insert: this.model.get('html') } });
        this.editorContainer = document.createElement('div');
        this.editorContainer.style.display = 'none';
        this.editorContainer.className = 'editor-container';
        this.editorContainer.appendChild(this.codeContainer);
        this.editorContainer.appendChild(this.htmlContainer);
        this.controlContainer = document.createElement('div');
        this.controlContainer.className = 'control-container';
        this.controlContainer.style.display = 'flex';
        this.showBtn = document.createElement('button');
        this.showBtn.innerText = 'show code';
        this.showBtn.onclick = this.toggleCode.bind(this);
        this.runBtn = document.createElement('button');
        this.runBtn.innerText = 'run code';
        // this.runBtn.onclick = this.runCode.bind(this);
        this.runBtn.onclick = this.run.bind(this);
        this.runBtn.style.display = 'none';
        this.controlContainer.appendChild(this.showBtn);
        this.controlContainer.appendChild(this.runBtn);
        this.outputContainer = document.createElement('iframe');
        this.outputContainer.className = "output-container";
        this.outputContainer.width = this.model.get('width');
        this.outputContainer.height = this.model.get('height');
        this.setHtml();
        this.widgetContainer = document.createElement('div');
        this.widgetContainer.className = "divewidget";
        this.widgetContainer.appendChild(this.outputContainer);
        this.widgetContainer.appendChild(this.controlContainer);
        this.widgetContainer.appendChild(this.tabContainer);
        this.widgetContainer.appendChild(this.editorContainer);
        this.el.appendChild(this.widgetContainer);
        // this.outputContainer.onload = (function (this: DIVEWidgetView) {
        //   this.outputDocument = this.outputContainer.contentDocument!;
        //   this.codeScript = this.outputDocument!.createElement('script');
        //   this.outputDocument.body.appendChild(this.codeScript);
        //   this.setCode();
        //   this.model.on('change:code', this.setCode, this);
        //   this.model.on('change:code', this.setHtml, this);
        // }).bind(this);
    }
    run() {
        const html = this.htmlView.state.doc.toString();
        const code = this.codeView.state.doc.toString();
        this.model.set('html', html);
        this.model.set('code', code);
        this.model.save_changes();
    }
    /*
    Update the html in the output container with the model html.
    */
    setHtml() {
        this.outputContainer.srcdoc = this.model.get('html');
        this.outputContainer.onload = (function () {
            this.outputDocument = this.outputContainer.contentDocument;
            this.codeScript = this.outputDocument.createElement('script');
            this.outputDocument.body.appendChild(this.codeScript);
            this.setCode();
            this.model.on('change:code', this.setCode, this);
            this.model.on('change:html', this.setHtml, this);
        }).bind(this);
    }
    /*
    Update the script element in the output container with the model code.
    */
    setCode() {
        let script = this.outputDocument.createElement('script');
        script.innerHTML = this.model.get('code');
        this.outputDocument.body.replaceChild(script, this.codeScript);
        this.codeScript = script;
    }
    toggleCode() {
        if (this.editorContainer.style.display == 'block') {
            this.showBtn.innerText = 'show code';
            this.tabContainer.style.display = 'none';
            this.editorContainer.style.display = 'none';
            this.runBtn.style.display = 'none';
        }
        else {
            this.showBtn.innerText = 'hide code';
            this.tabContainer.style.display = 'flex';
            this.editorContainer.style.display = 'block';
            this.runBtn.style.display = 'block';
        }
    }
}
exports.DIVEWidgetView = DIVEWidgetView;
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".tab-container {\n  display: none;\n  flex-direction: row;\n  overflow: hidden;\n}\n\n.tab-container > div {\n  padding: 6px 6px;\n  margin: 2px;\n  background-color:aliceblue;\n  display: block; \n  overflow: hidden;\n  border: none;\n}\n\n.tab-container > div.active-tab {\n  background-color:bisque;\n}\n\n.output-container {\n  resize: both;\n  overflow: auto;\n  max-width: 100%;\n  border: none;\n}\n\n.editor-container {\n  resize: horizontal;\n  overflow: auto;\n  max-width: 100%;\n  border: none;\n}", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {

"use strict";


/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
// eslint-disable-next-line func-names
module.exports = function (useSourceMap) {
  var list = []; // return the list of modules as css string

  list.toString = function toString() {
    return this.map(function (item) {
      var content = cssWithMappingToString(item, useSourceMap);

      if (item[2]) {
        return "@media ".concat(item[2], " {").concat(content, "}");
      }

      return content;
    }).join('');
  }; // import a list of modules into the list
  // eslint-disable-next-line func-names


  list.i = function (modules, mediaQuery, dedupe) {
    if (typeof modules === 'string') {
      // eslint-disable-next-line no-param-reassign
      modules = [[null, modules, '']];
    }

    var alreadyImportedModules = {};

    if (dedupe) {
      for (var i = 0; i < this.length; i++) {
        // eslint-disable-next-line prefer-destructuring
        var id = this[i][0];

        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }

    for (var _i = 0; _i < modules.length; _i++) {
      var item = [].concat(modules[_i]);

      if (dedupe && alreadyImportedModules[item[0]]) {
        // eslint-disable-next-line no-continue
        continue;
      }

      if (mediaQuery) {
        if (!item[2]) {
          item[2] = mediaQuery;
        } else {
          item[2] = "".concat(mediaQuery, " and ").concat(item[2]);
        }
      }

      list.push(item);
    }
  };

  return list;
};

function cssWithMappingToString(item, useSourceMap) {
  var content = item[1] || ''; // eslint-disable-next-line prefer-destructuring

  var cssMapping = item[3];

  if (!cssMapping) {
    return content;
  }

  if (useSourceMap && typeof btoa === 'function') {
    var sourceMapping = toComment(cssMapping);
    var sourceURLs = cssMapping.sources.map(function (source) {
      return "/*# sourceURL=".concat(cssMapping.sourceRoot || '').concat(source, " */");
    });
    return [content].concat(sourceURLs).concat([sourceMapping]).join('\n');
  }

  return [content].join('\n');
} // Adapted from convert-source-map (MIT)


function toComment(sourceMap) {
  // eslint-disable-next-line no-undef
  var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap))));
  var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
  return "/*# ".concat(data, " */");
}

/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var isOldIE = function isOldIE() {
  var memo;
  return function memorize() {
    if (typeof memo === 'undefined') {
      // Test for IE <= 9 as proposed by Browserhacks
      // @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
      // Tests for existence of standard globals is to allow style-loader
      // to operate correctly into non-standard environments
      // @see https://github.com/webpack-contrib/style-loader/issues/177
      memo = Boolean(window && document && document.all && !window.atob);
    }

    return memo;
  };
}();

var getTarget = function getTarget() {
  var memo = {};
  return function memorize(target) {
    if (typeof memo[target] === 'undefined') {
      var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself

      if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
        try {
          // This will throw an exception if access to iframe is blocked
          // due to cross-origin restrictions
          styleTarget = styleTarget.contentDocument.head;
        } catch (e) {
          // istanbul ignore next
          styleTarget = null;
        }
      }

      memo[target] = styleTarget;
    }

    return memo[target];
  };
}();

var stylesInDom = [];

function getIndexByIdentifier(identifier) {
  var result = -1;

  for (var i = 0; i < stylesInDom.length; i++) {
    if (stylesInDom[i].identifier === identifier) {
      result = i;
      break;
    }
  }

  return result;
}

function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];

  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var index = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3]
    };

    if (index !== -1) {
      stylesInDom[index].references++;
      stylesInDom[index].updater(obj);
    } else {
      stylesInDom.push({
        identifier: identifier,
        updater: addStyle(obj, options),
        references: 1
      });
    }

    identifiers.push(identifier);
  }

  return identifiers;
}

function insertStyleElement(options) {
  var style = document.createElement('style');
  var attributes = options.attributes || {};

  if (typeof attributes.nonce === 'undefined') {
    var nonce =  true ? __webpack_require__.nc : 0;

    if (nonce) {
      attributes.nonce = nonce;
    }
  }

  Object.keys(attributes).forEach(function (key) {
    style.setAttribute(key, attributes[key]);
  });

  if (typeof options.insert === 'function') {
    options.insert(style);
  } else {
    var target = getTarget(options.insert || 'head');

    if (!target) {
      throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
    }

    target.appendChild(style);
  }

  return style;
}

function removeStyleElement(style) {
  // istanbul ignore if
  if (style.parentNode === null) {
    return false;
  }

  style.parentNode.removeChild(style);
}
/* istanbul ignore next  */


var replaceText = function replaceText() {
  var textStore = [];
  return function replace(index, replacement) {
    textStore[index] = replacement;
    return textStore.filter(Boolean).join('\n');
  };
}();

function applyToSingletonTag(style, index, remove, obj) {
  var css = remove ? '' : obj.media ? "@media ".concat(obj.media, " {").concat(obj.css, "}") : obj.css; // For old IE

  /* istanbul ignore if  */

  if (style.styleSheet) {
    style.styleSheet.cssText = replaceText(index, css);
  } else {
    var cssNode = document.createTextNode(css);
    var childNodes = style.childNodes;

    if (childNodes[index]) {
      style.removeChild(childNodes[index]);
    }

    if (childNodes.length) {
      style.insertBefore(cssNode, childNodes[index]);
    } else {
      style.appendChild(cssNode);
    }
  }
}

function applyToTag(style, options, obj) {
  var css = obj.css;
  var media = obj.media;
  var sourceMap = obj.sourceMap;

  if (media) {
    style.setAttribute('media', media);
  } else {
    style.removeAttribute('media');
  }

  if (sourceMap && typeof btoa !== 'undefined') {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  } // For old IE

  /* istanbul ignore if  */


  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
    while (style.firstChild) {
      style.removeChild(style.firstChild);
    }

    style.appendChild(document.createTextNode(css));
  }
}

var singleton = null;
var singletonCounter = 0;

function addStyle(obj, options) {
  var style;
  var update;
  var remove;

  if (options.singleton) {
    var styleIndex = singletonCounter++;
    style = singleton || (singleton = insertStyleElement(options));
    update = applyToSingletonTag.bind(null, style, styleIndex, false);
    remove = applyToSingletonTag.bind(null, style, styleIndex, true);
  } else {
    style = insertStyleElement(options);
    update = applyToTag.bind(null, style, options);

    remove = function remove() {
      removeStyleElement(style);
    };
  }

  update(obj);
  return function updateStyle(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap) {
        return;
      }

      update(obj = newObj);
    } else {
      remove();
    }
  };
}

module.exports = function (list, options) {
  options = options || {}; // Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
  // tags it will allow on a page

  if (!options.singleton && typeof options.singleton !== 'boolean') {
    options.singleton = isOldIE();
  }

  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];

    if (Object.prototype.toString.call(newList) !== '[object Array]') {
      return;
    }

    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDom[index].references--;
    }

    var newLastIdentifiers = modulesToDom(newList, options);

    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];

      var _index = getIndexByIdentifier(_identifier);

      if (stylesInDom[_index].references === 0) {
        stylesInDom[_index].updater();

        stylesInDom.splice(_index, 1);
      }
    }

    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"jupyter-divewidgets","version":"0.1.1","description":"Jupyter Widgets for DIVE virtual learning environment.","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/DIVE/divewidgets","bugs":{"url":"https://github.com/DIVE/divewidgets/issues"},"license":"BSD-3-Clause","author":{"name":"Chung Chan","email":"chungc@alum.mit.edu"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/DIVE/divewidgets"},"scripts":{"build":"jlpm run build:lib && jlpm run build:nbextension:dev && jlpm run build:labextension:dev","build:prod":"jlpm run build:lib && jlpm run build:nbextension && jlpm run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack --mode=production","build:nbextension:dev":"webpack --mode=development","clean":"jlpm run clean:lib && jlpm run clean:nbextension && jlpm run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf divewidgets/labextension","clean:nbextension":"rimraf divewidgets/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"jlpm run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@codemirror/lang-html":"^6.1.0","@codemirror/lang-javascript":"^6.0.2","@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","codemirror":"^6.0.1"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^28.1.6","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"divewidgets/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.ea561641ae4b9b377b74.js.map