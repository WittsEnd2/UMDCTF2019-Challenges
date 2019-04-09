(function() {
    $("#defaultForm").on('submit', function(e){
        e.preventDefault();
        $.ajax({
          url: "http://127.0.0.1:5000/api/authenticate",
          type: "POST",
          datatype: "jsonp",
          data: { "username": $("#username").val(), "password": $("#password").val()},
          success: function(response){
              if (response === -1){
                  alert("You are unauthorized to view this webpage.");
              } else {
                var now = new Date();
                var minutes = 5;
                now.setTime(now.getTime()+(minutes*60*1000));
                document.cookie = "info="+escape(response[0][2]) + ";";
                document.cookie = "expires=" +now.toUTCString() + ";";
                printVal = []
                for (var i = 0; i < response.length; i++)
                    printVal.push({"username": response[i][0], "password": response[i][1]})
                console.log(printVal);
                $("#loginHTML").html("<div class = 'row'><div class = 'col-12'><h3 class = 'text-center'>You are authenticated</h3></div></div>");
                
            }
          }
        })
    })
    $("#flagForm").on('submit', function(e){
        e.preventDefault();
        $.post(
            "http://127.0.0.1:5000/api/flag",
            {"flagid": $("#flags").val(), "info": document.cookie},
            function(response, status) {
                if (response == -1 || response == -2){
                    response = parseInt(response);
                }
                var isObject = typeof response === "object"; 
                if (response === -1) {
                    alert("You are not authorized.");

                } else if (response === -2) {
                    alert("Flag doesn't exist");
                } else if (isObject) {
                    $("#flagArea").html("<img src='" + response.img + "' flag='" + response.flg + "' height='25%'/>");
                } else {
                    $("#flagArea").html("<img src='" + response + "' flag='nope :)' height='30%'/>");

                }
                // switch (response) {
                //     case -1: 
                //         break;
                //     case -2:
                //         alert("Flag doesn't exist");
                //         break;
                //     case isObject:
                //         console.log(response);

                //     default:
                //         console.log(response, typeof response);
                //         break;
                // }
            }
        )
    
    });
})()

