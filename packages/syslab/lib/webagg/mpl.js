/* Put everything inside the global mpl namespace */
/* global mpl */
window.mpl = {};

// webSocket 类型
mpl.get_websocket_type = function () {
  if (typeof WebSocket !== 'undefined') {
    return WebSocket;
  } else if (typeof MozWebSocket !== 'undefined') {
    return MozWebSocket;
  } else {
    alert(
      'Your browser does not have WebSocket support. ' +
        'Please try Chrome, Safari or Firefox ≥ 6. ' +
        'Firefox 4 and 5 are also supported but you ' +
        'have to enable WebSockets in about:config.'
    );
  }
};
// 创建figure对象
mpl.figure = function (
  figure_id,
  parent_element,
  imageBaseUrl = '',
  vscode_postMessage,
  mouseMoveInterval,
  mouseDragInterval
) {
  this.id = figure_id;
  this.imageBaseUrl = imageBaseUrl;

  // this.supports_binary = this.ws.binaryType !== undefined;
  this.supports_binary = true;  
  this.vscode_postMessage = vscode_postMessage;
  if (!this.supports_binary) {
    var warnings = document.getElementById('mpl-warnings');
    if (warnings) {
      warnings.style.display = 'block';
      warnings.textContent =
        'This browser does not support binary websocket messages. ' +
        'Performance may be slow.';
    }
  }
  // window.onmessage = this._make_on_message_function

  window.addEventListener('message', (e) => {
    console.log('mpl-message', e)
    let message = e.data
    if (e.data.type == "plotConnect") {
      message = e.data.data
    }
    switch (message.type) {
      case 'ws_message': {
        this._make_on_message_function(this)(message.value);
        break;
      }
    }
  });
  this.imageObj = new Image();

  this.context = undefined;
  this.message = undefined;
  this.canvas = undefined;
  this.rubberband_canvas = undefined;
  this.rubberband_context = undefined;
  this.format_dropdown = undefined;
  this.limitConnect = 3;
  this.image_mode = 'full';
  this.menu_list = [];
  this.menu_position = {
    left: 0,
    top: 0,
  };
  this.root = document.createElement('div');
  this.root.classList = 'mpl-figure-box';
  this.mousePressed = false;
  // 限制请求事件的频率
  this.mouseMoveInterval = mouseMoveInterval;
  this.mouseDragInterval = mouseDragInterval;
  this.zoomMode = false;
  // 判断鼠标是否在画布内
  this.InFigure = false;
  this.zoomX0 = undefined;
  this.zoomX1 = undefined;
  this.zoomY1 = undefined;
  this.zoomY2 = undefined;
  // this.root.setAttribute("style", "display: inline-block");
  this._root_extra_style(this.root);

  parent_element.appendChild(this.root);

  // this._init_header(this);
  this._init_toolbar(this);
  this._init_canvas(this);

  var fig = this;

  this.waiting = false;

  this.imageObj.onload = function () {
    if (fig.image_mode === 'full') {
      // Full images could contain transparency (where diff images
      // almost always do), so we need to clear the canvas so that
      // there is no ghosting.
      fig.context.clearRect(0, 0, fig.canvas.width, fig.canvas.height);
    }
    fig.context.drawImage(fig.imageObj, 0, 0);
  };

  this.imageObj.onunload = function () {
    // fig.ws.close();
  };
  this.colorLabel = 'color';
  this.colorPicker = Colorpicker.create({
    // el: "color-picker",
    color: '#ff000',
    change: function (hex) {},
    confirm: (value) => {
      this.send_message('set_prop', { label: this.colorLabel, value });
    },
  });
  this.confirmBox = ConfirmBox.create({
    title: '',
    content: '',
    confirm: (key, value) => {
      this.send_message('set_prop', { label: key, value });
    },
    cancel: (key, value) => {
      this.send_message('set_prop', { label: key, value });
    },
    imageBaseUrl: this.imageBaseUrl,
  });
  this.textEditor = TextEditor.create({
    confirm: (value, type = 'text_edit') => {
      this.send_message('set_prop', { label: type, value });
    },
  });
};
mpl.figure.prototype._init_websocket = function () {
  this.send_message('supports_binary', { value: this.supports_binary });
  this.send_message('send_image_mode', {});
  if (this.ratio !== 1) {
    this.send_message('set_device_pixel_ratio', {
      device_pixel_ratio: this.ratio,
    });
  }
  this.request_resize(
    this.canvas_div.clientWidth,
    this.canvas_div.clientHeight
  );
};
// websocket 重连
mpl.figure.prototype._reconnect_websocket = function () {
  this.send_message('reconnect');
};
mpl.figure.prototype._init_header = function () {
  var titlebar = document.createElement('div');
  titlebar.classList =
    'ui-dialog-titlebar ui-widget-header ui-corner-all ui-helper-clearfix';
  var titletext = document.createElement('div');
  titletext.classList = 'ui-dialog-title';
  titletext.setAttribute(
    'style',
    'width: 100%; text-align: center; padding:3px 0;'
  );
  titlebar.appendChild(titletext);
  this.root.appendChild(titlebar);
  this.header = titletext;
};

mpl.figure.prototype._canvas_extra_style = function (_canvas_div) {};

mpl.figure.prototype._root_extra_style = function (_canvas_div) {};

