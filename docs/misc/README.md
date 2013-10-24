Please note these files are DER encoded certificates.

Most webservers on Unix expect PEM encoded certificates.  If you need PEM encoding, you can
do this by running the following command from a shell prompt:

     openssl x509 -in <file_name.cer> -inform DER -outform PEM -out <file_name.pem>
