var wsocket = new WebSocket("wss://161.246.5.31:443/ws");

    
        wsocket.onopen = function(){
          var temp1 = $("#ip").text();
          var temp2 = "open ";
          var temp_id = $("#temp_id").text();
          var ip_msg = temp2.concat(temp1);
          wsocket.send(ip_msg);
          var id_msg = "#id: ";
          id_msg = id_msg.concat(temp_id);
          wsocket.send(id_msg)
          console.log("connected"); 
        }; 
 
        wsocket.onmessage = function (message) {
          //console.log("receiving: " + message.data);


          if(message.data.substr(0,3)=="sos"){
            $("#edit_song_list").html(message.data.substr(3,message.data.length)+"<br><input type='submit' id='edit_playlist_submit'>");
            $("#edit_song_list_form").attr("action","/edit");
            $("#edit_song_list_form").attr("method","post");
          }

          if(message.data == "error"){
            window.location = "https://161.246.5.31/setplayer";
          }

          else if(message.data.substr(0,6)=="status"){
            $("#status").val(message.data.substr(6,message.data.length));
          }

          else if(IsJson(message.data)){
            var json = JSON.parse(message.data);
            $("#file_list").html("");
            jQuery.each(json,function(){

              $("#file_list").append('<input type="radio" name="file" value="'+this.file_name+'">'+this.file_name+'<br>');
            });

          }
        };
 
        wsocket.onclose = function(){
          console.log("disconnected"); 
        };
 
        sendMsg = function(message) {
          wsocket.send(message);
        };