mpl.figure.prototype._init_canvas = function () {
  var fig = this;

  var canvas_div = (this.canvas_div = document.createElement('div'));
  canvas_div.classList = 'mpl-canvas-div';
  var menu_div = (this.menu_div = document.getElementById('menu'));
  canvas_div.setAttribute('tabindex', '0');
  canvas_div.setAttribute(
    'style',
    // "border: 1px solid #ddd;" +
    'box-sizing: content-box;' +
      'clear: both;' +
      'min-height: 1px;' +
      'min-width: 1px;' +
      'outline: 0;' +
      'overflow: hidden;' +
      'position: relative;' +
      // "resize: both;" +
      'z-index: 2;'
  );

  function on_keyboard_event_closure(name) {
    return function (event) {
      return fig.key_event(event, name);
    };
  }

  canvas_div.addEventListener(
    'keydown',
    on_keyboard_event_closure('key_press')
  );
  canvas_div.addEventListener(
    'keyup',
    on_keyboard_event_closure('key_release')
  );

  this._canvas_extra_style(canvas_div);
  this.root.appendChild(canvas_div);

  var canvas = (this.canvas = document.createElement('canvas'));
  canvas.classList.add('mpl-canvas');
  canvas.setAttribute(
    'style',
    'box-sizing: content-box;' +
      'pointer-events: none;' +
      'position: relative;' +
      'z-index: 0;'
  );

  this.context = canvas.getContext('2d');

  var backingStore =
    this.context.backingStorePixelRatio ||
    this.context.webkitBackingStorePixelRatio ||
    this.context.mozBackingStorePixelRatio ||
    this.context.msBackingStorePixelRatio ||
    this.context.oBackingStorePixelRatio ||
    this.context.backingStorePixelRatio ||
    1;

  this.ratio = (window.devicePixelRatio || 1) / backingStore;

  var rubberband_canvas = (this.rubberband_canvas =
    document.createElement('canvas'));
  rubberband_canvas.setAttribute(
    'style',
    'box-sizing: content-box;' +
      'left: 0;' +
      'pointer-events: none;' +
      'position: absolute;' +
      'top: 0;' +
      'z-index: 1;'
  );

  // Apply a ponyfill if ResizeObserver is not implemented by browser.
  if (this.ResizeObserver === undefined) {
    if (window.ResizeObserver !== undefined) {
      this.ResizeObserver = window.ResizeObserver;
    } else {
      var obs = _JSXTOOLS_RESIZE_OBSERVER({});
      this.ResizeObserver = obs.ResizeObserver;
    }
  }

  this.resizeObserverInstance = new this.ResizeObserver(function (entries) {
    var nentries = entries.length;
    for (var i = 0; i < nentries; i++) {
      var entry = entries[i];
      var width, height;
      if (entry.contentBoxSize) {
        if (entry.contentBoxSize instanceof Array) {
          // Chrome 84 implements new version of spec.
          width = entry.contentBoxSize[0].inlineSize;
          height = entry.contentBoxSize[0].blockSize;
        } else {
          // Firefox implements old version of spec.
          width = entry.contentBoxSize.inlineSize;
          height = entry.contentBoxSize.blockSize;
        }
      } else {
        // Chrome <84 implements even older version of spec.
        width = entry.contentRect.width;
        height = entry.contentRect.height;
      }

      // Keep the size of the canvas and rubber band canvas in sync with
      // the canvas container.
      if (entry.devicePixelContentBoxSize) {
        // Chrome 84 implements new version of spec.
        canvas.setAttribute(
          'width',
          entry.devicePixelContentBoxSize[0].inlineSize
        );
        canvas.setAttribute(
          'height',
          entry.devicePixelContentBoxSize[0].blockSize
        );
      } else {
        canvas.setAttribute('width', width * fig.ratio);
        canvas.setAttribute('height', height * fig.ratio);
      }
      /* This rescales the canvas back to display pixels, so that it
       * appears correct on HiDPI screens. */
      canvas.style.width = width + 'px';
      canvas.style.height = height + 'px';

      rubberband_canvas.setAttribute('width', width);
      rubberband_canvas.setAttribute('height', height);

      // And update the size in Python. We ignore the initial 0/0 size
      // that occurs as the element is placed into the DOM, which should
      // otherwise not happen due to the minimum size styling.
      if (width !== 0 && height !== 0) {
        fig.request_resize(width, height);
      }
    }
  });
  this.resizeObserverInstance.observe(canvas_div);

  function on_mouse_event_closure(name) {
    /* User Agent sniffing is bad, but WebKit is busted:
     * https://bugs.webkit.org/show_bug.cgi?id=144526
     * https://bugs.webkit.org/show_bug.cgi?id=181818
     * The worst that happens here is that they get an extra browser
     * selection when dragging, if this check fails to catch them.
     */

    var UA = navigator.userAgent;
    var isWebKit = /AppleWebKit/.test(UA) && !/Chrome/.test(UA);
    if (isWebKit) {
      return function (event) {
        /* This prevents the web browser from automatically changing to
         * the text insertion cursor when the button is pressed. We
         * want to control all of the cursor setting manually through
         * the 'cursor' event from matplotlib */
        event.preventDefault();
        return fig.mouse_event(event, name);
      };
    } else {
      return function (event) {
        return fig.mouse_event(event, name);
      };
    }
  }

  canvas_div.addEventListener('mousedown', function (event) {
    on_mouse_event_closure('button_press')(event);
    fig.mousePressed = true;
    if (fig.buttons['Zoom'].classList.contains('active') && fig.InFigure) {
      fig.zoomMode = true;
      const boundingRect = fig.canvas.getBoundingClientRect();
      fig.zoomX0 = (event.clientX - boundingRect.left) * fig.ratio;
      fig.zoomY0 = (event.clientY - boundingRect.top) * fig.ratio;
    }
  });

  canvas_div.addEventListener('mouseup', function (event) {
    on_mouse_event_closure('button_release')(event);
    fig.mousePressed = false;
    if (fig.buttons['Zoom'].classList.contains('active')) {
      fig.zoomMode = false;
      fig.rubberband_context.clearRect(
        0,
        0,
        fig.canvas.width / fig.ratio,
        fig.canvas.height / fig.ratio
      );
    }
  });
  let startTime = 0;
  let frequency = 0;
  canvas_div.addEventListener('dblclick', on_mouse_event_closure('dblclick'));
  // Throttle sequential mouse events to 1 every 20ms.
  const debouncedMotionNotify = _.throttle(function (event) {
    // 处理鼠标松开时候的移动事件的代码
    const currentTime = Date.now();
    const timeInterval = (currentTime - startTime) / 1000;
    if (timeInterval > 0) {
      frequency = 1 / timeInterval;
      // console.log(`鼠标移动事件频率为:${frequency.toFixed(2)}次/秒`);
    }
    startTime = currentTime;
    on_mouse_event_closure('motion_notify')(event);
  }, fig.mouseMoveInterval);
  const debouncedPressedMotionNotify = _.throttle(function (event) {
    // 处理鼠标按压状态下的移动事件的代码
    const currentTime = Date.now();
    const timeInterval = (currentTime - startTime) / 1000;
    if (timeInterval > 0) {
      frequency = 1 / timeInterval;
      // console.log(`鼠标移动事件频率为:${frequency.toFixed(2)}次/秒`);
    }
    startTime = currentTime;
    on_mouse_event_closure('motion_notify')(event);
  }, fig.mouseDragInterval);
  canvas_div.addEventListener('mousemove', function (event) {
    if (fig.zoomMode && fig.InFigure) {
      fig.mousePressed = false;
      const boundingRect = fig.canvas.getBoundingClientRect();
      fig.zoomX1 = (event.clientX - boundingRect.left) * fig.ratio;
      fig.zoomY1 = (event.clientY - boundingRect.top) * fig.ratio;
      var x0 = fig.zoomX0 / fig.ratio;
      var y0 = fig.zoomY0 / fig.ratio;
      var x1 = fig.zoomX1 / fig.ratio;
      var y1 = fig.zoomY1 / fig.ratio;
      x0 = Math.floor(x0) + 0.5;
      y0 = Math.floor(y0) + 0.5;
      x1 = Math.floor(x1) + 0.5;
      y1 = Math.floor(y1) + 0.5;
      var min_x = Math.min(x0, x1);
      var min_y = Math.min(y0, y1);
      var width = Math.abs(x1 - x0);
      var height = Math.abs(y1 - y0);

      fig.rubberband_context.clearRect(
        0,
        0,
        fig.canvas.width / fig.ratio,
        fig.canvas.height / fig.ratio
      );

      fig.rubberband_context.strokeRect(min_x, min_y, width, height);
    }
    fig.mousePressed
      ? debouncedPressedMotionNotify(event)
      : debouncedMotionNotify(event);
  });
  canvas_div.addEventListener(
    'mouseenter',
    on_mouse_event_closure('figure_enter')
  );
  canvas_div.addEventListener(
    'mouseleave',
    on_mouse_event_closure('figure_leave')
  );
  canvas_div.addEventListener(
    'contextmenu',
    on_mouse_event_closure('contextmenu')
  );
  this.root.addEventListener('click', (e) => {
    menu_div.style.top = -5000 + 'px';
  });
  window.onblur = () => {
    menu_div.style.top = -5000 + 'px';
  };

  canvas_div.addEventListener('wheel', function (event) {
    if (event.deltaY < 0) {
      event.step = 1;
    } else {
      event.step = -1;
    }
    on_mouse_event_closure('scroll')(event);
  });

  canvas_div.appendChild(canvas);
  canvas_div.appendChild(rubberband_canvas);

  this.rubberband_context = rubberband_canvas.getContext('2d');
  this.rubberband_context.strokeStyle = '#000000';

  this._resize_canvas = function (width, height, forward) {
    if (forward) {
      // canvas_div.style.width = width + "px";
      // canvas_div.style.height = height + "px";
      canvas_div.style.width = '100%';
      canvas_div.style.height = '100%';
    }
  };

  // Disable right mouse context menu.
  canvas_div.addEventListener('contextmenu', function (_e) {
    _e.preventDefault();
    return false;
  });

  function set_focus() {
    canvas.focus();
    canvas_div.focus();
  }

  window.setTimeout(set_focus, 100);
};
// 初始化工具栏
mpl.figure.prototype._init_toolbar = function () {
  var fig = this;

  var toolbar = document.createElement('div');
  toolbar.classList = 'mpl-toolbar';
  this.root.appendChild(toolbar);

  function on_click_closure(name, value) {
    return function (_event) {
      return fig.toolbar_button_onclick(name, value);
    };
  }

  fig.buttons = {};
  let buttonGroup = document.createElement('div');
  buttonGroup.classList = 'mpl-button-group';
  for (const toolbar_ind in mpl.toolbar_items) {
    const name = mpl.toolbar_items[toolbar_ind][0];
    const tooltip = mpl.toolbar_items[toolbar_ind][1];
    const image = mpl.toolbar_items[toolbar_ind][2];
    const method_name = mpl.toolbar_items[toolbar_ind][3];

    if (!name) {
      if (buttonGroup.hasChildNodes()) {
        toolbar.appendChild(buttonGroup);
      }
      buttonGroup = document.createElement('div');
      buttonGroup.classList = 'mpl-button-group';
      continue;
    }
    function renderMultiTools(selectDom, currentEvent) {
      const button = (fig.buttons[name] = document.createElement('button'));
      button.classList = 'mpl-widget';
      button.classList.add('mpl-more-widget');
      button.setAttribute('role', 'button');
      button.setAttribute('title', tooltip);
      button.setAttribute('aria-disabled', 'false');
      const icon_img = document.createElement('img');
      icon_img.src = fig.imageBaseUrl + '_images/' + image + '.svg';

      const down_button = document.createElement('img');
      down_button.classList.add('down-button');
      down_button.src = fig.imageBaseUrl + '_images/down.svg';
      const combo_img = document.createElement('div');
      combo_img.classList.add('combo-img');
      combo_img.appendChild(icon_img);
      combo_img.appendChild(down_button);
      combo_img.style.display = 'flex';
      combo_img.alt = tooltip;
      button.appendChild(combo_img);
      button.appendChild(selectDom);
      buttonGroup.appendChild(button);
      if (currentEvent) {
        icon_img.addEventListener('click', currentEvent);
        down_button.addEventListener('click', function () {
          if (selectDom.style.display !== 'block') {
            button.classList.add('active');
            selectDom.style.display = 'block';
          }
        });
      } else {
        button.addEventListener('click', function () {
          if (selectDom.style.display !== 'block') {
            button.classList.add('active');
            selectDom.style.display = 'block';
          }
        });
      }

      document.addEventListener('click', (e) => {
        if (!button.contains(e.target) && selectDom.style.display === 'block') {
          selectDom.style.display = 'none';
          button.classList.remove('active');
        }
      });
      return button;
    }
    // 保存下拉
    if (name === 'Save') {
      const selectDom = document.createElement('ul');
      selectDom.id = 'save_list';
      selectDom.classList.add('fmt');
      const button = renderMultiTools(selectDom, null);
      for (let index = 0; index < mpl.extensions.length; index++) {
        const element = mpl.extensions[index];
        const child_dom = document.createElement('li');
        child_dom.title = 'save as ' + element;
        child_dom.classList.add('fmt-child');
        const img = document.createElement('img');
        img.src = fig.imageBaseUrl + '_images/' + element + '.svg';
        const span = document.createElement('span');
        span.innerText = '保存为 ' + element;
        child_dom.appendChild(img);
        child_dom.appendChild(span);
        child_dom.setAttribute('data-value', element);
        selectDom.appendChild(child_dom);
      }
      selectDom.addEventListener('click', (e) => {
        e.stopPropagation();
        let target = e.target;
        while (target.tagName !== 'LI') {
          target = target.parentNode;
        }
        value = target.getAttribute('data-value');
        if (value === 'fig') {
          fig.toolbar_button_onclick('export_fig');
        } else {
          fig.toolbar_button_onclick(method_name, value);
        }
        selectDom.style.display = 'none';
        button.classList.remove('active');
      });
    } else if (name === 'Draw') {
      //插入图形下拉
      const button = (fig.buttons[name] = document.createElement('button'));
      button.classList = 'mpl-widget';
      button.classList.add('mpl-more-widget');
      button.setAttribute('role', 'button');
      button.setAttribute('title', tooltip);
      button.setAttribute('aria-disabled', 'false');
      button.setAttribute('data-value', 'draw_line');
      const drawSelectDom = document.createElement('ul');
      drawSelectDom.id = 'draw_list';
      drawSelectDom.classList.add('fmt');
      for (let index = 0; index < mpl.drawTypes.length; index++) {
        const element = mpl.drawTypes[index];
        const child_dom = document.createElement('li');
        child_dom.title = element.name;
        child_dom.classList.add('fmt-child');
        const img = document.createElement('img');
        img.src = fig.imageBaseUrl + '_images/' + element.image + '.svg';
        const span = document.createElement('span');
        span.innerText = element.name;
        child_dom.appendChild(img);
        child_dom.appendChild(span);
        child_dom.setAttribute('data-value', element.method);
        drawSelectDom.appendChild(child_dom);
      }

      buttonGroup.appendChild(drawSelectDom);
      const icon_img = document.createElement('img');

      icon_img.src = fig.imageBaseUrl + '_images/' + image + '.svg';
      const down_button = document.createElement('img');
      down_button.classList.add('down-button');
      down_button.src = fig.imageBaseUrl + '_images/down.svg';
      const combo_img = document.createElement('div');
      combo_img.classList.add('combo-img');
      combo_img.appendChild(icon_img);
      combo_img.appendChild(down_button);
      combo_img.style.display = 'flex';
      combo_img.alt = tooltip;
      button.appendChild(combo_img);
      buttonGroup.appendChild(button);

      drawSelectDom.addEventListener('click', (e) => {
        let target = e.target;
        while (target.tagName !== 'LI') {
          target = target.parentNode;
        }
        value = target.getAttribute('data-value');
        button.setAttribute('data-value', value);
        icon_img.src = fig.imageBaseUrl + '_images/' + value + '.svg';
        this.send_message('toolbar_button', { name: value });
        // drawSelectDom.style.display='none';
      });
      icon_img.addEventListener('click', () => {
        const value = button.getAttribute('data-value');
        this.send_message('toolbar_button', { name: value });
      });
      down_button.addEventListener('click', function () {
        if (drawSelectDom.style.display !== 'block') {
          button.classList.add('active');
          drawSelectDom.style.display = 'block';
        }
      });
      document.addEventListener('click', (e) => {
        if (
          !button.contains(e.target) &&
          drawSelectDom.style.display === 'block'
        ) {
          drawSelectDom.style.display = 'none';
          button.classList.remove('active');
        }
      });
    } else if (name === 'Import Fig') {
      //导入fig下拉

      const selectDom = document.createElement('ul');
      selectDom.id = 'import_list';
      selectDom.classList.add('fmt');
      const button = renderMultiTools(selectDom, function () {
        fig.toolbar_button_onclick('import_fig');
      });
      for (let index = 0; index < mpl.importTypes.length; index++) {
        const element = mpl.importTypes[index];
        const child_dom = document.createElement('li');
        child_dom.title = element.label;
        child_dom.classList.add('fmt-child');
        const img = document.createElement('img');
        img.src = fig.imageBaseUrl + '_images/' + element.key + '.svg';
        const span = document.createElement('span');
        span.innerText = element.label;
        child_dom.appendChild(img);
        child_dom.appendChild(span);
        child_dom.setAttribute('data-value', element.key);
        selectDom.appendChild(child_dom);
      }
      selectDom.addEventListener('click', (e) => {
        e.stopPropagation();
        let target = e.target;
        while (target.tagName !== 'LI') {
          target = target.parentNode;
        }
        value = target.getAttribute('data-value');
        fig.toolbar_button_onclick(value);
        selectDom.style.display = 'none';
        button.classList.remove('active');
      });
    } else {
      const button = (fig.buttons[name] = document.createElement('button'));
      button.classList = 'mpl-widget';
      button.setAttribute('role', 'button');
      button.setAttribute('title', tooltip);
      button.setAttribute('aria-disabled', 'false');
      button.addEventListener('click', on_click_closure(method_name));
      var icon_img = document.createElement('img');

      icon_img.src = fig.imageBaseUrl + '_images/' + image + '.svg';

      icon_img.alt = tooltip;
      button.appendChild(icon_img);

      buttonGroup.appendChild(button);
    }
  }

  if (buttonGroup.hasChildNodes()) {
    toolbar.appendChild(buttonGroup);
  }
};

