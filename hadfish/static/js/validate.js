$(document).ready(function(){
    /* 自定义验证器 */
    jQuery.validator.addMethod("tel", function(value, element) {       
        var length = value.length;   
        var mobile = /^(((13[0-9]{1})|(15[0-9]{1}))+\d{8})$/;   
        return this.optional(element) || (length == 11 && mobile.test(value));       
    }, "请正确填写您的手机号码");
    jQuery.validator.addMethod("qq", function(value, element) {
        var tel = /^[1-9]\d{4,9}$/;
        return this.optional(element) || (tel.test(value));
    }, "QQ 号错误");

    /* 注册表单验证 */
    if ($('#regform')) {
    $('#regform').validate({
        errorPlacement: function(error, element) {
            var $error = error;
            var $regerror = element.parent().next();
            $regerror.append($error);
            $regerror.children().eq(0).css("display", "none");
        },
        errorElement: "span",
        //errorClass: "alert-wrong",
        debug: true,
        rules: {
            username: {
                required: true,
                rangelength:[6,20]
            },
            email: {
                required: true,
                email: true,
                maxlength: 50
            },
            password: {
                required: true,
                rangelength:[6,32]
            },
            password2: {
                required: true,
                equalTo: "input[name=password]"
            },
            tel: {
                tel: true
            },
            QQ: {
                qq: true
            }

        },
        messages: {
            email: {
                required: "请输入邮箱",
                email: "请输入正确的 email 地址",
                maxlength: "邮箱不能超过50个字符"
            },
            username: {
                required: "请输入用户名",
                rangelength: jQuery.format("用户名需要{0}到{1}个字符")

            },
            password: {
                required: "请输入密码",
                rangelength: jQuery.format("密码需要{0}到{1}个字符")
            },
            password2: {
                required: "请再输入一遍密码",
                equalTo: "两次密码不一样"
            },
        },
        success: function(span) {
            span.prev().css("display", "block");
            span.remove();
        }
    });
    }
    if ($('#loginform')) {
    /* 登录表单验证 */
    $('#loginform').validate({
        errorPlacement: function(error, element) {
            var $error = error;
            var $regerror = element.parent().next();
            $regerror.append($error);
            //$regerror.children().eq(0).css("display", "none");
        },
        errorElement: "span",
        //errorClass: "alert-wrong",
        debug: true,
        rules: {
            username: {
                required: true,
            },
            password: {
                required: true,
            },
        },
        messages: {
            username: {
                required: "请输入用户名",
            },
            password: {
                required: "请输入密码",
            }
        },
        success: function(span) {
            //span.prev().css("display", "block");
            span.remove();
        }
    });
    }

    $('.reginput').focusin(function() {
        $(this).parent().parent().children().eq(3).fadeIn();
    });

    $('.reginput').focusout(function() {
        $(this).parent().parent().children().eq(3).fadeOut();
    });
});

