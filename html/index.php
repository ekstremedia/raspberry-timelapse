<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SigerfjordCam #02</title>
</head>

<body>
    SigerfjordCam #02 - Reloading every 40 sec
    <br /> <br />
    <div id="imgdiv">
        <img src="../status.jpg" id="camera" class="responsive">
    </div>
    <div>
<br><br>
    <?php 
$localIP = $_SERVER['SERVER_ADDR'];
$hostname = gethostname();

?>
<a href="http://<?= $localIP ?>">http://<?= $localIP ?></a>
<br><br>
<a href="http://<?= $hostname ?>">http://<?= $hostname?></a>
</div>
</body>
<style>
    body {
        text-align: center;
        color: hotpink;
        background-color: #000;
    }
    #imgdiv {
        width: auto;
        max-width: 1200px;
        margin: auto;
    }
    .responsive {
        border-radius: 10px;
        border: 2px rgba(225,105,180,0.5) solid;
        width: 90%;
        height: auto;
    }
</style>
<script>
    setInterval(function() {
        var myImageElement = document.getElementById('camera');
        myImageElement.src = '../status.jpg?rand=' + Math.random();
    }, 40000);
</script>

</html>