// 初始化右键菜单
mpl.figure.prototype._update_menu_list = function () {
  const menu_list = this.menu_list;
  const fig = this;
  this.menu_div.innerHTML = null;
  for (let index = 0; index < menu_list.length; index++) {
    const menu_item = menu_list[index];
    const menu_item_dom = document.createElement('div');
    menu_item_dom.id = 'menu_' + menu_item.value;
    menu_item_dom.classList.add('menu__item');
    menu_item_dom.innerText = menu_item.label;
    this.menu_div.appendChild(menu_item_dom);
    if (menu_item.disabled) {
      menu_item_dom.classList.add('disabled');
      continue;
    }
    if (menu_item.children.length === 0) {
      menu_item_dom.addEventListener('click', () => {
        fig.menu_item_onclick(menu_item.value, menu_item.default_value);
      });

      continue;
    }
    const icon_dom = document.createElement('span');
    icon_dom.classList.add('iconfont', 'icon-xiangyoujiantou');
    menu_item_dom.appendChild(icon_dom);
    const submenu_dom = document.createElement('div');
    submenu_dom.classList.add('submenu');
    // submenu_dom.style.top = `${10 + index * 15}px`;
    submenu_dom.id = menu_item.value;
    submenu_dom.addEventListener('click', (e) => {
      const value = e.target.getAttribute('data-value');
      // changeLine(value, "line.dash");
      fig.menu_item_onclick(menu_item.value, value);
    });
    for (
      let child_index = 0;
      child_index < menu_item.children.length;
      child_index++
    ) {
      const menu_child = menu_item.children[child_index];
      const menu_child_dom = document.createElement('div');
      menu_child_dom.classList.add('submenu__item');
      menu_child_dom.setAttribute('data-value', menu_child.value);
      if (menu_item.default_value === menu_child.value) {
        menu_child_dom.innerText = menu_child.label;
        const menu_i_dom = document.createElement('i');
        menu_i_dom.classList.add('el-icon-check');
        menu_child_dom.appendChild(menu_i_dom);
      } else {
        menu_child_dom.innerText = menu_child.label;
      }
      submenu_dom.appendChild(menu_child_dom);
    }
    menu_item_dom.appendChild(submenu_dom);
    menu_item_dom.addEventListener('mouseenter', (e) => {
      let submenu_dom = e.target.querySelector('.submenu');
      let menu_dom = e.target.parentElement;
      if (menu_dom && submenu_dom) {
        if (
          parseInt(menu_dom.style.left) +
            menu_dom.offsetWidth +
            submenu_dom.offsetWidth >
          document.body.offsetWidth
        ) {
          submenu_dom.style.left = -submenu_dom.offsetWidth + 'px';
        } else {
          submenu_dom.style.right = -submenu_dom.offsetWidth + 'px';
        }

        if (
          parseInt(menu_dom.style.top) +
            e.target.offsetTop +
            submenu_dom.offsetHeight >
          document.body.offsetHeight
        ) {
          let submenu_dom_bottom =
            parseInt(menu_dom.style.top) +
            e.target.offsetTop +
            e.target.offsetHeight -
            submenu_dom.offsetHeight;
          submenu_dom.style.bottom = Math.min(submenu_dom_bottom, 0) + 'px';
        } else {
          submenu_dom.style.top = '0px';
        }
      }
    });
  }

  if (
    document.body.clientWidth <
    this.menu_position.left + this.menu_div.clientWidth
  ) {
    this.menu_div.style.left =
      Math.max(this.menu_position.left - this.menu_div.clientWidth, 0) + 'px';
  } else {
    this.menu_div.style.left = this.menu_position.left + 'px';
  }
  if (
    document.body.clientHeight <
    this.menu_position.top + this.menu_div.clientHeight
  ) {
    this.menu_div.style.top =
      Math.max(this.menu_position.top - this.menu_div.clientHeight, 0) + 'px';
  } else {
    this.menu_div.style.top = this.menu_position.top + 'px';
  }
};
// figure重置尺寸 resize
mpl.figure.prototype.request_resize = function (x_pixels, y_pixels) {
  // Request matplotlib to resize the figure. Matplotlib will then trigger a resize in the client,
  // which will in turn request a refresh of the image.
  this.send_message('resize', { width: x_pixels, height: y_pixels });
};
// 发送消息
mpl.figure.prototype.send_message = function (type, properties) {
  properties['type'] = type;
  properties['figure_id'] = this.id;
  // console.log(properties)
  this.vscode_postMessage({ type: 'ws_send', value: properties });
  // this.ws.send(JSON.stringify(properties));
};
// 发送绘图信息
mpl.figure.prototype.send_draw_message = function () {
  // console.log('触发send_draw_message',Date.now());
  if (!this.waiting) {
    this.waiting = true;
    this.vscode_postMessage({
      type: 'ws_send',
      value: { type: 'draw', figure_id: this.id },
    });

    // this.ws.send(JSON.stringify({ type: 'draw', figure_id: this.id }));
  }
};
// 保存
mpl.figure.prototype.handle_save = function (fig, fmt) {
  // var format_dropdown = fig.format_dropdown;
  // var format = format_dropdown.options[format_dropdown.selectedIndex].value;
  this.vscode_postMessage({ type: 'download', value: fmt });
};
// 设置绘图刷新 refresh
let resizeDate = Date.now();
let resizeFrequency = 0;
mpl.figure.prototype.handle_resize = _.throttle(function (fig, msg) {
  var size = msg['size'];
  if (size[0] !== fig.canvas.width || size[1] !== fig.canvas.height) {
    fig._resize_canvas(size[0], size[1], msg['forward']);
    fig.send_message('refresh', {});
  }
},50);

