(function () {
    const util = {
        css: function (elem, obj) {
            for (var i in obj) {
                elem.style[i] = obj[i];
            }
        },
        hasClass: function (elem, classN) {
            var className = elem.getAttribute("class");
            return className.indexOf(classN) != -1;
        }
    };
    /**
     * @param {{confirm:Function}} opt
     * 
     */
    function ConfirmBox(opt) {
        if (this === window) { throw `ConfirmBox: Can't call a function directly`; }
        this.init(opt);
    }
    ConfirmBox.prototype = {
        init(opt) {
            /**
            *@param:{confirm:function}
            **/
            this.opt = opt;
            // this.content = "";
            this.key = '';
            this.title = '';
  
            // 渲染dom
            const div = document.createElement("div");
            div.innerHTML = this.render(this.title, this.content);
            div.style.display = 'none';
            document.body.appendChild(div);
            this.elem_wrap = div;
            const mask = document.createElement("div");
            mask.classList.add("editor-mask");
            document.body.appendChild(mask);

            this.mask = mask;
            const _this = this;
            const confirmBtn = document.getElementById("confirmBoxConfirm");
            const cancelBtn = document.getElementById("confirmBoxCancel");

            this.confirmBtn = confirmBtn;
            this.cancelBtn = cancelBtn;

            // title
            const mplConfirmTitle = document.getElementById('mplConfirmTitle');
            this.mplConfirmTitleDom = mplConfirmTitle;
            // 内容
            const mplConfirmContent = document.getElementById('mplConfirmContent');
            this.mplConfirmContentDom = mplConfirmContent;
            confirmBtn.addEventListener('click', function () {
                // 确定
                // let value;
                _this.hide();
                if(_this.key){
                    _this.opt.confirm(_this.key, true);
                }

                // console.log(_this.opt);
            });
            cancelBtn.addEventListener('click', function () {
                // 取消
                _this.hide();
                if(_this.key){
                    _this.opt.cancel(_this.key, false);
                }

            });
            // textInput.addEventListener("input",function(e){
            //     // _this.content = textInput
            //     console.log(e.target.value);
            // });
        },
        render(title, content) {
            return `
            <div class="content-card">
                <div class="confirm-box">
                <div class='mplConfirmTitle'>
                    <img class="logo" src="${this.opt.imageBaseUrl + '_images/logo.svg'}"/>
                    <span id="mplConfirmTitle">${title}</span>
                </div>
                <div id='mplConfirmContent'>${content}</div>
                </div>
                <div class="text-edit-options">
                    <button id="confirmBoxConfirm" style="margin-right:5px">确定</button>
                    <button id="confirmBoxCancel">取消</button>
                </div>
            </div>
            `;
        },
        /**
         * @param {String}content
         */
        show(title, content, key) {
            util.css(this.elem_wrap, {
                "display": "block"
            });
            util.css(this.mask, {
                "display": "block"
            });
            this.key = key;
            this.content = content;
            this.mplConfirmTitleDom.innerText = title;
            this.mplConfirmContentDom.innerText = content;
            if(key === ''){
                this.cancelBtn.style.display = 'none';
            }
        },
        hide() {
            util.css(this.elem_wrap, {
                "display": "none"
            });
            util.css(this.mask, {
                "display": "none"
            });
            this.content = null;
        }
    };
    ConfirmBox.create = function (opt) {
        return new ConfirmBox(opt);
    };
    window.ConfirmBox = ConfirmBox;
})();