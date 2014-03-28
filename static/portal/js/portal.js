$(document).ready(function(){
    $acstate = $('.ac-state');
    $ac_district = $(".ac-district");
    $ac_city = $(".ac-city");
    $ac_location = $(".ac-location");
    $ac_pincode = $(".pincode");
    $acstate.attr("disabled");
    $acstate.change(function() {
        var state = $(this).val();
        $.ajax({
            url: "/portal/ajax-state/",
            type: "POST",
            data: {
                state: state
            },
            success: function(data) {
                if(data[0]){
                    $ac_district.html(data[0]);
                   //$ac_district.trigger("chosen:updated");
                    $ac_district.removeAttr("disabled");
                }else{
                    $ac_district.html('<option>-- None -- </option>')
                   //$ac_district.trigger("chosen:updated");
                    $ac_district.attr("disabled", "disabled");
                    alert('No District found for this State!!');
                }
                if(data[1]){
                    $ac_city.html(data[1]);
                   //$ac_city.trigger("chosen:updated");
                    $ac_city.removeAttr("disabled");
                }else{
                    $ac_city.html('<option>-- None -- </option>')
                   //$ac_city.trigger("chosen:updated");
                    $ac_city.attr("disabled", "disabled");
                    alert('No City found for this State!!');
                }
            }
        });
    });

    $ac_district.change(function(){
        var district = $(this).val();
        $.ajax({
            url: "/portal/ajax-location/",
            type: "POST",
            data: {
                district: district
            },
            success: function(data) {
                if(data){
                    $ac_location.html(data);
                   //$ac_location.trigger("chosen:updated");
                    $ac_location.removeAttr("disabled");
                }else{
                    $ac_location.html('<option>-- None -- </option>')
                   //$ac_location.trigger("chosen:updated");
                    $ac_location.attr("disabled", "disabled");
                    alert('No Location found for this District!!');
                }
            }
        });
    });

    $ac_location.change(function(){
        var location = $(this).val();
        $.ajax({
            url: "/portal/ajax-pincode/",
            type: "POST",
            data: {
                location: location
            },
            success: function(data) {
                if(data){
                    $ac_pincode.val(data);
                    $ac_pincode.removeAttr("disabled");
                }else{
                    alert('No pincode found for this Location!!');
                }
            }
        });
    });
});