// mpl.figure.prototype.handle_rubberband = function (fig, msg) {
//   var x0 = msg['x0'] / fig.ratio;
//   var y0 = (fig.canvas.height - msg['y0']) / fig.ratio;
//   var x1 = msg['x1'] / fig.ratio;
//   var y1 = (fig.canvas.height - msg['y1']) / fig.ratio;
//   x0 = Math.floor(x0) + 0.5;
//   y0 = Math.floor(y0) + 0.5;
//   x1 = Math.floor(x1) + 0.5;
//   y1 = Math.floor(y1) + 0.5;
//   var min_x = Math.min(x0, x1);
//   var min_y = Math.min(y0, y1);
//   var width = Math.abs(x1 - x0);
//   var height = Math.abs(y1 - y0);

//   fig.rubberband_context.clearRect(
//     0,
//     0,
//     fig.canvas.width / fig.ratio,
//     fig.canvas.height / fig.ratio
//   );

//   fig.rubberband_context.strokeRect(min_x, min_y, width, height);
// };

// 设置figure label
mpl.figure.prototype.handle_figure_label = function (fig, msg) {
  // Updates the figure title.
  if (fig.header) {
    fig.header.textContent = msg['label'];
  }
};
// 设置鼠标样式
mpl.figure.prototype.handle_cursor = function (fig, msg) {
  fig.canvas_div.style.cursor = msg['cursor'];
  if (msg['cursor'] === 'crosshair') {
    fig.InFigure = true;
  } else if (msg['cursor'] === 'default') {
    fig.InFigure = false;
  }
};
// figure监听消息
mpl.figure.prototype.handle_message = function (fig, msg) {
  if (fig.message) {
    fig.message.textContent = msg['message'];
  }
};
// figure触发绘图
mpl.figure.prototype.handle_draw = function (fig, _msg) {
  // Request the server to send over a new figure.
  fig.send_draw_message();
};
// 图片模式
mpl.figure.prototype.handle_image_mode = function (fig, msg) {
  fig.image_mode = msg['mode'];
};
// 右键菜单
mpl.figure.prototype.handle_contextmenu = function (fig, msg) {
  // console.log(msg)
  fig.menu_list = msg['menu_list'];
  fig._update_menu_list(this);
};

