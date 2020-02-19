function searchMovie() {  
    let xhr = new XMLHttpRequest();  
    let query = document.getElementById("movieForm").movie_name;
    

    xhr.open("GET", "//api.themoviedb.org/3/search/movie?api_key=" + apiKey + "&language=en-US&query=" + query + "&page=1&include_adult=false");
    xhr.send();
    
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
        }
        else {
            console.log("no data");            
        }
    };
}

function displayText(data) {
    data = JSON.parse(data);
    let list = "";
    
    for (let i in data.results) {
        list += "<li>" + data.results[i].title + "</li>";
    }
    
    document.getElementById("data").innerHTML = "<ul>" + list + "</ul>";
    
    $("li").click(function() {
        alert(this.textContent);
    });
}
