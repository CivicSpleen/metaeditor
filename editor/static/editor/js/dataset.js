(function() {
    "use strict";

    $(function() {
        var addNewForm = function($fieldset, name, url) {
            // Adds new form (django formset form) to the given fieldset.
            var formIdx = $(".dynamic-formset-form", $fieldset).size();
            var $newForm = $($(".empty-form", $fieldset).html().replace(/__prefix__/g, formIdx));
            $newForm.addClass("dynamic-formset-form");
            if (name) {
                $('.name', $newForm).val(name);
            }
            if (url) {
                $('.url', $newForm).val(url);
            }
            if (name || url) {
                $newForm.prependTo($(".formset", $fieldset));
            } else {
                $newForm.appendTo($(".formset", $fieldset));
            }
            $("#" + $(".formset", $fieldset).attr("data-total-forms-id")).val(parseInt(formIdx) + 1);
        };

        $(".add-new").click(function(e) {
            e.preventDefault();
            addNewForm($(this).closest("fieldset"));
        });

        $(".show-remote-links-modal").click(function(e) {
            // shows remote links modal if download page is valid. Otherwise alerts warning.
            e.preventDefault();
            if ($("#id_download_page").val() === "") {
                alert("Set download page first.");
            } else {
                $("#remoteLinksModal").modal("show");
            }
        });

        var showLinks = function(links) {
            // populates remote links popup with links.
            var length = links.length;
            if (length === 0) {
                alert('No urls found on remote site.');
            } else {
                var $tmpl = $("#remoteLinksModal .modal-body table tr.tmpl");
                var elemsToAppend = $();
                var $current = null;
                for (var i = 0; i < links.length; ++i) {
                    $current = $tmpl.clone();
                    $("a", $current).text(links[i].text);
                    $("a", $current).attr("href", links[i].href);
                    $("a", $current).attr("title", links[i].title);
                    elemsToAppend = elemsToAppend.add($current);
                }
                elemsToAppend.appendTo("#remoteLinksModal .modal-body table.links tbody.content");
            }
        };

        var showErrors = function(errors) {
            // shows given errors to user.
            // TODO: use bootstrap error instead of alert.
            alert(errors.join('; '));
        };


        $("#remoteLinksModal").on("shown.bs.modal", function () {
            // Gets remote links from server side and populates popup.
            var downloadUrl = $("#id_download_page").val();

            // assuming downloadUrl is not empty because it checked before popup showing.
            $("#remoteLinksModal .modal-body .wait")
                .show()
                .text("Scrapping " + downloadUrl + " . Please wait...");
            $("#remoteLinksModal .modal-body table tbody.content").empty();
            $.ajax({
                statusCode: {
                    500: function() {
                        showErrors(["Server error. Please, try later."]);
                        $("#remoteLinksModal").modal("hide");
                    }
                },
                url: "/editor/scrape",
                type: "post",
                data: {url: downloadUrl},
                success: function(response) {
                    $("#remoteLinksModal .modal-body .wait").text("").hide();
                    if (response.errors) {
                        showErrors(response.errors);
                        $("#remoteLinksModal").modal("hide");
                    } else {
                        showLinks(response.links);
                    }
                }
            });
        });

        $("#remoteLinksModal .btn-primary").on("click", function () {
            // user selected urls and clicked Ok.
            $("#remoteLinksModal table tbody.content input:checked").each(function(i, e) {
                var $a = $("a", $(e).closest("tr"));
                addNewForm($($("fieldset").get(0)), $a.text(), $a.attr("href"));
            });
            $("#remoteLinksModal").modal("hide");
        });
    });
})();
