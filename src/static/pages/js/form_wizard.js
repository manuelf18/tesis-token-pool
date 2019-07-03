(function($) {

    'use strict';

    $(document).ready(function() {

        $('#rootwizard').bootstrapWizard({
            onTabShow: function(tab, navigation, index) {
                var $total = navigation.find('li').length;
                var $current = index + 1;

                // If it's the last tab then hide the last button and show the finish instead
                if ($current >= $total) {
                    $('#rootwizard').find('.pager .next').hide();
                    $('#rootwizard').find('.pager .previous').hide();
                    $('#rootwizard').find('.pager .finish').show().removeClass('disabled hidden');
                } else {
                    $('#rootwizard').find('.pager .next').show();
                    $('#rootwizard').find('.pager .finish').hide();
                }
            },
            onNext: function(tab, navigation, index) {
                let nexPage = index + 1;
                if ( nexPage === 2 ){
                    if (!App.validators.validatePageOne()){
                        Swal.fire({
                            type:'error',
                            text: 'Faltan campos por llenar',
                        });
                        return false;
                    } 
                }
                else if ( nexPage === 3 ){
                    return App.sendInfo();
                }
            },
            onPrevious: function(tab, navigation, index) {
                let current = index + 1;
                if ( current !== 2 ){
                    App.utils.disableNextButton(false);
                }
            },
            onInit: function() {
                $('#rootwizard ul').removeClass('nav-pills');
            }

        });

        $('.remove-item').click(function() {
            $(this).parents('tr').fadeOut(function() {
                $(this).remove();
            });
        });

    });

})(window.jQuery);
