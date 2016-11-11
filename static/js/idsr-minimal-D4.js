/**
 * Created by austinsdoe on 11/6/16.
 */

(function ($) {
    'use strict';
    $(document).ready(function () {
   
        document.getElementById("num_of_vaccinations").disabled = true;
        document.getElementById("date_of_most_recent_vaccination").disabled = true;
        $(("#D4 #vaccinated_no") || ("#D4 #vaccinated_unknown")).click(function () {
            document.getElementById("num_of_vaccinations").disabled = true;
            document.getElementById("date_of_most_recent_vaccination").disabled = true;
        });
        $("#D4 #vaccinated_yes").click(function () {
            document.getElementById("num_of_vaccinations").disabled = false;
            document.getElementById("date_of_most_recent_vaccination").disabled = false;
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

