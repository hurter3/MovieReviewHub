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
    console.log(data);
    let list = "";
    
    for (let i in data.results) {
        let poster = "https://image.tmdb.org/t/p/w200" + data.results[i].backdrop_path; 
        let img= "<img class='media-poster card-header' src=" + poster + " alt='image'></img>";
    
      list += "<li>" + img + "<a href='" + data.results[i].title + "'>" + data.results[i].title + "</a></li>" +
      "<span>" + data.results[i].overview + "</span>";

//    <img class="media-poster card-header" src="{{movie.url}}" alt="1917"></img>       
}
    
    document.getElementById("data").innerHTML = "<ul>" + list + "</ul>";

    $("li").click(function() {
        alert(this.textContent);
    });
    }     
    });
}