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
        if (data.results[i].poster_path === null) {
        } else {
        let movie_header = "<div><h4>" + data.results[i].title + "</h4></div>";
        let poster = "https://image.tmdb.org/t/p/w200" + data.results[i].poster_path;
        let movie_overview = data.results[i].overview;
        let movie_title = "'" + data.results[i].title + "'";
        let sel_movie_btn = `<a href="{{ url_for('insertmovie', title= ${movie_title} )}}"type="button" class="btn btn-success btn-sm">Reviews</a>`;
        let img= "<div><img class='media-poster card-header' src=" + poster + " alt='image'></img>"+ sel_movie_btn + "</div>";
        list += '<li>' + movie_header + img + '</a></li>' + '<span>' + movie_overview + '</span>';
        }
}


    document.getElementById("data").innerHTML = "<ul>" + list + "</ul>";

    $("li").click(function() {
        alert(this.textContent);
    });
    }     
    });
}