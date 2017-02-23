(function ($) {
    $(document).ready(function () {
        $("#application").steps({
            headerTag: "h1",
            bodyTag: "section",
            cssClass: "wizard",
            transitionEffect: "slideLeft",
            enableAllSteps: true,
            labels: {
                finish: "SUBMIT",
            },
            onFinished: function (event, currentIndex) {
                var form = $(this);

                // Submit form input

                form.submit();
            }
        })


        $('div.steps').first().addClass('mainsteps');
    })
})(jQuery);

