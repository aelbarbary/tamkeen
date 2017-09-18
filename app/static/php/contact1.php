<?php

$EmailFrom = ($_POST['Email']);
$EmailTo = "hodehlion@gmail.com";
$Subject = "Contact Form";
$Name = Trim(stripslashes($_POST['Name']));  
$mail = Trim(stripslashes($_POST['Email'])); 
$Message = Trim(stripslashes($_POST['Message'])); 

// validation
$validationOK=true;
if (!$validationOK) {
  print "<meta http-equiv=\"refresh\" content=\"0;URL=error.htm\">";
  exit;
}

// prepare email body text 
//$body = "From: $name \n E-mail: $mail \n Message: $message";

$Body = "";
$Body .= "Name: ";
$Body .= $Name;
$Body .= "\n";
$Body .= "Email: ";
$Body .= $mail;
$Body .= "\n";
$Body .= "Message: \n";
$Body .= $Message;

// send email 
$success = mail($EmailTo, $Subject, $Body, "From: <$EmailFrom>");

// redirect to success page 
if ($success){
    echo '<script language="javascript">';
    echo 'alert("Message Successfully Sent");';
    echo 'window.location.assign("http://hritconsulting.com/haytham/pwp_about.html");';
    echo '</script>';
} 
else{
    echo '<script language="javascript">';
    echo 'alert("Their has been an error")';
    echo '</script>';
}

?>