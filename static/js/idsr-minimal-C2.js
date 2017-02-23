(function ($) {
    $(document).ready(function () {
        //
        /**
         * Created by austinsdoe on 10/26/16.
         * This file creates a drop down menu of counties.  When the counties are selected, the file further genereate
         *another drop down menu of the districts in the county
         */

        // Liberia counties and districts as a dictionary

        var liberia_counties = {

            "Bomi": ["Dewoin", "Klay", "Mecca", "Senjeh"],
            "Bong": ["Fuamah", "Jorquelleh", "Kokoyah", "Panta-Kpa", "Salala", "Sanayea ", "Suakoko", "Zota"],
            "Gbarpolu": ["Belleh", "Bopolu", "Bokomu", "Kongba", "Gbarma"],
            "Grand Bassa": ["District #1", "District #2", "District #3", "District #4", "Owensgrove", "St. John River"],
            "Grand Cape Mount": ["Commonwealth", "Garwula", "Gola Konneh", "Porkpa", "Tewor"],
            "Grand Gedeh": ["Gbarzon", "Konobo", "Tchien"],
            "Grand Kru": ["Buah", "Lower Kru Coast", "Sasstown", "Upper Kru Coast"],
            "Lofa": ["Foya", "Kolahun", "Salayea", "Vahun", "Voinjama", "Zorzor"],
            "Margibi": ["Firestone", "Gibi", "Kakata", "Mambah-Kaba"],
            "Maryland": ["Barrobo", "Pleebo/Sodeken"],
            "Montserrado": ["Careysburg", "Greater Monrovia", "Commonwealth", "St. Paul River", "Todee"],
            "Nimba": ["Gbehlageh", "Saclepea", "Sanniquelleh-Mahn", "Tappita", "Yarwein-Mehnsohnneh", "Zoegeh"],
            "River Gee": ["Gbeapo", "Webbo"],
            "Rivercess": ["Morweh", "Timbo"],
            "Sinoe": ["Butaw", "Dugbe River", "Greenville", "Jaedae Jaedepo", "Juarzon", "Kpayan", "Pyneston"]
        }

        //Dynamically generate the option of the <select> of counties which are key of the liberia_counties dictionary

        function countiesList() {

            html = '<option disabled selected value>--Select--</option>'//make the default option blank

            for (var key in liberia_counties) {
                html += "<option value=" + key + ">" + key + "</option>"
            }

            $("#C2 #patient_county_of_residence").append(html);
        }

        //Dynamically generate the option of the <select> of district based on the county selected

        function districtMap(county_select_key) {

            var county_string = county_select_key;

            $("#C2 #patient_district_of_residence").empty()  //delete all options under the select with id = "district

            html_district = "<option value=" + ">--Select--</option>" //make the default option blank

            district_for_county = liberia_counties[county_string];

            for (var district in district_for_county) {

                html_district += "<option value=" + district_for_county[district] + ">" +district_for_county[district]+"</option>"
            }

            $("#C2 #patient_district_of_residence").append(html_district);
        }

        countiesList();

        // Upon a particular option been selected in the county drop down, get the select county and call the
        // districtMap function

        $("#C2").find("#patient_county_of_residence").change(function () {

            var county_key = $("#C2 #patient_county_of_residence option:selected").text();

            districtMap(county_key);


        });


    })
})(jQuery);


