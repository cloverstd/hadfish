/*
 * 2013.07.17
 * @Cloverstd
 */

function fileQueueError(file, errorCode, message) {
    var errorMsg = '';
    switch (errorCode) {
        case SWFUpload.QUEUE_ERROR.QUEUE_LIMIT_EXCEEDED:
            errorMsg = "您选择的文件过多，只允许上传" + this.settings.file_upload_limit + "个文件";
            break;
        case SWFUpload.QUEUE_ERROR.FILE_EXCEEDS_SIZE_LIMIT:
            errorMsg = "您选择的文件过大，只允许上传" + this.settings.file_size_limit + "MB 的文件";
            break;
        case SWFUpload.QUEUE_ERROR.ZERO_BYTE_FILE:
            errorMsg = "文件不允许为空";
            break;
        case SWFUpload.QUEUE_ERROR.INVALID_FILETYPE:
            errorMsg = "只允许上传" + this.settings.file_types + "的文件";
            break;
        default:
            errorMsg = "未知错误，请联系管理员"
            break;
    }
    $("#imgerror").html(errorMsg);
}

function fileDialogComplete(numFilesSelected, numFilesQueued) {
    initSuccessfuUploads();
    if (numFilesQueued > 0) {
        this.startUpload();
    }
}

function uploadStart(file) {
    initSuccessfuUploads();
    var span = $('<span></span>');
    var div = $('<div></div>');
    //var test = $('<a></a>');
    //test.addClass("delimg");
    //test.html("X");
    // img.attr("src", "/static/js/swfupload/uploader.gif");
    div.addClass("imgprocess");
    div.css("display", "none");
    // div.html("100%");
    div.appendTo(span);
    //test.appendTo(span);
    span.appendTo($('#wait-uploadimg'));

    /*
    var li = $('<li class="postimg-item"></li>');
    var img = $('<img class="postimg-item-img img-polaroid"/>');
    img.attr("src", "/static/js/swfupload/uploader.gif");
    img.appendTo(li);
    li.append('<span class="postimg-item-msg"></span>');
    li.appendTo($(".postimg"));
    */
    var t = new Date();
    var timeFormat = "" + t.getFullYear() + t.getMonth() + t.getDate() + t.getHours() + t.getMinutes() + t.getSeconds() + t.getMilliseconds();
    var index = this.getStats().successful_uploads;
    //console.log(index);
    //console.log(SETTINGS.successful_uploads);
    //index += SETTINGS.successful_uploads;
    //console.log(index);
    //var key = QINIU.uid.toString() + "-" + timeFormat + "-" + Math.floor((Math.random()*100)+1).toString() + file.type;
    var key = QINIU.uid.toString() + "-" + timeFormat + "-" + index + file.type;
    this.addFileParam(file.id, "key", key);
    //console.log(swfu.getStats().successful_uploads + 1);
}

function uploadProgress(file, bytesLoaded) {
    var percent = Math.ceil((bytesLoaded / file.size) * 100);

    myProgress(file, percent);
}

function uploadSuccess(file, serverData) {
    //console.log(serverData);
    var result = $.parseJSON(serverData);
    if (result.key){
        var index = swfu.getStats().successful_uploads - 1;
        var msg = $(".imgprocess").eq(index);
        msg.css("display", "none");
        var delimg = $('<a></a>');
        delimg.addClass("delimg");
        delimg.html("X");
        delimg.attr('onClick', 'delUploadedFile($(this))')
        delimg.attr('href', 'javascript:void(0);');
        delimg.data("filename", result.key);
        delimg.appendTo($('#wait-uploadimg span').eq(index));
        var span= $('#wait-uploadimg span').eq(index);
        var img = $('<img />');
        img.attr('src', "http://" + QINIU.name + ".qiniudn.com/" + result.key + "_90.90");
        img.appendTo(span);

        //console.log(index);
        //index += SETTINGS.successful_uploads;
        /*
        $(".postimg-item-img").eq(index).attr("src", "http://" + QINIU.name + ".qiniudn.com/" + result.key + "_thumb120.120");
        $(".postimg-item-msg").eq(index).html("上传完成");
        $(".postimg-item").eq(index).append($('<a data-filename="' + result.key + '" class="postimg-item-del" href="javascript:void(0)" onClick="delUploadedFile(this);"><i class="icon-trash"></i></a>'));
        */
        // 添加到 form 里
        //$(".postimg-item").eq(index).append($('<input hidden name="img_' + index + '"' + ' value="' + serverData.substring(9) + '" />'));
        if (index !== 0) {
            var value = $("#postimg-ipt").attr("value") + ";" + result.key;
        } else {
            value = result.key;
        }
        $("#postimg-ipt").attr("value", value);
    } else {
        console.log("错误");
        console.log(result);
    }

    /*
    if (serverData.substring(0, 9) === "FILENAME:") {
        //console.log(serverData);
        var index = swfu.getStats().successful_uploads - 1;
        $(".postimg-item-img").eq(index).attr("src", "http://hadfish.qiniudn.com/" + serverData.substring(9) + "_test");
        $(".postimg-item-msg").eq(index).html("上传完成");
        $(".postimg-item").eq(index).append($('<a class="postimg-item-del" href="javascript:void(0)" onClick="delUploadedFile(this);">删除</a>'));

        // 添加到 form 里
        //$(".postimg-item").eq(index).append($('<input hidden name="img_' + index + '"' + ' value="' + serverData.substring(9) + '" />'));
        if (index !== 0) {
            var value = $("#postimg-ipt").attr("value") + ";" + serverData.substring(9);
        } else {
            value = serverData.substring(9);
        }
        $("#postimg-ipt").attr("value", value);
    } else {
        $("#errorMsg").html("发生了一些错误，请重新上传");
    }
    */
}

