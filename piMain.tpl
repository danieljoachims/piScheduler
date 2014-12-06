<html lang="en">
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


      <style type="text/css">
         h3 {
            background: silver;
         }

         h4 {
            background: silver;
         }

         .btn-input {
            display: block;
         }

         .btn-input .btn.form-control {
            text-align: left;
         }

         .btn-input .btn.form-control span:first-child {
            left: 10px;
            overflow: hidden;
            position: absolute;
            right: 25px;
         }

         .btn-input .btn.form-control .caret {
            margin-top: -1px;
            position: absolute;
            right: 10px;
            top: 50%;
         }
      </style>

   </head>

   <body>

      <section class="container">

         <div class="container">
            <div class="row">
               <h3 style="cursor:pointer" title="Select function"><i> piScheduler </i><small> -- Main Menu</small></h3>
            </div>

            <ul class="nav nav-pills">
               <li role="presentation" class="active"><a href="/prefs">Preferences and Jobs</a></li>
               <li role="presentation"><a href="/logs">Day Logs</a></li>
               <li role="presentation"><a href={{pilight}}>pilight</a></li>

  <li role="presentation" class="dropdown">
    <a class="dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-expanded="false">
     Docu <span class="caret"></span>
    </a>
    <ul class="dropdown-menu" role="menu">
        <li role="presentation"><a href="https://dl.dropboxusercontent.com/u/35444930/piScheduler_doc_0.2/piScheduler.md.html">Overview</a></li>
        <li role="presentation"><a href="https://dl.dropboxusercontent.com/u/35444930/piScheduler_doc_0.2/piScheduleExamples.md.html">Schedule Examples</a></li>
        <li role="presentation"><a href="https://dl.dropboxusercontent.com/u/35444930/piScheduler_doc_0.2/piScheduleFeatures.md.html">Schedule Features</a></li>

    </ul>
  </li>



            </ul>

         </div>
       </section>

      <section id="logList">

      </section>

      <script>
         $('#home').on('click', function(event) {
            location.replace('/')
         });

         $('#daySelect').on('click', 'li', function(event) {

            var $target = $(event.currentTarget);
            var sDay = $target.text().trim()

            $target.closest('.btn-group').find('[data-bind="label"]').text($target.text()).end().children('.dropdown-toggle').dropdown('toggle');
            $('#formAction').attr('action', ('/logList?' + sDay))
            $('#formAction').submit();
            return sDay;
         });

      </script>


   </body>

</html>
