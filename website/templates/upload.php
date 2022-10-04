<!doctype html>
<title>File Uploader</title>
<style>
    body,
    .center {
        margin: auto;
        width: 50%;
        border: 3px solid green;
        padding: 10px;
    }
</style>
<body>
 

    <h1 class="title">
  Flask Login Example
</h1>
    <h2 class="subtitle">
  Easy authentication and authorization in Flask.
</h2> 
    
<form method="post" action="/upload" enctype="multipart/form-data">

        <div class="box__input">
            <dl>
                <p> upload_key: <input name="psw" type="password" /></p>
                <p>
                    <input type="file" name="files[]" multiple="true" autocomplete="off" required>
                </p>
            </dl>
            <p>
                <input type="submit" value="Submit">
            </p>
        </div>


    </form>