// 历史按钮
mpl.figure.prototype.handle_history_buttons = function (fig, msg) {
  for (var key in msg) {
    if (!(key in fig.buttons)) {
      continue;
    }
    fig.buttons[key].disabled = !msg[key];
    fig.buttons[key].setAttribute('aria-disabled', !msg[key]);
  }
};
// 更新工具栏状态
mpl.figure.prototype.handle_toolbar_update = function (fig, msg) {
  let key = msg['action'];
  if ('disabled' in msg) {
    fig.buttons[key].disabled = msg['disabled'];
  }
  if ('active' in msg) {
    let active = msg['active'];
    if (active) {
      fig.buttons[key].classList.add('active');
    } else {
      fig.buttons[key].classList.remove('active');
    }
  }
};
mpl.figure.prototype.handle_heartbeat = function (fig, msg) {
  // console.log('heartbeat');
};
// figure工具栏设置平移/缩放样式
mpl.figure.prototype.handle_navigate_mode = function (fig, msg) {
  if (msg['mode'] === 'PAN') {
    fig.buttons['Pan'].classList.add('active');
    fig.buttons['Zoom'].classList.remove('active');
  } else if (msg['mode'] === 'ZOOM') {
    fig.buttons['Pan'].classList.remove('active');
    fig.buttons['Zoom'].classList.add('active');
  } else if (msg['mode'] === 'SELECT') {
    fig.buttons['Pan'].classList.remove('active');
    fig.buttons['Zoom'].classList.remove('active');
  } else {
    fig.buttons['Pan'].classList.remove('active');
    fig.buttons['Zoom'].classList.remove('active');
  }
};
// websocket 重连
mpl.figure.prototype.handle_reconnect = function (fig, msg) {
  fig._reconnect_websocket();
};
mpl.figure.prototype.handle_init_websocket = function (fig, msg) {
  fig._init_websocket();
};
// websocket 关闭
mpl.figure.prototype.handle_close = function (fig, msg) {
  this.vscode_postMessage({ type: 'figure_not_find' });
  this.send_message('close');
};
// 弹窗
mpl.figure.prototype.handle_paste_reminder = function (fig, msg) {
  fig.confirmBox.show(
    '提示',
    '待粘贴数据量较大，是否继续粘贴',
    'paste_reminder'
  );
};

