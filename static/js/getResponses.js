$(document).ready(function() {
  $('#userInput').submit(function (evt) {
    evt.preventDefault();
    let agents = ["sad", "happy", "angry", "disgust"];
      for (let i = 0; i < agents.length; ++i) {
        $.ajax({
          url: "response",
          data: {
            "agent": agents[i],
            "query": $("form#userInput input[name='query']").val()
          }
        }).done(function(response){
          $(`article.bot.${response["name"]} textarea`).text(response["response"]);

          let userVal = $("form#userInput input[name='query']").val();
          if (userVal) {
            $("form#userInput input[name='query']").attr('placeholder', $("form#userInput input[name='query']").val());
            $("form#userInput input[name='query']").val("");
          }
        });
      }
  });
});
