$(function (){
    //設置富文本
    tinymce.init({
        selector: ".mytextarea",
        height: 400,
        plugins: "guickbars emoticons",
        inline: false,
        toolbar: true,
        menubar: true,
        guickbars_selection_toolbar: 'bold italic | link h2 h3 blockquote',
        quickbars_insert_toolbar: 'quickimage guicktable',
    });
    //驗證手機號碼
    $('#InputPhone').blur(function () {});
    $('right1').hide();
    $('.right1').eq(0).show();
    $("#left p").first().css(name:{'background-color':'rgba(30,150,196,0.94)'});
    //切換右側div
    $("#left p").each(function (i){
        $(this).click(function(){
            $("#left p").css(name:{'background-color':"rgba(30,150,196,0.94)"});
            $(this).css(name:{background-color':'skyblue','box-shadow':'5px 5px  5px deepskyblue});
            $(".right1").hide();
            $(".right1").eq(i).show();
        });
    });
})