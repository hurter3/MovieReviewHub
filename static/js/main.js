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
            let movie_header = "<div><h4 id='movie_title'>" + data.results[i].title + "</h4></div>";
            let poster = "https://image.tmdb.org/t/p/w200" + data.results[i].poster_path;
            let tmdb_id = data.results[i].id;
            let movie_overview = data.results[i].overview;
            let sel_movie_btn = `<button onclick="selectMovie(\'${tmdb_id}\')" class="btn btn-success">Select movie to review</button>`;
            let img= "<img class='media-poster card-header' src=" + poster + " alt='image'></img>";
            list += '<div class="row item-border"><div class="col-md-4">'+ img + '</div><div class="col-md-8"><div>' + movie_header + '</div><p>'+ movie_overview + '</p>'+sel_movie_btn+'</div></div></div>' ;
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
                    let sel_movie_btn = `<button onclick="selectMovie(\'${tmdb_id}\')" class="btn btn-success">Select movie to review</button>`;
                    let img= "<img class='media-poster card-header' src=" + poster + " alt='image'></img>";
                    list += '<div class="row item-border"><div class="col-md-4">'+ img + '</div><div class="col-md-8"><div>' + movie_header + '</div><p>'+ movie_overview + '</p>'+sel_movie_btn+'</div></div></div>' ;
        }
        }
            }
    }
    document.getElementById("data").innerHTML = "<ul>" + list + "</ul>";
    }     
    });
}


function posterPath(poster_path) {
if(typeof poster_path === 'undefined') {
        return('False');
    } else if(poster_path === null){
        return('False');
    } else {
        return('True');
    }
}



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
    let list = "";
    
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
