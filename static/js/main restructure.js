let xhr = new XMLHttpRequest();  
let APIKEY = "51977f79d5e5c6689cf9b9ec7dcc8716";
function searchMovie() {  
    
    let query = document.getElementById("movieForm").movie_name;
    xhr.open("GET", "https://api.themoviedb.org/3/search/movie?api_key=51977f79d5e5c6689cf9b9ec7dcc8716&language=en-US&query=" + query + "&page=1&include_adult=false");
    xhr.send();
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


xhr.onreadystatechange = function() {
    document.getElementById("data").innerHTML = this.responseText;
    debugger;
    if (this.readyState == 4 && this.status == 200) {
        displayText(this.responseText);
        console.log(this.responseText);
    }
    else {
        console.log("no data");
        debugger;  
        console.log(this.readyState);
        debugger;
        console.log(this.status);
        debugger;          
    }
    };  
  

