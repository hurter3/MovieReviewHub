// onclick="search(); return false;" add this to search.html

function searchMovie() {
    let film = document.getElementById("movie_name").value;
    let key = config.apiKey;
    // alert(film + key);
    $.ajax({    
        type: 'GET',
        url : "https://api.themoviedb.org/3/search/movie?api_key=" + key + "&language=en-US&query=" + film + "&page=1&include_adult=false",
        async: false,
        data: {
            format: 'json'
        },
        success: function(data) {
    // var jsondata = JSON.parse(data);
    let list = "";
    
    for (let i in data.results) {
        list += "<li><a href='" + data.results[i].title + "'>" + data.results[i].title + "</a></li>";
    }
    
    document.getElementById("data").innerHTML = "<ul>" + list + "</ul>";

    $("li").click(function() {
        alert(this.textContent);
    });
    }     
    });
}