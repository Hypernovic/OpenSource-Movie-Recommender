



function debounce(callback, wait) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(function () { callback.apply(this, args); }, wait);
    };
  }
  
  document.getElementById("searchBox").addEventListener('input', debounce( (e) => {
        console.log("aaa")
        search((e.target).value)  
  }, 500))

dummyfetch()
recommendedMovies()
favourites()

function dummyfetch(){
    $("#filler2").empty()
    fetch("/dummy",{
    method:"GET",   
    headers: {
        'Content-Type': 'application/json',
      }}            
    ).then(response => {
            return response.json()})
        .then(response => {
            for(var i = 0; i < response.length; i++) {
                var obj = response[i];
                var Genre = (obj.Genres).replace(/[\[\]']+/g, '');
                    $("#filler2").append(
                        `<div class="listed" onclick="confirmModal(this)"">
                        <div class="col mb-4">
                            <div class="card">
                              <img src="${obj.poster}" class="card-img-top">
                              <div class="card-body">
                                <h5 class="card-title">${obj.Name}</h5>
                                <p>${Genre}</p>
                              </div>
                            </div>
                      </div>`
                    );
            }
        }).catch(function(error){
            console.error(String(error));
            if(error=="TypeError: Failed to fetch"){
                alert("The Server is Offline !")
            }
        });
}


function search(input){
    $("#filler2").empty()
    fetch("/search?title="+input,{
    method:"GET",
    headers: {
        'Content-Type': 'application/json',
      }}            
    ).then(response => {
            return response.json()})
        .then(response => {
            for(var i = 0; i < response.length; i++) {
                var obj = response[i];
                var Genre = (obj.genres).replace(/[\[\]']+/g, '');
                    $("#filler2").append(
                        `<div class="listed" onclick="confirmModal(this)"">
                        <div class="col mb-4">
                            <div class="card">
                              <img src="${obj.poster}" class="card-img-top">
                              <div class="card-body">
                                <h5 class="card-title">${obj.original_title}</h5>
                                <p>${Genre}</p>
                              </div>
                            </div>
                      </div>`
                    );
            }
        }).catch(function(error){
            console.error(String(error));
        });
}


function favourites(){
    $("#filler3").empty()
    fetch("/favourites",{
    method:"GET",   
    headers: {
        'Content-Type': 'application/json',
      }}            
    ).then(response => {
            return response.json()})
        .then(response => {
            if(response.length==0){
                $(".msg").css("display", "block");
                document.getElementById("checkbox3").checked = false;
            }else{
                $(".msg").css("display", "none");
                document.getElementById("checkbox1").checked = false;
            }
            for(var i = 0; i < response.length; i++) {
                var obj = response[i];
                    $("#filler3").append(
                        `<div class="favourites" onclick="removeModal(this)">
                        <div class="col mb-4">
                            <div class="card h-100">
                              <img src="${obj.pic}" class="card-img-top">
                              <div class="card-body">
                                <h5 class="card-title">${obj.movieName}</h5>
                              </div>
                            </div>
                      </div>`
                    );
            }
        }).catch(function(error){
            console.error(String(error));
            $('.msg').toggle();
        });
}


function recommendedMovies(){
    $("#filler1").empty()
    fetch("/recommended",{
    method:"GET",   
    headers: {
        'Content-Type': 'application/json',
      }}            
    ).then(response => {
            return response.json()})
        .then(response => {
            for(var i = 0; i < response.length; i++) {
                var obj = response[i];
                var Genre = (obj.Genres).replace(/[\[\]']+/g, '');
                    $("#filler1").append(
                        `<div class="recommended" onclick="confirmModal(this)">
                        <div class="col mb-4">
                            <div class="card">
                            <img intrinsicsize="203 x 300" src="${obj.poster}" class="card-img-top">
                              <div class="card-body">
                                <h5 class="card-title">${obj.Name}</h5>
                                <p>${Genre}</p>
                              </div>
                            </div>
                            </div>
                      </div>`
                    );
            }
        }).catch(function(error){
            console.error(String(error));
            if(error=="TypeError: Failed to fetch"){
                alert("The Server is Offline !")
            }
        });
}

var Clicked
function confirm(elementhide){
        elementhide.remove()
        movieName=$(Clicked).find('.card-title').text();
        moviePic=$(Clicked).find('img').attr('src');

        fetch("/add",{
            method:"POST",
            headers: {
                'Content-Type': 'application/json',
              },
              body:JSON.stringify(
                    {
                        movieName:movieName,
                        moviePic:moviePic})
                    }).then(response => {
                    if (response.status==200){
                        console.log("success")
                        favourites()
                        recommendedMovies()
                    }
                    
        }).catch(function(error){
            console.error(String(error));
            $('.msg').toggle();
        });

}


function remove(elementhide){
    elementhide.remove()
    movieName=$(Clicked).find('.card-title').text();

    fetch("/remove",{
        method:"POST",
        headers: {
            'Content-Type': 'application/json',
          },
          body:JSON.stringify(
                {
                    movieName:movieName})
                }).then(response => {
                if (response.status==200){
                    console.log("success")
                    favourites()
                    recommendedMovies()
                }
                
    }).catch(function(error){
        console.error(String(error));
        $('.msg').toggle();
    });

}


function confirmModal(click){
    Clicked=click
    $(function(){
        $("body").before(`
        <!-- The Modal -->
        <div id="myModal" class="modal">
        <!-- Modal content -->
            <div class="modal-content">
                <p>Do you want to add this to your favs ?</p>
                <div class="modal-buttons">
                    <button type="button" class="btn btn-success" onclick="confirm(((this.parentNode).parentNode).parentNode)">Yes!</button>
                    <button type="button" class="btn btn-danger" onclick="(((this.parentNode).parentNode).parentNode).remove()">Cancel</button>
                </div>
            </div>
        </div>
        `);
    });
}



function removeModal(click){
    Clicked=click
    $(function(){
        $("body").before(`
        <!-- The Modal -->
        <div id="myModal" class="modal">
        <!-- Modal content -->
            <div class="modal-content">
                <p>Do you want to Remove this from your favs ???</p>
                <div class="modal-buttons">
                    <button type="button" class="btn btn-success" onclick="(((this.parentNode).parentNode).parentNode).remove()">Cancel</button>
                    <button type="button" class="btn btn-danger" onclick="remove(((this.parentNode).parentNode).parentNode)" >Yes!</button>
                </div>
            </div>
        </div>
        `);
    });
}