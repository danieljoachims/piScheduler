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
                    <h3>piScheduler <small><i> - Main Menu</i></small></h3>

                    <div class="col-sm-2">
                        <form id="formAction" action="/home" method="post">
                            <button type="submit" class="btn btn-primary">
                                Home
                            </button>
                        </form>
                    </div>

                    <div class="col-sm-2" width="80px">
                        <form id="formAction1" action="/prefs" method="post">
                            <button type="submit" class="btn btn-primary">
                                Prefs & Jobs
                            </button>
                        </form>
                    </div>


                    <div class="col-sm-2">
                        <form id="formAction2" action="/logs" method="post">
                            <button type="submit" class="btn btn-primary">
                                Log List
                            </button>
                        </form>
                    </div>


                </div>
            </div>


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
            	
        </section>
    </body>

</html>


