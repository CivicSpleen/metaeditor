$(function() {
    "use strict";

    // jstree initialization.
    $("#tree")
        .on("select_node.jstree", function (e, node) {
            window.location.href = node.node.a_attr.href;
        })
    .jstree({
        "plugins": ["search"]});

    // search handler.
    var to = false;
    $("#query").keyup(function () {
        if(to) {
            clearTimeout(to);
        }
        to = setTimeout(function () {
            var v = $("#query").val();
            $("#tree").jstree(true).search(v);
        }, 250);
    });
});
