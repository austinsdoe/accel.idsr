(function ($) {
    $(document).ready(function () {

        $("#B1 #other_disease").hide();

        $("#B1 #other").click(function () {
            $("#B1 #other_disease").show();
        });
        $("#B1 .idsr_disease").click(function () {
            $("#B1 #other_disease").hide();
        });

        $("#B1 input").checkboxradio();

    })
})(jQuery);
