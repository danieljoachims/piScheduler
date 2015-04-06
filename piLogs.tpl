<html lang="en">
   <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">

      <title>piScheduler Logs</title>

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

         <div class="container">
            <div class="row">

               <h3 style="cursor:pointer;height:32px" id="home" title="Go to Main Menu" >
                  <i> piSchedule </i><small> -- {{dayList}}</small>
                  <button class="btn btn-default btn-sm dropdown-toggle glyphicon glyphicon-home pull-right" type="button">
                  </button>
               </h3>

               <ul class="nav nav-pills">

                  <li role="presentation" class="active" id="formAction">
                     <a href="/logs">{{Today}}</a>
                  </li>

                  <li role="presentation" class="dropdown">
                     <a class="dropdown-toggle" data-toggle="dropdown" 
                         href="#" role="button" 
                         aria-expanded="false"> {{selectDay}} <span class="caret"></span> </a>
                     <ul class="dropdown-menu" role="menu" id="daySelect">
                        <li>
                           <a href="/logs?Monday">{{Monday}}</a>
                        </li>
                        <li>
                           <a href="/logs?Tuesday">{{Tuesday}}</a>
                        </li>
                        <li>
                           <a href="/logs?Wednesday">{{Wednesday}}</a>
                        </li>
                        <li>
                           <a href="/logs?Thursday">{{Thursday}}</a>
                        </li>
                        <li>
                           <a href="/logs?Friday">{{Friday}}</a>
                        </li>
                        <li>
                           <a href="/logs?Saturday">{{Saturday}}</a>
                        </li>
                        <li>
                           <a href="/logs?Sunday">{{Sunday}}</a>
                        </li>
                     </ul>
                  </li>
               </ul>

            </div>
         </div>


         <h4>&&currentDay&&</h4>

         <script>
            $('#home').on('click', function(event) {
               location.replace('/')
            });

            // with page loading display "Today" logs
            $(document).ready(function() {
               var href = location.href;
               if (href.substring(8).split("/")[1] == "logs")
                  $('#formAction').submit();
            });
            //  document.ready

         </script>

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

      </section>

      <section class="container" id="logList">
         {{!logList}}
      </section>
   </body>

</html>


