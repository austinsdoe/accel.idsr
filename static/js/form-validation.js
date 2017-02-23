/**
 * Created by austinsdoe on 1/4/17.
 */

/*
$(function () {
    // Initialize form validation on the registration form.
    // It has the name attribute "registration"
    $("form[name='registration']").validate({
        // Specify validation rules
        rules: {

            reporting_date: {
                required: true,
                date: true,
            },
            county_code: {
                required: true,
                maxlength: 2,
                minLength: 2,
                digits: true,

            },
            facility_code: {
                required: true,
                maxlength: 8
            },
            case_id: {
                required: true,
                minlength: 3,
                maxlength: 7
            },
            patient_record_id: {},
            reporting_health_facility: {
                required: true,

            },
            reporting_county: {
                required: true,

            },
            reporting_district: {
                required: true,

            },
            condition_of_alert: {
                required: true,
            },
            patient_gender: {
                required: true,
            },
            age_of_patient: {
                required: true,
                digits: true,
            },
            patient_date_of_birth: {
                required: true,
                date: true,
            },
            patient_age_years: {
                required: true,
                digits: true,
            },
            patient_age_months: {
                required: true,
                digits: true,
            },
            patient_age_days: {
                required: true,
                digits: true,
            },
            patient_county_of_residence: {
                required: true,
            },
            patient_district_of_residence: {
                required: true,
            },
            patient_community_of_residence: {
                required: true,
            },
            head_of_household: {},
            patient_parent_name: {},
            patient_parent_phone_number: {},
            patient_cross_border_in_last_month: {},
            case_detected_at_community_level: {},
            date_of_disease_onset: {
                required: true,
            },
            date_patient_seen: {
                required: true,
            },
            patient_type: {
                required: true,
            },
            case_outcome: {
                required: true,
            },
            reporting_person_first_name: {
                required: true,
            },
            reporting_person_last_name: {
                required: true,
            },
            phone_number_of_person_reporting: {
                digits: true,
            },
            name_of_person_collecting_specimen: {},
            phone_number_of_person_collecting_specimen: {
                digits: true,

            },
            health_worker_comments: {},
            vaccinated_for_disease: {},
            num_of_vaccinations: {
                digits: true,
            },
            date_of_most_recent_vaccination: {
                date: true,
            },
            date_of_specimen_collection: {
                required: true,
                date: true,
            },
            date_specimen_sent_to_lab: {
                required: true,
                date: true,
            },
            specimen_type: {
                required: true,
            },
            lab_analysis_requested: {
                required: true,
            },
            lab_specimen_id: {
                required: true,
            },
            final_lab_result: {
                required: true,
            },
            date_results_reported: {
                required: true,
                date: true,
            }
        },
        // Specify validation error messages
        messages: {
            firstname: "Please enter your firstname",
            lastname: "Please enter your lastname",
        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function (form) {
            form.submit();
        }
    });
});

*/