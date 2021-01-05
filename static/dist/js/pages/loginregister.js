$(document).ready(function () {
    $('#mostrar').on('click', function () {
        console.log($('#id_password').attr('type'));
        if($('#id_password').attr('type')=='password'){
            $(this).addClass('fa-eye').removeClass('fa-eye-slash');
            $('#id_password').attr('type','text');
        }else{
            $('#id_password').attr('type','password');
            $(this).addClass('fa-eye-slash').removeClass('fa-eye');
        }
    });

    $('#mostrar_pass1').on('click', function () {
        if($('#id_password1').attr('type')=='password'){
            $(this).addClass('fa-eye').removeClass('fa-eye-slash');
            $('#id_password1').attr('type','text');
        }else{
            $('#id_password1').attr('type','password');
            $(this).addClass('fa-eye-slash').removeClass('fa-eye');
        }
    });
    
    $('#mostrar_pass2').on('click', function () {
        if($('#id_password2').attr('type')=='password'){
            $(this).addClass('fa-eye').removeClass('fa-eye-slash');
            $('#id_password2').attr('type','text');
        }else{
            $('#id_password2').attr('type','password');
            $(this).addClass('fa-eye-slash').removeClass('fa-eye');
        }
    });


    $('#mostrar_pass1').on('click', function () {
        if($('#id_new_password1').attr('type')=='password'){
            $(this).addClass('fa-eye').removeClass('fa-eye-slash');
            $('#id_new_password1').attr('type','text');
        }else{
            $('#id_new_password1').attr('type','password');
            $(this).addClass('fa-eye-slash').removeClass('fa-eye');
        }
    });
    
    $('#mostrar_pass2').on('click', function () {
        if($('#id_new_password2').attr('type')=='password'){
            $(this).addClass('fa-eye').removeClass('fa-eye-slash');
            $('#id_new_password2').attr('type','text');
        }else{
            $('#id_new_password2').attr('type','password');
            $(this).addClass('fa-eye-slash').removeClass('fa-eye');
        }
    });
})