// 弹窗提示
mpl.figure.prototype.handle_show_dialog = function (fig, msg) {
  fig.confirmBox.show(msg.title, msg.message, '');
};
mpl.figure.prototype.handle_edit_finish = function (fig, msg) {
  fig.vscode_postMessage({ type: 'property_ready' });
};
// 更新canvas事件
mpl.figure.prototype.updated_canvas_event = function () {
  // Called whenever the canvas gets updated.
  // this.send_message('ack', {});
};
// 处理websocket消息
// A function to construct a web socket function for onmessage handling.
// Called in the figure constructor.
mpl.figure.prototype._make_on_message_function = function (fig) {
  return function socket_on_message(evt) {
    console.log("websocket消息收到的消息", evt);
    if (evt instanceof Blob) {
      var img = evt;
      if (img.type !== 'image/png') {
        /* FIXME: We get "Resource interpreted as Image but
         * transferred with MIME type text/plain:" errors on
         * Chrome.  But how to set the MIME type?  It doesn't seem
         * to be part of the websocket stream */
        img.type = 'image/png';
      }

      /* Free the memory for the previous frames */
      if (fig.imageObj.src) {
        (window.URL || window.webkitURL).revokeObjectURL(fig.imageObj.src);
      }

      fig.imageObj.src = (window.URL || window.webkitURL).createObjectURL(img);
      fig.updated_canvas_event();
      fig.waiting = false;
      return;
    } else if (
      typeof evt === 'string' &&
      evt.slice(0, 21) === 'data:image/png;base64'
    ) {
      fig.imageObj.src = evt;
      fig.updated_canvas_event();
      fig.waiting = false;
      return;
    }

    var msg = JSON.parse(evt);
    var msg_type = msg['type'];

    // Call the  "handle_{type}" callback, which takes
    // the figure and JSON message as its only arguments.
    try {
      var callback = fig['handle_' + msg_type];
    } catch (e) {
      console.log("No handler for the '" + msg_type + "' message type: ", msg);
      return;
    }

    if (callback) {
      try {
        // console.log("Handling '" + msg_type + "' message: ", msg);
        callback(fig, msg);
      } catch (e) {
        console.log(
          "Exception inside the 'handler_" + msg_type + "' callback:",
          e,
          e.stack,
          msg
        );
      }
    }
  };
};

