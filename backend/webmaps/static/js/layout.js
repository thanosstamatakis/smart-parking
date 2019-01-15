// Font end layout javascript script file.

// Initialization of sidenav on smaller screens.
$(document).ready(function () {
    $('.sidenav').sidenav();

    $("#show_map_btn").on("click", function() {
        $('.folium-map').toggle()
    });
});

