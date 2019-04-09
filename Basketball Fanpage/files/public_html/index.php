<?php
$list = ""; 

if (isset($_POST['submit'])) {

    $option = $_POST['option'];
    
    if (strpos($option, '.txt') === false) {
        die("No luck, hackers :) ");
    }
    

    $fp=fopen("data/" . $option, "r");
    // check to see if file has been found

    $list = "<table class = 'table table-bordered text-center'>";
    
    while ($line = fgets($fp)) {
        if ($option === "stats.txt") {
            $stringsplit = explode("\t", $line);
            $list = $list . "<tr><th>" . $stringsplit[0] . "</th>";

            for ($i = 1; $i < sizeof($stringsplit); $i++) {
                $list = $list . "<td>" . $stringsplit[$i] . "</td>";
            }
            $list .= "</tr>";
        } else {
            $list = $list . "<tr><th>" . $line . "</th></tr>";
        }

    }

    $list .= "</table>";

}

?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Maryland Basketball Fan Page</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <link rel="stylesheet" type="text/css" media="screen" href="main.css">
</head>
<body>
    <!-- Make a bootstrap navbar! -->
    <div class = "container">
        <div class = "row">

            <div class = "col-12 text-center">
                <br />
                <h1> Maryland Basketball Fan Page </h1>
            </div>
        </div>

        <form method = "post" action="./index.php" name="fileForm" enctype="multipart/form-data">
            <div class = "row">
                <div class = 'col-12 text-center'>
                    <select name = "option" id = "getFile" class = "form-control">
                        <option> -- Select a Category -- </option>
                        <option value = "maryland.txt">Maryland Players</option>
                        <option value = "opponents.txt">Opponent Team Names</option>
                        <option value = "stats.txt">Stats</option>
                    </select>
                </div>
            </div>
            <br>
            <div class = "row">
                <div class = "col-12 text-center">

                    <input type="submit" class = "btn btn-primary" name="submit" id="submit" value = "Submit">
                </div>
            </div>
        </form>
        <br>
        <div class = "row"> 
            <div class = "col-12">
            
                <?php echo $list; ?>
                
            </div>
        </div>
    </div>



    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>