(function() {
    "use strict";

    $(function() {
        $(".add-new").click(function(e) {
            e.preventDefault();
            var $section = $(this).closest('.section');
            var formIdx = $('.dynamic-formset-form', $section).size();
            var $newForm = $($('.empty-form', $section).html().replace(/__prefix__/g, formIdx));
            $newForm.addClass('dynamic-formset-form');
            $newForm.appendTo($('.formset', $section));
            $('#' + $('.formset', $section).attr('data-total-forms-id')).val(parseInt(formIdx) + 1);
        });
    });
})();
