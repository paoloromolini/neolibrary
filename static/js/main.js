let author = $('input[name="author"]');
author.keyup(function() {
    $.get('/authors?q=' + author.val(), function( data ) {
        let authorAutoComplete = $('.author-auto-complete');
        if (authorAutoComplete.length > 0 ) {
            authorAutoComplete.replaceWith(data);
        } else {
            author.parent().append(data);
        }
    });
});

function changeInputWithValue(value) {
    author.val(value);
    $('.author-auto-complete').remove();
}

$(document).on('click',function(){
    $('.author-auto-complete').remove();
});

function resetForm(){
  $('input').val('');
  $('select').prop('selectedIndex',0);
};