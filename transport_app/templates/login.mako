<!DOCTYPE html>
<html lang="en">
<head>
    <title>Вход</title>
</head>
<body>
    <h1>Login</h1>
    <span>
        ${message}
    </span>

    <form action="${url}" method="post">
        <input type="hidden" name="came_from" value="${came_from}"/>
        
        <label for="login">Username</label>
        
        <input type="text" id="login" name="login" value="${login}"/><br/>
        
        <label for="password">Password</label>
        
        <input type="password" id="password" name="password" value="${password}"/><br/>
        <input type="submit" name="form.submitted" value="Log In"/>
    </form>
</body>
</html>