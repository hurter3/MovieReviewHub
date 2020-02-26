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

        let title=data.results[i].title;    
        let select_movie_btn =  "<button onclick='selectMovie(" + title + ")'class='btn btn-success'>Select Movie</button>";

        let movie_title = "<div><h4 id='movie_title'>" + data.results[i].title + "</h4></div>";
        let poster = "https://image.tmdb.org/t/p/w200" + data.results[i].poster_path; 
        let img= "<div><img class='media-poster card-header' src=" + poster + " alt='image'></img>"+ select_movie_btn + "</div>";
        //let urlfor = '<a href=\"{{ url_for(\"insertmovie\",title=' + movie_title + ') }}\"';
        
        list += '<li>' + movie_title + img  + '<span>' + data.results[i].overview + '</span>';
        }
//    <img class="media-poster card-header" src="{{movie.url}}" alt="1917"></img> 
//  <a href="{{ url_for('reviews', movie_id=movie._id) }}"      
}
    
    document.getElementById("data").innerHTML = "<ul>" + list + "</ul>";

    $("li").click(function() {
        alert(this.textContent);
    });
    }     
    });
}

function selectMovie(title) {
    console.log("select movie has been invoked");
    console.log(document.getElementById("movie_title").innerHTML);
}