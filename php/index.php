<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sortland Camera 01</title>
</head>
<body>
        Sortland camera #01
        <img src="../status.jpg" id="camera" width="2000">
</body>
<script>
setInterval(function() {
    var myImageElement = document.getElementById('camera');
    myImageElement.src = '../status.jpg?rand=' + Math.random();
}, 15000);
</script>
</html>