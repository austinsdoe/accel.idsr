/**
 * Created by austinsdoe on 11/6/16.
 */

(function ($) {
    'use strict';
    $(document).ready(function () {
        $("#D4 #if_patient_vaccinated_for_disease").hide();

        $(("#D4 #vaccinated_no") || ("#D4 #vaccinated_unknown")).click(function () {
            $("#D4 #if_patient_vaccinated_for_disease").hide();
        });
        $("#D4 #vaccinated_yes").click(function () {
            $("#D4 #if_patient_vaccinated_for_disease").show();
            //cancatenate patient age field in a format required by minDate:
            var vaccination_period = "-".concat($("#C1 #patient_age_years").val().concat("Y")).concat(" ")
                .concat("-").concat($("#C1 #patient_age_month").val().concat("M")).concat(" ").concat("-")
                .concat($("#C1 #patient_age_days").val().concat("D"));

            $("#D4 #date_of_most_recent_vaccination").show().datepicker({
                minDate: vaccination_period,  //age restrcted to 121 years
                maxDate: "0D",   //date cannot be in the future
                dateFormat: "dd-mm-yy",
                changeMonth: true,
                changeYear: true,
            });
        });
    })
})(jQuery);

