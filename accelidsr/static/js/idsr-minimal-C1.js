(function ($) {
    $(document).ready(function () {
         $("#C1 #anonymous_patients").change(function () {
            if ($(this).is(':checked')) {

                $("#C1 #known_patient_fields").hide();
            }
            else if ($(this).is(':not(:checked)')) {
                $("#C1 #known_patient_fields").show();
            }
        });
        
        $("#C1 #pick_date_of_birth").hide();
        $("#C1 .age_enter_field").hide();
        $("#C1 #date_of_birth").click(function () {  // when the date of birth field is click
            $("#C1 #pick_date_of_birth").show().datepicker({

                minDate: "-121Y",  //age restrcted to 121 years
                maxDate: "0D",   //date cannot be in the future
                dateFormat: "yy-mm-dd",
                changeMonth: true,
                changeYear: true,
                onSelect: function (dateText, inst) {
                    var date_of_birth = ($(this).datepicker('getDate')).getTime();

                    var current_date = (new Date()).getTime();

                    var date_diff = parseInt((current_date - date_of_birth) / 1000);

                    var years = 0, months = 0, days = 0;

                    if (date_diff > 0) {

                        if (date_diff >= 31556926) {

                            years = Math.floor(date_diff / 31556926);
                            date_diff = parseInt((date_diff - (years * 31556926)));
                        }
                        if ((date_diff >= 2629743) && (date_diff < 31556926)) {
                            months = Math.floor(date_diff / 2629743);
                            date_diff = (date_diff - months * 2629743);
                        }
                        if (date_diff < 2629743) {
                            days = Math.floor(date_diff / 86400);
                        }
                    }
                    document.getElementById("patient_age_years").value = years;
                    document.getElementById("patient_age_month").value = months;
                    document.getElementById("patient_age_days").value = days;
                    document.getElementById("patient_age_years").disabled = true;
                    document.getElementById("patient_age_month").disabled = true;
                    document.getElementById("patient_age_days").disabled = true;
                }
            });
            $("#C1 .age_enter_field").show().disabled();
        });
        $("#C1 #age_of_patient").click(function () {
            document.getElementById("patient_age_years").disabled = false;
            document.getElementById("patient_age_month").disabled = false;
            document.getElementById("patient_age_days").disabled = false;
            $("#C1 #pick_date_of_birth").hide(); //hide date picker field
            $("#C1 .age_enter_field").show();
        });
        $("#C1 #age_of_patient").$("#C1 input[type='radio']").checkboxradio();
    })

})(jQuery);
