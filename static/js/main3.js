let xhr = new XMLHttpRequest();
​
function searchMovie() {
    
    let query = document.getElementById("movieForm")["movie_name"].value;
    xhr.open("GET", "//api.themoviedb.org/3/search/movie?api_key=" + API_KEY + "&language=en-US&query=" + query + "&page=1&include_adult=false");
    xhr.send();
}
​
function displayText(data) {
    data = JSON.parse(data);
    let list = "";
    
    for (let i in data.results) {
        list += "<li>" + data.results[i].title + "</li>";
    }
    
    document.getElementById("data").innerHTML = "<ul>" + list + "</ul>";
    
    $("li").click(function() {
        alert(this.textContent);
    })
    
}
​
xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        displayText(this.responseText);
    };
}