function uploadComplete(file) {
    /*  I want the next upload to continue automatically so I'll call startUpload here */
    if (this.getStats().files_queued > 0) {
        this.startUpload();
    } else {
        $("#imgerror").html("文件全部上传成功");
        $('#imgprocess').html(null);
    }
}

function uploadError(file, errorCode, message) {
    console.log("test");
    errorMsg = '';
    switch (errorCode) {
        case SWFUpload.UPLOAD_ERROR.FILE_CANCELLED:
            errorMsg = "上传被取消了";
            break;
        case SWFUpload.UPLOAD_ERROR.UPLOAD_STOPPED:
            errorMsg = "上传被中止了";
            break
        case SWFUpload.UPLOAD_ERROR.UPLOAD_LIMIT_EXCEEDED:
            errorMsg = "只允许上传" + this.settings.file_upload_limit + "个文件";
            break;
        default:
            error = "出现了未知错误，请联系管理员";
            break;
    }
    $("#imgerror").html(errorMsg);
}

function swfuInit(){
    swfu = new SWFUpload({
        upload_url: "http://up.qiniu.com/",
        file_post_name: "file",
        post_params: {
            "token": QINIU.token
        },

        // File Upload Settings
        file_size_limit: "5 MB",	// 5MB
        file_types: "*.jpg;*.png;*.jpeg",
        file_types_description: "文件类型",
        //file_upload_limit: SETTINGS.file_upload_limit,  // 最多 6 张图片
        file_upload_limit: 6,  // 最多 6 张图片

        // Event Handler Settings - these functions as defined in Handlers.js
        file_queue_error_handler: fileQueueError, // 文件添加到队列失败时会触发这个函数 
        file_dialog_complete_handler: fileDialogComplete,  // 文件选择完毕切选择的文件处理后会触发这个函数
        upload_progress_handler: uploadProgress, // 在文件上传的过程中反复触发
        upload_error_handler: uploadError, // 文件上传被中断或者文件没有成功上传会触发
        upload_success_handler: uploadSuccess, // 文件成功上传时触发
        upload_complete_handler: uploadComplete, // 文件上传的流程完成时（无论成败）会触发
        upload_start_handler : uploadStart, // 文件开始上传触发

        // Button Settings
        //button_image_url : "static/images/SmallSpyGlassWithTransperancy_17x18.png",
        button_placeholder_id: "buttonUpload",
        button_width: 51,
        button_height: 18,
        button_text: '<span class="button">选择文件</span>',
        button_text_style: '.button { font-size: 12pt; }',
        button_text_top_padding: 0,
        button_text_left_padding: 0,
        //button_window_mode: SWFUpload.WINDOW_MODE.TRANSPARENT,
        //button_cursor: SWFUpload.CURSOR.HAND,
        
        // Flash Settings
        flash_url : "/static/js/swfupload/swfupload.swf",

        custom_settings : {
            upload_target: "publish-list",
            uploader_img: "/static/js/swfupload/uploader.gif"
        },
        
        // Debug Settings
        debug: false
    });
}

function myProgress(file, percent) {
    //console.log("success");
    //console.log(swfu.getStats().successful_uploads);
    var msg = $(".imgprocess").eq(swfu.getStats().successful_uploads);
    msg.css("display", "block");
    msg.html(percent + "%");
    $('#imgerror').html(null);
    var cur = swfu.getStats().successful_uploads + 1;
    var wait = swfu.getStats().files_queued - 1;
    $('#imgprocess').html(wait + '等待上传，' + '正在上传第' + cur + '个文件');
}

function delUploadedFile(element) {
    initSuccessfuUploads();
    handleDelUploadedFile(element.data('filename'));
    element.parent().remove();
    var stats = swfu.getStats();
    stats.successful_uploads--;
    swfu.setStats(stats);
}

function handleDelUploadedFile(filename) {
    var ipt = $("#postimg-ipt").attr("value").split(';');
    var index = 0;
    for (var index = 0; index < ipt.length; index++) {
        if (ipt[index] === filename) {
            break;
        }
    }
    ipt.splice(index, 1);
    $("#postimg-ipt").attr("value", ipt.join(';'));
}

function initSuccessfuUploads() {
    if (SETTINGS.successful_uploads) {
        var stats = swfu.getStats();
        stats.successful_uploads = SETTINGS.successful_uploads;
        swfu.setStats(stats);
        SETTINGS.successful_uploads = undefined;
    }
}
