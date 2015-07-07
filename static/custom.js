$('#btn-edit').bind("click", function (e) {
        e.preventDefault();
        editToggle();
})

$('#btn-add-new').bind("click", function (e) {
        editToggle();
})

$('li').click( function () {
    $(".modify-buttons").fadeOut();
    $('#btn-edit').removeClass("ui-btn-active");
})


function editToggle() {

    if ( $(".modify-buttons").css('display') == 'none') {
        $(".modify-buttons").fadeIn();
        $('#btn-add-new').fadeIn();
        $('#btn-edit').addClass("ui-btn-active");
    } else {
        $(".modify-buttons").fadeOut();
        $('#btn-add-new').fadeOut();
        $('#btn-edit').removeClass("ui-btn-active");
   }

};

jQuery("#menu").on('pagebeforeshow', function(event, data) {
    $('#btn-add-new').hide();
});
