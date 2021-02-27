$(document).ready(function () {
    $(".sidenav").sidenav({edge: "right"});
    $("select").formSelect();
    $(".datepicker").datepicker({
        format: "dd/mm/yyyy",
        yearRange: 2,
        showClearBtn: true,
        i18n: {
            done: "Confirm Date"
        }
    });
});