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
            onFinished:function (event, currentIndex) {
                
                var form = $(this);

                // Submit form input

                form.submit();
            }
        });
        $("#A").steps({
            headerTag: "h2",
            bodyTag: "subsection",
            cssClass: "wizard",
            transitionEffect: "slideLeft",
            enableAllSteps: true
        });
        $("#B").steps({
            headerTag: "h2",
            bodyTag: "subsection",
            cssClass: "wizard",
            transitionEffect: "slideLeft",
            enableAllSteps: true
        });
        $("#C").steps({
            headerTag: "h2",
            bodyTag: "subsection",
            cssClass: "wizard",
            transitionEffect: "slideLeft",
            enableAllSteps: true
        });
        $("#D").steps({
            headerTag: "h2",
            bodyTag: "subsection",
            cssClass: "wizard",
            transitionEffect: "slideLeft",
            enableAllSteps: true
        });
        $('div.steps').first().addClass('mainsteps');
    })
})(jQuery);
