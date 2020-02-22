function searchMovie() {
    let film = document.getElementById("movie_name").value;
    let key = config.apiKey;
    let url = "https://api.themoviedb.org/3/search/movie?api_key=" + key + "&language=en-US&query=" + film + "&page=1&include_adult=false";
    // alert(film + key);
    let response = fetch(url);

    if (response.ok) {
    let json = response.json();
    } else {
    alert("HTTP-Error: " + response.status);
    }
  
    let list = "";
    
    for (let i in json.results) {
        list += "<li>" + json.results[i].title + "</li>";
    }
    
    document.getElementById("data").innerHTML = "<ul>" + list + "</ul>";
    debugger;

    $("li").click(function() {
        alert(this.textContent);
    });    
}