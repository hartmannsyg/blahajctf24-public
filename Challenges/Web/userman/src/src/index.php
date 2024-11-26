<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Management</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        h2 {
            color: #555;
            border-bottom: 2px solid #ccc;
            padding-bottom: 10px;
        }
        form {
            background: #fff;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        label {
            display: block;
            margin: 10px 0 5px;
        }
        input[type="text"],
        input[type="password"] {
            width: 98%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            background-color: #5cb85c;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        input[type="submit"]:hover {
            background-color: #4cae4c;
        }
    </style>
</head>
<body>
    <h1>BlahajCorp User Management System</h1>
    <?php 
        function makeDb($name){
            if (!preg_match('/^[0-9]+$/', $name)) {
                echo '<p>No hacking!!! This is not a LFI challenge dammit</p>';
                throw new InvalidArgumentException('Invalid database name. Only numbers are allowed.');
            }
            
            $db = new SQLite3('/var/www/html/databases/'.$name.'.db');

            $db->exec("CREATE TABLE IF NOT EXISTS users (
                username TEXT UNIQUE,
                userObject TEXT
            )");
            return $db;
        }

        class User{
            protected $_username;
            protected $_password;
            protected $_admin;
            protected $_reserved;
            
            public function __construct($username, $password){
                $this->_username = $username;
                $this->_password = $password;
                $this->_admin = false;
                $this->_reserved = "";
            }
            
            public function getName(){
                return $this->_username;
            }
            
            public function checkpass($pass){
                return $this->_password == $pass;
            }
            
            public function isAdmin(){
                return $this->_admin;
            }
        }

        function insertUser($db, $userObject) {
            $userser = str_replace(chr(0) . '*' . chr(0), '\0\0\0', serialize($userObject)); //database does not support null bytes, and the protected field has a \x00*\x00 preface. very bad
            $stmt = $db->prepare("INSERT INTO users (username, userObject) VALUES (:username, :userObject)");
            $stmt->bindValue(':username', $userObject->getName(), SQLITE3_TEXT);
            $stmt->bindValue(':userObject', $userser, SQLITE3_TEXT);
            $stmt->execute();
        }

        function getUserObject($db, $username, $pass){
            $stmt = $db->prepare("SELECT userObject FROM users WHERE username = :username");
            $stmt->bindValue(':username', $username, SQLITE3_TEXT);
            $result = $stmt->execute();
            if ($row = $result->fetchArray(SQLITE3_ASSOC)) {
                $user = unserialize(str_replace('\0\0\0', chr(0) . '*' . chr(0), $row['userObject']));
                if($user->checkpass($pass)){
                    return $user;
                }
                return null;
            } else {
                return null;
            }
        }

        // Handle database creation
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['create_db'])) {
            $dbname = random_int(100000, 999999); // Generate a random database name
            makeDb($dbname);
            echo "<p>Database '$dbname' created successfully.</p>";
        }
        // Handle account creation
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['username']) && isset($_POST['password']) && isset($_POST['dbname'])) {
            $username = $_POST['username'];
            $password = $_POST['password'];
            
            $dbname = $_POST['dbname'];
            $db = makeDb($dbname);
            
            $user = new User($username, $password);
            insertUser($db, $user);
            echo "<p>Account created successfully for user '$username'.</p>";
        }

        // Handle login
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['login_username']) && isset($_POST['login_password']) && isset($_POST['dbname'])) {
            $username = $_POST['login_username'];
            $password = $_POST['login_password'];
            
            $dbname = $_POST['dbname'];
            $db = makeDb($dbname);
            
            $user = getUserObject($db, $username, $password);
            if ($user) {
                echo "<p>Login successful for user '$username'. </p>";
                if ($user->isAdmin()) {
                    echo "<p>Wow, you are an admin! Here is your flag: blahaj{d1Dnt_kN0w_pHP_C0u1D_0V3rf10W}</p>";
                } else {
                    echo "<p>But you are not an admin!</p>";
                }
            } else {
                echo "<p>Invalid username or password.</p>";
            }
        }
    ?>
    <h2>Request New Private Database</h2>
    <form action="" method="POST">
        <input type="hidden" name="create_db" value="1">
        <input type="submit" value="Create Private Database">
    </form>

    <h2>Create New Account</h2>
    <form action="" method="POST">
        <label for="dbname">Database Name:</label>
        <input type="text" id="dbname" name="dbname" required>
        
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        
        <input type="submit" value="Create Account">
    </form>

    <h2>Login to Your Account</h2>
    <form action="" method="POST">
        <label for="dbname">Database Name:</label>
        <input type="text" id="dbname" name="dbname" required>
        
        <label for="login_username">Username:</label>
        <input type="text" id="login_username" name="login_username" required>
        
        <label for="login_password">Password:</label>
        <input type="password" id="login_password" name="login_password" required>
        
        <input type="submit" value="Login">
    </form>
    
</body>
</html>
