        $('#play').click(function(){
          var song = $("#var").val();
          var play = "#play ";
          var res = play.concat(song);
          sendMsg(res);  
        });

        $('#add_button').click(function(){
          var playlist = $("#add_playlist").val();

          if(playlist == ""){
            $("#result").html("zero length") ;
          }
          else{
            $("#result").html(playlist);
            var add_playlist = "addpl ";
            add_playlist = add_playlist.concat(playlist);
            sendMsg(add_playlist);
          }

        });

        $('#load_playlist').click(function(){
          var playlist = $("#playlist_name").val();
          $("#result").html(playlist);
          var load_playlist = "loadpl ";
          load_playlist = load_playlist.concat(playlist);
          sendMsg(load_playlist);
        });
        $(document).on('change','input[type=radio][name=file]',function() {
          $("#var").val(this.value);
        });

        function OnClick(value){
          sendMsg(value);
        }

        function IsJson(str) {
          try {
            JSON.parse(str);
            } 
          catch (e) {
            return false;
          }
          return true;
        }

        $("#edit_playlist").click(function(){
          var pl_name = $("#playlist_name").val();
          $("#playlist_temp").attr("value",pl_name)
          sendMsg("editpl"+pl_name);
        }); 

        $('#edit_playlist_submit').click(function(){
          $("#edit_song_list_form").submit()
        });