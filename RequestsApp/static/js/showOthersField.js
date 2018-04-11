function showOtherField() {
    var ddl = document.getElementById("id_rubro");

    var selectedValue = ddl.options[ddl.selectedIndex].value;
    if (selectedValue === "otros") {
        var fieldContainer = document.getElementById("id_otro_rubro").parentElement;

        fieldContainer.classList.remove("hidden-field");
        fieldContainer.classList.add("visible-field");
    } else {
        var fieldContainer = document.getElementById("id_otro_rubro").parentElement;

        fieldContainer.classList.remove("visible-field");
        fieldContainer.classList.add("hidden-field");
    }
}

function initializeWatcher() {
    var ddl = document.getElementById("id_rubro");

    ddl.addEventListener(
        "change",
        showOtherField,
        false
    );
}

initializeWatcher();