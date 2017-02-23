/**
 * Created by austinsdoe on 11/5/16.
 */
(function ($) {
    $(document).ready(function () {
        $("#D1 #date_of_disease_onset").click().show().datepicker({

            minDate: "-10Y",  //
            maxDate: "0D",   //date cannot be in the future
            dateFormat: "dd-mm-yy",
            changeMonth: true,
            changeYear: true,
        });
        $("#D1 #date_patient_seen").click().show().datepicker({

            minDate: "-10Y",  //
            maxDate: "0D",   //date cannot be in the future
            dateFormat: "dd-mm-yy",
            changeMonth: true,
            changeYear: true,
        });
    })
})(jQuery);