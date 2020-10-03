<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sortland Camera 01</title>
</head>

<body>
    Sortland camera #01 - Reloading every 15 sec
    <br /> <br />
    <img src="../status.jpg" id="camera" class="responsive">
</body>
<style>
    body {
        text-align: center;
        color: hotpink;
        background-color: #000;
    }
    .responsive {
        border-radius: 5px;
        border: 1px rgba(225,105,180,0.3) solid;
        width: 90%;
        height: auto;
    }
</style>
<script>
    setInterval(function() {
        var myImageElement = document.getElementById('camera');
        myImageElement.src = '../status.jpg?rand=' + Math.random();
    }, 15000);
</script>

</html>