// searchMovie is triggered by both buttons on the search.html page but the result is in different layout hence 
// the if statement to build a list of movies with the tmdb_id key on each button and injected in the data element. 
function searchMovie(searchBy) {
    let query = document.getElementById("searchInput").value;
    let key = config.apiKey;
    $.ajax({    
        type: 'GET',
        url : "https://api.themoviedb.org/3/search/" + searchBy + "?api_key=" + key + "&language=en-US&query=" + query + "&page=1&include_adult=false",
        async: false,
        data: {
            format: 'json'
        },
        success: function(data) {
    let list = "";
    if (searchBy==="movie"){
        for (let i in data.results) {
            if (posterPath(data.results[i].poster_path)=== 'True') {
            let movie_header = '<div><h4 id="movie_title">' + data.results[i].title + '</h4></div>';
            let poster = "https://image.tmdb.org/t/p/w200" + data.results[i].poster_path;
            let tmdb_id = data.results[i].id;
            let movie_overview = data.results[i].overview;
            let sel_movie_btn = `<button onclick="selectMovie(\'${tmdb_id}\')" class="btn btn-success btn-spread">The Reviews</button>`;
            let img= '<img class="media-poster card-header" src=' + poster + ' alt="image"></img>';
            let part1 = '<div class="container-fluid"><div class="row row-margin-bottom"><div class="col-md-8 no-padding lib-item" data-category="view"><div class="lib-panel"><div class="row box-shadow"><div class="col-md-6">' + img + '</div><div class="col-md-6"><div class="lib-row lib-header">';
            let part2 =  movie_header + '<div class="lib-header-seperator"></div></div><div class="lib-row lib-desc">' + movie_overview + '<div>' + sel_movie_btn + '</div></div></div></div></div></div></div></div>';
            list += part1 + part2;
        }
}
    } else {
        for (let i in data.results) {
            for (j in data.results[i].known_for) {
                 if (posterPath(data.results[i].known_for[j].poster_path)=== 'True') {
                    let movie_header = "<div><h4 id='movie_title'>" + data.results[i].known_for[j].title + "</h4></div>";
                    let poster = "https://image.tmdb.org/t/p/w200" + data.results[i].known_for[j].poster_path;
                    let tmdb_id = data.results[i].known_for[j].id;
                    let movie_overview = data.results[i].known_for[j].overview;
                    let sel_movie_btn = `<button onclick="selectMovie(\'${tmdb_id}\')" class="btn btn-success btn-spread">Explore Reviews</button>`;
                    let img= "<img class='media-poster card-header' src=" + poster + " alt='image'></img>";
                    let part1 = '<div class="container-fluid"><div class="row row-margin-bottom"><div class="col-md-8 no-padding lib-item" data-category="view"><div class="lib-panel"><div class="row box-shadow"><div class="col-md-6">' + img + '</div><div class="col-md-6"><div class="lib-row lib-header">';
                    let part2 =  movie_header + '<div class="lib-header-seperator"></div></div><div class="lib-row lib-desc">' + movie_overview + '<div>' + sel_movie_btn + '</div></div></div></div></div></div></div></div>';
                    list += part1 + part2;
               }
        }
            }
    }
    document.getElementById("data").innerHTML = "<ul>" + list + "</ul>";
    }     
    });
}

// The posterPath is called in the searchMovie to ensure there is valid and defined data when building the list of movies
function posterPath(poster_path) {
if(typeof poster_path === 'undefined') {
        return('False');
    } else if(poster_path === null){
        return('False');
    } else {
        return('True');
    }
}

// selectMovie is the movie the user selects and an additional api get is performed to get all the related fields
// to populate the form that is POSTED with action="{{ url_for('insertmovie')}}" 
function selectMovie(tmdb_id) {
    let key = config.apiKey;
    $.ajax({    
        type: 'GET',
        url : "https://api.themoviedb.org/3/movie/" + tmdb_id + "?api_key=" + key + "&language=en-US",
        async: false,
        data: {
            format: 'json'
        },
        success: function(data) {
    document.getElementById('form_tmdb_id').value = tmdb_id; 
    document.getElementById('form_movie_title').value = data.title; 
    document.getElementById('form_poster_url').value = "https://image.tmdb.org/t/p/w200" + data.poster_path; 
    document.getElementById('form_movie_overview').value = data.overview; 
    document.getElementById('form_release_date').value = data.release_date;  
    document.getElementById('form_vote_average').value = data.vote_average; 
    document.getElementById('formInsertMovie').submit();
    }     
    });
}
