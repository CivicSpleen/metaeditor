(function() {
    "use strict";

    $(function() {
        $(".add-new").click(function(e) {
            e.preventDefault();
            var $fieldset = $(this).closest('fieldset');
            var formIdx = $('.dynamic-formset-form', $fieldset).size();
            var $newForm = $($('.empty-form', $fieldset).html().replace(/__prefix__/g, formIdx));
            $newForm.addClass('dynamic-formset-form');
            $newForm.appendTo($('.formset', $fieldset));
            $('#' + $('.formset', $fieldset).attr('data-total-forms-id')).val(parseInt(formIdx) + 1);
        });
        $(".scrape").click(function(e) {
            e.preventDefault();
            // TODO: implement scrape.
        });
    });
})();
