# API Documentation
* **URL**  

  ` http://localhost:8080/url`  

* **Method:**  

  `POST`

* **URL Params**  

  {"url":"url_of_valid_image_file"}
  
* **Success Response:**

  If image is safe  
  
  `{"filename": "image_property", "ScanResult": "Nothing exposed"}`  
  
  If private parts are exposed in the image  
  
  `{"filename": "image_property", "ScanResult": "Private parts exposed"}`  

* **Error Response:**  

`{
    "ScanResult": false,
    "filename": "invalid file"
}`
  
