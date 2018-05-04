$.ajax({
   url: 'https://1bj8u6759k.execute-api.us-east-2.amazonaws.com/production/leaderboard',
   headers: {'Content-Type': 'application/json'},
   type: "GET",
   dataType: "json",
   error: function(jqXHR, textStatus, errorThrown) {
      console.log("BOOO")
   },
   success: function(data, textStatus, jqXHR) {
      console.log(data)
      $.each(data, function(index, user) {
         row = $("<tr><td>" + (index+1) + "</td><td>" + user.email + "</td><td>" + user.wins + "</td><td>" + user.losses + "</td></tr>")
         $("#leader-table").append(row)
      })
   }
});