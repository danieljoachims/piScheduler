<html lang="de">
   <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">

      <title>piScheduler Edit</title>

      <!-- optional: Einbinden der jQuery-Bibliothek -->
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

      <!-- Latest compiled and minified CSS -->
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css">

      <!-- Optional theme -->
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap-theme.min.css">

      <!-- Latest compiled and minified JavaScript -->
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.0/js/bootstrap.min.js"></script>

      <script>
         $.valHooks.textarea = {
            get : function(elem) {
               return elem.value.replace(/\n/g, "|").replace(/#/g, "%23");
            }
         };

      </script>
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

      <span id="jobDefTitleEdit" style="&&jobDefEdit&&">
         <h4><b>{{jobDef}}</b>&nbsp;&nbsp;&nbsp;<small><i>{{createSchedule}}</i></small></h4>
      </span>
      <span id="jobDefTitleExec" style="&&jobDefExec&&">
         <h4><b>{{jobDef}}</b>&nbsp;&nbsp;&nbsp;<small><i>{{createJob}}</i></small></h4>
      </span>

      <!-- edit /create / delete Job definitions  etc  -->
      <div class="jumbotron" style="padding:10px">
         <div class="btn-group">
            <button class="btn btn-default btn-sm dropdown-toggle" type="button"
                  id="device" noItem
                  data-toggle="dropdown" aria-expanded="false">
                  {{Device}} &nbsp; -- &nbsp;&nbsp;&nbsp;<span class="caret"></span>
            </button>
            <ul class="dropdown-menu" role="menu">
               <li role="presentation">
                  <a role="menuitem" noItem onclick="changeDevice(this)">{{Device}}&nbsp; -- &nbsp;</a>
                  &&deviceList&&
        <!--
                     <a role="menuitem" onclick="changeDevice(this)">Haustuer</a>
        -->
               </li>
            </ul>
         </div>   <!-- device -->

         <div class="btn-group">  <!-- ON -->
            <button class="btn btn-default btn-sm dropdown-toggle" type="button"
                  id="ON"
                  data-toggle="dropdown" aria-expanded="false">
                  {{ON}} &nbsp; -- &nbsp;&nbsp;&nbsp;<span class="caret"></span>
            </button>
            <ul class="dropdown-menu" role="menu">
               <li role="presentation" menuType="ON">

                  <a role="menuitem" noItem   typ=""         onclick="changeTime(this)">&nbsp; -- &nbsp;</a>
                  <a role="menuitem" tControl typ="time"     onclick="changeTime(this)">{{Time}}</a>
                  <a role="menuitem" sun      typ="sunrise"  onclick="changeTime(this)">{{Sunrise}}</a>
                  <a role="menuitem" sun      typ="sunset"   onclick="changeTime(this)">{{Sunset}}</a>

               </li>
            </ul>
         </div>   <!-- ON -->

         <div class="btn-group">   <!-- ONoffset -->
            <button class="btn btn-default btn-sm dropdown-toggle" type="button"
                  id="ONoffset"
                  data-toggle="dropdown" aria-expanded="false">
                  {{ONoffset}} &nbsp; -- &nbsp;&nbsp;&nbsp;<span class="caret"></span>
            </button>
            <ul class="dropdown-menu" role="menu">
                  <li role="presentation" menuType= 'ONoffset'>
                     <a role="menuitem" noItem   typ=""         onclick="changeTime(this)">&nbsp; -- &nbsp;</a>
                     <a role="menuitem" tControl typ="time+"    onclick="changeTime(this)">+</a>
                     <a role="menuitem" tControl typ="time-"    onclick="changeTime(this)">-</a>
                     <a role="menuitem" tControl typ="random"   onclick="changeTime(this)">{{random}}</a>
                     <a role="menuitem" tControl typ="random-"  onclick="changeTime(this)">{{randomMinus}}</a>
                  </li>
            </ul>
         </div>   <!-- ONoffset -->

         <div class="btn-group">   <!-- OFF -->
            <button class="btn btn-default btn-sm dropdown-toggle" type="button"
                  id="OFF"
                  data-toggle="dropdown" aria-expanded="false">
                  {{OFF}} &nbsp; -- &nbsp;&nbsp;&nbsp;<span class="caret"></span>
            </button>
            <ul class="dropdown-menu" role="menu">
               <li role="presentation" menuType="OFF">

                  <a role="menuitem" noItem   typ=""         onclick="changeTime(this)">&nbsp; -- &nbsp;</a>
                  <a role="menuitem" tControl typ="time+"    onclick="changeTime(this)">+</a>
                  <a role="menuitem" tControl typ="time"     onclick="changeTime(this)">{{Time}}</a>
                  <a role="menuitem"          typ="sunrise"  onclick="changeTime(this)">{{Sunrise}}</a>
                  <a role="menuitem"          typ="sunset"   onclick="changeTime(this)">{{Sunset}}</a>

               </li>
            </ul>
         </div>   <!-- OFF -->

         <div class="btn-group">   <!-- OFFoffset -->
            <button class="btn btn-default btn-sm dropdown-toggle" type="button"
                  id="OFFoffset"
                  data-toggle="dropdown" aria-expanded="false">
                  {{OFFoffset}} &nbsp; -- &nbsp;&nbsp;&nbsp;<span class="caret"></span>
            </button>
            <ul class="dropdown-menu" role="menu">
               <li role="presentation" menuType="OFFoffset">
                  <a role="menuitem" noItem   typ=""         onclick="changeTime(this)">&nbsp; -- &nbsp;</a>
                  <a role="menuitem" tControl typ="time+"    onclick="changeTime(this)">+</a>
                  <a role="menuitem" tControl typ="time-"    onclick="changeTime(this)">-</a>
                  <a role="menuitem" tControl typ="random"   onclick="changeTime(this)">{{random}}</a>
                  <a role="menuitem" tControl typ="random-"  onclick="changeTime(this)">{{randomMinus}}</a>
               </li>
            </ul>
         </div>  <!-- OFFoffset -->


         <div class="btn-group pull-right">   <!--  edit Job button  -->
            <button class="btn btn-default btn-sm dropdown-toggle glyphicon glyphicon-pencil" type="button"
                  id="jobAction" title="{{editJob}}"
                  data-toggle="dropdown" aria-expanded="false"> <span class="caret"></span>
            </button>
            <ul class="dropdown-menu" role="menu">
                  <li role="presentation">
                     <a role="menuitem" style="cursor:pointer;" onclick="jobAction(this,'clear')">&nbsp; {{clearJob}} &nbsp;</a>

                     <a role="menuitem" id="jobAdd"  style="cursor:pointer;&&jobAdd&&"  onclick="jobAction(this,'add')">&nbsp; {{addJob}} &nbsp;</a>
                     <a role="menuitem" id="jobExec" style="cursor:pointer;&&jobExec&&" onclick="controlGET()"  >&nbsp; {{exJob}} &nbsp;</a>

                     <a role="menuitem" style="cursor:pointer;" onclick="openHelp('Job')">&nbsp; {{helpDocu}}: {{prefJobs}} &nbsp;</a>
                  </li>

            </ul>
         </div>


         <!--  row with jobNo and current Job text -->
         <div style="margin-left:20px;margin-top:5px">
                <textbox id="jobNo" class="col-md-1">#</textbox></span>
                <i><textbox id="currentJob">---</textbox></i>
                <small><textbox class="pull-right" id="controlStatus">-s-</textbox></i></small>

         </div>
      </div>   <!-- edit /create / delete Job definitions  etc  -->


      <!-- Set Time   -->
      <div class="row" id="setTime" style="display:none;" >
            <div class="col-xs-1"></div>
            <div class="col-xs-6 bg-info" >

               <span placeholder=".col-xs-6" class="bg-info container">
                  <button class="btn btn-default" id="inkrementTime1" onclick="editTime(this)"> ++ </button>
                  <button class="btn btn-default" id="inkrementTime" onclick="editTime(this)"> + </button>

                  <a class="bg-info" style="color:blue;font-size:120%;" onclick="editTime(this)" status="false" id="HH">12</a> :
                  <a class="bg-info" style="color:blue;font-size:120%;" onclick="editTime(this)" status="false" id="MIN">02</a>

                  <button class="btn btn-default" id="dekrementTime" onclick="editTime(this)"> - </button>
                  <button class="btn btn-default" id="dekrementTime1" onclick="editTime(this)"> -- </button>
                  <button class="btn btn-default" id="_setTime" onclick="changeTime(this)">
                     {{SetTime}}
                  </button> </span>
            </div>
      </div> <!--  Set Time -->


      <span id="daySchedule" style="&&displaySchedule&&">
         <h4><b>{{daySchedule}} </b><small><i> &nbsp; &nbsp; {{collJob}} &nbsp;&nbsp;</i></small></h4>

         <div class="jumbotron" style="padding:10px">
            <div class="input-group pull-right" >
               <span class="input-group-addon"><b>{{scheduleFile}}</b></span>
               <input class="form-control" id="fileName" placeholder="&&FILE&&" style="width:350px" type="text"/>
               <span>
                      <button class="btn btn-default btn-sm dropdown-toggle glyphicon glyphicon-cog pull-right " 
                         type="button" id="jobAction" title="{{jobListFunctions}}" 
                         data-toggle="dropdown" aria-expanded="false"> 
                         <span class="caret"></span>
                      </button>
                      <ul class="dropdown-menu pull-right" role="menu">
                         <a role="menuitem">&nbsp; {{scheduleFile}} ...</a>
                         <li role="presentation" style="cursor: pointer">
                            <a role="menuitem" style="cursor: pointer" id="saveDaySchedule" onclick="saveIt()" disabled="disabled">&nbsp; {{save}} </a> 
                            <a role="menuitem" style="cursor: pointer" onclick="deleteIt()">&nbsp; {{erase}}</a></li>

                            <a role="menuitem"  title="{{jobsToScheduler}}">&nbsp; {{actualDaySchedule}} ... </a>
                         <li>
                            <a role="menuitem" style="cursor: pointer" id="addJobs" onclick="jobAction(this,'addJobs')">&nbsp; {{addJobs}} &nbsp;</a> 
                            <a role="menuitem" style="cursor: pointer" id="removeJobs" onclick="jobAction(this,'removeJobs')">&nbsp; {{removeJobs}} &nbsp;</a> 
                            <a role="menuitem" style="cursor: pointer" id="loadJobs" onclick="jobAction(this,'loadJobs')">&nbsp; {{loadJobs}} &nbsp;</a></li>
                      </ul>
               </span>

               <span>
                     <button
                        class="btn btn-default btn-sm dropdown-toggle glyphicon glyphicon-pencil pull-right "
                        type="button" id="jobAction" title="{{editJobandList}}"
                        data-toggle="dropdown" aria-expanded="false">
                        <span class="caret"></span>
                     </button>
                     <ul class="dropdown-menu pull-right " role="menu">
                        <a role="menuitem">&nbsp; {{selectedJob}} ... </a>
                        <li role="presentation">
                           <a role="menuitem" style="cursor: pointer" id="jobEdit" onclick="jobAction(this,'edit')">&nbsp; {{edit}} &nbsp;</a> 
                           <a role="menuitem" style="cursor: pointer" id="jobDelete" onclick="jobAction(this,'delete')">&nbsp; {{erase}} &nbsp;</a> 
                           <a role="menuitem" style="cursor: pointer" id="jobUp" onclick="jobAction(this,'up')">&nbsp; {{shiftUp}} &nbsp;</a> 
                           <a role="menuitem" style="cursor: pointer" id="jobdown" onclick="jobAction(this,'down')">&nbsp; {{shiftDown}} &nbsp;</a>
                           <a> </a> 
                           <a role="menuitem" style="cursor: pointer" onclick="openHelp('editSchedule')">&nbsp; {{helpDocu}}: {{prefJobs}}&nbsp;</a></li>
                  </ul>
               </span>
            </div> 
            <span><b>&nbsp;&nbsp;&nbsp;{{jobList}}</b></span>
            <!-- /input-group -->

            <!--   List of ini entries -->
            <select id="jobsList" class="form-control" size="10">
                 &&JOBS&&
            </select>
         </div> <!-- jumbotron-->
      </span>  <!-- daySchedule -->

   </section>


   <script>

      var language = "{{locale}}";
      console.log("piEdit Locale  language:" + language)


      function controlGET() {
         $.get('/control', $('#currentJob').text(), function(data, status) {
            $('#controlStatus').html(status)
         });
      };

      function openHelp(name) {
         var main = "https://dl.dropboxusercontent.com/u/35444930/piScheduler/"+ language + "/"

         switch (name) {
         case 'Job':
            window.open(main + "piScheduleFeatures.html", '_blank');
            break;
         case 'DaySchedule':
            window.open(main + "piScheduleOverview.html", '_blank');
            break;
         case 'editSchedule':
            window.open(main + "piScheduleEdit.html", '_blank');
            break;
         }
      }

      function clearButton(name, title) {
         var button = $('#' + name)
         button.removeAttr('value')
         button.html(title
             + ' &nbsp; -- &nbsp;&nbsp;&nbsp;<span class="caret"></span>')
      }

      function checkButton(button) {
         return !($('#' + button)[0].attributes.value == null)
      }

      /**
       *  write a 'job' line to Job Definition  and parse it for buttons
       **/
      function jobSetup(job, jobNo) {
         jobAction(null, 'clear')

         $('#currentJob').html(job)
         $('#jobNo').html('#' + jobNo)

         //parse job to get: device;on,onOffset;off,offOffset
         var sArray = job.split(";")

         if (sArray.length > 0) {
            // first item can't be 'on' or 'off'
            if ((sArray[0].substring(0, 2).toLowerCase() == 'on')
                  || (sArray[0].substring(0, 3).toLowerCase() == 'off')) {
               alert('{{errJob}}!\n' + sArray[0])
               return

            }

            setDevice = sArray[0].trim()
            // iterate over control strings sep by  ; starting without 'device'
            for (var i = 1; i < sArray.length; i++) {
               var cItem = sArray[i].trim()
               var aItems = cItem.split(",")

               var onOff = aItems[0].trim()

               if (onOff == 'on') {
                  for (var j = 1; j < aItems.length; j++) {
                     var arg = aItems[j].trim()

                     if ((arg == 'sunrise') || (arg == 'sunset')) {
                        modeON = arg
                        setON = arg
                     }
                     if (arg.substring(0, 2) == '~-') {
                        modeONoffset = '~-'
                        setONoffset = arg.substring(2).trim()
                     } else if ((arg[0] == '+') || (arg[0] == '-')
                           || (arg[0] == '~')) {
                        modeONoffset = arg[0]
                        setONoffset = arg.substring(1).trim()
                     } else {
                        setON = arg.trim()
                        modeON = ""
                     }
                     if (setON[0] == ":")
                        setON = "00" + setON
                     if (setONoffset[0] == ":")
                        setONoffset = "00" + setONoffset
                  }
               }

               else if (onOff == 'off') {
                  for (var j = 1; j < aItems.length; j++) {
                     var arg = aItems[j].trim()

                     if ((arg == 'sunrise') || (arg == 'sunset')) {
                        modeOFF = arg
                        setOFF = arg
                     } else if (arg.substring(0, 2) == '~-') {
                        modeOFFoffset = '~-'
                        setOFFoffset = arg.substring(2).trim()
                     } else if ((arg[0] == '-') || (arg[0] == '~')) {
                        modeOFFoffset = arg[0]
                        setOFFoffset = arg.substring(1).trim()
                        offOffset = arg
                     } else if ((arg[0] == '+') && (setOFF == '')) {
                        modeOFF = '+'
                        setOFF = arg.substring(1).trim()
                     } else if ((arg[0] == '+') && (setOFF != '')) {
                        modeOFFoffset = '+'
                        setOFFoffset = arg.substring(1).trim()
                     } else {
                        modeOFF = ''
                        setOFF = arg.trim()
                     }
                     if (setOFF[0] == ":")
                        setOFF = "00" + setOFF
                     if (setOFFoffset[0] == ":")
                        setOFFoffset = "00" + setOFFoffset
                  }
               }

               else {
                  alert("Instruction >>" + onOff + "<< unknown!")
               }

            } // for time values
         } // for control string

         //console.log("ON   " + setON  + "  mode >>"+ modeON  +"<<  ONoffset:  " + setONoffset  + "   mode >>"+ modeONoffset + "<<")
         //console.log("OFF  " + setOFF + "  mode >>"+ modeOFF +"<<  OFFoffset: " + setOFFoffset + "   mode >>"+ modeOFFoffset + "<<")

         //set the buttons
         var b = bold(setDevice)
         $('#device').html(b[0] + setDevice + ' &nbsp;&nbsp;<span class="caret"></span>' + b[1])
         $('#device').attr('value', setDevice)

         var b = bold(setON)
         $('#ON').html(b[0] + '{{ON}} ' + ' &nbsp;' + setON + '&nbsp;<span class="caret"></span>' + b[1])
         $('#ON').attr('value', setON)

         var b = bold(setONoffset)
         $('#ONoffset').html(b[0] + '{{ONoffset}} ' + modeONoffset + ' &nbsp;' + setONoffset + '&nbsp;<span class="caret"></span>' + b[1])
         $('#ONoffset').attr('value', setOFFoffset)

         var b = bold(setOFF)
         $('#OFF').html(b[0] + '{{OFF}} ' + modeOFF + ' &nbsp;' + setOFF + '&nbsp;<span class="caret"></span>' + b[1])
         $('#OFF').attr('value', setOFF)

         var b = bold(setOFFoffset)
         $('#OFFoffset').html(b[0] + '{{OFFoffset}} ' + modeOFFoffset + ' &nbsp;' + setOFFoffset + '&nbsp;<span class="caret"></span>' + b[1])
         $('#OFFoffset').attr('value', setOFFoffset)

         function bold(s) {
            var b = [];
            b[0] = '<b>';  b[1] = '</b>'
            if (s == "") {
               b[0] = '';  b[1] = ''
            }
            return b
         }
      }

      /**
       *  get the button settings and build the 'job'
       *  @param  setJob:  if passed write to text line 
       **/
      function buildJob(setJob) {
         var _ONoffset = "", _OFFoffset = ""

         var _ON = (setON != "") ? ";on," + setON : ""
         if (_ON != "")
            _ONoffset = (setONoffset != "") ? "," + modeONoffset + setONoffset : ""

         var _OFF = (setOFF != "") ? ";off," + modeOFF + setOFF : ""
         if (_OFF != "")
            _OFFoffset = (setOFFoffset != "") ? "," + modeOFFoffset + setOFFoffset : ""

         var job = setDevice + _ON + _ONoffset + _OFF + _OFFoffset
         if (setJob != null) {
            $('#currentJob').html(job)
            $('#controlStatus').html(' -- ')
         }
         return job
      }

      /**
       *    actions for 'Job' on Job Definition section
       *   @param  {object} eThis 
       *           {string} info: controls action,
       *              'build'  build job from buttons
       *              'read'   read from Day Schedule active line
       *              'add'    add the current job before active line
       *              'delete' delete active entry from Day Schedule
       **/
      function jobAction(eThis, info) {

         var msg = ""
         if (info == 'addJobs') {
            msg = "Alle im Fenster 'Tagesplan' gezeigten Jobs dem 'Aktuellen Tagesplan' hinzufuegen?"
            if (confirm(msg) == true) {
               var jobs = getJobs()
               $.get('/cmd?addJobs:'+jobs);
            }
            return
         }


         if (info == 'removeJobs') {
             msg = "Alle Jobs von dem 'Aktuellen Tagesplan' entfernt?"
             if (confirm(msg) == true) {
                $.get('/cmd?removeJobs')
             }
             return
         }


         if (info == 'loadJobs') {
            msg = "Die Jobs des 'Aktuellen Tagesplan' löschen"
                + "\nund mit allen im Fenster 'Tagesplan' gezeigten Jobs ersetzt."
                + "\n\nDiese Jobs werden als 'Tagesplan Datei' gespeichert."

            if (confirm(msg) == true) {
               var fP = saveIt()
               $.get('/cmd?removeJobs')
               $.get('/cmd?loadJobs:'+fP)
            }
            return
         }



         if (info == 'clear') {
            clearButton('device', '{{Device}}')
            clearButton('ON', '{{ON}}')
            clearButton('ONoffset', '{{ONoffset}}')
            clearButton('OFF', '{{OFF}}')
            clearButton('OFFoffset', '{{OFFoffset}}')

            $('#currentJob').html(' --- ')
            $('#controlStatus').html(' -- ')
            $('#jobNo').html('#')
            $('#setTime').attr('style', 'display:none')

            setON = "";
            setONoffset = "";
            setOFF = "";
            setOFFoffset = "";
            modeON = "";
            modeONoffset = "";
            modeOFF = "";
            modeOFFoffset = "";

            return

         }

         if (info == 'build') {
            var check = $('#device')
            var device = check[0].textContent.trim()
            if (!!check[0].attributes.noItem) {
               alert("{{deviceNotSelected}}")
               return

            }
            var rv = buildJob()
            //       alert ("[jobAction]  " + info + "  >>" + rv + '<<')
            return;
         }

         // check Day Schedule if a 'job' is selected
         var jobsList = $('#jobsList')
         var jobNo = jobsList[0].selectedIndex

         if (jobNo == -1) {
            if (info == 'add') {
               alert("[jobAction]  " + "{{selectRow}}\n{{selectRow1}}")
            } else {
               alert("[jobAction]  " + "{{selectJobRow}}")
            }
            return;
         }

         var job = jobsList[0].selectedOptions[0].text

         // read activated job on Day Schedule and place it to Job Definition
         if (info == 'edit') {
            //       alert ("[jobAction]  " + info + "  >>" + job + '<<')

            jobSetup(job, jobNo)
            return;
         }

         // add the 'Job' on job definition line to the jobsList
         if (info == 'add') {
            var cJob = $('#currentJob')[0].textContent

            //  if no Device selected, terminate
            if (checkButton('device') == false) {
               alert(" {{deviceNotDefined}}")
               return;
            }

            if ((checkButton('ON') == false)
                  && ((checkButton('OFF') == false))) {
               alert(" {{defineTime}}")
               return

            }
            // insert in 'Day Schedule' before activated line
            var option = document.createElement("option");
            option.text = cJob;
            document.getElementById("jobsList").add(option, jobNo);

            // jobList has changed !  ==> set "changed"
            changed = true;
         }

         if (info == 'delete') {
            //TODO   ask user if OK to delete !
            var a = jobsList
            jobsList[0][jobNo].remove()

            // jobList has changed !  ==> set "changed"
            changed = true;
         }

         //shift activate 'job' on jobsList
         if (info == 'up') {
            if (jobNo == 0)
               return

            var a = jobsList[0][jobNo]
            jobsList[0][jobNo].remove()
            document.getElementById("jobsList").add(a, jobNo - 1);

            // jobList has changed !  ==> set "changed"
            changed = true;
         }

         //shift activate 'job' on jobsList
         if (info == 'down') {
            if (jobNo == jobsList.length - 1)
               return

            var a = jobsList[0][jobNo]
            jobsList[0][jobNo].remove()
            document.getElementById("jobsList").add(a, jobNo + 1);

            // jobList has changed !  ==> set "changed"
            changed = true;
         }

         if (changed == true)
            $("#saveDaySchedule").removeAttr('disabled');
      }

      $('#main').on('click', function(event) {
         if (changed == true) {
            alert("{{leavePage}}")
            return

         }
         location.replace('/')
      });

      /**
         Global parameters
       **/
      var changed = false

      var menuType, timeType, timeTypeLocal, timeValue

      //default time values
      var ONhh = '11'
      var ONmin = '00'

      var OFFhh = '12'
      var OFFmin = '00'

      var OFFSEThh = '00'
      var OFFSETmin = '25'

      var setDevice = "", setON = "", setONoffset = "", setOFF = "", setOFFoffset = ""
      var modeDevice, modeON, modeONoffset, modeOFF, modeOFFset

      function editTime(eThis) {
         var action = eThis.id

         function setHM(action) {
            if ((action == "HH") || (action == "MIN") || (action == "SEC")) {

               $('#HH').attr('style',
                     "color:blue;font-size:120%;background-color:#D9EDF7")
               $('#MIN').attr('style',
                     "color:blue;font-size:120%;background-color:#D9EDF7")
               $('#HH').attr('status', 'false')
               $('#MIN').attr('status', 'false')

               $('#' + action).attr('style',
                     "color:red;font-size:120%;background-color:#F2F5A9")
               $('#' + action).attr('status', 'true')
            }
         }

         setHM(action);

         var aHH = ($('#HH').attr('status') == 'true')
         var aMin = ($('#MIN').attr('status') == 'true')

         var elem = $('#HH')
         var max = 24

         if (aMin) {
            var max = 60
            elem = $('#MIN')
         }
         var d = (max == 60) ? 10 : 3

         if ((action == "inkrementTime") || (action == "inkrementTime1")) {
            if (!aHH && !aMin) // && !aSec)
               setHM('HH')

            d = (action == "inkrementTime1") ? d : 1
            var v = +elem[0].textContent.replace(':', '') + d
            if (v > max)
               v = 0;
            elem.html(two(v));
         }

         if ((action == "dekrementTime") || (action == "dekrementTime1")) {
            if (!aHH && !aMin) // && !aSec)
               setHM('HH')

            d = (action == "dekrementTime1") ? d : 1
            var v = +elem[0].textContent.replace(':', '') - d
            if (v < 0)
               v = max - 1;
            elem.html(two(v));
         }
      }

      function two(num) {
         if (+(num) < 10)
            num = '0' + +(num)
         return num
      }

      function changeDevice(eThis) {
         setDevice = eThis.textContent
         //  alert(" .... change Device ... :" + device)
         $('#device').html('<b>'+ setDevice
              + '&nbsp;&nbsp;&nbsp;</b><span class="caret"></span>')
         if (eThis.getAttribute('noitem') == "") {
            $('#device').removeAttr('value')
         } else {
            $('#device').attr('value', setDevice)
         }
         buildJob(true)
      }

      function changeTime(eThis) {
         timeTypeLocal = eThis.textContent // {{Sunset}}  or {{Time}}
         timeType = 'time'

         _menuType = eThis.parentElement.getAttribute('menuType')
         if (_menuType != null)
            menuType = _menuType // 'ON'  or  'ONoffset'

         _timeType = eThis.getAttribute('typ')
         if (_timeType != null)
            timeType = eThis.getAttribute('typ') // 'time'  or  'sunset'

         var deco = '', deco1 = '', mode = ''

         if (eThis.attributes.tControl) { // controls the extra menu to set time value 
            $('#setTime').attr('style', 'display:block')
         } else {
            $('#setTime').attr('style', 'display:none')
         }

         if (timeType == "time+")
            mode = "+"
         if (timeType == "time-")
            mode = "-"
         if (timeType == "random")
            mode = "~"
         if (timeType == "random-")
            mode = "~-"

         if (menuType == 'ON') {
            if (eThis.id == '_setTime') {
               ONhh = $('#HH')[0].textContent
               ONmin = $('#MIN')[0].textContent
               setON = ONhh + ':' + ONmin
               timeValue = modeON + " " + setON
               var deco = '<b>';
               var deco1 = '</b>'

            } else {
               modeON = mode
               if ((timeType == 'sunrise') || (timeType == 'sunset')) {
                  setON = timeType
                  timeValue = timeTypeLocal
                  var deco = '<b>';
                  var deco1 = '</b>'
               } else {

                  var tDetails = $('#' + menuType)[0].textContent
                        .match(/\d+/g)
                  if (tDetails == null) {
                     var t = new Date()
                     ONhh = two(t.getHours())
                     ONmin = two(t.getMinutes())
                  } else {
                     ONhh = two(tDetails[0])
                     ONmin = two(tDetails[1])
                  }
                  $('#HH').html(ONhh)
                  $('#MIN').html(ONmin)
                  setON = ONhh + ":" + ONmin
                  timeValue = modeON + " " + setON
                  var deco = '<i>';
                  var deco1 = '</i>'
               }
            }
            //console.log("ON   setON:" + setON + "   modeON >>" + modeON + "<<")

            $('#' + menuType).html(deco + '{{ON}} ' + '&nbsp;&nbsp;' + timeValue
                  + '&nbsp;&nbsp;&nbsp;' + deco1
                  + '<span class="caret"></span>')
         }

         if (menuType == 'ONoffset') {
            if (eThis.id == '_setTime') {
               ONSEThh = $('#HH')[0].textContent
               ONSETmin = $('#MIN')[0].textContent
               setONoffset = ONSEThh + ':' + ONSETmin
               timeValue = modeONoffset + " " + setONoffset
               var deco = '<b>';
               var deco1 = '</b>'
            } else {
               modeONoffset = mode

               var tDetails = $('#' + menuType)[0].textContent.match(/\d+/g)
               if (tDetails == null) {
                  ONSEThh = '00'
                  OFFSETmin = '30'
               } else {
                  ONSEThh = two(tDetails[0]);
                  ONSETmin = two(tDetails[1]);
               }
               $('#HH').html(ONSEThh)
               $('#MIN').html(ONSETmin)
               setONoffset = ONSEThh + ":" + ONSETmin
               timeValue = modeONoffset + "  " + setONoffset
               deco = '<i>';
               deco1 = '</i>'
            }
            //console.log("ON   setONoffset:" + setONoffset + "   modeON >>" + modeONoffset + "<<")

            $('#' + menuType).html(deco + '{{ONoffset}} ' + '&nbsp;&nbsp;' + timeValue
                  + '&nbsp;&nbsp;&nbsp;' + deco1
                  + '<span class="caret"></span>')
         }

         if (menuType == 'OFF') {

            if (eThis.id == '_setTime') {
               OFFhh = $('#HH')[0].textContent
               OFFmin = $('#MIN')[0].textContent
               setOFF = OFFhh + ':' + OFFmin
               timeValue = modeOFF + " " + setOFF
               var deco = '<b>';
               var deco1 = '</b>'

            } else {
               modeOFF = mode
               if ((timeType == 'sunrise') || (timeType == 'sunset')) {
                  setOFF = timeType
                  timeValue = timeTypeLocal
                  var deco = '<b>';
                  var deco1 = '</b>'
               } else {

                  var tDetails = $('#' + menuType)[0].textContent.match(/\d+/g)
                  if (tDetails == null) {
                     var t = new Date()
                     OFFhh = two(t.getHours())
                     OFFmin = two(t.getMinutes())
                  } else {
                     OFFhh = two(tDetails[0])
                     OFFmin = two(tDetails[1])
                  }
                  $('#HH').html(OFFhh)
                  $('#MIN').html(OFFmin)
                  setOFF = OFFhh + ":" + OFFmin
                  timeValue = modeOFF + setOFF
                  var deco = '<i>';
                  var deco1 = '</i>'
               }
            }
            //console.log("OFF   setOFF:" + setOFF + "   modeOFF >>" + modeOFF + "<<")

            $('#' + menuType).html(deco + '{{OFF}} ' + '&nbsp;&nbsp;' + timeValue
                  + '&nbsp;&nbsp;&nbsp;' + deco1
                  + '<span class="caret"></span>')
         }

         if (menuType == 'OFFoffset') {
            if (eThis.id == '_setTime') {
               OFFSEThh = $('#HH')[0].textContent
               OFFSETmin = $('#MIN')[0].textContent
               setOFFoffset = OFFSEThh + ':' + OFFSETmin
               timeValue = modeOFFoffset + " " + setOFFoffset
               var deco = '<b>';
               var deco1 = '</b>'
            } else {
               modeOFFoffset = mode

               var tDetails = $('#' + menuType)[0].textContent.match(/\d+/g)
               if (tDetails == null) {
                  OFFSEThh = '00'
                  OFFSETMIN = '30'
               } else {
                  OFFSEThh = tDetails[0];
                  OFFSETmin = tDetails[1];
               }
               $('#HH').html(OFFSEThh)
               $('#MIN').html(OFFSETmin)
               setOFFoffset = OFFSEThh + ":" + OFFSETmin
               timeValue = modeOFFoffset + setOFFoffset
               deco = '<i>';
               deco1 = '</i>'
            }
            //console.log("OFF   setOFFoffset:" + setOFFoffset + "   modeOFFoffset >>" + modeOFFoffset + "<<")

            $('#' + menuType).html(deco + '{{OFFoffset}} ' + '&nbsp;&nbsp;' + timeValue
                  + '&nbsp;&nbsp;&nbsp;' + deco1
                  + '<span class="caret"></span>')
         }

         buildJob(true)
      }

      /**
       *  ini File functions
       **/
      function deleteIt() {
         change = false;
         var fN = $('input#fileName').val()
         var fP = $('input#fileName').attr('placeholder')
         $.post('/fDelete?[{"fName":"' + fN + '"},{"pName":"' + fP + '"}]');
         setTimeout(function() {
            location.replace('/')
         }, 100)
      };

      function saveIt() {
         var jobs = getJobs()

         var fN = $('input#fileName').val()
         var fP = $('input#fileName').attr('placeholder')
         $.post('/fSave?[{"fName":"' + fN + '"},{"pName":"' + fP
               + '"},{"jobs":"' + jobs + '"}]');
         changed = false;
         $("#saveDaySchedule").attr('disabled', 'disabled');
         return fP
      };

      function getJobs() {
         var jobsList = $('#jobsList')[0]
         var jobs = ""
         var len = jobsList.length
         for (var i = 0; i < len; i++) {
            jobs += (jobsList[i].value + ((i != len) ? "|" : ""))
         }
         return jobs
      }

      $(window).on('beforeunload', function(e) {
         if (changed == true) {
            return '{{unsavedStuff}}';
         }
      });
   </script>


   <style type="text/css">
      h3 {background: silver;
      }
   </style>

   </body>
</html>
