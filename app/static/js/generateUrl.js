$(function() {
    $('#generateUrlBtn').click(function() {
        $.ajax({
            url: '/generateUrl',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                window.location.replace(response)
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});