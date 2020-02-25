function searchMovie() {
    let film = document.getElementById("movie_name").value;
    let key = config.apiKey;
    let url = "https://api.themoviedb.org/3/search/movie?api_key=" + key + "&language=en-US&query=" + film + "&page=1&include_adult=false";
    // alert(film + key);

    fetch(url, {
	method: 'get'
    }).then(displayText(response) {
	
    }).catch(function(err) {
	// Error :(
    });

    

    function displayText(data) {
    data = JSON.parse(data);
    let list = "";
    
    for (let i in data.results) {
        list += "<li>" + data.results[i].title + "</li>";
    }
    
    document.getElementById("data").innerHTML = "<ul>" + list + "</ul>";
    debugger;

    $("li").click(function() {
        alert(this.textContent);
    });
    debugger;
}
debugger;

