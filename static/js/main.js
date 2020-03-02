// onclick="search(); return false;" add this to search.html
function searchMovie() {
    let film = document.getElementById("movie_name").value;
    let key = config.apiKey;
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
        let movie_header = "<div><h4 id='movie_title'>" + data.results[i].title + "</h4></div>";
        let poster = "https://image.tmdb.org/t/p/w200" + data.results[i].poster_path;
        let tmdb_id = data.results[i].id;
        let movie_overview = data.results[i].overview;
        let movie_title = data.results[i].title;
        let release_date = data.results[i].release_date;
        let vote_average = data.results[i].vote_average;
        let sel_movie_btn = `<button onclick="selectMovie(\'${tmdb_id}\',\'${movie_title}\',\'${poster}\',\'${release_date}\',\'${vote_average}\',\'${movie_overview}\')" class="btn btn-success">Select movie to review</button>`;
        let img= "<div><img class='media-poster card-header' src=" + poster + " alt='image'></img>"+ sel_movie_btn + "</div>";
        list += '<li>' + movie_header + img + '</a></li>' + '<span id="movie_overview">' + movie_overview + '</span>';
        }
}
    document.getElementById("data").innerHTML = "<ul>" + list + "</ul>";
    }     
    });
}


function selectMovie(tmdb_id,movie_title,poster,release_date,vote_average,movie_overview) {
    document.getElementById('form_tmdb_id').value = tmdb_id; 
    document.getElementById('form_movie_title').value = movie_title; 
    document.getElementById('form_poster_url').value = poster; 
    document.getElementById('form_movie_overview').value = movie_overview; 
    document.getElementById('form_release_date').value = release_date;  
    document.getElementById('form_vote_average').value = vote_average; 
    document.getElementById('formInsertMovie').submit();
}