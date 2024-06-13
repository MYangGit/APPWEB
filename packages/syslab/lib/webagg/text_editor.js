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
    function TextEditor(opt){
        if(this ===window){throw `TextEditor: Can't call a function directly`;}
        this.init(opt);
    }
    TextEditor.prototype = {
        init(opt){
            /**
            *@param:{confirm:function}
            **/
            this.opt = opt;
            this.editContent = "";
            this.type='input';
            // 渲染dom
            const div = document.createElement("div");
            div.innerHTML = this.render(opt.content);
            div.style.display = 'none';
            document.body.appendChild(div);
            this.elem_wrap = div;
            const mask = document.createElement("div");
            mask.classList.add("editor-mask");
            document.body.appendChild(mask);

            this.mask = mask;
            const _this = this;
            const confirmBtn = document.getElementById("textEditConfirm");
            const cancelBtn = document.getElementById("textEditCancel");
            this.textInput = document.getElementById("textEditInput");
            this.textEditTextarea = document.getElementById("textEditTextarea");
            confirmBtn.addEventListener('click',function() {
                // 确定
                let value;
                if(_this.type === 'input'){
                    console.log(/^\d+(\.\d+)?$/.test(_this.textInput.value));
                    if(/^\d+(\.\d+)?$/.test(_this.textInput.value)){
                        value = _this.textInput.value;
                        _this.opt.confirm(value,'adjust_datumline_coordinate');
                        _this.hide();

                    }else {
                        _this.textInput.value = this.editContent;
                    }

                }else if(_this.type === 'textarea'){
                    value = _this.textEditTextarea.value.replace(/(?:\r\n|\r|\n)/g,'\\n');
                    _this.opt.confirm(value,'text_edit');
                    _this.hide();

                }

                // console.log(_this.opt);
            });
            cancelBtn.addEventListener('click',function(){
                // 取消
                _this.hide();

            });
            // textInput.addEventListener("input",function(e){
            //     // _this.editContent = textInput
            //     console.log(e.target.value);
            // });
        },
        render(content){
            return `
            <div class="content-card">
                <div class="text-edit-title">编辑</div>
                <textarea id="textEditTextarea" class="text-edit-input"></textarea>
                <input id="textEditInput" class="text-edit-input"></input>
                <div class="text-edit-options">
                    <button id="textEditConfirm" style="margin-right:5px">确定</button>
                    <button id="textEditCancel">取消</button>
                </div>
            </div>
            `;
        },
        /**
         * @param {String}content
         */ 
        show(content,type='textarea'){
            this.type = type;
            util.css(this.elem_wrap,{
                "display":"block"
            });
            util.css(this.mask,{
                "display":"block"
            });
            if(this.type === 'textarea'){
                util.css(this.textInput,{
                    "display":"none"
                });
                this.textEditTextarea.value = content;
            }else if(this.type === 'input'){
                util.css(this.textEditTextarea,{
                    "display":"none"
                });
                this.textInput.value = content;
            }
            this.editContent = content;

        },
        hide(){
            util.css(this.elem_wrap,{
                "display":"none"
            });
            util.css(this.mask,{
                "display":"none"
            });
            this.textInput.value = null;
            this.editContent = null;
        }
    };
    TextEditor.create = function(opt){
        return new TextEditor(opt);
    };
    window.TextEditor = TextEditor;
})();