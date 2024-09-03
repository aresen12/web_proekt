function showDiv(Div) {
    var x = document.getElementById(Div);
    if(x.style.display=="none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}