/*
 * return a copy of an object with only non-object keys
 * we need this to avoid circular references
 * https://stackoverflow.com/a/24161582/3208463
 */
function simpleKeys(original) {
  return Object.keys(original).reduce(function (obj, key) {
    if (typeof original[key] !== 'object') {
      obj[key] = original[key];
    }
    return obj;
  }, {});
}
// 鼠标事件
mpl.figure.prototype.mouse_event = function (event, name) {
  if (name === 'button_press') {
    this.canvas.focus();
    this.canvas_div.focus();
  }
  if (event.button === 2) {
    event.preventDefault();
    //根据事件对象中鼠标点击的位置，进行定位
    this.menu_position.left = event.clientX;
    this.menu_position.top = event.clientY;
  }
  // from https://stackoverflow.com/q/1114465
  var boundingRect = this.canvas.getBoundingClientRect();
  var x = (event.clientX - boundingRect.left) * this.ratio;
  var y = (event.clientY - boundingRect.top) * this.ratio;

  this.send_message(name, {
    x: x,
    y: y,
    button: event.button,
    step: event.step,
    guiEvent: simpleKeys(event),
  });
  return false;
};

mpl.figure.prototype._key_event_extra = function (_event, _name) {
  // Handle any extra behaviour associated with a key event
};
// 键盘事件
mpl.figure.prototype.key_event = function (event, name) {
  // Prevent repeat events
  if (name === 'key_press') {
    if (event.key === this._key) {
      return;
    } else {
      this._key = event.key;
    }
  }
  if (name === 'key_release') {
    this._key = null;
  }

  var value = '';
  if (event.ctrlKey && event.key !== 'Control') {
    value += 'ctrl+';
  } else if (event.altKey && event.key !== 'Alt') {
    value += 'alt+';
  } else if (event.shiftKey && event.key !== 'Shift') {
    value += 'shift+';
  }

  value += 'k' + event.key;

  this._key_event_extra(event, name);

  this.send_message(name, { key: value, guiEvent: simpleKeys(event) });
  return false;
};
// 工具栏点击事件
mpl.figure.prototype.toolbar_button_onclick = function (name, value) {
  if (name === 'download') {
    this.vscode_postMessage({ type: 'download', value });
  } else if (name === 'export_csv') {
    this.vscode_postMessage({ type: 'export_csv' });
    // } else if (name === 'export_figure') {
    //   this.vscode_postMessage({ type: 'export_figure' });
  } else if (name === 'property_setting') {
    this.vscode_postMessage({ type: 'property_setting' });
    // this.send_message({type:"property_init"});
  } else if (name === 'export_fig') {
    this.vscode_postMessage({ type: 'export_fig' });
  } else if (name === 'import_fig') {
    this.vscode_postMessage({ type: 'import_fig' });
  } else if (name === 'import_current_fig') {
    this.vscode_postMessage({ type: 'import_current_fig' });
  } else {
    this.send_message('toolbar_button', { name: name });
  }
};
// 右键菜单点击事件yin
mpl.figure.prototype.menu_item_onclick = function (key, value) {
  // this.send_message("set_figure_attribute", { [key]: value });
  if (key === 'del_datatip') {
    this.send_message('delete_current_datatip', { label: key, value: value });
  } else if (key === 'delall_datatips') {
    this.send_message('delete_all_datatips', { label: key, value: value });
  } else if (key === 'color') {
    this.colorPicker.show(value);
  } else if (key === 'property') {
    this.vscode_postMessage({ type: 'property_setting', value });
  } else if (key === 'text_edit') {
    this.textEditor.show(value, 'textarea');
  } else if (key === 'adjust_datumline_coordinate') {
    this.textEditor.show(value, 'input');
  } else {
    this.send_message('set_prop', { label: key, value: value });
  }
  this.menu_div.style.left = -1000 + 'px';
  this.menu_div.style.top = -1000 + 'px';
};
// 工具栏hover出现tooltip
mpl.figure.prototype.toolbar_button_onmouseover = function (tooltip) {
  if (this.message) {
    this.message.textContent = tooltip;
  }
};

