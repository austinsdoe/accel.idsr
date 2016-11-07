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
            /**
            onStepChanged: function (event, currentIndex, priorIndex) {
                // Used to skip the "Warning" step if the user is old enough.
                if (currentIndex === 1) {
                    $("#application .actions a[href='#previous']").hide();
                }
            }, */
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

    })
})(jQuery);

/* read https://github.com/rstaib/jquery-steps/issues/23

 $("#application").steps({
 headerTag: "heading",
 bodyTag: "section",
 transitionEffect: "slideLeft"
 cssClass: "wizard",
 saveState: true,
 onStepChanging: function (event, cur_index, next_index) {
 if (cur_index==0) {
 $("#display_primary").html(primary_name);
 }
 if (next_index==1) {
 personal_info_wizard();
 }
 current_step = cur_index;
 return true;
 },
 onStepChanged: function (e, c, p) {
 $("#application-p-"+p).hide();
 $("#application-p-"+c).fadeIn();
 current_step = true;
 }
 });


 function personal_info_wizard() {
 $("action.actions").hide();
 if (!$("subaction").hasClass("actions")){
 $("#personal_information").steps({
 headerTag: "subheader",
 bodyTag: "section",
 transitionEffect: 1,
 actionContainerTag: "subaction",
 cssClass: "subwizard",
 enablePagination: true,
 enableKeyNavigation: true,
 saveState: true,
 stepsOrientation: "horizontal",
 enableContentCache: true,
 startIndex: 0,
 onStepChanging: function (e,c,p) {
 if (p==0){
 current_sub_step = false;
 }
 return true;
 },
 onStepChanged: function (event, currentIndex, otherIndex) {
 if (currentIndex==0){
 current_step = true;
 }
 if ($("#personal_information-p-"+currentIndex).hasClass("skip")) {
 if (otherIndex<currentIndex) {
 $("#personal_information").steps("next");
 } else {
 $("#personal_information").steps("previous");
 }
 }
 if ($("#personal_information-p-"+currentIndex).html().trim()==""){
 if (otherIndex<currentIndex) {
 $("#personal_information").steps("next");
 } else {
 $("#personal_information").steps("previous");
 }
 }
 add_helpers();
 },
 onFinished: function() {
 $("#application").steps("next");
 $("action.actions").show();
 }
 });
 }
 add_helpers();
 }
 */
