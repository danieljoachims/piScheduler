<html lang="en">
   <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">

      <title>piSchedule</title>

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
               <h3 style="cursor:pointer" title="{{mainMenuText}}"><i> piSchedule </i><small> -- {{mainMenu}}</small></h3>
            </div>

            <ul class="nav nav-pills">
               <li role="presentation" class="active"><a title="{{mainTitle}}" href="/prefs">{{mainText}}</a></li>

               <li role="presentation" class="dropdown">
                  <a class="dropdown-toggle" data-toggle="dropdown"  role="button" aria-expanded="false" 
                     href="#"  title="{{editTitle}}">{{editText}}<span class="caret"></span>
                  </a>
                  <ul id="editMenu" class="dropdown-menu" role="menu">
                     &&iniFileList&&
                  </ul>
               </li>


               <li role="presentation"><a href="/logs">{{dayLogs}}</a></li>
               <li role="presentation"><a href={{pilight}}>pilight</a></li>

               <li role="presentation" class="dropdown">
                  <a class="dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-expanded="false">
                    Docu <span class="caret"></span>
                  </a>
                  <ul class="dropdown-menu" role="menu">
                       <li role="presentation" >
                          <a role="menuitem" style="cursor:pointer;" onclick="openHelp('Overview')">&nbsp; {{docOverview}} &nbsp;</a>
                          <a role="menuitem" style="cursor:pointer;" onclick="openHelp('Edit')">&nbsp; {{docEdit}} &nbsp;</a>
                          <a role="menuitem" style="cursor:pointer;" onclick="openHelp('Examples')">&nbsp; {{docExamples}} &nbsp;</a>
                          <a role="menuitem" style="cursor:pointer;" onclick="openHelp('Features')">&nbsp; {{docFeatures}} &nbsp;</a>
                       </li>

                       <li class='divider'></li>

                       <li role='presentation'>
                           <a role="menuitem"  style="cursor:pointer;" onclick="setLocale('DE')"  >&nbsp; Deutsch &nbsp;</a>
                           <a role="menuitem"  style="cursor:pointer;" onclick="setLocale('EN')"  >&nbsp; English &nbsp;</a>
                       </li>

                       <li class='divider'></li>

                       <li role='presentation'>
                           <a role="menuitem"  style="cursor:pointer;" onclick="piClose()"  >&nbsp; {{terminate}}</a>
                       </li>


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



         function piClose() {
           if (confirm("  *** piSchedule  beenden?") == true) {
               var info = ("  *** piSchedule beendet " + new Date().toLocaleString())
               console.log(info)
               $.get('/close?' + info)
              return
           }
        }


         function setLocale(lang) {
             language = lang
console.log("piMain   set 'Locale'  language:" + language)
             $.get('/locale', lang)

             setTimeout(function() { location.replace('/')},150);
          };


         var page = null;
         var language = '&&language&&'

         function openHelp(name) {
             var main = "https://dl.dropboxusercontent.com/u/35444930/piScheduler/"

             //console.log('**** piSchedule/piMain   language:' + language)

             if (page != null) {page.close()}
             switch (name) {
                case 'Overview':  page = window.open(main + language + "/piScheduleOverview.html",'piScheduleDocu');break;
                case 'Edit':      page = window.open(main + language + "/piScheduleEdit.html",'piScheduleDocu');break;
                case 'Examples':  page = window.open(main + language + "/piScheduleExamples.html",'piScheduleDocu');break;
                case 'Features':  page = window.open(main + language + "/piScheduleFeatures.html",'piScheduleDocu');break;
             }
          }

        </script>


   </body>

</html>