///////////////// REMAINING CONTENT GENERATED BY embed_js.py /////////////////
// prettier-ignore
var _JSXTOOLS_RESIZE_OBSERVER = function (A) { var t, i = new WeakMap, n = new WeakMap, a = new WeakMap, r = new WeakMap, o = new Set; function s(e) { if (!(this instanceof s)) throw new TypeError("Constructor requires 'new' operator"); i.set(this, e) } function h() { throw new TypeError("Function is not a constructor") } function c(e, t, i, n) { e = 0 in arguments ? Number(arguments[0]) : 0, t = 1 in arguments ? Number(arguments[1]) : 0, i = 2 in arguments ? Number(arguments[2]) : 0, n = 3 in arguments ? Number(arguments[3]) : 0, this.right = (this.x = this.left = e) + (this.width = i), this.bottom = (this.y = this.top = t) + (this.height = n), Object.freeze(this) } function d() { t = requestAnimationFrame(d); var s = new WeakMap, p = new Set; o.forEach((function (t) { r.get(t).forEach((function (i) { var r = t instanceof window.SVGElement, o = a.get(t), d = r ? 0 : parseFloat(o.paddingTop), f = r ? 0 : parseFloat(o.paddingRight), l = r ? 0 : parseFloat(o.paddingBottom), u = r ? 0 : parseFloat(o.paddingLeft), g = r ? 0 : parseFloat(o.borderTopWidth), m = r ? 0 : parseFloat(o.borderRightWidth), w = r ? 0 : parseFloat(o.borderBottomWidth), b = u + f, F = d + l, v = (r ? 0 : parseFloat(o.borderLeftWidth)) + m, W = g + w, y = r ? 0 : t.offsetHeight - W - t.clientHeight, E = r ? 0 : t.offsetWidth - v - t.clientWidth, R = b + v, z = F + W, M = r ? t.width : parseFloat(o.width) - R - E, O = r ? t.height : parseFloat(o.height) - z - y; if (n.has(t)) { var k = n.get(t); if (k[0] === M && k[1] === O) return } n.set(t, [M, O]); var S = Object.create(h.prototype); S.target = t, S.contentRect = new c(u, d, M, O), s.has(i) || (s.set(i, []), p.add(i)), s.get(i).push(S) })) })), p.forEach((function (e) { i.get(e).call(e, s.get(e), e) })) } return s.prototype.observe = function (i) { if (i instanceof window.Element) { r.has(i) || (r.set(i, new Set), o.add(i), a.set(i, window.getComputedStyle(i))); var n = r.get(i); n.has(this) || n.add(this), cancelAnimationFrame(t), t = requestAnimationFrame(d) } }, s.prototype.unobserve = function (i) { if (i instanceof window.Element && r.has(i)) { var n = r.get(i); n.has(this) && (n.delete(this), n.size || (r.delete(i), o.delete(i))), n.size || r.delete(i), o.size || cancelAnimationFrame(t) } }, A.DOMRectReadOnly = c, A.ResizeObserver = s, A.ResizeObserverEntry = h, A }; // eslint-disable-line
mpl.toolbar_items = [
  ['Import Fig', 'Open Syslab Fig', 'import_fig', 'import_fig'],
  ['Save', 'Save as', 'save', 'download'],
  // ['Save as', 'Save as the Syslab Figure', 'save_as', 'exsport_figure'],
  ['Export', 'Export csv ', 'export_csv', 'export_csv'],
  // ['Export Fig', 'Export .csv file', 'export_csv', 'export_fig'],

  ['', '', '', ''],
  ['Pan', 'Pan axes with left mouse,zoom with right', 'pan', 'ty_pan'],
  ['Zoom', 'Zoom to rectangle', 'zoom_in', 'ty_zoom'],
  ['Home', 'Reset original view', 'home', 'home'],
  ['Back', 'Back to previous view', 'back', 'back'],
  ['Forward', 'Forward to next view', 'forward', 'forward'],
  ['', '', '', ''],
  ['Cursor', 'Cursor line', 'cursor', 'cursor'],
  ['DataTips', 'Data tips', 'data_tips', 'data_tips'],
  ['Grid', 'Show grid', 'grid', 'grid'],
  ['Legend', 'Show legend', 'legend', 'legend'],
  // ['Colorbar', 'Colorbar', 'colorbar', 'colorbar'],
  // ['AdjustMargin', 'Adjust margin', 'adjust_margin', 'adjust_margin'],
  ['', '', '', ''],
  // ['DrawText', 'Draw text', 'draw_text', 'draw_text'],
  // ['DrawRect', 'Draw rectangle', 'draw_rect', 'draw_rect'],
  // ['DrawEllipse', 'Draw ellipse', 'draw_ellipse', 'draw_ellipse'],
  // ['DrawLine', 'Draw line', 'draw_line', 'draw_line'],
  // ['DrawArrow', 'Draw arrow', 'draw_arrow', 'draw_arrow'],
  // ['DrawTextArrow', 'Draw text arrow', 'draw_text_arrow', 'draw_text_arrow'],
  // [
  //   'DrawDoubleArrow',
  //   'Draw double arrow',
  //   'draw_double_arrow',
  //   'draw_double_arrow',
  // ],
  ['Draw', 'Draw', 'draw_line', 'draw_line'],
  ['', '', '', ''],
  ['EditMode', 'Edit Mode', 'edit_mode', 'editmode'],
  ['PropertySetting', 'Property setting', 'setting', 'property_setting'],
];
// 导出格式
// mpl.extensions = ['eps', 'jpeg', 'pdf', 'png', 'svg', 'tif'];
mpl.extensions = ['fig', 'png', 'jpg', 'svg', 'tif'];
mpl.drawTypes = [
  { type: 'line', name: '线', image: 'draw_line', method: 'draw_line' },
  { type: 'arrow', name: '箭头', image: 'draw_arrow', method: 'draw_arrow' },
  {
    type: 'textArrow',
    name: '文本箭头',
    image: 'draw_text_arrow',
    method: 'draw_text_arrow',
  },
  {
    type: 'doubleArrow',
    name: '双箭头',
    image: 'draw_double_arrow',
    method: 'draw_double_arrow',
  },
  { type: 'text', name: '文本框', image: 'draw_text', method: 'draw_text' },
  { type: 'rect', name: '矩形', image: 'draw_rect', method: 'draw_rect' },
  {
    type: 'ellipse',
    name: '椭圆',
    image: 'draw_ellipse',
    method: 'draw_ellipse',
  },
];
mpl.default_extension = 'png';

mpl.importTypes = [
  { key: 'import_fig', label: '在新窗口中打开' },
  { key: 'import_current_fig', label: '在当前窗口中打开' },
];
