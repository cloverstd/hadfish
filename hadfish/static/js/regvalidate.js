    $('#regform').validate({
        /*
        errorPlacement: function(error, element) {
        },
        */
        rules: {
            username: {
                required: true,
                maxlength: 20
            },
            email: {
                required: true,
                email: true,
                maxlength: 50
            }
        },
        messages: {
            email: {
                required: "邮箱必填",
                email: "请输入正确的 email 地址",
                maxlength: "邮箱不能超过50个字符"
            },
            username: {
                required: "用户名必须的",
                maxlength: "用户名不能超过 20 个字符"
            }
        },
        success: function(label) {
            label.addClass("success");
        }
    });

$('.reginput').focusin(function() {
    $(this).parent().parent().children().eq(3).fadeIn();
});

$('.reginput').focusout(function() {
    $(this).parent().parent().children().eq(3).fadeOut();
});
