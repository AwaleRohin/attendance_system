import React, { useRef, useState, useEffect } from "react";
import Webcam from "react-webcam";
import axios from "axios";

const WebCam = () => {
  const webcamRef = useRef(null);
  const [image, setImage] = useState("");
  const [response, setResponse] = useState("");
  const imageRef = useRef(image);
  imageRef.current = image;
  const capture = () => {
    const imagesrc = webcamRef.current.getScreenshot();
    setImage(imagesrc);
  };
  const check = async () => {
    console.log("image", imageRef.current);
    const res = await axios.post("http://localhost:5000", {
      image: imageRef.current,
    });
    console.log(res.data.data);
    setResponse(res.data.data);
  };
  useEffect(() => {
    const timer = setTimeout(capture, 3000);
    const timer1 = setTimeout(check, 4000);
    return () => clearTimeout(timer, timer1);
  }, []);
  return (
    <React.Fragment>
      <Webcam audio={false} ref={webcamRef} screenshotFormat="image/jpeg" />
      {response && <h4>{response}</h4>}
    </React.Fragment>
  );
};

export default WebCam;
