(function() {
    "use strict";

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            var cookies = document.cookie.split(";");
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie("csrftoken");

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(function() {
        $('#id_coverage').typeahead({
            ajax: '/editor/coverage-list'});

        var addNewForm = function($fieldset, link) {
            // Adds new form (django formset form) to the given fieldset.
            var formIdx = $(".dynamic-formset-form", $fieldset).size();

            // get name of the input containing total forms.
            var inputName = $(".formset", $fieldset).attr("data-total-forms-input-name");

            // find empty form and create from it new form.
            var $newForm = $($(".empty-form", $fieldset).html().replace(/__prefix__/g, formIdx));
            $newForm.addClass("dynamic-formset-form");

            if (link) {
                // initialize form with link data.
                $(".name", $newForm).val(link.text);
                $("select", $newForm).val(link.format.id);
                $(".url", $newForm)
                    .val(link.href)
                    .hide();
                $(".link", $newForm)
                    .attr("href", link.href)
                    .text(link.truncated_href)
                    .show();
                $newForm.prependTo($(".formset", $fieldset));
                validateURL($(".url", $newForm));
            } else {
                // render empty form.
                $newForm.appendTo($(".formset", $fieldset));
            }

            // increase total forms counter
            $("input[name=" + inputName + "]").val(parseInt(formIdx) + 1);
        };

        $(".add-new").click(function(e) {
            e.preventDefault();
            addNewForm($(this).closest("fieldset"));
        });

        $(".show-remote-links-modal").click(function(e) {
            // shows remote links modal if download page is valid. Otherwise alerts warning.
            e.preventDefault();
            if ($("#id_download_page").val() === "" && $("#id_page").val() === "") {
                alert("Set Page or Download page first.");
            } else {
                $.data($("#remoteLinksModal").get(0), "fieldset", $(this).closest("fieldset"));
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
                    $("a", $current)
                        .attr("href", links[i].href)
                        .attr("title", links[i].title)
                        .attr("data-truncated-href", links[i].truncated_href)
                        .text(links[i].text);
                    if (links[i].format) {
                        $("a", $current)
                            .attr("data-format-id", links[i].format.id)
                            .attr("data-format-name", links[i].format.name);
                        $(".format-name", $current).text(links[i].format.name);
                        $(".file-name", $current).text(links[i].file_name);
                    }
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

        var aToLink = function($a) {
            // converts <a> node to the link object.
            return {
                text: $a.text(),
                href: $a.attr("href"),
                truncated_href: $a.attr("data-truncated-href"),
                format: {
                    id: $a.attr("data-format-id"),
                    name: $a.attr("data-format-name")}
            };
        };

        $("#remoteLinksModal").on("shown.bs.modal", function () {
            // Gets remote links from server side and populates popup.
            var downloadURL = $("#id_download_page").val();
            if (!downloadURL) {
                downloadURL = $("#id_page").val();
            }

            // assuming downloadURL is not empty because it checked before popup showing.
            $("#remoteLinksModal .modal-body .wait")
                .show()
                .text("Scrapping " + downloadURL + " . Please wait...");
            $("#remoteLinksModal .modal-body table tbody.content").empty();
            $.ajax({
                statusCode: {
                    500: function() {
                        showErrors(["Server error. Please, try later."]);
                        $("#remoteLinksModal").modal("hide");
                    },
                    403: function() {
                        showErrors(["Forbidden."]);
                        $("#remoteLinksModal").modal("hide");
                    }
                },
                url: "/editor/scrape?" + $("#remoteLinksModal").data("fieldset").attr("id"),
                type: "post",
                data: {url: downloadURL},
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
                var $fieldset = $("#remoteLinksModal").data("fieldset");
                addNewForm(
                    $fieldset,
                    aToLink($("a", $(e).closest("tr"))));
            });
            $("#remoteLinksModal").modal("hide");
        });

        var validateURL = function($input) {
            // validates url and its existance.
            if ($input.data("bs.popover")) {
                // popover already exists, change content.
                $input.data("bs.popover").options.content = "Validating...";
            } else {
                // initialize popover.
                $input.popover({"content": "Validating...", "trigger": "manual click"});
            }
            $input.popover("show");
            $.ajax({
                statusCode: {
                    500: function() {
                        $input.data("bs.popover").options.content = "Server error.";
                        $input.popover("show");
                    },
                    403: function() {
                        $input.data("bs.popover").options.content = "Forbidden.";
                    }
                },
                url: "/editor/validate-url",
                type: "post",
                data: {url: $input.val()},
                success: function(response) {
                    if (response.error) {
                        $input.data("bs.popover").options.content = response.error;
                        $input.popover("show");
                    } else {
                        $input.data("bs.popover").options.content = "Available";
                        $input.popover("hide");
                    }
                }
            });
        };

        $("#datafiles, #documentfiles").on("change", ".url", function(e) {
            validateURL($(this));
        });

        $(".toggle-all").change(function(e) {
            e.preventDefault();
            $("tbody.content input[type=checkbox]", $(this).closest("table"))
                .prop("checked", $(this).is(":checked"));
        });
    });
})();
