  <html lang="de">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>piScheduler Status</title>

    <!-- optional: Einbinden der jQuery-Bibliothek -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css">

    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap-theme.min.css">

    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.0/js/bootstrap.min.js"></script>

  </head>

  <body>

    <section class="container">

      <h3 style="cursor:pointer;height:32px" id="main" title="{{gotoMain}}" >
          <i> piSchedule </i><small> -- {{prefJobs}}</small>
          <button class="btn btn-default btn-sm dropdown-toggle glyphicon glyphicon-home pull-right" type="button">
          </button>
      </h3>

      <p></p>
      <table class="table table-striped table-bordered">
         <tbody>
            <tr>
               <td><b>{{Location}}</b></td>
               <td><b>{{dateTime}}</b></td>
               <td>{{sunrise[:10]}} / &&datetime&&</td>
            </tr>
            <tr>
               <td><b>Latitude </b> {{Latitude}}</td>
               <td><b>{{Sunrise}}</b></td>
               <td>{{sunrise[10:16]}}</td>
            </tr>
            <tr>
               <td><b>Longitude </b> {{Longitude}}</td>
               <td><b>{{Sunset}}</b></td>
               <td>{{sunset[10:16]}}</td>
            </tr>
         </tbody>
      </table>
      &&timeTable&&
    </section>


    <script>
        $('#main').on('click', function(event) {
            location.replace('/')
        });
    </script>


    <style type="text/css">
         h3 {
             background: silver;
         }
    </style>

    </body>
    </html>
