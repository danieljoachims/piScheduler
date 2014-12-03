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

    </head>

    <body>

        <section class="container">

            <div class="container">
                <div class="row">
                    <h3>piScheduler <small><i> - Day List of Jobs</i></small></h3>

                    <div class="col-sm-1">
                        <form id="formAction" action="/logList?{{today}}" method="post">
                            <button type="submit" class="btn btn-primary">
                                Today
                            </button>
                        </form>
                    </div>

                    <div class="col-sm-3">

                        <div class="btn-group btn-input clearfix">

                            <button type="button" class="btn btn-default dropdown-toggle form-control" data-toggle="dropdown">
                                <span data-bind="label">Select Day</span>&nbsp;<span class="caret"></span>
                            </button>

                            <ul class="dropdown-menu" role="menu" id="daySelect">
                                <li>
                                    <a href="#">Monday</a>
                                </li>
                                <li>
                                    <a href="#">Tuesday</a>
                                </li>
                                <li>
                                    <a href="#">Wednesday</a>
                                </li>
                                <li>
                                    <a href="#">Thursday</a>
                                </li>
                                <li>
                                    <a href="#">Friday</a>
                                </li>
                                <li>
                                    <a href="#">Saturday</a>
                                </li>
                                <li>
                                    <a href="#">Sunday</a>
                                </li>
                            </ul>
                        </div>

                    </div>

                </div>
            </div>

            <h4>{{selectedDay}}</h4>

            <script>
                $('#daySelect').on('click', 'li', function(event) {

                    var $target = $(event.currentTarget);
                    var sDay = $target.text().trim()

                    $target.closest('.btn-group').find('[data-bind="label"]').text($target.text()).end().children('.dropdown-toggle').dropdown('toggle');
                    $('#formAction').attr('action', ('/logList?' + sDay))
                    $('#formAction').submit();
                    return sDay;
                });

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

        <section id="logList">
            {{!logList}}	
        </section>
    </body>

</html>


