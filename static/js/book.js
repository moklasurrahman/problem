(function($){

	"use strict";

	$(document).ready(function () {
		search.init();
	});

	var search = {

		init: function () {

			$("[id^=baggage-fare-policy-]").tabs();

			
			$(".toggle-icon").click(function (e) {
				$(this).closest('.head-line').siblings('.can-collapsed').toggleClass('show-collapsed');
                $(this).closest('.head-line').toggleClass('on');
              
			});
            // $(".flite-travaler-form-demo .toggle-icon").click(function (e) {
            //     $('.flite-review-title').toggleClass('on');
            //     // $('.flite-travaler-form-view').toggleClass('custome-show');
            // });

            $(".fight-demos").click(function(){
                $(this).toggleClass("addon");
                $(".flight-summry").toggleClass("summry-custome");
            });
            // debugger
            const input = document.querySelector("#mobile_code");
            const intlTelInput = window.intlTelInput(input, {
                preferredCountries: ['bd', 'gb', 'us', 'in'],
                utilsScript: "/static/plugins/intl-tel-input/js/utils.js",
                initialCountry: "bd",
                separateDialCode: true
            });
            $('#next-step').on('click', function(e){
                e.preventDefault();
                var total_results = [];
                var total_errors = {};
                $(".book-review fieldset").each(function(index){
                    const travelerId = $(this).data("id");
                    const keys = [
                        'firstName', 'lastName', 'gender', 'dateOfBirth',
                        'emailAddress', 'country', 'phoneNumber', 'passportNumber', 'passportIssueDate',
                        'passportExpiryDate', 'passportCountry', 'type'
                    ];
                    var errors = {};
                    var results = {};
                    for(var i=0; i < keys.length; i++){
                        const element = $(this).find(`[name="${keys[i]}_${travelerId}"]`);
                        var value = element.val();
                        if(value){
                            results['travelerId'] = travelerId;
                            results[keys[i]] = value;
                        }else{
                            total_errors[`${keys[i]}_${travelerId}`] = "This field is required";
                        }
                    }
                    total_results.push(results);
                })
                if(Object.keys(total_errors).length > 0){
                    $.each(total_errors, function(key, val){
                        $(`#${key}`).text(val);
                    });
                    return false;
                }else{
                    $('#traveler_from').submit()
                }
            });

		}
	}

})(jQuery);
