(function() {
    "use strict";

    // Disabling autoDiscover, otherwise Dropzone will try to attach twice.
    Dropzone.autoDiscover = false;
    Dropzone.createImageThumbnails = false;

    $(function() {
        var toDropzone = function(selector) {
            var myDropzone = new Dropzone(
                selector,
                {url: '/editor/upload/',
                previewTemplate: "<div>FIXME:</div>"});

            myDropzone.on("success", function(file, response) {
                /* Maybe display some more file information on your page */
                var $elem = $(this.element);
                var $section = $elem.closest('.section');
                var formIdx = $('.dynamic-formset-form', $section).size();
                var $newForm = $($('.empty-form', $section).html().replace(/__prefix__/g, formIdx));
                $('.upload_id', $newForm).val(response.file.id);
                $newForm.addClass('dynamic-formset-form');
                $('.formset', $section).append($newForm);
                $('#' + $('.formset', $section).attr('data-total-forms-id')).val(parseInt(formIdx) + 1);
            });
            myDropzone.on("processing", function(file) {
                this.options.url = $(this.element).attr('data-dropzone-upload-url');
            });
        };
        toDropzone('#datafiles-dropzone');
        toDropzone('#docfiles-dropzone');
    });
})();
