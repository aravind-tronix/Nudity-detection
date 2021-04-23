# API Documentation
* **URL**  

  Endpoint for sending image via url

  ` http://localhost:8080/url`  

* **Method:**  

  `POST`

* **URL Params**  

  json body params
  
  {"url":"url_of_valid_image_file"}
  
* **Success Response:**

  If image is safe  
  
  `{"filename": "image_property", "ScanResult": "Nothing exposed"}`  
  
  If private parts are exposed in the image  
  
  `{"filename": "image_property", "ScanResult": "Private parts exposed"}`  

* **Error Response:**  

  `{"ScanResult": false,"filename": "invalid file"}`
  
  
* **URL**  

  Endpoint for sending image as a file

  `http://localhost:8080/uploader`  

* **Method:**  

  `POST`

* **URL Params**  

  body form data
  
  {"file":"image_file"}
  
* **Success Response:**

  If image is safe  
  
  `{"filename": "image_property", "ScanResult": "Nothing exposed"}`  
  
  If private parts are exposed in the image  
  
  `{"filename": "image_property", "ScanResult": "Private parts exposed"}`  

* **Error Response:**  

  `{"ScanResult": false,"filename": "invalid file"}`
  
